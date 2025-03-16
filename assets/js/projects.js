// Make the function globally available for Alpine.js
window.initializeProjects = function () {
  return {
    allProjects: [],
    filteredProjects: [],
    selectedTags: [],
    allTags: [],

    init() {
      console.log("Initializing projects component");

      // Initialize with all projects
      this.allProjects = Array.from(
        document.querySelectorAll(".project-card")
      ).map((card) => ({
        element: card,
        tags: Array.from(card.querySelectorAll(".tag")).map((tag) =>
          tag.textContent.trim()
        ),
      }));
      this.filteredProjects = [...this.allProjects];

      // Extract all unique tags
      const tagSet = new Set();
      this.allProjects.forEach((project) => {
        project.tags.forEach((tag) => tagSet.add(tag));
      });
      this.allTags = Array.from(tagSet).sort();

      console.log(`Found ${this.allProjects.length} projects`);

      // Fetch fresh GitHub stats after page load
      console.log("Starting GitHub stats refresh");
      this.refreshGitHubStats();
    },

    getCsrfToken() {
      // Get CSRF token from cookie
      const name = "csrftoken=";
      const decodedCookie = decodeURIComponent(document.cookie);
      const cookieArray = decodedCookie.split(";");
      for (let cookie of cookieArray) {
        cookie = cookie.trim();
        if (cookie.indexOf(name) === 0) {
          return cookie.substring(name.length, cookie.length);
        }
      }
      return "";
    },

    refreshGitHubStats() {
      console.log("Refreshing GitHub stats...");

      fetch("/api/refresh-github-stats/", {
        headers: {
          "X-CSRFToken": this.getCsrfToken(),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => {
          console.log("Received response:", response.status);
          return response.json();
        })
        .then((data) => {
          console.log("Received data:", data);
          // Update GitHub stats in the UI
          const stats = data.github_stats;
          Object.keys(stats).forEach((projectId) => {
            this.updateProjectStats(projectId, stats[projectId]);
          });
          console.log("Stats updated successfully");
        })
        .catch((error) => {
          console.error("Error refreshing GitHub stats:", error);
        });
    },

    updateProjectStats(projectId, stats) {
      // Find the project card and update the stats
      const projectCard = document.querySelector(
        `.project-card[data-project-id="${projectId}"]`
      );
      if (!projectCard) return;

      // Update each stat
      const statsContainer = projectCard.querySelector(".github-stats");
      if (statsContainer) {
        statsContainer.querySelector('[data-stat="stars"] span').textContent =
          stats.stars;
        statsContainer.querySelector('[data-stat="forks"] span').textContent =
          stats.forks;
        statsContainer.querySelector('[data-stat="issues"] span').textContent =
          stats.open_issues;
        statsContainer.querySelector('[data-stat="prs"] span').textContent =
          stats.open_prs;
      }
    },

    toggleTag(tag) {
      if (this.selectedTags.includes(tag)) {
        this.selectedTags = this.selectedTags.filter((t) => t !== tag);
      } else {
        this.selectedTags.push(tag);
      }
      this.filterProjects();
    },

    filterProjects() {
      // Filter projects based on selected tags
      this.filteredProjects = this.allProjects.filter((project) => {
        const hasAllSelectedTags =
          this.selectedTags.length === 0 ||
          this.selectedTags.every((tag) => project.tags.includes(tag));

        if (hasAllSelectedTags) {
          project.element.classList.remove("hidden");
        } else {
          project.element.classList.add("hidden");
        }

        return hasAllSelectedTags;
      });
    },

    isTagSelected(tag) {
      return this.selectedTags.includes(tag);
    },
  };
};
