<template>
  <button
      aria-label="Toggle dark mode"
      class="theme-toggle-button"
      @click="toggleTheme"
  >
    <!-- Sun icon for dark mode -->
    <svg
        v-if="isDark"
        class="sun-icon"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
    >
      <path
          d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
      />
    </svg>

    <!-- Moon icon for light mode -->
    <svg
        v-else
        class="moon-icon"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
    >
      <path
          d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
      />
    </svg>
  </button>
</template>

<script>
export default {
  name: 'ThemeToggle',
  data() {
    return {
      isDark: false
    }
  },
  mounted() {
    // Check for saved theme preference or use system preference
    const savedTheme = localStorage.getItem('theme')
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

    this.isDark = savedTheme === 'dark' || (savedTheme === null && systemPrefersDark)
    this.updateTheme()
  },
  methods: {
    toggleTheme() {
      this.isDark = !this.isDark
      this.updateTheme()
    },
    updateTheme() {
      // Update the document class
      if (this.isDark) {
        document.documentElement.classList.add('dark')
        localStorage.setItem('theme', 'dark')
      } else {
        document.documentElement.classList.remove('dark')
        localStorage.setItem('theme', 'light')
      }
    }
  }
}
</script>

<style>
/* Theme toggle button */
.theme-toggle-button {
  @apply rounded-full p-2 transition-colors hover:bg-gray-200 dark:hover:bg-gray-700;
}

/* Icon styles */
.sun-icon {
  @apply h-5 w-5 text-yellow-500;
}

.moon-icon {
  @apply h-5 w-5 text-indigo-600;
}
</style> 