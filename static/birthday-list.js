'use strict';

var addButton = document.getElementById('addButtonId');
var saveForm = document.getElementById('saveFormId');
addButton.addEventListener('click', function() {
    addButton.classList.toggle('d-none');
    saveForm.classList.toggle('d-none');
});
