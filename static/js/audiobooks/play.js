(function () {
  var isPlaying = false;
  var skipBackButton = document.querySelector('#skip-back-button');
  var playPauseButton = document.querySelector('#play-pause-button');
  var skipForwardButton = document.querySelector('#skip-forward-button');
  var progressBar = document.querySelector('#progress-bar');
  var elapsedTime = document.querySelector('#elapsed-time');
  var totalTime = document.querySelector('#total-time');
  var chaptersTable = document.querySelector('#chapters-table');

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

  chaptersTable.ondblclick = function(e) {
    let trElement = e.target.parentNode;

    // Ignorar se houver duplo clique na mesma linha
    if (trElement.classList.contains('table-active')) return;

    chaptersTable.querySelectorAll('tr.table-active').forEach((el) => el.classList.remove('table-active'));
    trElement.classList.add('table-active');
  }
})();