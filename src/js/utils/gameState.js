import { gameDataManager } from './gameDataManager.js';

export default class GameState {
    constructor() {
        this.score = 10;
        this.highScore = this.loadHighScore();
        this.currentFace = null;
        this.nextFace = null;
        this.gameMode = 'easy';
        this.isGameOver = false;
        this.scoreTimer = null;
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
        this.scoreTimer = setInterval(() => {
            this.score = Math.max(0, this.score - 1);
            callback(this.score);
            
            if (this.score === 0) {
                this.endGame();
                callback(this.score, true); // true indicates game over
            }
        }, 2000); // Reduce score every 2 seconds
    }

    stopScoreTimer() {
        if (this.scoreTimer) {
            clearInterval(this.scoreTimer);
            this.scoreTimer = null;
        }
    }

    updateScore(points) {
        this.score += points; // No cap on score
        if (this.score > this.highScore) {
            this.highScore = this.score;
            this.saveHighScore();
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
    }

    endGame() {
        this.stopScoreTimer();
        this.isGameOver = true;
        if (this.score > this.highScore) {
            this.highScore = this.score;
            this.saveHighScore();
        }
    }
}

export const gameState = new GameState(); 