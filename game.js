// Game state
let usedImages = new Set();
let currentImage = null;
let gameStarted = false;
let gameData = null;
let currentPerson = null;
let currentMode = 'easy'; // 'easy' or 'hard'
let score = 10;
let highScore = 0;
let correctNameOnTop = false; // Track which name is correct

// DOM Elements
const faceImage = document.getElementById('faceImage');
const startGameBtn = document.getElementById('startGame');
const easyModeBtn = document.getElementById('easyMode');
const hardModeBtn = document.getElementById('hardMode');
const gameOverModal = document.getElementById('gameOverModal');
const nameTop = document.getElementById('nameTop');
const nameBottom = document.getElementById('nameBottom');
const scoreDisplay = document.getElementById('score');
const highScoreDisplay = document.getElementById('highScore');
const playAgainBtn = document.getElementById('playAgain');

// Disable hard mode button
hardModeBtn.disabled = true;

// Load game data
async function loadGameData() {
    try {
        const response = await fetch('data.json');
        if (!response.ok) {
            throw new Error('Failed to load game data');
        }
        gameData = await response.json();
        console.log('Game data loaded:', gameData);
    } catch (error) {
        console.error('Error loading game data:', error);
        alert('Failed to load game data. Please refresh the page.');
    }
}

// Handle name click
function handleNameClick(isTopName) {
    if (!gameStarted) return;
    
    const isCorrect = (isTopName === correctNameOnTop);
    
    // Update score
    if (isCorrect) {
        score += 1;
        // Add current person to used images if correct
        usedImages.add(currentPerson.id);
    } else {
        score -= 1;
        // Don't add to used images if incorrect
    }
    
    // Update score display
    updateScore();
    
    // Check for game over
    if (score <= 0) {
        gameOver();
        return;
    }
    
    // Move to next person
    selectRandomPerson();
}

// Image selection function
function selectRandomPerson() {
    // Get available people (excluding used images)
    const availablePeople = gameData.people.filter(person => !usedImages.has(person.id));
    
    // If all images have been used correctly, reset the used images set
    if (availablePeople.length === 0) {
        usedImages.clear();
        availablePeople = gameData.people;
    }
    
    // Get a random person from available people
    const randomIndex = Math.floor(Math.random() * availablePeople.length);
    currentPerson = availablePeople[randomIndex];
    
    // Get a random person for the other name (excluding current person and used images)
    let otherPerson;
    do {
        otherPerson = gameData.people[Math.floor(Math.random() * gameData.people.length)];
    } while (otherPerson.id === currentPerson.id || usedImages.has(otherPerson.id));
    
    // Randomly decide if correct name goes on top or bottom
    correctNameOnTop = Math.random() < 0.5;
    
    // Set names based on mode and random placement
    if (currentMode === 'easy') {
        if (correctNameOnTop) {
            nameTop.textContent = currentPerson.firstName;
            nameBottom.textContent = otherPerson.firstName;
        } else {
            nameTop.textContent = otherPerson.firstName;
            nameBottom.textContent = currentPerson.firstName;
        }
    } else {
        if (correctNameOnTop) {
            nameTop.textContent = currentPerson.lastName;
            nameBottom.textContent = otherPerson.lastName;
        } else {
            nameTop.textContent = otherPerson.lastName;
            nameBottom.textContent = currentPerson.lastName;
        }
    }
    
    // Set the current person's image
    currentImage = `images/${currentPerson.image}`;
    faceImage.src = currentImage;
    
    // Handle image loading errors
    faceImage.onerror = () => {
        console.error('Failed to load image:', currentImage);
        faceImage.src = 'placeholder.jpg';
    };
    
    // Log for debugging
    console.log('Selected person:', currentPerson);
    console.log('Other person:', otherPerson);
    console.log('Current mode:', currentMode);
    console.log('Correct name on top:', correctNameOnTop);
    console.log('Used images:', Array.from(usedImages));
    console.log('Displayed names:', {
        top: nameTop.textContent,
        bottom: nameBottom.textContent
    });
}

// Game control functions
function startGame() {
    gameStarted = true;
    usedImages.clear(); // Reset used images when starting a new game
    score = 10; // Reset score
    updateScore();
    selectRandomPerson();
    startGameBtn.textContent = 'Next Person';
    startGameBtn.onclick = selectRandomPerson;
}

function resetGame() {
    gameStarted = false;
    usedImages.clear();
    startGameBtn.textContent = 'Start Game';
    startGameBtn.onclick = startGame;
    faceImage.src = 'placeholder.jpg';
    nameTop.textContent = '';
    nameBottom.textContent = '';
}

function updateScore() {
    scoreDisplay.textContent = score;
}

function gameOver() {
    if (score > highScore) {
        highScore = score;
        highScoreDisplay.textContent = highScore;
    }
    gameOverModal.classList.remove('hidden');
}

// Mode selection
function setMode(mode) {
    currentMode = mode;
    if (gameStarted) {
        resetGame();
    }
    
    // Update button styles
    easyModeBtn.classList.toggle('active', mode === 'easy');
    hardModeBtn.classList.toggle('active', mode === 'hard');
}

// Event Listeners
startGameBtn.addEventListener('click', startGame);

easyModeBtn.addEventListener('click', () => {
    setMode('easy');
});

hardModeBtn.addEventListener('click', () => {
    setMode('hard');
});

playAgainBtn.addEventListener('click', () => {
    gameOverModal.classList.add('hidden');
    startGame();
});

// Add click listeners for names
nameTop.addEventListener('click', () => handleNameClick(true));
nameBottom.addEventListener('click', () => handleNameClick(false));

// Initialize game
loadGameData();
setMode('easy'); // Set default mode to easy 