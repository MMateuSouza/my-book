(function () {
  document.querySelector('#main').classList.add('active');

  let favoriteButtons = document.querySelectorAll('.fav-btn');

  function addOrRemoveClass(el, classToAdd, classToRemove) {
    let starIcon = el.querySelector('i');

    if (starIcon.classList.contains(classToAdd)) return;

    starIcon.classList.remove(classToRemove);
    starIcon.classList.add(classToAdd);
  }

  function addOrRemoveFromFavorite(el) {
    let audioBookId = el.querySelector('input[type="number"]').value || null;

    // let xhr = new XMLHttpRequest();
    // xhr.overrideMimeType('application/json');

    // xhr.onreadystatechange = function () {
    //   if (this.readyState == 4 && this.status == 200) {
    //     let response = JSON.parse(xhr.responseText);
    //     console.log(response);
    //   }
    // }

    // xhr.open('GET', `/audiobooks/${audioBookId}/favorite/`, true);
    // xhr.send();
  }

  favoriteButtons.forEach((el) => {
    el.onmouseover = () => addOrRemoveClass(el, 'bi-star-fill', 'bi-star');
    el.onmouseleave = () => addOrRemoveClass(el, 'bi-star', 'bi-star-fill');
    el.onclick = () => addOrRemoveFromFavorite(el);
  });
})();