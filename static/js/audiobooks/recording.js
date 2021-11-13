(function () {
  let formElement = document.querySelector('#audiobook_form');
  let submitFormButton = document.querySelector('#submit_form');
  let fileInputElements = document.querySelectorAll('input[type="file"]');

  submitFormButton.onclick = (e) => validateFormBeforeSubmit(e);

  fileInputElements.forEach(function(el) {
    el.oninput = function() {
      let targetValue = el.value;
      let isInvalid = el.classList.contains('is-invalid');

      !targetValue && !isInvalid && el.classList.add('is-invalid');
      targetValue && isInvalid && el.classList.remove('is-invalid');
    }
  });

  function validateFormBeforeSubmit(e) {
    e.preventDefault();
    let isValid = true;

    fileInputElements.forEach(function(el) {
      let audioRegex = new RegExp('^audio\/[^]*$');
      if (!el.value || !audioRegex.test(el.files[0].type)) {
        isValid = false;
        el.classList.add('is-invalid');
      }
    });

    isValid && formElement.submit();
  }
})();