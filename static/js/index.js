document.addEventListener('DOMContentLoaded', () => {
  const progressRing = document.getElementById('progressRing');
  const progressValue = document.getElementById('progressValue');

  // Get progress value from the style
  const progress = parseFloat(getComputedStyle(progressRing).getPropertyValue('--progress'));

  // Ensure progress value is between 0 and 100
  if (isNaN(progress) || progress < 0 || progress > 100) {
      console.error('Invalid progress value');
      return;
  }

  // Update the visual progress incrementally
  let currentProgress = 0;
  const interval = setInterval(() => {
    if (currentProgress < progress) {
      currentProgress++;
      // Update the custom CSS property '--progress' to set the ring's progress
      progressRing.style.setProperty('--progress', `${currentProgress}%`);
      // Update the displayed progress value text
      progressValue.textContent = `${currentProgress}%`;
    } else {
      clearInterval(interval);
    }
  }, 20); // Adjust speed of progress animation here
});
