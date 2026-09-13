// =============================
// Image Preview
// =============================

function previewImage(event){

    const file = event.target.files[0];

    if(file){

        document.getElementById("file-name").innerHTML=file.name;

        const preview=document.getElementById("preview");

        preview.src=URL.createObjectURL(file);

        preview.style.display="block";

    }

}

// =============================
// Character Counter
// =============================

function countCharacters(){

    const box=document.getElementById("message");

    if(box){

        document.getElementById("charCount").innerHTML=box.value.length;

    }

}

// =============================
// Password Toggle
// =============================

function togglePassword(){

    const pass=document.getElementById("password");

    if(pass.type==="password")

        pass.type="text";

    else

        pass.type="password";

}

// =============================
// Drag & Drop Upload
// =============================

const dropArea=document.getElementById("drop-area");

if(dropArea){

    dropArea.addEventListener("dragover",function(e){

        e.preventDefault();

        dropArea.classList.add("dragover");

    });

    dropArea.addEventListener("dragleave",function(){

        dropArea.classList.remove("dragover");

    });

    dropArea.addEventListener("drop",function(e){

        e.preventDefault();

        dropArea.classList.remove("dragover");

        const files=e.dataTransfer.files;

        if(files.length){

            document.getElementById("image").files=files;

            previewImage({target:{files:files}});

        }

    });

}