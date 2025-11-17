const previewCanvas = document.getElementById("pdf-preview");
const ctx = previewCanvas.getContext("2d");

// Placeholder temporário
function showPlaceholder() {
    ctx.fillStyle = "#1e293b";
    ctx.fillRect(0, 0, previewCanvas.width, previewCanvas.height);

    ctx.fillStyle = "#38bdf8";
    ctx.font = "24px Segoe UI";
    ctx.fillText("Nenhum PDF carregado", 20, 50);
}

showPlaceholder();

