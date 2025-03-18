// Function to update captcha theme based on site theme
function updateCaptchaTheme(theme) {
  // Get all reCAPTCHA iframes
  const recaptchaIframes = document.querySelectorAll(
    'iframe[src*="recaptcha"]'
  );

  // Determine the appropriate theme value
  let captchaTheme = "light";
  if (
    theme === "dark" ||
    (theme === "system" &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    captchaTheme = "dark";
  }

  // Update the iframe src
  recaptchaIframes.forEach((iframe) => {
    let src = iframe.src;

    // If src already contains a theme parameter, replace it
    if (src.includes("&theme=")) {
      src = src.replace(/&theme=(light|dark)/, `&theme=${captchaTheme}`);
    } else {
      // Otherwise, add the theme parameter
      src = src + `&theme=${captchaTheme}`;
    }

    iframe.src = src;
  });
}

// Initialize captcha theme when the page loads
document.addEventListener("DOMContentLoaded", () => {
  // Set initial theme based on current site theme
  const currentTheme = getTheme();

  // Initial setup might need a delay as reCAPTCHA loads asynchronously
  setTimeout(() => {
    updateCaptchaTheme(currentTheme);
  }, 1000);

  // Listen for theme changes
  document.addEventListener("themeChanged", (e) => {
    updateCaptchaTheme(e.detail.theme);
  });
});
