import { screenManager } from './utils/screenManager.js';
import StartScreen from './screens/StartScreen.js';
import GameScreen from './screens/GameScreen.js';
import LeaderboardScreen from './screens/LeaderboardScreen.js';
import NameEntryScreen from './screens/NameEntryScreen.js';

// Initialize screens
const startScreen = new StartScreen();
const gameScreen = new GameScreen();
const leaderboardScreen = new LeaderboardScreen();
const nameEntryScreen = new NameEntryScreen();

// Add screens to manager
screenManager.addScreen('start', startScreen);
screenManager.addScreen('game', gameScreen);
screenManager.addScreen('leaderboard', leaderboardScreen);
screenManager.addScreen('nameEntry', nameEntryScreen);

// Show initial screen
screenManager.showScreen('start'); 