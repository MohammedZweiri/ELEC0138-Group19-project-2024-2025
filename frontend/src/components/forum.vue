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
          <p>{{ thread.content }}</p>
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
        </form>
      </section>
    </main>
    <footer>
      <p>&copy; 2025 My Forum. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      threads: [
        { id: 1, title: 'Welcome to the Forum!', author: 'Admin', date: '2025-02-07', content: 'This is the first thread in our forum. Feel free to start a new discussion or reply to this thread.', protected: true },
        { id: 2, title: 'Forum Guidelines', author: 'Moderator', date: '2025-02-06', content: 'Please read our forum guidelines before posting. There is none, LOL!!', protected: true }
      ],
      newThread: {
        username: '',
        title: '',
        content: ''
      },
      isEditing: false,
      editIndex: null,
      currentUser: localStorage.getItem("currentUser") || "", // Retrieve logged-in user
    };
  },
  mounted() {
    console.log('Component mounted, fetching posts');
    this.checkAuth();
    this.fetchPosts(); // Call the method to fetch posts when the component is mounted
  },
  methods: {
    fetchPosts() {
      const baseUrl = import.meta.env.VITE_BASE_URL;
      fetch(`${baseUrl}/api/post`)
          .then(response => response.json())
          .then(data => {
            if (Array.isArray(data)) {
              const formattedPosts = data.map(post => ({
                id: post.post_id,
                author: post.username,
                content: post.text,
                date: post.time,
                title: `Post #${post.post_id}`,
                protected: false
              }));
              this.threads = [...this.threads, ...formattedPosts];
            } else {
              console.error('Unexpected data structure');
            }
          })
          .catch(error => {
            console.error('Error fetching posts:', error);
          });
    },

    async submitThread() {
      if (this.newThread.content) {
        const currentTime = new Date().toISOString().slice(0, 19).replace('T', ' ');

        if (this.isEditing) {
          try {
            const updatedPost = {
              forum_id: 1,
              post_id: this.newThread.id,
              username: this.newThread.username,
              text: this.newThread.content
            };

            const baseUrl = import.meta.env.VITE_BASE_URL;
            const response = await fetch(`${baseUrl}/api/post`, {
              method: "PUT",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(updatedPost)
            });

            if (!response.ok) {
              throw new Error(`Failed to update post: ${response.statusText}`);
            }

            console.log("Post successfully updated");

            this.threads[this.editIndex] = {
              ...this.threads[this.editIndex],
              title: this.newThread.title,
              content: this.newThread.content
            };

            this.isEditing = false;
            this.editIndex = null;
          } catch (error) {
            console.error("Error updating post:", error);
          }
        } else {
          try {
            const newPost = {
              forum_id: 1,
              username: this.newThread.username,
              time: currentTime,
              text: this.newThread.content
            };

            const baseUrl = import.meta.env.VITE_BASE_URL;
            const response = await fetch(`${baseUrl}/api/post`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(newPost)
            });

            if (!response.ok) {
              throw new Error(`Failed to create post: ${response.statusText}`);
            }

            console.log("Post successfully created");

            this.newThread = {username: "", title: "", content: ""};

            this.fetchPosts();
          } catch (error) {
            console.error("Error creating post:", error);
          }
        }
      }
    },

    logout() {
      localStorage.removeItem("currentUser");
      localStorage.removeItem("currentRole");
      this.$router.push("/"); // Redirect to login page
    },

    checkAuth() {
      const username = localStorage.getItem("currentUser");
      if (!username) {
        this.$router.push("/"); // Redirect to login if not authenticated
      } else {
        this.newThread.username = username;
      }
    },

    async deleteThread(index) {
      try {
        const postToDelete = {
          forum_id: 1,
          post_id: this.threads[index].id,
          username: this.threads[index].author
        };

        const baseUrl = import.meta.env.VITE_BASE_URL;
        const response = await fetch(`${baseUrl}/api/post`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(postToDelete)
        });

        if (!response.ok) {
          throw new Error(`Failed to delete post: ${response.statusText}`);
        }

        console.log("Post successfully deleted");

        this.threads.splice(index, 1);
      } catch (error) {
        console.error("Error deleting post:", error);
      }
    },

    editThread(index) {
      this.newThread = {
        id: this.threads[index].id,
        title: this.threads[index].title,
        content: this.threads[index].content,
        username: this.threads[index].author
      };
      this.isEditing = true;
      this.editIndex = index;
    },
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