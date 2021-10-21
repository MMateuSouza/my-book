(function () {
  /*
  *  Início - Autores
  */
  let authorsElement = document.querySelector('#authors_name_list');
  let addAuthorButton = document.querySelector('#add_author_name');
  let removeAuthorButton = document.querySelector('#remove_author_name');

  addAuthorButton.addEventListener('click', () => addNewAuthor());
  removeAuthorButton.addEventListener('click', () => removeAuthors());

  function addNewAuthor() {
    let authorNameInput = document.querySelector('#author_name');
    let authorName = authorNameInput.value;
    let inputContainsIsInvalidClass = authorNameInput.classList.contains('is-invalid');

    if(!authorName) {
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
    authorNameInput.value = '';
    authorNameInput.focus();
  }

  function removeAuthors() {
    if(confirm('Você deseja remover o(s) autore(s)?')) {
      authorsElement.querySelectorAll('option:checked').forEach((opt) => opt.remove());
    }
  }

  /*
  *  Início - Capítulos
  */

  let chaptersObject = document.querySelector('#chapters');
  let chaptersQuantity = chaptersObject.querySelectorAll('li');
  let addChappterButton = document.querySelector('#add-chapter');

  if (chaptersQuantity.length === 0) {
    addNewChapter();
  }

  addChappterButton.addEventListener('click', () => addNewChapter());

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

  function getButtonWithIcon(iconClass) {
    let icon = createElement('i', ['bi', iconClass]);
    let button = createElement('button', ['btn', 'btn-outline-secondary']);
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
    let inputTitleElement = getInputElement();
    let removeButtonElement = getRemoveButtonElement();
    let addButtonElement = getAddButtonElement();
    let orderedListElement = getOrderedListElement();

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