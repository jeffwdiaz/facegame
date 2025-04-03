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
let gameTimer = null;
let highestScoreThisGame = 0;
let lastClickTime = 0; // Track the last time a click was registered
const CLICK_BUFFER_TIME = 500; // Buffer time in milliseconds

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
const wrongMessage = document.getElementById('wrongMessage');
const faceContainer = document.querySelector('.face-container');
let touchStartY = 0;
let touchEndY = 0;
const SWIPE_THRESHOLD = 50; // Minimum distance for a swipe

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
    
    // Check if enough time has passed since the last click
    const currentTime = Date.now();
    if (currentTime - lastClickTime < CLICK_BUFFER_TIME) {
        console.log('Click buffered - too soon after last click');
        return; // Ignore this click
    }
    
    // Update the last click time
    lastClickTime = currentTime;
    
    const isCorrect = (isTopName === correctNameOnTop);
    
    // Update score
    if (isCorrect) {
        score += 1;
        // Add current person to used images if correct
        usedImages.add(currentPerson.id);
        // Hide wrong message if it was showing
        wrongMessage.classList.remove('show');
    } else {
        score -= 1;
        // Don't add to used images if incorrect
        // Show wrong message
        wrongMessage.classList.add('show');
        // Hide wrong message after 1 second
        setTimeout(() => {
            wrongMessage.classList.remove('show');
        }, 500);
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
    highestScoreThisGame = 10; // Reset highest score for this game
    lastClickTime = 0; // Reset the last click time
    updateScore();
    selectRandomPerson();
    startGameBtn.textContent = 'Next Person';
    startGameBtn.onclick = selectRandomPerson;
    
    // Start the timer that decreases score every second
    if (gameTimer) clearInterval(gameTimer);
    gameTimer = setInterval(() => {
        score -= 1;
        updateScore();
        
        // Check for game over
        if (score <= 0) {
            gameOver();
        }
    }, 1000);
}

function resetGame() {
    gameStarted = false;
    usedImages.clear();
    startGameBtn.textContent = 'Start Game';
    startGameBtn.onclick = startGame;
    faceImage.src = 'placeholder.jpg';
    nameTop.textContent = '';
    nameBottom.textContent = '';
    
    // Clear the timer
    if (gameTimer) {
        clearInterval(gameTimer);
        gameTimer = null;
    }
}

function updateScore() {
    scoreDisplay.textContent = score;
    
    // Update highest score if current score is higher
    if (score > highestScoreThisGame) {
        highestScoreThisGame = score;
    }
}

function gameOver() {
    // Clear the timer
    if (gameTimer) {
        clearInterval(gameTimer);
        gameTimer = null;
    }
    
    // Update global high score if this game's highest score is higher
    if (highestScoreThisGame > highScore) {
        highScore = highestScoreThisGame;
        highScoreDisplay.textContent = highScore;
    }
    
    // Display the highest score achieved in this game
    highScoreDisplay.textContent = highestScoreThisGame;
    
    gameOverModal.classList.remove('hidden');
    gameStarted = false;
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

// Touch event handlers
faceContainer.addEventListener('touchstart', (e) => {
    if (!gameStarted) return;
    touchStartY = e.touches[0].clientY;
});

faceContainer.addEventListener('touchmove', (e) => {
    if (!gameStarted) return;
    e.preventDefault();
    
    const currentY = e.touches[0].clientY;
    const deltaY = currentY - touchStartY;
    
    // Add visual feedback based on swipe direction
    if (deltaY < -20) {
        faceContainer.classList.add('swiping-up');
        faceContainer.classList.remove('swiping-down');
    } else if (deltaY > 20) {
        faceContainer.classList.add('swiping-down');
        faceContainer.classList.remove('swiping-up');
    }
});

faceContainer.addEventListener('touchend', (e) => {
    if (!gameStarted) return;
    touchEndY = e.changedTouches[0].clientY;
    
    // Remove swipe classes
    faceContainer.classList.remove('swiping-up', 'swiping-down');
    
    const swipeDistance = touchEndY - touchStartY;
    
    // Check if enough time has passed since the last click
    const currentTime = Date.now();
    if (currentTime - lastClickTime < CLICK_BUFFER_TIME) {
        console.log('Swipe buffered - too soon after last interaction');
        return; // Ignore this swipe
    }
    
    if (Math.abs(swipeDistance) >= SWIPE_THRESHOLD) {
        // Update the last click time
        lastClickTime = currentTime;
        
        if (swipeDistance < 0) {
            handleNameClick(true);
        } else {
            handleNameClick(false);
        }
    }
});

// Add touchcancel handler to reset state
faceContainer.addEventListener('touchcancel', () => {
    faceContainer.classList.remove('swiping-up', 'swiping-down');
});

// Initialize game
loadGameData();
setMode('easy'); // Set default mode to easy 