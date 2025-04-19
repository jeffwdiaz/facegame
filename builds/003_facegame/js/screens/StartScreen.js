import Screen from './Screen.js';
import { screenManager } from '../utils/screenManager.js';
import { gameState } from '../utils/gameState.js';

export default class StartScreen extends Screen {
    constructor() {
        super('start-screen');
        this.render();
        this.setupEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <div class="start-screen-content">
                <h1 class="game-title">Face Match Game</h1>
                <div class="menu-buttons">
                    <button id="play-button" class="btn-primary">Play Game</button>
                    <button id="leaderboard-button" class="btn-secondary">Leaderboard</button>
                    <div class="mode-selector">
                        <button id="easyMode" class="btn-secondary active">Easy Mode</button>
                        <button id="hardMode" class="btn-secondary">Hard Mode</button>
                    </div>
                </div>
            </div>
        `;

        // Cache DOM elements
        this.elements = {
            playButton: this.container.querySelector('#play-button'),
            leaderboardButton: this.container.querySelector('#leaderboard-button'),
            easyModeButton: this.container.querySelector('#easyMode'),
            hardModeButton: this.container.querySelector('#hardMode')
        };

        // Set initial game mode
        gameState.setGameMode('easy');
    }

    setupEventListeners() {
        this.elements.playButton.addEventListener('click', () => {
            screenManager.showScreen('game');
        });

        this.elements.leaderboardButton.addEventListener('click', () => {
            screenManager.showScreen('leaderboard');
        });

        this.elements.easyModeButton.addEventListener('click', () => {
            this.setGameMode('easy');
        });

        this.elements.hardModeButton.addEventListener('click', () => {
            this.setGameMode('hard');
        });
    }

    setGameMode(mode) {
        gameState.setGameMode(mode);
        
        // Update button states
        this.elements.easyModeButton.classList.toggle('active', mode === 'easy');
        this.elements.hardModeButton.classList.toggle('active', mode === 'hard');
    }
} 