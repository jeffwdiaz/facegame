from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv
import os
import chromadb
import json
from datetime import datetime
import random
import time
from collections import defaultdict
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .init_chroma import init_chroma
from .data_definitions import CATEGORIES, KNOWLEDGE_BASE
from .topic_utils import TopicManager

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()

# Rate limiting configuration
RATE_LIMIT_WINDOW = 60  # 1 minute window
MAX_REQUESTS_PER_WINDOW = 10  # Maximum requests per minute
request_timestamps = defaultdict(list)

def check_rate_limit():
    """Check if the current request should be rate limited."""
    current_time = time.time()
    window_start = current_time - RATE_LIMIT_WINDOW
    
    # Clean up old timestamps
    request_timestamps['global'] = [ts for ts in request_timestamps['global'] if ts > window_start]
    
    # Check if we've exceeded the rate limit
    if len(request_timestamps['global']) >= MAX_REQUESTS_PER_WINDOW:
        return False
    
    # Add current timestamp
    request_timestamps['global'].append(current_time)
    return True

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Initialize FastAPI app
app = FastAPI(title="AI Study Buddy")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')

# Initialize ChromaDB
try:
    chroma_client = init_chroma()
    knowledge_base = chroma_client.get_collection("knowledge_base")
    user_progress = chroma_client.get_collection("user_progress")
    print("ChromaDB initialized successfully")
except Exception as e:
    print(f"Error initializing ChromaDB: {str(e)}")
    raise

# Load knowledge base into ChromaDB
print("Loading knowledge base into ChromaDB...")
for category_id, items in KNOWLEDGE_BASE.items():
    category = next((cat for cat in CATEGORIES if cat["id"] == category_id), None)
    if not category:
        continue
        
    for item in items:
        try:
            knowledge_base.add(
                documents=[item["content"]],
                metadatas=[{
                    "category": category["name"],
                    "difficulty": item["difficulty"],
                    "type": item["type"],
                    "source": item["source"]
                }],
                ids=[f"{category_id}_{item['type']}_{item['source']}"]
            )
            print(f"Added {item['type']} content for category: {category_id}")
        except Exception as e:
            print(f"Error adding content for {category_id}: {str(e)}")
            continue

print("Knowledge base loaded successfully!")

# Initialize TopicManager
topic_manager = TopicManager()

