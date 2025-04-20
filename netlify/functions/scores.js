// Netlify Function: scores.js
// Provides GET and POST endpoints for leaderboard using Google Sheets as backend
// Requires service-account.json in project root and googleapis as a dependency

const { google } = require('googleapis');
const path = require('path');
const key = require(path.join(__dirname, '../../service-account.json'));

const sheetId = '1uQ9S0ridEh0dFVMnO1sZEQ34jGU-ww89IiQEeP_Ahyw';
const SCOPES = ['https://www.googleapis.com/auth/spreadsheets'];

const auth = new google.auth.JWT(
  key.client_email,
  null,
  key.private_key,
  SCOPES
);
const sheets = google.sheets({ version: 'v4', auth });

exports.handler = async function(event, context) {
  if (event.httpMethod === 'POST') {
    try {
      const { mode, name, score } = JSON.parse(event.body);
      if (!mode || typeof score !== 'number') {
        return { statusCode: 400, body: JSON.stringify({ error: 'Invalid input' }) };
      }
      const date = new Date().toISOString();
      await sheets.spreadsheets.values.append({
        spreadsheetId: sheetId,
        range: 'Sheet1!A:D',
        valueInputOption: 'USER_ENTERED',
        requestBody: { values: [[mode, name, score, date]] }
      });
      return { statusCode: 200, body: JSON.stringify({ success: true }) };
    } catch (err) {
      return { statusCode: 500, body: JSON.stringify({ error: 'Failed to save score' }) };
    }
  }

  // GET
  if (event.httpMethod === 'GET') {
    try {
      const mode = (event.queryStringParameters && event.queryStringParameters.mode) || 'easy';
      const result = await sheets.spreadsheets.values.get({
        spreadsheetId: sheetId,
        range: 'Sheet1!A:D'
      });
      const rows = result.data.values || [];
      const scores = rows
        .filter(row => row[0] === mode)
        .map(([mode, name, score, date]) => ({ mode, name, score: Number(score), date }))
        .sort((a, b) => b.score - a.score)
        .slice(0, 10);
      return { statusCode: 200, body: JSON.stringify(scores) };
    } catch (err) {
      return { statusCode: 500, body: JSON.stringify({ error: 'Failed to load scores' }) };
    }
  }

  // Method not allowed
  return {
    statusCode: 405,
    body: JSON.stringify({ error: 'Method not allowed' })
  };
};