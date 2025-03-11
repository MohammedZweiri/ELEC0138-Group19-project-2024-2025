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
            <label for="thread-title">Thread Title:</label>
            <input type="text" id="thread-title" v-model="newThread.title" required>
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
      fetch(`${baseUrl}/post/get`)
        .then(response => response.json())
        .then(data => {
          if (data.code === 200 && data.messages) {
            this.threads = [
              ...this.threads,
              ...data.messages.map(post => ({
                id: post.postID,
                author: post.postName,
                content: post.postText,
                date: post.postTime,
                protected: false // Add any default or fetched data here
              }))
            ];
          } else {
            console.error('No posts or unexpected data structure');
          }
        })
        .catch(error => {
          console.error('Error fetching posts:', error);
        });
    }
    ,

    async submitThread() {
      let newPost = null;
      let formattedPost = null;
      let updatedPost = null;
      let updatedPostDB = null;
      if (this.newThread.title && this.newThread.content) {
        if (this.isEditing) {
          try {
            updatedPostDB = {
              forumID: 1,
              postID: this.newThread.id,
              postName: this.newThread.username,
              postTime: new Date().toISOString().split("T")[0],
              postText: this.newThread.content
            }
            const baseUrl = import.meta.env.VITE_BASE_URL;
            const response = await fetch(`${baseUrl}/post/update`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(updatedPostDB) // Convert formattedPost to JSON format
            });

            if (!response.ok) {
              throw new Error(`Failed to update post: ${response.statusText}`);
            }

            const responseData = await response.json();
            console.log("Post successfully updated:", responseData);

            updatedPost = {
              id: updatedPostDB.postID,
              title: this.newThread.title,
              content: updatedPostDB.postText,
              author: updatedPostDB.postName,
              date: updatedPostDB.postTime

            }
            this.threads = updatedPost;

          } catch (error) {
            console.error("Error updating post:", error);
          }
          this.isEditing = false;
          this.editIndex = null;
        } else {
          newPost = {
            id: this.threads.length + 5,
            title: this.newThread.title,
            author: this.newThread.username,
            date: new Date().toISOString().split('T')[0],
            content: this.newThread.content
          }
          formattedPost = {
            forumID: 1,
            postID: newPost.id,
            postName: newPost.author,
            postText: newPost.content,
            postTime: newPost.date
          }


          try {
            const baseUrl = import.meta.env.VITE_BASE_URL;
            const response = await fetch(`${baseUrl}/post/send`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(formattedPost) // Convert formattedPost to JSON format
            });

            if (!response.ok) {
              throw new Error(`Failed to send post: ${response.statusText}`);
            }

            const responseData = await response.json();
            console.log("Post successfully sent:", responseData);

            // If the post was successfully sent, add it to the local threads list
            this.threads.push(newPost);
            this.newThread = { username: "", title: "", content: "" }; // Reset form fields
          } catch (error) {
            console.error("Error submitting post:", error);
          }

        }
      }

      window.location.reload()
    },

    logout() {
      localStorage.removeItem("userToken"); // Remove authentication token
      this.$router.push("/"); // Redirect to login page
    },

    checkAuth() {
      const isAuthenticated = localStorage.getItem("userToken");
      if (!isAuthenticated) {
        this.$router.push("/"); // Redirect to login if not authenticated
      }
    },

    async deleteThread(index) {
      let formattedPost = null;
      formattedPost = {
        forumID: 1,
        postID: this.threads[index].id,
        postName: this.threads[index].author
      }
      try {
        const baseUrl = import.meta.env.VITE_BASE_URL;
        const response = await fetch(`${baseUrl}/post/delete`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(formattedPost) // Convert formattedPost to JSON format
        });

        if (!response.ok) {
          throw new Error(`Failed to delet post: ${response.statusText}`);
        }

        const responseData = await response.json();
        console.log("Post successfully deleted:", responseData);

      } catch (error) {
        console.error("Error deleting post:", error);
      }
      this.threads.splice(index, 1);
      window.location.reload()
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