var el = x => document.getElementById(x);
document.getElementById('button').style.visibility = 'hidden';
var upload_img = document.getElementById('fileInput').addEventListener('change', fileChange, false);

function fileChange(e) {

    document.getElementById('button').style.visibility = 'visible';

    var file = e.target.files[0];

    if (file.type == "image/jpeg" || file.type == "image/png" || file.type == "image/jpg") {

        var reader = new FileReader();
        reader.onload = function(readerEvent) {

            var image = new Image();
            image.onload = function(imageEvent) {
                var max_size = 1080;
                var w = image.width;
                var h = image.height;
                 console.log("width:",w, "height:", h);
                if (w > h) {
                    if (w > max_size) {
                        h*=max_size/w; w=max_size;
                    }
                } else {
                    if (h > max_size) {
                        w*=max_size/h; h=max_size;
                    }
                }
                 console.log("Updated width:",w, "Updated height:", h);

                var canvas = document.createElement('canvas');

                //  NO FORCEFUL Just Use Default Image
                canvas.width = w;
                canvas.height = h;
                canvas.getContext('2d').drawImage(image, 0, 0, w, h);

                if (file.type == "image/jpeg") {
                var dataURL = canvas.toDataURL("image/jpeg", 0.80);
                if (adjustImageFileSize(dataURL) > 1) {
                    dataURL = canvas.toDataURL("image/jpeg", 0.50);
                }

                }
                else {
                    var dataURL = canvas.toDataURL("image/png", 0.80);
                    if (adjustImageFileSize(dataURL) > 1) {
                        dataURL = canvas.toDataURL("image/png", 0.50);
                    }
                }



                el('fileDisplayArea').src = dataURL;
                el('fileDisplayArea').className = '';
                // before sending to server, split dataURL to send only data bytes
                data_bytes = dataURL.split(',');
                document.getElementById('uploaded_file').value = data_bytes[1];
                console.log("put data to uploaded file");

                // save local data_bytes[1]
                localStorage.setItem("data64", data_bytes[1]);
                var dataImage = localStorage.getItem('imgData');
                // console.log("data_bytes[1]:", data_bytes[1]);
            }

            image.src = readerEvent.target.result;
        }

        reader.readAsDataURL(file);

    } else {
        document.getElementById('fileInput').value = '';
        alert('Please select image only in JPG or PNG format!');	
    }
}

function adjustImageFileSize(imageDataURL) {
    
    // var base64String = imageDataURL.split(",")[1];
    // console.log("base64", base64String.length);
  
    // //console.log("non blob", stringToBytesFaster(base64String).length);
    // var nonBlob = stringToBytesFaster(base64String).length;
    // console.log("non blob", nonBlob/1000000, "MB", "-----", nonBlob/1000, "KB");
  
    var file = dataURLtoBlob(imageDataURL);
    var size = file.size;
  
    var sizeKB = size/1000;
    var sizeMB = size/1000000;
    console.log("size", sizeMB, "MB", "-----", sizeKB, "KB");

    return sizeMB;
}

function dataURLtoBlob(dataURL) {
    // Decode the dataURL
    var imageType = dataURL.split(',')[0];     
    var binary = atob(dataURL.split(',')[1]);
    // Create 8-bit unsigned array
    var array = [];
    for(var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    // Return our Blob object
    // console.log("imageType", imageType);

    if (imageType.indexOf("jpeg") >=0) {
        return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
    }
    else {
        return new Blob([new Uint8Array(array)], {type: 'image/png'});
    }
  }


