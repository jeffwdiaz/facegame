export default class Screen {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = containerId;
            document.querySelector('.game-container').appendChild(this.container);
        }
        this.container.classList.add('screen');
        this.hide();
    }

    show() {
        this.container.style.display = 'flex';
    }

    hide() {
        this.container.style.display = 'none';
    }

    render() {
        // Override this method in child classes
        throw new Error('render() method must be implemented');
    }

    cleanup() {
        // Override this method in child classes if needed
    }
} 