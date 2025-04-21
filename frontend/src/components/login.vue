<template>
  <div class="login-container">
    <div class="absolute top-4 right-4">
      <ThemeToggle/>
    </div>

    <div class="login-card">
      <div class="mb-8 text-center">
        <h2 class="login-title">
          {{ isRegistering ? 'Join Our Community' : 'Welcome Back' }}
        </h2>
        <p class="login-subtitle">
          {{ isRegistering ? 'Create a new account' : 'Sign in to your account' }}
        </p>
      </div>

      <form @submit.prevent="isRegistering ? userRegister() : userLogin()" class="space-y-6">
        <div>
          <label for="username" class="form-label">Username</label>
          <div class="relative">
            <input type="text" id="username" v-model="username"
                   placeholder="Enter your username" required class="form-input">
          </div>
        </div>

        <div v-if="isRegistering">
          <label for="email" class="form-label">Email</label>
          <div class="relative">
            <input type="email" id="email" v-model="email"
                   placeholder="you@example.com" required class="form-input">
          </div>
        </div>

        <div>
          <label for="password" class="form-label">Password</label>
          <div class="relative">
            <input type="password" id="password" v-model="password"
                   placeholder="Enter your password" required class="form-input">
          </div>
        </div>

        <button type="submit" class="submit-button">
          {{ isRegistering ? 'Create Account' : 'Sign In' }}
        </button>
      </form>

      <div class="mt-8 text-center">
        <p v-if="!isRegistering" class="mb-4">
          <a href="#" class="forgot-password-link"> Forgot your password? </a>
        </p>
        <div class="divider">
          <div class="divider-line"></div>
          <div class="divider-text">
            <span class="divider-label">
              {{ isRegistering ? "Already have an account?" : "Need an account?" }}
            </span>
          </div>
        </div>
        <button @click="toggleForm" class="toggle-form-button">
          {{ isRegistering ? "Sign in instead" : "Create an account" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import ThemeToggle from './ThemeToggle.vue';
import {useAuthStore} from '@/stores/auth';

export default {
  components: {
    ThemeToggle
  },
  data() {
    return {username: '', email: '', password: '', loading: false, isRegistering: false};
  },

  methods: {
    async submitLogin(token) {
      if (!this.username || !this.password) {
        alert("Please fill in all fields.");
        return;
      }

      try {
        const authStore = useAuthStore();
        await authStore.login(this.username, this.password, token);
        this.$router.push("/forum");
      } catch (error) {
        console.error("Login error:", error);
        alert("Login failed. Please check your credentials.");
      }
    },

    async userLogin() {
      const siteKey = import.meta.env.VITE_SITE_KEY

      if (!window.grecaptcha || !window.grecaptcha.execute) {
        console.error('reCAPTCHA not loaded');
        alert('reCAPTCHA is not loaded. Please refresh the page.');
        return;
      }

      try {
        const token = await window.grecaptcha.execute(siteKey, {action: 'login'});
        await this.submitLogin(token);
      } catch (error) {
        console.error('reCAPTCHA error:', error);
        alert('Error verifying reCAPTCHA. Please try again.');
      }
    },

    async userRegister() {
      if (!this.username || !this.email || !this.password) {
        alert("Please fill in all fields.");
        return;
      }

      try {
        const authStore = useAuthStore();
        await authStore.register(this.username, this.email, this.password);

        alert("Account created successfully! Please log in.");
        this.toggleForm();
      } catch (error) {
        console.error("Registration error:", error);
        alert("Failed to register. Try again later.");
      }
    },

    toggleForm() {
      this.isRegistering = !this.isRegistering;
      this.username = "";
      this.email = "";
      this.password = "";
    }
  }
};
</script>

<style>
/* Login page container */
.login-container {
  @apply min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4;
}

/* Card styles */
.login-card {
  @apply w-full max-w-md bg-white dark:bg-gray-800 rounded-xl shadow-2xl p-8 transition-all duration-300;
}

.login-title {
  @apply text-3xl font-extrabold text-gray-900 dark:text-white mb-2;
}

.login-subtitle {
  @apply text-gray-600 dark:text-gray-400;
}

/* Form elements */
.form-label {
  @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1;
}

.form-input {
  @apply w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200;
}

.submit-button {
  @apply w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 transform hover:scale-[1.02] shadow-md;
}

/* Links and toggles */
.forgot-password-link {
  @apply text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 text-sm transition-colors;
}

.toggle-form-button {
  @apply mt-2 inline-flex items-center justify-center text-indigo-600 dark:text-indigo-400 hover:underline transition-colors;
}

/* Divider */
.divider {
  @apply relative py-3;
}

.divider-line {
  @apply absolute inset-0 flex items-center;
}

.divider-line:before {
  @apply w-full border-t border-gray-300 dark:border-gray-600 content-[''];
}

.divider-text {
  @apply relative flex justify-center;
}

.divider-label {
  @apply px-2 bg-white dark:bg-gray-800 text-sm text-gray-500 dark:text-gray-400;
}
</style>
