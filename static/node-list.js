'use strict';

if (focusId) {
    console.log(focusId);

    var element = document.getElementById(focusId);
    if (element) {
        console.log(element);

        element.focus();
    }
}
