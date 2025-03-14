import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/login.vue";

const routes = [
  { path: "/", component: Login } // Default Route (Login Page)

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation Guard to Protect Forum Page
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("currentUser"); // Check if user is logged in

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/"); // Redirect to Login if not authenticated
  } else {
    next(); // Proceed to requested route
  }
});

export default router;
