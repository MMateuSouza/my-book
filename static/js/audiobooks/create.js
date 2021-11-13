(function () {
  /*
  *  Início - Autores
  */
  let isNewBook = document.querySelector('#is-new-book').checked
  let authorsElement = document.querySelector('#authors_name_list');
  let authorNameInput = document.querySelector('#author_name');
  let authorsNameInput = document.querySelector('#authors_names');
  let hasAuthors = !!authorsNameInput.value;
  let chaptersInput = document.querySelector('#chapters_str');
  let hasChapters = !!chaptersInput.value && chaptersInput.value !== '[]';
  let addAuthorButton = document.querySelector('#add_author_name');
  let removeAuthorButton = document.querySelector('#remove_author_name');
  let formElement = document.querySelector('#audiobook_form');
  let submitFormButton = document.querySelector('#submit_form');

  addAuthorButton.onclick = addAuthor;
  removeAuthorButton.onclick = removeAuthors;
  submitFormButton.onclick = (e) => validateFormBeforeSubmit(e);
  authorNameInput.onkeypress = function (e) {
    if (!e) e = window.event;
    let keyCode = e.code || e.key;

    keyCode == 'Enter' && addAuthor();
  };

  if (hasAuthors) {
    let authorsNamesList = authorsNameInput.value.split(';');
    authorsNamesList.forEach((name) => addNewAuthor(name));
  }

  function addAuthor() {
    let authorName = authorNameInput.value;
    addNewAuthor(authorName);
  }

  function addNewAuthor(name) {
    let authorName = name ? name : '';
    let inputContainsIsInvalidClass = authorNameInput.classList.contains('is-invalid');

    if (!authorName) {
      // Se já houver a classe, não adicioná-la
      !inputContainsIsInvalidClass && authorNameInput.classList.add('is-invalid');
      return;
    }

    // Se houver a classe, removê-la
    inputContainsIsInvalidClass && authorNameInput.classList.remove('is-invalid');

    let optionElement = createElement('option', []);
    optionElement.textContent = authorName;
    optionElement.value = authorName;

    authorsElement.append(optionElement);
    fillAuthorsNames();
    authorNameInput.value = '';
    authorNameInput.focus();
  }

  function removeAuthors() {
    if (confirm('Você deseja remover o(s) autore(s)?')) {
      authorsElement.querySelectorAll('option:checked').forEach((opt) => opt.remove());
      fillAuthorsNames();
    }
  }

  function fillAuthorsNames() {
    let authorsNames = [];

    authorsElement.querySelectorAll('option').forEach((el) => {
      authorsNames.push(el.value.trim().toLowerCase());
    });

    authorsNameInput.value = authorsNames.join(';');
  }

  function validateFormBeforeSubmit(e) {
    e.preventDefault();
    let isValid = true;

    !isNewBook && fillAuthorsNames();
    if (!authorsNameInput.value) {
      isValid = false;
      authorNameInput.classList.add('is-invalid');
    }

    // Se capítulos todos preenchidos
    getConvertedChapter();

    isValid && formElement.submit();
  }

  /*
  *  Início - Capítulos
  */

  let chaptersObject = document.querySelector('#chapters');
  let addChappterButton = document.querySelector('#add-chapter');

  if (!hasChapters) {
    addNewChapter();
  } else {
    loadChapters();
  }

  addChappterButton.onclick = addNewChapter;

  function createElement(tag, classList) {
    if (typeof tag !== 'string' || typeof classList !== 'object') {
      return;
    }

    let element = document.createElement(tag);
    classList.forEach((cls) => element.classList.add(cls));

    return element;
  }

  function getListItemElement() {
    return createElement('li', ['list-group-item', 'border-0', 'py-0', 'pe-0']);
  }

  function getDivElement() {
    return createElement('div', ['input-group', 'input-group-sm']);
  }

  function getInputElement() {
    return createElement('input', ['form-control', 'text-capitalize']);
  }

  function getChapterIdInputElement() {
    let inputElement = getInputElement();
    inputElement.type = 'number';
    inputElement.name = 'chapter-id';
    inputElement.classList.add('d-none');

    return inputElement;
  }

  function getButtonWithIcon(iconClass) {
    let icon = createElement('i', ['bi', iconClass]);
    let button = createElement('button', ['btn', 'btn-outline-secondary']);
    button.type = 'button';
    button.append(icon);

    return button;
  }

  function createButtonWithFunction(iconClass, func) {
    if (typeof iconClass !== 'string' || typeof func !== 'function') {
      return;
    }

    let button = getButtonWithIcon(iconClass);
    button.onclick = func;

    return button;
  }

  function getRemoveButtonElement() {
    return createButtonWithFunction('bi-trash', removeChapter);
  }

  function getAddButtonElement() {
    return createButtonWithFunction('bi-plus', addNewSubchapter);
  }

  function getOrderedListElement() {
    return createElement('ol', ['list-group', 'list-group-numbered']);
  }

  function createListItemElement() {
    let listItemElement = getListItemElement();
    let divElement = getDivElement();
    let inputChapterIdElement = getChapterIdInputElement();
    let inputTitleElement = getInputElement();
    let removeButtonElement = getRemoveButtonElement();
    let addButtonElement = getAddButtonElement();
    let orderedListElement = getOrderedListElement();

    divElement.append(inputChapterIdElement);
    divElement.append(inputTitleElement);
    divElement.append(removeButtonElement);
    divElement.append(addButtonElement);
    listItemElement.append(divElement);
    listItemElement.append(orderedListElement);

    return listItemElement;
  }

  function addNewChapter() {
    let listItemElement = createListItemElement();
    chaptersObject.append(listItemElement);
  }

  function convertChaptersToHTML(chapters) {
    let listItemElements = [];

    chapters.forEach(function (chapter) {
      let subchaptersListItemElements;

      if (chapter.subchapters) {
        subchaptersListItemElements = convertChaptersToHTML(chapter.subchapters);
      }

      let listItemElement = createListItemElement();
      listItemElement.querySelector('input[type="number"]').value = chapter.id;
      listItemElement.querySelector('input:not([type="number"])').value = chapter.title;
      listItemElements.push(listItemElement);

      if (subchaptersListItemElements) {
        let subchaptersElement = listItemElement.querySelector('ol');
        subchaptersListItemElements.forEach((el) => subchaptersElement.append(el));
      }
    });

    return listItemElements;
  }

  function loadChapters() {
    let chaptersString = chaptersInput.value;
    chaptersString = chaptersString.replace(/'/g, '"');
    let chapters = JSON.parse(chaptersString);

    if (!chapters) {
      addNewChapter();
      return;
    }

    let chaptersElements = convertChaptersToHTML(chapters);
    chaptersElements.forEach((el) => chaptersObject.append(el));
  }

  function convertChapter(element) {
    let sequence = 0;
    let chapters = [];
    let orderedListElement = element;

    let listItem = orderedListElement.querySelector('li:first-child');

    while (listItem) {
      sequence ++;
      let insideOrderedListElement = listItem.querySelector('ol');
      let subchapters = convertChapter(insideOrderedListElement);

      let chapterIdInputElement = listItem.querySelector('input[type="number"]');
      let chapterInputElement = listItem.querySelector('input:not([type="number"])');
      let chapterTitle = chapterInputElement.value;
      let chapter = {};
      chapter.id = chapterIdInputElement.value;
      chapter.title = chapterTitle;
      chapter.sequence = sequence;
      chapter.subchapters = subchapters;
      chapters.push(chapter);

      listItem.remove();
      listItem = orderedListElement.querySelector('li:first-child');
    }

    return chapters;
  }

  function getConvertedChapter() {
    let orderListObject = document.querySelector('#chapters');
    let chapters = convertChapter(orderListObject.cloneNode(true));

    chaptersInput.value = JSON.stringify(chapters);
  }

  function getParentNode(event) {
    let parentNode;

    switch (event.target.tagName) {
      case 'I':
        parentNode = event.target.parentNode.parentNode.parentNode;
        break;
      case 'BUTTON':
        parentNode = event.target.parentNode.parentNode;
        break;
    }

    return parentNode;
  }

  function addNewSubchapter(e) {
    e.preventDefault();
    let parentNode = getParentNode(e);

    if (parentNode) {
      let orderedListElement = parentNode.querySelector('ol');
      let listItemElement = createListItemElement();

      orderedListElement.append(listItemElement);
    }
  }

  function removeChapter(e) {
    e.preventDefault();
    let parentNode = getParentNode(e);

    if (parentNode && confirm('Você deseja remover o capítulo? Lembre-se que os subcapítulos serão removidos.')) {
      parentNode.remove();
    }
  }
})();