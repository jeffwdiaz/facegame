import Screen from './Screen.js';
import { screenManager } from '../utils/screenManager.js';
import { leaderboardManager } from '../utils/leaderboardManager.js';

export default class LeaderboardScreen extends Screen {
    constructor() {
        super('leaderboard-screen');
        this.currentMode = 'easy';
        this.render();
        this.setupEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <div class="leaderboard-header">
                <h1 class="leaderboard-title">Leaderboard</h1>
                <p class="leaderboard-subtitle">Top 10 Scores</p>
            </div>

            <div class="mode-toggle">
                <button id="easyModeToggle" class="btn-secondary active">Easy Mode</button>
                <button id="hardModeToggle" class="btn-secondary">Hard Mode</button>
            </div>

            <div class="leaderboard-list" id="leaderboardList">
                <!-- Scores will be inserted here -->
            </div>

            <div class="leaderboard-controls">
                <button id="backButton" class="btn-primary">Back to Menu</button>
            </div>
        `;

        // Cache DOM elements
        this.elements = {
            leaderboardList: this.container.querySelector('#leaderboardList'),
            easyModeToggle: this.container.querySelector('#easyModeToggle'),
            hardModeToggle: this.container.querySelector('#hardModeToggle'),
            backButton: this.container.querySelector('#backButton')
        };

        this.updateLeaderboard();
    }

    setupEventListeners() {
        this.elements.easyModeToggle.addEventListener('click', () => {
            this.setMode('easy');
        });

        this.elements.hardModeToggle.addEventListener('click', () => {
            this.setMode('hard');
        });

        this.elements.backButton.addEventListener('click', () => {
            screenManager.showScreen('start');
        });
    }

    setMode(mode) {
        this.currentMode = mode;
        
        // Update button states
        this.elements.easyModeToggle.classList.toggle('active', mode === 'easy');
        this.elements.hardModeToggle.classList.toggle('active', mode === 'hard');
        
        // Update leaderboard
        this.updateLeaderboard();
    }

    updateLeaderboard() {
        const scores = leaderboardManager.getScores(this.currentMode);
        
        if (scores.length === 0) {
            this.elements.leaderboardList.innerHTML = `
                <div class="empty-state">
                    No scores yet. Start playing to set some records!
                </div>
            `;
            return;
        }

        this.elements.leaderboardList.innerHTML = scores
            .map((score, index) => `
                <div class="leaderboard-item">
                    <div class="rank">#${index + 1}</div>
                    <div class="player-info">
                        <div class="player-name">${score.name || 'Anonymous'}</div>
                        <div class="date">${this.formatDate(score.date)}</div>
                    </div>
                    <div class="player-score">${score.score}</div>
                </div>
            `)
            .join('');
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString(undefined, {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    show() {
        super.show();
        this.updateLeaderboard();
    }
} 