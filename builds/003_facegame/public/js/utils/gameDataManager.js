class GameDataManager {
    constructor() {
        this.allFaces = [];        // All faces from data.json
        this.remainingFaces = [];  // Faces still to be guessed
        this.currentIndex = 0;
        this.currentFace = null;
        this.nextFace = null;
        this.gameMode = 'easy';
        this.loadFaces();
    }

    async loadFaces() {
        try {
            const response = await fetch('data.json');
            const data = await response.json();
            this.allFaces = data.people; // Extract the people array
            this.resetGame();
        } catch (error) {
            console.error('Error loading faces:', error);
            this.allFaces = [];
            this.remainingFaces = [];
        }
    }

    shuffleFaces() {
        // Fisher-Yates shuffle algorithm
        for (let i = this.remainingFaces.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.remainingFaces[i], this.remainingFaces[j]] = 
                [this.remainingFaces[j], this.remainingFaces[i]];
        }
    }

    setGameMode(mode) {
        this.gameMode = mode;
    }

    getNameForMode(person) {
        if (this.gameMode === 'easy') {
            // Easy mode: always use first name
            return person.firstName || person.name.split(' ')[0];
        } else {
            // Hard mode: randomly use first or last name
            if (Math.random() < 0.5) {
                return person.firstName || person.name.split(' ')[0];
            } else {
                return person.lastName || person.name.split(' ').slice(-1)[0];
            }
        }
    }

    getRandomIncorrectFace(currentFace) {
        // Filter out the current face and get faces with matching gender
        const possibleFaces = this.allFaces.filter(face => 
            // Different person (not the same first or last name)
            (face.firstName !== currentFace.firstName || 
             face.lastName !== currentFace.lastName) &&
            // Same gender
            face.gender === currentFace.gender
        );

        // If no faces with matching gender are found (shouldn't happen normally),
        // fall back to any face except the current one
        if (possibleFaces.length === 0) {
            console.warn('No faces found with matching gender, falling back to any face');
            return this.allFaces.find(face => 
                face.firstName !== currentFace.firstName || 
                face.lastName !== currentFace.lastName
            );
        }

        // Return a random face from the possible faces
        return possibleFaces[Math.floor(Math.random() * possibleFaces.length)];
    }

    getNextPair() {
        if (this.remainingFaces.length === 0) {
            return null;
        }

        // Get the current face
        const currentFace = this.remainingFaces[0];

        // Get a random incorrect face that's different from the current face
        const incorrectFace = this.getRandomIncorrectFace(currentFace);

        // Randomly decide if the correct name should be on top
        const isTopCorrect = Math.random() < 0.5;

        return {
            currentFace,
            incorrectFace,
            isTopCorrect
        };
    }

    handleAnswer(isCorrect) {
        if (this.remainingFaces.length === 0) return;

        if (isCorrect) {
            // Remove the current face from remaining faces
            this.remainingFaces.shift();
        } else {
            // Move the current face to a random position in the remaining faces
            const currentFace = this.remainingFaces.shift();
            const randomIndex = Math.floor(Math.random() * (this.remainingFaces.length + 1));
            this.remainingFaces.splice(randomIndex, 0, currentFace);
        }
    }

    checkAnswer(isSwipeUp, currentPair) {
        if (!currentPair) return false;
        return (isSwipeUp && currentPair.isTopCorrect) ||
               (!isSwipeUp && !currentPair.isTopCorrect);
    }

    resetGame() {
        // Make a copy of all faces for the remaining faces
        this.remainingFaces = [...this.allFaces];
        this.shuffleFaces();
    }

    getRemainingCount() {
        return this.remainingFaces.length;
    }

    getTotalCount() {
        return this.allFaces.length;
    }
}

export const gameDataManager = new GameDataManager(); 