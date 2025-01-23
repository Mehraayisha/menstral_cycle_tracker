document.addEventListener('DOMContentLoaded', () => {
    const progressRing = document.getElementById('progressRing');
    const progressValue = document.getElementById('progressValue');
  
    // Get progress value from the rendered style
    const progress = parseFloat(getComputedStyle(progressRing).getPropertyValue('--progress'));
  
    // Update the visual progress incrementally
    let currentProgress = 0;
    const interval = setInterval(() => {
      if (currentProgress < progress) {
        currentProgress++;
        progressRing.style.setProperty('--progress', `${currentProgress}%`);
        progressValue.textContent = `${currentProgress}%`;
      } else {
        clearInterval(interval);
      }
    }, 20); // Adjust speed here
  });
  