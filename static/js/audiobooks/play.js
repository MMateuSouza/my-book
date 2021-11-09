(function () {
  var isPlaying = false;
  var skipBackButton = document.querySelector('#skip-back-button');
  var playPauseButton = document.querySelector('#play-pause-button');
  var skipForwardButton = document.querySelector('#skip-forward-button');
  var progressBar = document.querySelector('#progress-bar');
  var elapsedTime = document.querySelector('#elapsed-time');
  var totalTime = document.querySelector('#total-time');
  var chaptersTable = document.querySelector('#chapters-table');
  var audioBookId = document.querySelector('#audiobook-id').value || null;
  var audioElement = document.querySelector('#audio-element');
  var currentAudioBookChapter = null;

  audioElement.addEventListener('loadedmetadata', (e) => {
    // Início - Tratativa para problema de duração retornando `Infinity`
    if (audioElement.duration == Infinity) {
      audioElement.currentTime = 1e101;
      audioElement.ontimeupdate = function () {
        this.ontimeupdate = () => {
          return;
        }
        audioElement.currentTime = 0;
        return;
      }
    }
    // Fim - Tratativa para problema de duração retornando `Infinity`
    setAudioBookTotalTime();
  });

  audioElement.addEventListener('timeupdate', (e) => {
    updateProgressBar();
  });

  audioElement.addEventListener('canplay', (e) => {
    isPlaying && audioElement.play();
  });

  function setAudioBookChapterUrlById(chapterId) {
    let xhr = new XMLHttpRequest();
    xhr.overrideMimeType('application/json');

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        let response = JSON.parse(xhr.responseText);
        audioElement.src = response.recording_file;
        audioElement.load();
      }
    }

    xhr.open('GET', `/audiobooks/${audioBookId}/play/${chapterId}`, true);
    xhr.send();
  }

  function getAudioBookChapter() {
    let idInputElement = currentAudioBookChapter.querySelector('input.chapter-id');
    let chapterId = idInputElement.value;

    setAudioBookChapterUrlById(chapterId);
  }

  function init() {
    if (!currentAudioBookChapter) {
      currentAudioBookChapter = chaptersTable.querySelector('tr');
      currentAudioBookChapter.classList.add('table-active');

      getAudioBookChapter();
    }
  }

  function getAudioDuration(duration) {
    if (duration === Infinity) getAudioDuration(0);

    let date = new Date(null);
    date.setSeconds(duration);

    return date.toISOString().substr(11, 8);
  }

  function setAudioBookTotalTime() {
    totalTime.innerHTML = getAudioDuration(audioElement.duration);
  }

  function clearInterface() {
    // Limpa o tempo decorrido
    elapsedTime.innerHTML = getAudioDuration(0);
    // Limpa a barra de progresso
    progressBar.value = 0;
  }

  function updateProgressBar() {
    let currentTime = audioElement.currentTime;
    let progress = Math.floor((currentTime * 100) / audioElement.duration);

    progressBar.value = progress ? progress : 0;
    elapsedTime.innerHTML = getAudioDuration(currentTime);
  }

  function getNextPreviousAudioBookChapter(reverse=false) {
    let chaptersList = Array.from(chaptersTable.querySelectorAll('tr'));
    if (reverse) chaptersList = chaptersList.reverse();
    let currentIndex = chaptersList.indexOf(currentAudioBookChapter);
    let nextIndex = (currentIndex + 1) % chaptersList.length;

    currentAudioBookChapter = chaptersList[nextIndex];
    changeAudioBookChapter();
  }

  function getPreviousAudioBookChapter() {
    getNextPreviousAudioBookChapter(true);
  }

  function changePlayPauseButtonState() {
    let newActiveState = playPauseButton.querySelector('i.d-none');
    let currentActiveState = playPauseButton.querySelector('i:not(.d-none)');

    newActiveState.classList.remove('d-none');
    currentActiveState.classList.add('d-none');

    isPlaying = !isPlaying;
  }

  function playOrPauseAudioBookChapter() {
    isPlaying && audioElement.pause();
    !isPlaying && audioElement.play();

    changePlayPauseButtonState();
  }

  function getNextAudioBookChapter() {
    getNextPreviousAudioBookChapter();
  }

  skipBackButton.onclick = getPreviousAudioBookChapter;
  playPauseButton.onclick = playOrPauseAudioBookChapter;
  skipForwardButton.onclick = getNextAudioBookChapter;

  function changeAudioBookChapter() {
    if (currentAudioBookChapter.classList.contains('table-active')) return;

    chaptersTable.querySelectorAll('tr.table-active').forEach((el) => el.classList.remove('table-active'));
    currentAudioBookChapter.classList.add('table-active');

    clearInterface();
    getAudioBookChapter();
  }

  chaptersTable.ondblclick = function (e) {
    currentAudioBookChapter = e.target.parentNode;
    changeAudioBookChapter();
  }

  init();
})();