const { getScores, saveScores } = require('../utils/scoresDb');

exports.handler = async function(event, context) {
    try {
        if (event.httpMethod === 'GET') {
            const mode = event.queryStringParameters?.mode || 'easy';
            const scores = await getScores(mode);
            return {
                statusCode: 200,
                body: JSON.stringify(scores)
            };
        }
        
        if (event.httpMethod === 'POST') {
            const { mode, name, score } = JSON.parse(event.body);
            if (!mode || !name || score === undefined) {
                return {
                    statusCode: 400,
                    body: JSON.stringify({ error: 'Missing required fields' })
                };
            }
            
            await saveScores(mode, name, score);
            const updatedScores = await getScores(mode);
            
            return {
                statusCode: 200,
                body: JSON.stringify(updatedScores)
            };
        }
        
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Server error' })
        };
    }
} 