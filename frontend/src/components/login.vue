<template>
  <div class="login-container">

    <!-- <img src="./images/logo.png" alt="MyReddit"/> -->

    <h2 v-if="isRegistering">Create an Account</h2>
    <h2 v-else>Forum Login</h2>

    <form @submit.prevent="isRegistering ? userRegister() : userLogin()">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" placeholder="Enter your username" required>
      </div>

      <div v-if="isRegistering" class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" placeholder="Enter your email" required>
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" placeholder="Enter your password" required>
      </div>

      <button type="submit" class="login-btn">{{ isRegistering ? 'Register' : 'Login' }}</button>
    </form>

    <div class="extra-links">
      <p v-if="!isRegistering"><a href="#">Forgot Password?</a></p>
      <p>
        {{ isRegistering ? "Already have an account?" : "Don't have an account?" }}
        <br>
        <a href="#" @click="toggleForm">{{ isRegistering ? "Login here" : "Register here" }}</a>
      </p>
    </div>

  </div>
</template>

<script>
import {useAuthStore} from '@/stores/auth';

export default {
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

<style scoped>
/* Global reset */
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

.login-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(250, 249, 249, 0.1);
  width: 300px;
}

.login-container h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  background-color: #3498db;
  color: #fff;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}

.login-btn:hover {
  background-color: #2980b9;
}

.extra-links {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.extra-links a {
  color: #3498db;
  text-decoration: none;
  cursor: pointer;
}

.extra-links a:hover {
  text-decoration: underline;
}
</style>
