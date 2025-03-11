<template>
  <div class="login-container">
    <h2 v-if="isRegistering">Create an Account</h2>
    <h2 v-else>Forum Login</h2>

    <form @submit.prevent="isRegistering ? registerUser() : submitLogin()">
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
export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      isRegistering: false
    };
  },
  methods: {
    async submitLogin() {
      if (!this.username || !this.password) {
        alert("Please fill in all fields.");
        return;
      }

      const loginData = {
        username: this.username,
        password: this.password
      };

      try {
        const baseUrl = import.meta.env.VITE_BASE_URL
        const response = await fetch(`${baseUrl}/user/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(loginData)
        });

        if (!response.ok) {
          throw new Error("Invalid login credentials.");
        }

        const result = await response.json();
        console.log("Login successful:", result);

        // Store authentication token
        localStorage.setItem("userToken", result.token);
        localStorage.setItem("currentUser", this.username);

        //alert("Login successful!");
        this.$router.push("/forum"); // Redirect to Forum Page
      } catch (error) {
        console.error("Login error:", error);
        alert("Login failed. Please check your credentials.");
      }
    },

    async registerUser() {
      if (!this.username || !this.email || !this.password) {
        alert("Please fill in all fields.");
        return;
      }

      const newUser = {
        username: this.username,
        email: this.email,
        password: this.password
      };

      try {
        const baseUrl = import.meta.env.VITE_BASE_URL
        const response = await fetch(`${baseUrl}/user/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(newUser)
        });

        if (!response.ok) {
          throw new Error("Registration failed.");
        }

        console.log("Registration successful:", await response.json());

        alert("Account created successfully! Please log in.");
        this.toggleForm(); // Switch to login form after registration
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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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
