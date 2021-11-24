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
  var chapterTitleSpanElement = document.querySelector('#chapter-title');
  var currentChapterPageSpanElement = document.querySelector('#current-chapter-page');

  audioElement.addEventListener('loadedmetadata', () => {
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

  audioElement.addEventListener('timeupdate', () => {
    updateProgressBar();
    updateCurrentChapterPage();
  });

  audioElement.addEventListener('canplay', () => {
    isPlaying && audioElement.play();
  });

  audioElement.addEventListener('ended', () => {
    getNextAudioBookChapter();
  });

  function setAudioBookChapterUrl(recordingFile) {
    audioElement.src = recordingFile;
    audioElement.load();
  }

  function getAudioBookChapter() {
    let chapterTitle = currentAudioBookChapter.querySelector('td.chapter-title').innerHTML;
    chapterTitleSpanElement.innerHTML = chapterTitle;

    let recordingFileInputElement = currentAudioBookChapter.querySelector('input.recording-file');
    let recordingFile = recordingFileInputElement.value;

    setAudioBookChapterUrl(recordingFile);
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

  function updateCurrentChapterPage() {
    let totalPagesInputElement = currentAudioBookChapter.querySelector('input.total-pages');
    let totalPages = parseInt(totalPagesInputElement.value) || 0;
    let chapterStartPageInputElement = currentAudioBookChapter.querySelector('input.start-page');
    let chapterStartPage = parseInt(chapterStartPageInputElement.value) || 0;
    let secondsPerPage;
    let currentChapterPage;

    if (!totalPages || !chapterStartPage || !audioElement.duration) return;

    secondsPerPage = audioElement.duration / totalPages;
    currentChapterPage = Math.floor(audioElement.currentTime / secondsPerPage);
    if (currentChapterPage <= totalPages) {
      currentChapterPageSpanElement.innerHTML = chapterStartPage + currentChapterPage;
    }
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