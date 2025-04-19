class LeaderboardManager {
    constructor() {
        this.easyModeScores = this.loadScores('easy');
        this.hardModeScores = this.loadScores('hard');
    }

    loadScores(mode) {
        const scores = localStorage.getItem(`leaderboard_${mode}`);
        return scores ? JSON.parse(scores) : [];
    }

    saveScores(mode) {
        const scores = mode === 'easy' ? this.easyModeScores : this.hardModeScores;
        localStorage.setItem(`leaderboard_${mode}`, JSON.stringify(scores));
    }

    addScore(mode, name, score) {
        const scores = mode === 'easy' ? this.easyModeScores : this.hardModeScores;
        
        // Add new score
        scores.push({
            name,
            score,
            date: new Date().toISOString()
        });

        // Sort by score (descending) and date (most recent first)
        scores.sort((a, b) => {
            if (b.score !== a.score) {
                return b.score - a.score;
            }
            return new Date(b.date) - new Date(a.date);
        });

        // Keep only top 10 scores
        if (scores.length > 10) {
            scores.length = 10;
        }

        // Save to localStorage
        this.saveScores(mode);
    }

    getScores(mode) {
        return mode === 'easy' ? this.easyModeScores : this.hardModeScores;
    }

    clearScores(mode) {
        if (mode === 'easy') {
            this.easyModeScores = [];
        } else {
            this.hardModeScores = [];
        }
        this.saveScores(mode);
    }

    isHighScore(mode, score) {
        const scores = this.getScores(mode);
        const lowestScore = scores.length > 0 ? scores[scores.length - 1].score : 0;
        const isHigh = scores.length < 10 || score > lowestScore;
        
        console.log(`High score check for ${mode} mode:`, {
            currentScore: score,
            scoresCount: scores.length,
            scores: scores,
            lowestScore: lowestScore,
            isHighScore: isHigh,
            reason: scores.length < 10 ? 'Leaderboard not full' : 
                   score > lowestScore ? 'Score higher than lowest' : 
                   'Score not high enough'
        });
        
        return isHigh;
    }
}

export const leaderboardManager = new LeaderboardManager(); 