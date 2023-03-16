document.addEventListener('DOMContentLoaded', function () {
  const timeRemainingElement = document.getElementById('timeRemaining');
  if (timeRemainingElement) {
    let estimatedTime = parseInt(timeRemainingElement.dataset.estimatedTime);

    function updateTimeRemaining() {
      estimatedTime -= 1;
      timeRemainingElement.textContent = `Estimated time remaining: ${estimatedTime} seconds`;

      if (estimatedTime <= 0) {
        clearInterval(interval);
        timeRemainingElement.textContent = 'The GLB file should be ready now.';
      }
    }

    const interval = setInterval(updateTimeRemaining, 1000);
  }
});
