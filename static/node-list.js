'use strict';

var focusIdElement = document.getElementById('focusId');
var focusId = focusIdElement && focusIdElement.value;

if (focusId) {
    var noteElement = document.getElementById(focusId);
    if (noteElement) {
        noteElement.focus();
    }
}
