/**
 * Handle tag filtering with HTMX
 */

// Update hidden form fields for selected tags
function updateSelectedTags() {
  const selectedTags = Array.from(
    document.querySelectorAll(".tag-filter.selected")
  ).map((btn) => btn.textContent.trim());

  // Clear existing form fields
  const formFieldsContainer = document.getElementById("tag-form-fields");
  formFieldsContainer.innerHTML = "";

  // Create hidden input fields for each selected tag
  selectedTags.forEach((tag) => {
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = "tags";
    input.value = tag;
    formFieldsContainer.appendChild(input);
  });

  // Update clear filters button state
  updateClearFiltersButton(selectedTags.length > 0);
}

// Update clear filters button state
function updateClearFiltersButton(hasSelectedTags) {
  const clearFiltersBtn = document.getElementById("clear-filters");
  if (clearFiltersBtn) {
    if (hasSelectedTags) {
      clearFiltersBtn.classList.remove("opacity-30", "cursor-not-allowed");
      clearFiltersBtn.classList.add("hover:underline", "cursor-pointer");
      clearFiltersBtn.disabled = false;
    } else {
      clearFiltersBtn.classList.add("opacity-30", "cursor-not-allowed");
      clearFiltersBtn.classList.remove("hover:underline", "cursor-pointer");
      clearFiltersBtn.disabled = true;
    }
  }
}

// Initialize event listeners
document.addEventListener("DOMContentLoaded", function () {
  // Handle clear filters button
  const clearFiltersBtn = document.getElementById("clear-filters");
  if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener("click", function () {
      // Remove selected class from all tag filters
      document.querySelectorAll(".tag-filter.selected").forEach((btn) => {
        btn.classList.remove("selected");
      });

      // Clear hidden form fields
      const formFieldsContainer = document.getElementById("tag-form-fields");
      formFieldsContainer.innerHTML = "";

      // Update clear filters button state
      updateClearFiltersButton(false);
    });
  }
});
