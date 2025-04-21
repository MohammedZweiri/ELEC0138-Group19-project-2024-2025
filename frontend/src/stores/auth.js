import {defineStore} from 'pinia';
import {userService} from '@/services/api';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        currentUser: localStorage.getItem('currentUser') || null,
        accessToken: localStorage.getItem('access_token') || null
    }),

    getters: {
        isAuthenticated: (state) => !!state.accessToken,
        username: (state) => state.currentUser,
    },

    actions: {
        async login(username, password, recaptcha_token) {
            try {
                const loginData = {username, password, recaptcha_token};

                const result = await userService.login(loginData);

                this.currentUser = result.username;
                this.accessToken = result.access_token;

                localStorage.setItem('currentUser', result.username);
                localStorage.setItem('access_token', result.access_token);

                return true;
            } catch (error) {
                console.error('Login error:', error);
                throw error;
            }
        },

        async register(username, email, password) {
            try {
                const userData = {username, email, password};

                return await userService.register(userData);
            } catch (error) {
                console.error('Registration error:', error);
                throw error;
            }
        },

        logout() {
            this.currentUser = null;
            this.accessToken = null;

            localStorage.removeItem('currentUser');
            localStorage.removeItem('access_token');
        }
    }
});
