import {defineStore} from 'pinia';
import {postService} from '@/services/api';


export const useForumStore = defineStore('forum', {
    state: () => ({
        threads: [{
            id: 1,
            title: 'Welcome to the Forum!',
            author: 'Admin',
            date: '2025-02-07',
            content: 'This is the first thread in our forum. Feel free to start a new discussion or reply to this thread.',
            protected: true
        }, {
            id: 2,
            title: 'Forum Guidelines',
            author: 'Moderator',
            date: '2025-02-06',
            content: 'Please read our forum guidelines before posting. There is none, LOL!!',
            protected: true
        }], isEditing: false, editIndex: null, currentPost: {
            id: null, title: '', username: '', content: ''
        }
    }),

    getters: {
        allThreads: (state) => state.threads
    },

    actions: {
        async fetchPosts() {
            try {
                const posts = await postService.getPosts();

                if (Array.isArray(posts)) {
                    const formattedPosts = posts.map(post => ({
                        id: post.post_id,
                        author: post.username,
                        content: post.text,
                        date: post.time,
                        title: `Post #${post.post_id}`,
                        protected: false
                    }));

                    this.threads = [...this.threads.filter(thread => thread.protected), ...formattedPosts];
                }
            } catch (error) {
                console.error('Fetching posts error:', error);
                throw error;
            }
        },

        async createPost(postData) {
            try {
                await postService.createPost({
                    forum_id: 1,
                    username: postData.username,
                    time: new Date().toISOString().slice(0, 19).replace('T', ' '),
                    text: postData.content
                });

                await this.fetchPosts();

                this.resetCurrentPost();
            } catch (error) {
                console.error('Creating post error:', error);
                throw error;
            }
        },

        async updatePost(postData) {
            try {
                await postService.updatePost({
                    forum_id: 1, post_id: postData.id, username: postData.username, text: postData.content
                });

                if (this.editIndex !== null) {
                    this.threads[this.editIndex] = {
                        ...this.threads[this.editIndex], content: postData.content
                    };
                }

                this.isEditing = false;
                this.editIndex = null;
                this.resetCurrentPost();
            } catch (error) {
                console.error('Updating post error:', error);
                throw error;
            }
        },

        async deletePost(index) {
            try {
                const post = this.threads[index];

                await postService.deletePost({
                    forum_id: 1, post_id: post.id, username: post.author
                });

                this.threads.splice(index, 1);
            } catch (error) {
                console.error('Deleting post error:', error);
                throw error;
            }
        },

        startEditing(index) {
            const post = this.threads[index];

            this.currentPost = {
                id: post.id, title: post.title, username: post.author, content: post.content
            };

            this.isEditing = true;
            this.editIndex = index;
        },

        resetCurrentPost() {
            this.currentPost = {
                id: null, title: '', username: '', content: ''
            };
        },

        cancelEditing() {
            this.isEditing = false;
            this.editIndex = null;
            this.resetCurrentPost();
        }
    }
});
