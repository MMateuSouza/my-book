(function () {
  document.querySelector('#main').classList.add('active');

  let favoriteButtons = document.querySelectorAll('.fav-btn');
  let favoriteUrl = document.querySelector('#favorite-url').value || null;
  let userId = document.querySelector('#user-id').value || null;

  function addOrRemoveClass(el, classToAdd, classToRemove) {
    let starIcon = el.querySelector('i');

    if (starIcon.classList.contains(classToAdd)) return;

    starIcon.classList.remove(classToRemove);
    starIcon.classList.add(classToAdd);
  }

  function addOrRemoveFromFavorite(el) {
    let audioBookId = el.querySelector('input[type="number"]').value || null;

    let xhr = new XMLHttpRequest();
    xhr.overrideMimeType('application/json');

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        let response = JSON.parse(xhr.responseText);
        if (response.success) {
          !response.removed && addOrRemoveClass(el, 'bi-star-fill', 'bi-star');
          response.removed && addOrRemoveClass(el, 'bi-star', 'bi-star-fill');
        }
        alert(response.message);
      }
    }

    xhr.open('POST', favoriteUrl, true);
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.send(JSON.stringify({ userId, audioBookId }));
  }

  favoriteButtons.forEach((el) => {
    el.onclick = () => addOrRemoveFromFavorite(el);
  });
})();