# Mount static files after all initializations
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class QuestionResponse(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    category_id: str

@app.get("/")
async def read_root():
    """Serve the main HTML file."""
    return FileResponse("index.html", media_type="text/html")

@app.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get all available quiz categories."""
    categories = db.query(models.Category).all()
    return {"categories": [
        {
            "id": cat.id,
            "name": cat.name,
            "description": cat.description
        }
        for cat in categories
    ]}

@app.post("/quiz/{category_id}")
async def generate_question(category_id: str, difficulty: str = "beginner", db: Session = Depends(get_db)):
    """Generate a new question for the specified category."""
    print(f"Generating question for category: {category_id} with difficulty: {difficulty}")
    
    # Check rate limit
    if not check_rate_limit():
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please wait a moment before trying again."
        )
    
    # Validate category
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        print(f"Invalid category ID: {category_id}")
        raise HTTPException(status_code=400, detail=f"Invalid category ID: {category_id}")

    print(f"Found category: {category.name}")

    # Validate difficulty
    valid_difficulties = ["beginner", "intermediate", "advanced"]
    if difficulty not in valid_difficulties:
        print(f"Invalid difficulty: {difficulty}")
        raise HTTPException(status_code=400, detail=f"Invalid difficulty. Must be one of: {', '.join(valid_difficulties)}")

    # Get relevant topics for the category
    try:
        # Get all topics that match the category name
        topics = topic_manager.get_topics_by_name(category.name)
        print(f"Found {len(topics)} topics for category '{category.name}':")
        for topic in topics:
            print(f"- Topic ID: {topic['id']}, Topic: {topic['topic']}")
        
        if not topics:
            raise HTTPException(status_code=404, detail=f"No topics found for category: {category.name}")
        
        # Randomly select up to 5 topics for context
        selected_topics = random.sample(topics, min(5, len(topics)))
        print(f"\nSelected {len(selected_topics)} topics for context:")
        
        # Build context with more variety
        context = []
        for topic in selected_topics:
            print(f"\nUsing topic: {topic['topic']} (ID: {topic['id']})")
            
            # Randomly select which aspects to include
            aspects = [
                ("Definition", topic['definition']),
                ("Use Case", topic['use_case']),
                ("Benefits", ', '.join(topic['benefits'])),
                ("Challenges", ', '.join(topic['challenges'])),
                ("Relation to LLMs", topic['relation_to_LLMs'])
            ]
            
            # Randomly select 2-3 aspects for each topic
            selected_aspects = random.sample(aspects, random.randint(2, 3))
            for aspect_name, aspect_value in selected_aspects:
                context.append(f"{aspect_name}: {aspect_value}")
        
        # Shuffle the context to avoid predictable patterns
        random.shuffle(context)
        context = "\n".join(context)
        print("\nGenerated context length:", len(context))
        
    except Exception as e:
        print(f"Error getting topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topics")

    # Generate question using Gemini with improved prompt
    prompt = f"""You are a quiz generator for teaching about {category.name}. 
    Using this context: {context}
    
    Generate a {difficulty}-level multiple choice question that tests understanding of {category.name}.
    
    IMPORTANT: Make this question DIFFERENT from typical questions by:
    1. Using varied question types:
       - "What is..." (definition/explanation)
       - "Why is..." (reasoning/analysis)
       - "How does..." (process/mechanism)
       - "Which of the following..." (comparison/selection)
       - "In what scenario..." (application)
       - "What would happen if..." (hypothetical)
       - "Which statement best describes..." (analysis)
       - "What are the key differences between..." (comparison)
       - "How would you implement..." (practical application)
       - "What are the potential risks of..." (critical thinking)
    
    2. Varying cognitive levels:
       - Beginner: Focus on definitions, basic concepts, and simple relationships
       - Intermediate: Focus on applications, comparisons, and practical scenarios
       - Advanced: Focus on analysis, troubleshooting, and edge cases
    
    3. Using different question structures:
       - Direct questions
       - Scenario-based questions
       - Problem-solving questions
       - Comparison questions
       - "What if" questions
       - Case study questions
       - Implementation questions
       - Debugging questions
    
    4. Varying topics within {category.name}:
       - Core concepts
       - Implementation details
       - Best practices
       - Common challenges
       - Real-world applications
       - Edge cases
       - Performance considerations
       - Security implications
    
    5. Making options more interesting:
       - Include partially correct answers
       - Use realistic but incorrect alternatives
       - Add common misconceptions as options
       - Include "all of the above" or "none of the above" when appropriate
    
    Guidelines for {difficulty} level:
    - Use clear, precise language
    - Make options distinct and unambiguous
    - Include a helpful explanation
    - For beginner: focus on fundamental concepts
    - For intermediate: focus on practical applications
    - For advanced: focus on complex scenarios and edge cases
    
    Format your response as a valid JSON object with these exact fields:
    - question: the question text
    - options: array of 4 options prefixed with A), B), C), D)
    - correct_answer: just the letter (A, B, C, or D)
    - explanation: brief, easy-to-understand explanation of the correct answer
    
    Keep the response concise and ensure it's valid JSON."""

    try:
        print("Generating question with Gemini...")
        response = model.generate_content(prompt)
        response_text = response.text
        print("Raw response:", response_text)
        
        # Clean the response text to ensure valid JSON
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()
        
        print("Cleaned response:", cleaned_text)
        question_data = json.loads(cleaned_text)
        
        # Validate the response format
        required_fields = ["question", "options", "correct_answer", "explanation"]
        if not all(field in question_data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in question_data]
            print(f"Missing required fields: {missing_fields}")
            raise ValueError(f"Response missing required fields: {missing_fields}")
        if len(question_data["options"]) != 4:
            print(f"Invalid number of options: {len(question_data['options'])}")
            raise ValueError("Response must have exactly 4 options")
            
        # Store question in user progress
        try:
            progress = models.UserProgress(
                question_id=f"q-{datetime.now().timestamp()}",
                category_id=category_id,
                type="question",
                content=json.dumps(question_data)
            )
            db.add(progress)
            db.commit()
            print("Question stored in user progress")
        except Exception as e:
            print(f"Error storing question in user progress: {e}")
            db.rollback()
            # Continue even if storage fails
        
        return question_data
    except json.JSONDecodeError as je:
        print(f"JSON Decode Error: {je}")
        print("Response text:", response_text)
        raise HTTPException(status_code=500, detail="Failed to generate a valid question. Please try again.")
    except Exception as e:
        print(f"Error type: {type(e)}")
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the question: {str(e)}")

