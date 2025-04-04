class ScreenManager {
    constructor() {
        this.screens = new Map();
        this.currentScreen = null;
    }

    addScreen(name, screen) {
        this.screens.set(name, screen);
    }

    showScreen(name) {
        // Hide current screen if exists
        if (this.currentScreen) {
            this.currentScreen.hide();
        }

        // Show new screen
        const screen = this.screens.get(name);
        if (screen) {
            screen.show();
            this.currentScreen = screen;
        } else {
            console.error(`Screen ${name} not found`);
        }
    }

    getCurrentScreen() {
        return this.currentScreen;
    }
}

export const screenManager = new ScreenManager();
export default ScreenManager; 