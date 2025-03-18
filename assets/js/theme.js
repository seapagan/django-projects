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
  if (
    theme === "dark" ||
    (theme === "system" &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
  localStorage.theme = theme;
};

// Initialize theme
document.addEventListener("DOMContentLoaded", () => {
  const theme = getTheme();
  updateTheme(theme);
});

// Listen for system theme changes when in system mode
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", (e) => {
    if (localStorage.theme === "system") {
      updateTheme("system");
    }
  });
