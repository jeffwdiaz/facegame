class LeaderboardManager {
    constructor() {
        this.easyModeScores = [];
        this.hardModeScores = [];
        this.loadScores('easy');
        this.loadScores('hard');
    }

    async loadScores(mode) {
        try {
            // Try to load from API first
            const response = await fetch(`/.netlify/functions/scores?mode=${mode}`);
            if (response.ok) {
                const scores = await response.json();
                if (mode === 'easy') {
                    this.easyModeScores = scores;
                } else {
                    this.hardModeScores = scores;
                }
                // Update cache
                localStorage.setItem(`leaderboard_${mode}`, JSON.stringify(scores));
                return;
            }
        } catch (error) {
            console.warn('Failed to load scores from API, falling back to cache:', error);
        }

        // Fall back to localStorage if API fails
        const cachedScores = localStorage.getItem(`leaderboard_${mode}`);
        const scores = cachedScores ? JSON.parse(cachedScores) : [];
        if (mode === 'easy') {
            this.easyModeScores = scores;
        } else {
            this.hardModeScores = scores;
        }
    }

    async saveScores(mode, scores) {
        // Update local cache immediately
        localStorage.setItem(`leaderboard_${mode}`, JSON.stringify(scores));
    }

    async addScore(mode, name, score) {
        try {
            // Try to save to API
            const response = await fetch('/.netlify/functions/scores', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mode, name, score })
            });

            if (response.ok) {
                const updatedScores = await response.json();
                if (mode === 'easy') {
                    this.easyModeScores = updatedScores;
                } else {
                    this.hardModeScores = updatedScores;
                }
                // Update cache
                this.saveScores(mode, updatedScores);
                return;
            }
        } catch (error) {
            console.warn('Failed to save score to API, using local storage only:', error);
        }

        // Fall back to local storage if API fails
        const scores = mode === 'easy' ? this.easyModeScores : this.hardModeScores;
        
        scores.push({
            name,
            score,
            date: new Date().toISOString()
        });

        scores.sort((a, b) => {
            if (b.score !== a.score) {
                return b.score - a.score;
            }
            return new Date(b.date) - new Date(a.date);
        });

        if (scores.length > 10) {
            scores.length = 10;
        }

        this.saveScores(mode, scores);
    }

    getScores(mode) {
        return mode === 'easy' ? this.easyModeScores : this.hardModeScores;
    }

    async clearScores(mode) {
        if (mode === 'easy') {
            this.easyModeScores = [];
        } else {
            this.hardModeScores = [];
        }
        this.saveScores(mode, []);
        
        try {
            // Try to clear on API
            await fetch('/.netlify/functions/scores/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mode })
            });
        } catch (error) {
            console.warn('Failed to clear scores on API:', error);
        }
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