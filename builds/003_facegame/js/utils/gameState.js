import { gameDataManager } from './gameDataManager.js';
import { leaderboardManager } from './leaderboardManager.js';

export default class GameState {
    constructor() {
        this.score = 10;
        this.gameMode = 'easy';
        this.clearAllHighScores(); // Clear any existing high scores
        this.highScore = this.loadHighScore();
        this.currentFace = null;
        this.nextFace = null;
        this.isGameOver = false;
        this.scoreTimer = null;
        this.scoreCallback = null;
    }

    loadHighScore() {
        const savedScore = localStorage.getItem(`highScore_${this.gameMode}`);
        return savedScore ? parseInt(savedScore, 10) : 0;
    }

    saveHighScore() {
        localStorage.setItem(`highScore_${this.gameMode}`, this.highScore.toString());
    }

    startScoreTimer(callback) {
        this.stopScoreTimer();
        this.scoreCallback = callback;
        this.scoreTimer = setInterval(() => {
            console.log('Timer tick - current score:', this.score);
            this.updateScore(-1); // Decrease score every 2000ms
            if (this.scoreCallback) {
                this.scoreCallback(this.score);
            }
            
            if (this.score <= 0) {
                this.endGame();
            }
        }, 2000); // Changed to 2000ms for slower score decrease
    }

    stopScoreTimer() {
        if (this.scoreTimer) {
            clearInterval(this.scoreTimer);
            this.scoreTimer = null;
        }
    }

    updateScore(points) {
        console.log('Score update details:', {
            currentScore: this.score,
            pointsToAdd: points,
            newScore: this.score + points,
            currentHighScore: this.highScore,
            gameMode: this.gameMode
        });

        // Update the current score
        const newScore = Math.max(0, this.score + points);
        
        // Check if this is a new high score
        if (newScore > this.highScore) {
            console.log('New high score achieved:', {
                previousHighScore: this.highScore,
                newHighScore: newScore,
                gameMode: this.gameMode
            });
            this.highScore = newScore;
            this.saveHighScore(); // Save to localStorage immediately
        }

        // Update the current score after high score check
        this.score = newScore;

        // Update the display if callback exists
        if (this.scoreCallback) {
            this.scoreCallback(this.score);
        }
    }

    setGameMode(mode) {
        this.gameMode = mode;
        this.highScore = this.loadHighScore();
        gameDataManager.setGameMode(mode);
    }

    resetGame() {
        this.stopScoreTimer();
        this.score = 10;
        this.isGameOver = false;
        this.highScore = this.loadHighScore();
        if (this.scoreCallback) {
            this.scoreCallback(this.score);
        }
    }

    endGame() {
        // Store the high score achieved during the game
        const finalScore = Math.max(this.score, this.highScore);
        
        console.log('Saving final score to localStorage:', {
            score: finalScore,
            currentScore: this.score,
            currentHighScore: this.highScore,
            gameMode: this.gameMode
        });
        
        // Save the final score to localStorage
        localStorage.setItem('lastGameScore', finalScore.toString());
        
        // Double check it was saved correctly
        const savedScore = localStorage.getItem('lastGameScore');
        console.log('Verifying saved score:', {
            savedScore,
            parsedScore: parseInt(savedScore, 10)
        });

        this.stopScoreTimer();
        this.isGameOver = true;
        
        // Store the final score for leaderboard check
        this.score = finalScore;
    }

    clearHighScore() {
        localStorage.removeItem(`highScore_${this.gameMode}`);
        this.highScore = 0;
        console.log('High score cleared for mode:', this.gameMode);
    }

    clearAllHighScores() {
        localStorage.removeItem('highScore_easy');
        localStorage.removeItem('highScore_hard');
        console.log('All high scores cleared from localStorage');
    }
}

export const gameState = new GameState(); 