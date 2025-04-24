import {createRouter, createWebHistory} from "vue-router";
import Login from "@/components/login.vue";

const routes = [
    {path: "/", component: Login}, // Default Route (Login Page)
    {path: "/:pathMatch(.*)*", redirect: "/"} // Redirect all unknown routes to login
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
