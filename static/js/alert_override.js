document.addEventListener("DOMContentLoaded", function () {
  const alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
  const alertBody = document.getElementById('alertModalBody');

  window.alert = function (message) {
    alertBody.textContent = message;
    alertModal.show();
  };
});
