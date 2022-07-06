'use strict';

var focusIdElement = document.getElementById('focusId');
var focusId = focusIdElement && focusIdElement.value;

if (focusId) {
    var noteElement = document.getElementById(focusId);
    if (noteElement) {
        noteElement.focus();
    }
}

var addButtonElement = document.getElementById('addButtonId');
var saveFormElement = document.getElementById('saveFormId');
addButtonElement.addEventListener('click', function() {
    addButtonElement.classList.toggle('d-none');
    saveFormElement.classList.toggle('d-none');
});
