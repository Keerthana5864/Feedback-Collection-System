/**
 * theme.js - Universal Theme Management for Faculty Feedback System
 * Handles light/dark mode persistence and toggling.
 */

const ThemeManager = {
    storageKey: 'theme-preference',

    init() {
        this.applyTheme();
        this.setupToggle();
    },

    applyTheme() {
        const theme = localStorage.getItem(this.storageKey) || 'light';
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    },

    toggleTheme() {
        const isDark = document.body.classList.toggle('dark-mode');
        localStorage.setItem(this.storageKey, isDark ? 'dark' : 'light');
    },

    setupToggle() {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            // Set initial state of the toggle switch based on current theme
            const currentTheme = localStorage.getItem(this.storageKey) || 'light';
            themeToggle.checked = currentTheme === 'dark';

            themeToggle.addEventListener('change', () => {
                this.toggleTheme();
            });
        }
    }
};

// Initialize theme as early as possible to prevent flashing
ThemeManager.applyTheme();

// Also initialize on DOMContentLoaded to setup the toggle switch
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
});
