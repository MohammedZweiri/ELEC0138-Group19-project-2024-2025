<template>
  <div>
    <header>
      <h1>My Forum</h1>
      <button class="logout-btn" @click="logout">Logout</button>
    </header>
    <main>
      <section id="threads">
        <article class="thread" v-for="(thread, index) in threads" :key="thread.id">
          <h2>{{ thread.title }}</h2>
          <div class="thread-meta">Posted by {{ thread.author }} on {{ thread.date }}</div>
          <p v-html="thread.content"></p>
          <div v-if="!thread.protected && thread.author == currentUser">
            <button @click="editThread(index)">Edit</button>
            <button @click="deleteThread(index)">Delete</button>
          </div>
        </article>
      </section>
      <section class="new-thread">
        <h2>{{ isEditing ? 'Edit Thread' : 'Create a New Thread' }}</h2>
        <form @submit.prevent="submitThread">
          <div>
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="newThread.username" :disabled="isEditing" required>
          </div>
          <div>
            <label for="content">Content:</label>
            <textarea id="content" v-model="newThread.content" rows="6" required></textarea>
          </div>
          <button type="submit">{{ isEditing ? 'Update Thread' : 'Submit Thread' }}</button>
          <button v-if="isEditing" type="button" @click="cancelEdit">Cancel</button>
        </form>
      </section>
    </main>
    <footer>
      <p>&copy; 2025 My Forum. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import {useForumStore} from '@/stores/forum';
import {useAuthStore} from '@/stores/auth';

export default {
  data() {
    return {
      newThread: {username: '', title: '', content: ''}
    };
  },

  computed: {
    threads() {
      return this.forumStore.allThreads;
    },
    isEditing() {
      return this.forumStore.isEditing;
    },
    currentUser() {
      return this.authStore.username;
    }
  },

  created() {
    this.forumStore = useForumStore();
    this.authStore = useAuthStore();

    this.checkAuth();

    this.newThread.username = this.authStore.username || '';

    this.fetchPosts();
  },

  methods: {
    async fetchPosts() {
      try {
        await this.forumStore.fetchPosts();
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    },

    async submitThread() {
      if (!this.newThread.content) return;

      try {
        if (this.isEditing) {
          await this.forumStore.updatePost({
            id: this.forumStore.currentPost.id,
            username: this.forumStore.currentPost.username,
            content: this.newThread.content
          });
        } else {
          await this.forumStore.createPost({
            username: this.newThread.username,
            content: this.newThread.content
          });
        }
        this.newThread.content = '';
      } catch (error) {
        console.error('Error submitting thread:', error);
        alert('Oops! Something went wrong. Please try again.');
      }
    },

    async deleteThread(index) {
      try {
        await this.forumStore.deletePost(index);
      } catch (error) {
        console.error('Error deleting post:', error);
        alert('Oops! Something went wrong. Please try again.');
      }
    },

    editThread(index) {
      this.forumStore.startEditing(index);
      this.newThread.content = this.forumStore.currentPost.content;
    },

    cancelEdit() {
      this.forumStore.cancelEditing();
      this.newThread.content = '';
    },

    logout() {
      this.authStore.logout();
      this.$router.push('/');
    },

    checkAuth() {
      if (!this.authStore.isAuthenticated) {
        this.$router.push('/');
      }
    }
  }
}
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}

header {
  position: relative;
  left: 300px;
  background-color: #333;
  color: #fff;
  padding: 1em 0;
  text-align: center;
}

header nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
}

header nav ul li {
  margin: 0 15px;
}

header nav ul li a {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
}

main {
  position: relative;
  left: 300px;
  padding: 20px;
  max-width: 800px;
  margin: 20px auto;
}

.thread {
  background-color: #fff;
  border: 1px solid #ddd;
  margin-bottom: 20px;
  padding: 15px;
  border-radius: 5px;
}

.thread-meta {
  font-size: 0.9em;
  color: #777;
  margin-bottom: 10px;
}

.new-thread {
  background-color: #fff;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-top: 40px;
}

.new-thread form div {
  margin-bottom: 15px;
}

.new-thread form label {
  display: block;
  margin-bottom: 5px;
}

.new-thread form input,
.new-thread form textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.new-thread form button {
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

.new-thread form button:hover {
  background-color: #555;
}

footer {
  position: relative;
  left: 300px;
  background-color: #333;
  color: #fff;
  text-align: center;
  padding: 1em 0;
  margin-top: 40px;
}
</style>