@app.post("/feedback/{question_id}")
async def submit_feedback(question_id: str, feedback: dict, db: Session = Depends(get_db)):
    """Submit feedback for a question."""
    try:
        progress = models.UserProgress(
            question_id=question_id,
            type="feedback",
            content=json.dumps(feedback)
        )
        db.add(progress)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save feedback: {str(e)}")

@app.get("/debug/feedback")
async def get_feedback(db: Session = Depends(get_db)):
    """Get all feedback from user_progress"""
    feedback_items = db.query(models.UserProgress).filter(
        models.UserProgress.type == "feedback"
    ).all()
    return {
        "count": len(feedback_items),
        "items": [
            {
                "id": item.id,
                "question_id": item.question_id,
                "timestamp": item.timestamp.isoformat(),
                "content": json.loads(item.content)
            }
            for item in feedback_items
        ]
    }

@app.get("/debug/knowledge")
async def get_knowledge(db: Session = Depends(get_db)):
    """Get all entries from knowledge_items"""
    knowledge_items = db.query(models.KnowledgeItem).all()
    return {
        "count": len(knowledge_items),
        "items": [
            {
                "id": item.id,
                "content": item.content,
                "type": item.type,
                "source": item.source,
                "difficulty": item.difficulty,
                "category_id": item.category_id,
                "created_at": item.created_at.isoformat(),
                "updated_at": item.updated_at.isoformat()
            }
            for item in knowledge_items
        ]
    }

# Add new endpoints for topics
@app.get("/topics")
async def get_all_topics():
    """Get all unique topics"""
    return {"topics": topic_manager.get_unique_topics()}

@app.get("/topics/{topic_id}")
async def get_topic(topic_id: int):
    """Get detailed information about a specific topic"""
    topic = topic_manager.get_topic_by_id(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@app.get("/topics/search/{topic_name}")
async def search_topics(topic_name: str):
    """Search for topics by name"""
    topics = topic_manager.get_topics_by_name(topic_name)
    return {"topics": topics}

@app.get("/topics/{topic_id}/benefits")
async def get_topic_benefits(topic_id: int):
    """Get benefits for a specific topic"""
    benefits = topic_manager.get_topic_benefits(topic_id)
    if not benefits:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"benefits": benefits}

@app.get("/topics/{topic_id}/challenges")
async def get_topic_challenges(topic_id: int):
    """Get challenges for a specific topic"""
    challenges = topic_manager.get_topic_challenges(topic_id)
    if not challenges:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"challenges": challenges}

@app.get("/topics/{topic_id}/definition")
async def get_topic_definition(topic_id: int):
    """Get definition for a specific topic"""
    definition = topic_manager.get_topic_definition(topic_id)
    if not definition:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"definition": definition}

@app.get("/topics/{topic_id}/use-case")
async def get_topic_use_case(topic_id: int):
    """Get use case for a specific topic"""
    use_case = topic_manager.get_topic_use_case(topic_id)
    if not use_case:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"use_case": use_case}

@app.get("/topics/{topic_id}/relation")
async def get_topic_relation(topic_id: int):
    """Get relation to LLMs for a specific topic"""
    relation = topic_manager.get_topic_relation(topic_id)
    if not relation:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"relation_to_LLMs": relation} 