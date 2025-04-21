<template>
  <div class="forum-container">
    <!-- Modern Header with Glass Effect -->
    <header class="forum-header">
      <div class="container-wrapper">
        <h1 class="forum-title"> ELEC0138 Forum </h1>
        <div class="flex items-center gap-4">
          <ThemeToggle/>
          <span class="user-identifier">
            Signed in as <span class="font-medium">{{ currentUser }}</span>
          </span>
          <button @click="logout" class="logout-button">
            Logout
          </button>
        </div>
      </div>
    </header>

    <main class="container-wrapper">
      <!-- Thread List Section -->
      <section class="mb-10">
        <h2 class="section-title">
          <span class="mr-2">Recent Discussions</span>
          <span class="thread-counter">
            {{ threads.length }} threads
          </span>
        </h2>

        <div class="space-y-5">
          <article v-for="(thread, index) in threads" :key="thread.id" class="thread-card">

            <div class="flex items-start justify-between">
              <div>
                <h3 class="thread-title">{{ thread.title }}</h3>
                <div class="thread-meta">
                  <span class="inline-flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24"
                         stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                    {{ thread.author }}
                  </span>
                  <span>•</span>
                  <span class="inline-flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24"
                         stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                    {{ thread.date }}
                  </span>
                </div>
              </div>

              <div v-if="!thread.protected && thread.author == currentUser" class="flex space-x-2">
                <button @click="editThread(index)" class="edit-button">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                </button>
                <button @click="deleteThread(index)" class="delete-button">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </div>
            </div>

            <div class="mt-4 prose dark:prose-invert prose-sm max-w-none">
              <p class="thread-content" v-html="thread.content"></p>
            </div>
          </article>

          <div v-if="threads.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" class="empty-state-icon"
                 fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
            </svg>
            <p class="empty-state-title">No threads yet</p>
            <p class="empty-state-subtitle">Be the first to start a discussion!</p>
          </div>
        </div>
      </section>

      <!-- Create/Edit Thread Form -->
      <section class="form-card">
        <h2 class="form-title">
          <span class="mr-2">{{ isEditing ? 'Edit Your Post' : 'Start a New Discussion' }}</span>
          <span v-if="isEditing" class="edit-badge">
            Editing
          </span>
        </h2>

        <form @submit.prevent="submitThread" class="space-y-5">
          <div>
            <label for="username" class="form-label">
              Username
            </label>
            <input type="text" id="username" v-model="newThread.username" :disabled="isEditing"
                   required class="form-input">
          </div>

          <div>
            <label for="content" class="form-label"> Content </label>
            <textarea
                id="content"
                v-model="newThread.content"
                rows="8"
                required
                placeholder="Share your thoughts..."
                class="form-textarea"></textarea>
          </div>

          <div class="flex gap-3">
            <button
                type="submit"
                class="primary-button">
              {{ isEditing ? 'Update Post' : 'Publish Post' }}
            </button>
            <button
                v-if="isEditing"
                type="button"
                @click="cancelEdit"
                class="secondary-button">
              Cancel
            </button>
          </div>
        </form>
      </section>
    </main>

    <footer class="forum-footer">
      <div class="container-wrapper">
        <p class="footer-text">&copy; 2025 ELEC0138 Forum. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import ThemeToggle from './ThemeToggle.vue';
import {useForumStore} from '@/stores/forum';
import {useAuthStore} from '@/stores/auth';

export default {
  components: {
    ThemeToggle
  },
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

<style>
/* Add custom styles here */
.prose img {
  @apply rounded-lg shadow-md;
}

/* Container styles */
.forum-container {
  @apply flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900;
}

.container-wrapper {
  @apply container mx-auto px-4;
}

/* Header styles */
.forum-header {
  @apply sticky top-0 z-50 bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg shadow-sm border-b border-gray-200 dark:border-gray-700;
}

.forum-header .container-wrapper {
  @apply py-3 flex justify-between items-center;
}

.forum-title {
  @apply text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent;
}

.user-identifier {
  @apply text-gray-600 dark:text-gray-300 text-sm hidden md:inline-block;
}

.logout-button {
  @apply px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-pink-500 to-red-500 rounded-md shadow-sm hover:from-pink-600 hover:to-red-600 transition-all duration-200 transform hover:scale-[1.02];
}

/* Section titles */
.section-title {
  @apply text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center;
}

.thread-counter {
  @apply text-xs py-1 px-2 bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 rounded-full;
}

/* Thread cards */
.thread-card {
  @apply bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 transition-all duration-200 hover:shadow-lg border border-gray-100 dark:border-gray-700;
}

.thread-title {
  @apply text-xl font-bold text-gray-900 dark:text-white;
}

.thread-meta {
  @apply mt-1 flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400;
}

.thread-content {
  @apply text-gray-700 dark:text-gray-300;
}

/* Edit/Delete buttons */
.edit-button {
  @apply p-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-full transition-colors;
}

.delete-button {
  @apply p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors;
}

/* Empty state */
.empty-state {
  @apply text-center py-12 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-dashed border-gray-300 dark:border-gray-700;
}

.empty-state-icon {
  @apply h-12 w-12 mx-auto text-gray-400 dark:text-gray-600 mb-3;
}

.empty-state-title {
  @apply text-gray-600 dark:text-gray-400 text-lg font-medium;
}

.empty-state-subtitle {
  @apply text-gray-500 dark:text-gray-500 mt-1;
}

/* Form styles */
.form-card {
  @apply bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border border-gray-100 dark:border-gray-700;
}

.form-title {
  @apply text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center;
}

.edit-badge {
  @apply text-xs py-1 px-2 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1;
}

.form-input, .form-textarea {
  @apply w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors;
}

.form-input[disabled] {
  @apply opacity-60 cursor-not-allowed;
}

/* Button styles */
.primary-button {
  @apply px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-medium rounded-lg transition-all duration-200 transform hover:scale-[1.02] shadow-md;
}

.secondary-button {
  @apply px-4 py-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium rounded-lg transition-colors;
}

/* Footer styles */
.forum-footer {
  @apply bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-6 text-center;
}

.footer-text {
  @apply text-gray-600 dark:text-gray-400 text-sm;
}
</style>