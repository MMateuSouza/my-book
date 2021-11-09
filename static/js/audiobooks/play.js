(function () {
  var isPlaying = false;
  var skipBackButton = document.querySelector('#skip-back-button');
  var playPauseButton = document.querySelector('#play-pause-button');
  var skipForwardButton = document.querySelector('#skip-forward-button');
  var progressBar = document.querySelector('#progress-bar');
  var elapsedTime = document.querySelector('#elapsed-time');
  var totalTime = document.querySelector('#total-time');
  var chaptersTable = document.querySelector('#chapters-table');
  var mediaUrl = document.querySelector('#media-url');
  var audioElement = document.querySelector('#audio-element');

  function getAudioDuration() {
    let date = new Date(null);
    date.setSeconds(audioElement.duration);

    return date.toISOString().substr(11, 8);
  }

  function previousAudioBookChapter() {
    console.log('previousAudioBookChapter');
  }

  function changePlayPauseButtonState() {
    let newActiveState = playPauseButton.querySelector('i.d-none');
    let currentActiveState = playPauseButton.querySelector('i:not(.d-none)');

    newActiveState.classList.remove('d-none');
    currentActiveState.classList.add('d-none');

    isPlaying = !isPlaying;
  }

  function playOrPauseAudioBookChapter() {
    changePlayPauseButtonState();

    isPlaying && audioElement.pause();
    !isPlaying && audioElement.play();
  }

  function nextAudioBookChapter() {
    console.log('nextAudioBookChapter');
  }

  skipBackButton.onclick = previousAudioBookChapter;
  playPauseButton.onclick = playOrPauseAudioBookChapter;
  skipForwardButton.onclick = nextAudioBookChapter;

  chaptersTable.ondblclick = function(e) {
    let trElement = e.target.parentNode;

    // Ignorar se houver duplo clique na mesma linha
    if (trElement.classList.contains('table-active')) return;

    chaptersTable.querySelectorAll('tr.table-active').forEach((el) => el.classList.remove('table-active'));
    trElement.classList.add('table-active');
  }
})();