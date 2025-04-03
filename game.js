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
let imageCache = new Set(); // Track which images have been loaded
let imageLoadingPromises = new Map(); // Track image loading promises
let preloadedImages = new Set(); // Track preloaded images
const PRELOAD_COUNT = 5; // Number of images to preload

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

// Add after the DOM Elements section
const loadingIndicator = document.createElement('div');
loadingIndicator.className = 'loading-indicator';
loadingIndicator.textContent = 'Loading...';
faceContainer.appendChild(loadingIndicator);

// Add progress indicator
const progressIndicator = document.createElement('div');
progressIndicator.className = 'progress-indicator';
progressIndicator.textContent = 'Loading images: 0%';
faceContainer.appendChild(progressIndicator);

// Load game data
async function loadGameData() {
    try {
        const response = await fetch('data.json');
        if (!response.ok) {
            throw new Error('Failed to load game data');
        }
        gameData = await response.json();
        console.log('Game data loaded:', gameData);
        
        // Start preloading initial images
        const totalImages = gameData.people.length;
        let loadedImages = 0;
        
        // Update progress indicator
        progressIndicator.textContent = `Loading images: ${Math.round((loadedImages / totalImages) * 100)}%`;
        
        // Preload first batch of images
        await preloadNextImages();
        loadedImages = preloadedImages.size;
        progressIndicator.textContent = `Loading images: ${Math.round((loadedImages / totalImages) * 100)}%`;
        
        // Enable start button once initial images are loaded
        startGameBtn.disabled = false;
    } catch (error) {
        console.error('Error loading game data:', error);
        alert('Failed to load game data. Please refresh the page.');
    }
}

// Add new function for image loading
async function loadImage(imagePath) {
    // Return cached promise if image is already loading
    if (imageLoadingPromises.has(imagePath)) {
        return imageLoadingPromises.get(imagePath);
    }

    // Create new promise for image loading
    const loadPromise = new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => {
            imageCache.add(imagePath);
            imageLoadingPromises.delete(imagePath);
            resolve(img);
        };
        img.onerror = () => {
            console.error('Failed to load image:', imagePath);
            imageLoadingPromises.delete(imagePath);
            reject(new Error(`Failed to load image: ${imagePath}`));
        };
        img.src = imagePath;
    });

    imageLoadingPromises.set(imagePath, loadPromise);
    return loadPromise;
}

// Add new function for preloading images
async function preloadNextImages() {
    const availablePeople = gameData.people.filter(person => !usedImages.has(person.id));
    if (availablePeople.length === 0) return;

    const preloadCount = Math.min(PRELOAD_COUNT, availablePeople.length);
    const preloadPromises = [];

    for (let i = 0; i < preloadCount; i++) {
        const randomIndex = Math.floor(Math.random() * availablePeople.length);
        const person = availablePeople[randomIndex];
        if (!preloadedImages.has(person.id)) {
            preloadPromises.push(loadImage(`images/${person.image}`));
            preloadedImages.add(person.id);
        }
    }

    await Promise.all(preloadPromises);
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
async function selectRandomPerson() {
    // Show loading indicator
    loadingIndicator.style.display = 'block';
    faceImage.style.display = 'none';

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
    
    try {
        // Set the current person's image
        currentImage = `images/${currentPerson.image}`;
        await loadImage(currentImage);
        faceImage.src = currentImage;
        faceImage.style.display = 'block';
        loadingIndicator.style.display = 'none';
        
        // Start preloading next batch of images
        preloadNextImages();
    } catch (error) {
        console.error('Error loading image:', error);
        faceImage.src = 'placeholder.jpg';
        faceImage.style.display = 'block';
        loadingIndicator.style.display = 'none';
    }
    
    // Log for debugging
    console.log('Selected person:', currentPerson);
    console.log('Other person:', otherPerson);
    console.log('Current mode:', currentMode);
    console.log('Correct name on top:', correctNameOnTop);
    console.log('Used images:', Array.from(usedImages));
    console.log('Preloaded images:', Array.from(preloadedImages));
}

// Game control functions
function startGame() {
    // Reset game state
    usedImages.clear();
    preloadedImages.clear();
    score = 10;
    highestScoreThisGame = 0;
    gameStarted = true;
    lastClickTime = 0;
    
    // Hide game controls and show game elements
    document.querySelector('.game-controls').style.display = 'none';
    document.querySelector('.game-area').style.display = 'flex';
    document.querySelector('.game-header').style.display = 'flex';
    
    updateScore();
    gameOverModal.style.display = 'none';
    
    // Start the game
    selectRandomPerson();
    
    // Start the timer
    if (gameTimer) clearInterval(gameTimer);
    gameTimer = setInterval(() => {
        if (score > 0) {
            score -= 1;
            updateScore();
        } else {
            gameOver();
        }
    }, 2000);
}

function resetGame() {
    gameStarted = false;
    usedImages.clear();
    startGameBtn.textContent = 'Start Game';
    startGameBtn.onclick = startGame;
    faceImage.src = 'placeholder.jpg';
    nameTop.textContent = '';
    nameBottom.textContent = '';
    
    // Show game controls and hide game elements
    document.querySelector('.game-controls').style.display = 'flex';
    document.querySelector('.game-area').style.display = 'none';
    document.querySelector('.game-header').style.display = 'none';
    
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
    
    // Show the game over modal
    gameOverModal.classList.remove('hidden');
    gameOverModal.style.display = 'flex';
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
    gameOverModal.style.display = 'none';
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