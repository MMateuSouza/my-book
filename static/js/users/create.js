(function() {
  let isNewUser = document.querySelector('#is-new-user').checked
  let queryElementCondition = isNewUser ? 'input.form-control' : 'input.form-control:not([type=password])' ;

  document.querySelectorAll(queryElementCondition).forEach((el) => {
    el.addEventListener('input', (e) => {
      let target = e.target;
      let targetValue = target.value;
      let isInvalid = target.classList.contains('is-invalid');

      !targetValue && !isInvalid && target.classList.add('is-invalid');
      targetValue && isInvalid && target.classList.remove('is-invalid');
    })
  });
})();