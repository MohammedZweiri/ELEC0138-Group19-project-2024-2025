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
  const isAuthenticated = localStorage.getItem("userToken"); // Check if user is logged in

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/"); // Redirect to Login if not authenticated
  } else {
    next(); // Proceed to requested route
  }
});

export default router;
