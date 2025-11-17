const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const selectFiles = document.getElementById("select-files");

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "#22c55e";
});

dropZone.addEventListener("dragleave", () => {
    dropZone.style.borderColor = "#38bdf8";
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "#38bdf8";

    const files = [...e.dataTransfer.files];
    handleDroppedFiles(files);
});

// allow clicking to add files
selectFiles.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", () => {
    handleDroppedFiles([...fileInput.files]);
});

function handleDroppedFiles(files) {
    console.log("Ficheiros recebidos:", files);
    api.handleFiles(files);
}
