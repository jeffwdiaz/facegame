import Screen from './Screen.js';
import { screenManager } from '../utils/screenManager.js';
import { gameState } from '../utils/gameState.js';
import { gameDataManager } from '../utils/gameDataManager.js';
import { leaderboardManager } from '../utils/leaderboardManager.js';

export default class GameScreen extends Screen {
    constructor() {
        super('game-screen');
        this.currentPair = null;
        this.isPanning = false;
        // Preload audio for correct and incorrect answers
        // correct.wav: played when the answer is correct
        // incorrect.wav: played when the answer is wrong
        this.correctAudio = new Audio('audio/correct.wav');
        this.incorrectAudio = new Audio('audio/incorrect.wav');
        this.render();
        this.setupEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <header class="game-header">
                <div class="score">Score: <span id="score">0</span></div>
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
        `;

        // Cache DOM elements
        this.elements = {
            scoreDisplay: this.container.querySelector('#score'),
            nameTop: this.container.querySelector('#nameTop'),
            nameBottom: this.container.querySelector('#nameBottom'),
            faceImage: this.container.querySelector('#faceImage'),
            wrongMessage: this.container.querySelector('#wrongMessage'),
            exitGame: this.container.querySelector('#exitGame'),
            faceContainer: this.container.querySelector('.face-container')
        };

        // Add touch-action: none to prevent browser's default touch behavior
        this.elements.faceContainer.style.touchAction = 'none';
        
        // Enable hardware acceleration
        this.elements.faceImage.style.willChange = 'transform';
        this.elements.faceImage.style.transform = 'translate3d(0, 0, 0)';
    }

    setupEventListeners() {
        // Initialize Hammer.js
        const hammer = new Hammer(this.elements.faceContainer);
        
        // Enable vertical pan
        hammer.get('pan').set({ direction: Hammer.DIRECTION_VERTICAL });

        // Pan start event
        hammer.on('panstart', () => {
            this.isPanning = true;
            this.elements.faceImage.style.transition = 'none';
        });

        // Pan move event with throttling
        let lastUpdate = 0;
        const updateInterval = 1000 / 60; // 60fps
        hammer.on('panmove', (event) => {
            const now = performance.now();
            if (now - lastUpdate >= updateInterval) {
                this.updateImagePosition(event.deltaY);
                lastUpdate = now;
            }
        });

        // Pan end event
        hammer.on('panend', (event) => {
            this.isPanning = false;
            this.handleSwipe(event.velocityY);
        });

        // Exit button
        this.elements.exitGame.addEventListener('click', () => {
            screenManager.showScreen('start');
        });
    }

    updateImagePosition(deltaY) {
        this.elements.faceImage.style.transform = `translate3d(0, ${deltaY}px, 0)`;
    }

    handleSwipe(velocityY) {
        const isSwipeUp = velocityY < -0.3; // Threshold for swipe up
        const isSwipeDown = velocityY > 0.3; // Threshold for swipe down

        if (isSwipeUp || isSwipeDown) {
            const isCorrect = gameDataManager.checkAnswer(isSwipeUp, this.currentPair);
            console.log('Swipe result:', {
                isCorrect,
                currentScore: gameState.score,
                velocityY
            });

            // Play correct or incorrect sound based on answer
            if (isCorrect) {
                this.correctAudio.currentTime = 0;
                this.correctAudio.play();
                gameState.updateScore(2); // Reward for correct answer
                this.updateScore();
                const isGameComplete = gameDataManager.handleAnswer(true);
                if (isGameComplete) {
                    this.gameOver('complete');
                } else {
                    this.loadNextFace();
                }
            } else {
                this.incorrectAudio.currentTime = 0;
                this.incorrectAudio.play();
                gameState.updateScore(-1); // Penalty for wrong answer
                this.updateScore();
                gameDataManager.handleAnswer(false);
                this.showWrongMessage();
                setTimeout(() => this.loadNextFace(), 1000);
            }
        }
        
        // Reset position with smooth transition
        this.elements.faceImage.style.transition = 'transform 0.3s ease-out';
        this.resetImagePosition();
    }

    resetImagePosition() {
        this.elements.faceImage.style.transform = 'translate3d(0, 0, 0)';
    }

    showWrongMessage() {
        this.elements.wrongMessage.style.opacity = '1';
        setTimeout(() => {
            this.elements.wrongMessage.style.opacity = '0';
        }, 1000);
    }

    show() {
        super.show();
        this.startNewGame();
    }

    startNewGame() {
        gameState.resetGame();
        gameDataManager.resetGame();
        this.updateScore();
        this.loadNextFace();
        // Start the score timer
        gameState.startScoreTimer((score) => {
            this.updateScore();
            if (score <= 0) {
                this.gameOver('timeout');
            }
        });
    }

    updateScore() {
        console.log('Updating score display:', gameState.score);
        this.elements.scoreDisplay.textContent = gameState.score;
    }

    loadNextFace() {
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
        return gameDataManager.gameMode === 'easy' ? face.firstName : face.lastName;
    }

    gameOver(reason = 'complete') {
        console.log('Game over details:', {
            reason,
            finalScore: gameState.score,
            gameMode: gameState.gameMode,
            highScore: gameState.highScore
        });
        
        gameState.endGame();
        
        // Check if this is a high score
        const isHighScore = leaderboardManager.isHighScore(gameState.gameMode, gameState.score);
        console.log('High score check result:', {
            isHighScore,
            currentScore: gameState.score,
            mode: gameState.gameMode
        });
        
        if (isHighScore) {
            console.log('Showing name entry screen');
            screenManager.showScreen('nameEntry');
        } else {
            console.log('Returning to start screen - not a high score');
            screenManager.showScreen('start');
        }
    }
} 