import Screen from './Screen.js';
import { screenManager } from '../utils/screenManager.js';
import { leaderboardManager } from '../utils/leaderboardManager.js';
import { gameState } from '../utils/gameState.js';

export default class NameEntryScreen extends Screen {
    constructor() {
        super('name-entry-screen');
        this.render();
        this.setupEventListeners();
    }

    render() {
        // Get the high score that will be saved
        const finalScore = parseInt(localStorage.getItem('lastGameScore'), 10) || gameState.highScore;
        
        this.container.innerHTML = `
            <div class="name-entry-container">
                <h1 class="name-entry-title">New High Score!</h1>
                <p class="name-entry-subtitle">Your Best Score: ${finalScore}</p>
                <p class="name-entry-subtitle">Enter your name to save your score</p>
                
                <div class="name-entry-form">
                    <input type="text" 
                           id="playerName" 
                           class="name-input" 
                           placeholder="Enter your name"
                           maxlength="20"
                           required>
                    <div class="name-entry-controls">
                        <button id="saveScore" class="btn-primary">Save Score</button>
                        <button id="skipSave" class="btn-secondary">Skip</button>
                    </div>
                </div>
            </div>
        `;

        // Cache DOM elements
        this.elements = {
            playerName: this.container.querySelector('#playerName'),
            saveScore: this.container.querySelector('#saveScore'),
            skipSave: this.container.querySelector('#skipSave')
        };
    }

    setupEventListeners() {
        // Save score button
        this.elements.saveScore.addEventListener('click', () => {
            const name = this.elements.playerName.value.trim();
            if (name) {
                this.saveScore(name);
            }
        });

        // Skip button
        this.elements.skipSave.addEventListener('click', () => {
            this.saveScore('Anonymous');
        });

        // Handle Enter key
        this.elements.playerName.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                const name = this.elements.playerName.value.trim();
                if (name) {
                    this.saveScore(name);
                }
            }
        });
    }

    saveScore(name) {
        // Get the final score from localStorage
        const finalScore = parseInt(localStorage.getItem('lastGameScore'), 10);
        
        if (!finalScore && finalScore !== 0) {
            console.error('No final score found in localStorage!', {
                rawValue: localStorage.getItem('lastGameScore'),
                parsedValue: finalScore,
                stateScore: gameState.score
            });
            // Use gameState score as fallback
            finalScore = gameState.score;
        }
        
        console.log('Saving score:', {
            name,
            finalScore,
            stateScore: gameState.score,
            mode: gameState.gameMode,
            rawStoredScore: localStorage.getItem('lastGameScore')
        });
        
        // Add score to leaderboard using the final score
        leaderboardManager.addScore(gameState.gameMode, name, finalScore);
        
        // Clear the saved score
        localStorage.removeItem('lastGameScore');
        
        // Return to start screen
        screenManager.showScreen('start');
    }

    show() {
        super.show();
        // Focus the input field when the screen is shown
        this.elements.playerName.focus();
    }
} 