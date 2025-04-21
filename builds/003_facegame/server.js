// Minimal Express backend for storing and retrieving leaderboard scores
// Now stores scores in Google Sheets using the Google Sheets API
// To run: npm install express cors googleapis, then node server.js

const express = require('express');
const cors = require('cors');
const { google } = require('googleapis');
const key = require('./service-account.json');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

// === Google Sheets Setup ===
const sheetId = '1uQ9S0ridEh0dFVMnO1sZEQ34jGU-ww89IiQEeP_Ahyw'; // <-- Updated with your Google Sheet ID
const SCOPES = ['https://www.googleapis.com/auth/spreadsheets'];
const auth = new google.auth.JWT(
  key.client_email,
  null,
  key.private_key,
  SCOPES
);
const sheets = google.sheets({ version: 'v4', auth });

// POST /api/scores { mode, name, score }
app.post('/api/scores', async (req, res) => {
  try {
    const { mode, name, score } = req.body;
    if (!mode || typeof score !== 'number') {
      return res.status(400).json({ error: 'Invalid input' });
    }
    const date = new Date().toISOString();
    await sheets.spreadsheets.values.append({
      spreadsheetId: sheetId,
      range: 'Sheet1!A:D',
      valueInputOption: 'USER_ENTERED',
      requestBody: { values: [[mode, name, score, date]] }
    });
    res.json({ success: true });
  } catch (err) {
    console.error('Error saving score to Google Sheets:', err);
    res.status(500).json({ error: 'Failed to save score' });
  }
});

// GET /api/scores?mode=easy|hard
app.get('/api/scores', async (req, res) => {
  try {
    const mode = req.query.mode || 'easy';
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
    res.json(scores);
  } catch (err) {
    console.error('Error loading scores from Google Sheets:', err);
    res.status(500).json({ error: 'Failed to load scores' });
  }
});

app.listen(PORT, () => {
  console.log(`Leaderboard backend (Google Sheets) running at http://localhost:${PORT}`);
});
