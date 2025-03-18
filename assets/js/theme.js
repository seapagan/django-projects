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
  const recaptchaIframes = document.querySelectorAll(
    'iframe[src*="recaptcha"]'
  );

  if (recaptchaIframes.length > 0) {
    const captchaTheme = isDarkMode ? "dark" : "light";

    recaptchaIframes.forEach((iframe) => {
      let src = iframe.src;

      if (src.includes("&theme=")) {
        src = src.replace(/&theme=(light|dark)/, `&theme=${captchaTheme}`);
      } else {
        src = src + `&theme=${captchaTheme}`;
      }

      iframe.src = src;
    });
  }
};

// Initialize theme
document.addEventListener("DOMContentLoaded", () => {
  const theme = getTheme();
  updateTheme(theme);

  // Initial setup might need a delay as reCAPTCHA loads asynchronously
  setTimeout(() => {
    updateTheme(theme); // Re-apply theme after reCAPTCHA has likely loaded
  }, 1000);
});

// Listen for system theme changes when in system mode
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", (e) => {
    if (localStorage.theme === "system") {
      updateTheme("system");
    }
  });
