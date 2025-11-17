import os
from PyPDF2 import PdfMerger
from backend.core.pdf.image_converter import convert_image_to_pdf

class PDFMergerEngine:
    
    def __init__(self):
        pass

    def collect_files(self, group_path):
        """
        Obtém lista de ficheiros válidos para merge (pdf + imagens).
        Ordena alfabeticamente.
        """
        if not os.path.exists(group_path):
            return []

        files = [
            os.path.join(group_path, f)
            for f in os.listdir(group_path)
            if os.path.isfile(os.path.join(group_path, f)) 
               and not f.startswith("~")
        ]
        
        # ordenar alfabeticamente
        files.sort(key=lambda x: os.path.basename(x).lower())
        return files

    def prepare_file(self, filepath):
        """
        Se for imagem → converter para PDF temporário.
        Se for PDF → usar diretamente.
        """
        ext = filepath.lower().split(".")[-1]

        if ext in ["jpg", "jpeg", "png", "bmp", "gif", "tiff"]:
            return convert_image_to_pdf(filepath)
        return filepath

    def merge_month(self, month_key, rh_root, output_folder):
        """
        Junta ficheiros dos grupos 2..13 para um mês.
        Retorna: caminho final + lista de grupos vazios.
        """

        groups = [str(i) for i in range(2, 14)]
        group_warnings = []

        merger = PdfMerger()

        for g in groups:
            group_path = os.path.join(rh_root, g, month_key)

            files = self.collect_files(group_path)

            if not files:
                group_warnings.append(f"Grupo {g} vazio")
                continue

            for f in files:
                prepared = self.prepare_file(f)
                merger.append(prepared)

        # Criar pasta de saída
        os.makedirs(output_folder, exist_ok=True)

        output_pdf = os.path.join(output_folder, f"{month_key}_BASE_JOIN.pdf")

        merger.write(output_pdf)
        merger.close()

        return output_pdf, group_warnings
