const { getKVStore } = require('@netlify/blobs');

const STORE_NAME = 'leaderboard';

async function getScores(mode) {
    const store = getKVStore(STORE_NAME);
    try {
        const scores = await store.get(`scores_${mode}`);
        return scores ? JSON.parse(scores) : [];
    } catch (error) {
        console.error('Error reading scores:', error);
        return [];
    }
}

async function saveScores(mode, name, newScore) {
    const store = getKVStore(STORE_NAME);
    try {
        // Get current scores
        let scores = await getScores(mode);
        
        // Add new score
        scores.push({
            name,
            score: newScore,
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

        // Save back to store
        await store.set(`scores_${mode}`, JSON.stringify(scores));
        return scores;
    } catch (error) {
        console.error('Error saving scores:', error);
        throw error;
    }
}

module.exports = {
    getScores,
    saveScores
}; 