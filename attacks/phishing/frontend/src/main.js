import './assets/main.css'

import {createApp} from 'vue'

import App from './App.vue'
import router from "./router";

// Initialize theme based on user preference
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme')
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

    if (savedTheme === 'dark' || (savedTheme === null && systemPrefersDark)) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }
}

// Run theme initialization before app mount
initializeTheme();

console.log("🔵 Initializing Vue App...");

const app = createApp(App);

app.use(router);

app.mount('#app');
