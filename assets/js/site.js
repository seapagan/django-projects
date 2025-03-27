/**
 * Combined JavaScript for the site
 * Includes theme switching and tag filtering functionality
 */

// ===== Theme Switching =====

// Check if theme is stored in localStorage, otherwise use system preference
const getTheme = () => {
  if (
    localStorage.theme === "dark" ||
    (!("theme" in localStorage) &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    return "dark";
  } else if (localStorage.theme === "light") {
    return "light";
  }
  return "system";
};

// Function to update the theme
const updateTheme = (theme) => {
  // Determine if we should use dark mode
  const isDarkMode =
    theme === "dark" ||
    (theme === "system" &&
      window.matchMedia("(prefers-color-scheme: dark)").matches);

  // Update document theme
  if (isDarkMode) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }

  // Save theme preference
  localStorage.theme = theme;

  // Update reCAPTCHA theme
  const hCaptchaIframes = document.querySelectorAll('iframe[src*="hcaptcha"]');

  if (hCaptchaIframes.length > 0) {
    const captchaTheme = isDarkMode ? "dark" : "light";
    hCaptchaIframes.forEach((iframe) => {
      let src = iframe.src;

      if (src.includes("&theme=")) {
        src = src.replace(/&theme=(light|dark)/, `&theme=${captchaTheme}`);
      } else {
        src = src + `&theme=${captchaTheme}`;
      }

      // Completely remove and re-add the iframe. This seems to be the only way
      // we can get it to update theme without reloading the whole page
      const newIframe = iframe.cloneNode(true);
      newIframe.src = src;

      iframe.parentNode.replaceChild(newIframe, iframe);
    });
  }
};

// ===== Tag Filtering =====

// Toggle a tag in the filter UI by name
const toggleTagInFilter = (tagName) => {
  // Find the matching filter button
  const filterBtn = Array.from(document.querySelectorAll(".tag-filter")).find(
    (btn) => btn.textContent.trim() === tagName
  );

  if (filterBtn) {
    // Toggle the selected class
    filterBtn.classList.toggle("selected");
    // Update hidden form fields
    updateSelectedTags();
  }
};

// Update hidden form fields for selected tags
const updateSelectedTags = () => {
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
};

// Update clear filters button state
const updateClearFiltersButton = (hasSelectedTags) => {
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
};

// ===== Initialization =====

// Initialize everything when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  // Initialize theme
  const theme = getTheme();
  updateTheme(theme);

  // Initial setup might need a delay as reCAPTCHA loads asynchronously
  setTimeout(() => {
    updateTheme(theme); // Re-apply theme after reCAPTCHA has likely loaded
  }, 1000);

  // Handle clear filters button
  const clearFiltersBtn = document.getElementById("clear-filters");
  if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener("click", () => {
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

// Listen for system theme changes when in system mode
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", (e) => {
    if (localStorage.theme === "system") {
      updateTheme("system");
    }
  });
