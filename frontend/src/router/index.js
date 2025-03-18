import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/login.vue";
import Forum from "@/components/forum.vue";

const routes = [
  { path: "/", component: Login }, // Default Route (Login Page)
  { path: "/forum", component: Forum, meta: { requiresAuth: true } } // Protected Route
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation Guard to Protect Forum Page
router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem("access_token"); // Check if user has a valid token

  if (to.meta.requiresAuth && !accessToken) {
    next("/"); // Redirect to Login if no token
  } else {
    next(); // Proceed to requested route
  }
});

export default router;
