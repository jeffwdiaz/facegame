import { screenManager } from './utils/screenManager.js';
import StartScreen from './screens/StartScreen.js';
import GameScreen from './screens/GameScreen.js';
import LeaderboardScreen from './screens/LeaderboardScreen.js';

// Initialize screens
const startScreen = new StartScreen();
const gameScreen = new GameScreen();
const leaderboardScreen = new LeaderboardScreen();

// Add screens to manager
screenManager.addScreen('start', startScreen);
screenManager.addScreen('game', gameScreen);
screenManager.addScreen('leaderboard', leaderboardScreen);

// Show initial screen
screenManager.showScreen('start'); 