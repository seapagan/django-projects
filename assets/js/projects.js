// Make the function globally available for Alpine.js
window.initializeProjects = function () {
  return {
    allProjects: [],
    filteredProjects: [],
    selectedTags: [],
    allTags: [],

    init() {
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
