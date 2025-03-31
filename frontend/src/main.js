import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from "./router";
import { VueRecaptchaPlugin } from 'vue-recaptcha-v3';

console.log("🔵 Initializing Vue App...");

const app = createApp(App);

app.use(router);

// Load reCAPTCHA plugin safely
app.use(VueRecaptchaPlugin, {
    siteKey: "6LffjQMrAAAAALrbVBCHbmOqJrPJVvtlmSf2Cl-G", // Uses environment variable
    loaderOptions: {
        useRecaptchaNet: true,  // Useful for certain regions
        autoHideBadge: false    
    }
});

console.log("✅ VueRecaptchaPlugin registered!");

app.mount('#app');
console.log("✅ App mounted!");

// Debugging: Check if reCAPTCHA is available
// setTimeout(() => {
//     console.log("🔍 Checking window.grecaptcha:", window.grecaptcha);
// }, 3000);
