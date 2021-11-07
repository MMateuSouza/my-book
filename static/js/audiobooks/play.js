(function () {
  var isPlaying = false;
  var skipBackButton = document.querySelector('#skip-back-button');
  var playPauseButton = document.querySelector('#play-pause-button');
  var skipForwardButton = document.querySelector('#skip-forward-button');

  function changePlayPauseButtonState() {
    let newActiveState = playPauseButton.querySelector('i.d-none');
    let currentActiveState = playPauseButton.querySelector('i:not(.d-none)');

    newActiveState.classList.remove('d-none');
    currentActiveState.classList.add('d-none');

    isPlaying = !isPlaying;
  }

  playPauseButton.onclick = function() {
    changePlayPauseButtonState();
  }
})();