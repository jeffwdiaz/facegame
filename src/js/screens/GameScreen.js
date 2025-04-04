import Screen from './Screen.js';
import { screenManager } from '../utils/screenManager.js';
import { gameState } from '../utils/gameState.js';
import { leaderboardManager } from '../utils/leaderboardManager.js';
import { gameDataManager } from '../utils/gameDataManager.js';

export default class GameScreen extends Screen {
    constructor() {
        super('game-screen');
        this.touchStartY = 0;
        this.touchEndY = 0;
        this.swipeThreshold = 50;
        this.isAnimating = false;
        this.currentPair = null;
        this.render();
        this.setupEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <header class="game-header">
                <div class="score">Score: <span id="score">0</span></div>
                <div class="high-score">High Score: <span id="highScore">0</span></div>
            </header>

            <main class="game-main">
                <div class="name-top" id="nameTop"></div>
                <div class="face-container">
                    <img src="" alt="Face" id="faceImage" class="face-image">
                    <div id="wrongMessage" class="wrong-message">Wrong!</div>
                </div>
                <div class="name-bottom" id="nameBottom"></div>
            </main>

            <div class="game-controls">
                <button id="exitGame" class="btn-secondary">Exit Game</button>
            </div>

            <div id="gameOverModal" class="modal hidden">
                <div class="modal-content">
                    <h2>Game Over!</h2>
                    <p>Your score: <span id="finalScore">0</span></p>
                    <p>High score: <span id="finalHighScore">0</span></p>
                    <p>Result: <span id="gameResult"></span></p>
                    <button id="playAgain" class="btn-primary">Play Again</button>
                    <button id="backToMenu" class="btn-secondary">Back to Menu</button>
                </div>
            </div>
        `;

        // Cache DOM elements
        this.elements = {
            scoreDisplay: this.container.querySelector('#score'),
            highScoreDisplay: this.container.querySelector('#highScore'),
            nameTop: this.container.querySelector('#nameTop'),
            nameBottom: this.container.querySelector('#nameBottom'),
            faceImage: this.container.querySelector('#faceImage'),
            wrongMessage: this.container.querySelector('#wrongMessage'),
            gameOverModal: this.container.querySelector('#gameOverModal'),
            finalScore: this.container.querySelector('#finalScore'),
            finalHighScore: this.container.querySelector('#finalHighScore'),
            gameResult: this.container.querySelector('#gameResult'),
            playAgain: this.container.querySelector('#playAgain'),
            backToMenu: this.container.querySelector('#backToMenu'),
            exitGame: this.container.querySelector('#exitGame'),
            faceContainer: this.container.querySelector('.face-container')
        };
    }

    setupEventListeners() {
        // Touch events for swipe
        this.elements.faceContainer.addEventListener('touchstart', this.handleTouchStart.bind(this));
        this.elements.faceContainer.addEventListener('touchmove', this.handleTouchMove.bind(this));
        this.elements.faceContainer.addEventListener('touchend', this.handleTouchEnd.bind(this));

        // Mouse events for desktop
        this.elements.faceContainer.addEventListener('mousedown', this.handleMouseDown.bind(this));
        this.elements.faceContainer.addEventListener('mousemove', this.handleMouseMove.bind(this));
        this.elements.faceContainer.addEventListener('mouseup', this.handleMouseUp.bind(this));
        this.elements.faceContainer.addEventListener('mouseleave', this.handleMouseUp.bind(this));

        // Button events
        this.elements.playAgain.addEventListener('click', () => {
            this.startNewGame();
        });

        this.elements.backToMenu.addEventListener('click', () => {
            screenManager.showScreen('start');
        });

        this.elements.exitGame.addEventListener('click', () => {
            screenManager.showScreen('start');
        });
    }

    show() {
        super.show();
        this.startNewGame();
    }

    startNewGame() {
        gameState.resetGame();
        gameDataManager.resetGame();
        this.updateScore();
        this.elements.gameOverModal.classList.add('hidden');
        this.loadNextFace();
        
        // Start the score timer
        gameState.startScoreTimer((score, isGameOver) => {
            this.updateScore();
            if (isGameOver) {
                this.gameOver();
            }
        });
    }

    updateScore() {
        this.elements.scoreDisplay.textContent = gameState.score;
        this.elements.highScoreDisplay.textContent = gameState.highScore;
    }

    handleTouchStart(event) {
        if (this.isAnimating) return;
        this.touchStartY = event.touches[0].clientY;
    }

    handleTouchMove(event) {
        if (!this.touchStartY || this.isAnimating) return;
        event.preventDefault();
        const currentY = event.touches[0].clientY;
        const deltaY = currentY - this.touchStartY;
        this.updateImagePosition(deltaY);
    }

    handleTouchEnd() {
        if (this.isAnimating) return;
        const deltaY = this.touchEndY - this.touchStartY;
        this.handleSwipe(deltaY);
        this.touchStartY = null;
        this.touchEndY = null;
    }

    handleMouseDown(event) {
        if (this.isAnimating) return;
        this.touchStartY = event.clientY;
        this.elements.faceContainer.style.cursor = 'grabbing';
    }

    handleMouseMove(event) {
        if (!this.touchStartY || this.isAnimating) return;
        event.preventDefault();
        const deltaY = event.clientY - this.touchStartY;
        this.updateImagePosition(deltaY);
    }

    handleMouseUp(event) {
        if (!this.touchStartY || this.isAnimating) return;
        const deltaY = event.clientY - this.touchStartY;
        this.handleSwipe(deltaY);
        this.touchStartY = null;
        this.elements.faceContainer.style.cursor = 'grab';
    }

    updateImagePosition(deltaY) {
        this.elements.faceImage.style.transform = `translateY(${deltaY}px)`;
    }

    handleSwipe(deltaY) {
        const isSwipeUp = deltaY < -this.swipeThreshold;
        const isSwipeDown = deltaY > this.swipeThreshold;

        if (isSwipeUp || isSwipeDown) {
            this.isAnimating = true;
            const isCorrect = gameDataManager.checkAnswer(isSwipeUp, this.currentPair);
            
            if (isCorrect) {
                gameState.updateScore(1);
                this.updateScore();
                const isGameComplete = gameDataManager.handleAnswer(true);
                if (isGameComplete) {
                    this.gameOver('complete');
                } else {
                    this.animateSwipe(isSwipeUp);
                }
            } else {
                gameDataManager.handleAnswer(false);
                this.showWrongMessage();
                this.resetImagePosition();
                setTimeout(() => this.loadNextFace(), 1000);
            }
        } else {
            this.resetImagePosition();
        }
    }

    animateSwipe(isSwipeUp) {
        this.elements.faceContainer.classList.add(isSwipeUp ? 'swiping-up' : 'swiping-down');
        
        setTimeout(() => {
            this.elements.faceContainer.classList.remove('swiping-up', 'swiping-down');
            this.elements.faceImage.style.transform = '';
            this.isAnimating = false;
            this.loadNextFace();
        }, 1000);
    }

    resetImagePosition() {
        this.elements.faceImage.style.transition = 'transform 0.3s ease';
        this.elements.faceImage.style.transform = '';
        
        setTimeout(() => {
            this.elements.faceImage.style.transition = '';
            this.isAnimating = false;
        }, 300);
    }

    showWrongMessage() {
        this.elements.wrongMessage.classList.add('show');
        setTimeout(() => {
            this.elements.wrongMessage.classList.remove('show');
        }, 1000);
    }

    async loadNextFace() {
        const pair = gameDataManager.getNextPair();
        if (!pair) {
            this.gameOver('complete');
            return;
        }

        this.currentPair = pair;
        
        // Set the image source
        this.elements.faceImage.src = `images/${pair.currentFace.image}`;
        
        // Set the names based on their position
        if (pair.isTopCorrect) {
            this.elements.nameTop.textContent = this.getDisplayName(pair.currentFace);
            this.elements.nameBottom.textContent = this.getDisplayName(pair.incorrectFace);
        } else {
            this.elements.nameTop.textContent = this.getDisplayName(pair.incorrectFace);
            this.elements.nameBottom.textContent = this.getDisplayName(pair.currentFace);
        }
    }

    getDisplayName(face) {
        if (gameDataManager.gameMode === 'easy') {
            return face.firstName;
        } else {
            // In hard mode, randomly choose between first and last name
            return Math.random() < 0.5 ? face.firstName : face.lastName;
        }
    }

    gameOver(reason = 'timeout') {
        gameState.endGame();
        
        // Check if it's a high score
        if (leaderboardManager.isHighScore(gameState.gameMode, gameState.score)) {
            const playerName = prompt('Congratulations! You got a high score! Enter your name:') || 'Anonymous';
            leaderboardManager.addScore(gameState.gameMode, playerName, gameState.score);
        }

        this.elements.finalScore.textContent = gameState.score;
        this.elements.finalHighScore.textContent = gameState.highScore;
        this.elements.gameResult.textContent = reason === 'complete' ? 
            'Congratulations! You matched all faces!' : 
            'Time\'s up! Try again to match more faces!';
        this.elements.gameOverModal.classList.remove('hidden');
    }

    cleanup() {
        gameState.stopScoreTimer();
    }
} 