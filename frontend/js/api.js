const api = {
    handleFiles: (files) => {
        console.log("[API] ficheiros recebidos:", files);

        // Aqui integramos com FastAPI no futuro
        // e.g. enviar via FormData

        // Para já, atualizar UI:
        ui.showFiles(files);
    },

    scanFolder: (path) => {
        console.log("[API] scan folder:", path);
    }
};
