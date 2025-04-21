import './assets/main.css'

import {createApp} from 'vue'
import {createPinia} from 'pinia'
import {VueRecaptchaPlugin} from 'vue-recaptcha-v3';

import App from './App.vue'
import router from "./router";


console.log("🔵 Initializing Vue App...");

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(VueRecaptchaPlugin, {
    siteKey: import.meta.env.VITE_SITE_KEY, // Uses environment variable
    loaderOptions: {
        useRecaptchaNet: true,  // Useful for certain regions
        autoHideBadge: false
    }
});

app.mount('#app');
