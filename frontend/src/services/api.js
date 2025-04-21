const baseUrl = import.meta.env.VITE_BASE_URL;

async function handleResponse(response, errorMessage) {
    if (!response.ok) {
        throw new Error(errorMessage);
    }

    const contentType = response.headers.get("Content-Type");
    if (contentType && contentType.includes("application/json")) {
        const text = await response.text();
        return text ? JSON.parse(text) : null;
    }

    return null;
}

export const userService = {

    async login(loginData) {
        const response = await fetch(`${baseUrl}/api/user/login`, {
            method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(loginData)
        });

        return await handleResponse(response, "Login failed, please check your credentials");
    },

    async register(userData) {
        const response = await fetch(`${baseUrl}/api/user/register`, {
            method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(userData)
        });

        return await handleResponse(response, "Registration failed, please check your data");
    }
};

export const postService = {

    async getPosts() {
        const token = localStorage.getItem("access_token");

        const response = await fetch(`${baseUrl}/api/post`, {
            method: "GET", headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        return await handleResponse(response, "Failed to fetch posts");
    },

    async createPost(postData) {
        const token = localStorage.getItem("access_token");

        const response = await fetch(`${baseUrl}/api/post`, {
            method: "POST", headers: {
                "Content-Type": "application/json", "Authorization": `Bearer ${token}`
            }, body: JSON.stringify(postData)
        });

        return await handleResponse(response, "Failed to create post");
    },

    async updatePost(postData) {
        const token = localStorage.getItem("access_token");

        const response = await fetch(`${baseUrl}/api/post`, {
            method: "PUT", headers: {
                "Content-Type": "application/json", "Authorization": `Bearer ${token}`
            }, body: JSON.stringify(postData)
        });

        return await handleResponse(response, "Failed to update post");
    },

    async deletePost(postData) {
        const token = localStorage.getItem("access_token");

        const response = await fetch(`${baseUrl}/api/post`, {
            method: "DELETE", headers: {
                "Content-Type": "application/json", "Authorization": `Bearer ${token}`
            }, body: JSON.stringify(postData)
        });

        return await handleResponse(response, "Failed to delete post");
    }
};
