window.onload = function() {
    var fileInput = document.querySelector('input[type=file]');
    var fileNameSpan = document.querySelector('#filename');
  
    fileInput.addEventListener('change', function() {
      fileNameSpan.textContent = fileInput.files[0].name;
    });
  };
  