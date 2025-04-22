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
          <button class="logout-button" @click="logout">
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

        <div class="thread-list">
          <article v-for="(thread, index) in threads" :key="thread.id" class="thread-card">
            <div class="flex items-start justify-between">
              <div>
                <h3 class="thread-title">{{ thread.title }}</h3>
                <div class="thread-meta">
                  <span class="inline-flex items-center">
                    <UserIcon/>
                    {{ thread.author }}
                  </span>
                  <span>•</span>
                  <span class="inline-flex items-center">
                    <CalendarIcon/>
                    {{ thread.date }}
                  </span>
                </div>
              </div>

              <div v-if="!thread.protected && thread.author == currentUser" class="flex space-x-2">
                <button class="edit-button" @click="editThread(index)">
                  <EditIcon/>
                </button>
                <button class="delete-button" @click="deleteThread(index)">
                  <DeleteIcon/>
                </button>
              </div>
            </div>

            <div class="mt-4 prose dark:prose-invert prose-sm max-w-none">
              <p class="thread-content" v-html="thread.content"></p>
            </div>
          </article>

          <div v-if="threads.length === 0" class="empty-state">
            <EmptyStateIcon/>
            <p class="empty-state-title">No threads yet</p>
            <p class="empty-state-subtitle">Be the first to start a discussion!</p>
          </div>
        </div>
      </section>

      <!-- Create/Edit Thread Form -->
      <section class="form-section">
        <div class="form-card">
          <h2 class="form-title">
            <span class="mr-2">{{ isEditing ? 'Edit Your Post' : 'Start a New Discussion' }}</span>
            <span v-if="isEditing" class="edit-badge">
              Editing
            </span>
          </h2>

          <form class="space-y-5" @submit.prevent="submitThread">
            <div>
              <label class="form-label" for="username">
                Username
              </label>
              <input id="username" v-model="newThread.username" :disabled="isEditing" class="form-input"
                     readonly required type="text">
            </div>

            <div>
              <label class="form-label" for="content"> Content </label>
              <textarea id="content" v-model="newThread.content" class="form-textarea"
                        placeholder="Share your thoughts..." required rows="8">
              </textarea>
            </div>

            <div class="flex gap-3">
              <button
                  class="primary-button"
                  type="submit">
                {{ isEditing ? 'Update Post' : 'Publish Post' }}
              </button>
              <button
                  v-if="isEditing"
                  class="secondary-button"
                  type="button"
                  @click="cancelEdit">
                Cancel
              </button>
            </div>
          </form>
        </div>
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
import UserIcon from './icons/UserIcon.vue';
import CalendarIcon from './icons/CalendarIcon.vue';
import EditIcon from './icons/EditIcon.vue';
import DeleteIcon from './icons/DeleteIcon.vue';
import EmptyStateIcon from './icons/EmptyStateIcon.vue';

export default {
  components: {
    ThemeToggle,
    UserIcon,
    CalendarIcon,
    EditIcon,
    DeleteIcon,
    EmptyStateIcon
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

main.container-wrapper {
  @apply flex-1 flex flex-col;
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
  @apply text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center justify-center;
}

.thread-counter {
  @apply text-xs py-1 px-2 bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 rounded-full;
}

/* Thread List Section */
section.mb-10 {
  @apply flex-1 mt-8;
}

.thread-list {
  @apply space-y-5 flex-1;
}

/* Thread cards */
.thread-card {
  @apply bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 transition-all duration-200 hover:shadow-lg border border-gray-100 dark:border-gray-700 flex flex-col;
}

.thread-title {
  @apply text-xl font-bold text-gray-900 dark:text-white mb-2;
}

.thread-meta {
  @apply mb-3 flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400;
}

.thread-content {
  @apply text-gray-700 dark:text-gray-300 flex-1;
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
.form-section {
  @apply mt-8 mb-12;
}

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