var el = x => document.getElementById(x);

// For Image
var dataImage = localStorage.getItem('imgData');
saved_image = el('saved_image');
saved_image.src = "data:image/jpeg;base64," + dataImage;

import constants from './const.js';

console.log(constants.ANOTHER_VARIABLE);
console.log(constants.LISTING_TYPE_BRAND);
console.log(constants.DAYS);
console.log(constants.MAP_CONTENT_TYPE_TO_EXTENSION);
