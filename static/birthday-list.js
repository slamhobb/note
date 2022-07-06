'use strict';

var addButtonElement = document.getElementById('addButtonId');
var saveFormElement = document.getElementById('saveFormId');
addButtonElement.addEventListener('click', function() {
    addButtonElement.classList.toggle('d-none');
    saveFormElement.classList.toggle('d-none');
});
