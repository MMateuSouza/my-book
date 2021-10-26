(function () {
  document.querySelectorAll('input.form-control').forEach((el) => {
    el.addEventListener('input', (e) => {
      let target = e.target;
      let targetValue = target.value;
      let isInvalid = target.classList.contains('is-invalid');

      !targetValue && !isInvalid && target.classList.add('is-invalid');
      targetValue && isInvalid && target.classList.remove('is-invalid');
    })
  });
})();