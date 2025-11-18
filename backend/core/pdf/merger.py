import os
from PyPDF2 import PdfMerger
from backend.utils.path_utils import ensure_dir, join_path

class PDFMergerEngine:
    def __init__(self, rh_root: str):
        self.rh_root = rh_root
        self.output_dir = join_path(rh_root, "14")
        ensure_dir(self.output_dir)

    def merge_month(self, month_key: str, groups: list):
        """
        Receives groups = scanner_result["groups"]
        Produces base_<month>.pdf inside RH/<year>/14/
        """
        pdfs = []
        warnings = []

        for g in groups:
            for file in sorted(g["files"]):
                pdfs.append(file)

            if len(g["files"]) == 0:
                warnings.append(f"Grupo {g['group']} vazio.")

        output_path = join_path(self.output_dir, f"base_{month_key}.pdf")

        if pdfs:
            merger = PdfMerger()
            for p in pdfs:
                try:
                    merger.append(p)
                except Exception as e:
                    warnings.append(f"Erro em {p}: {str(e)}")

            merger.write(output_path)
            merger.close()
        else:
            warnings.append("Nenhum PDF encontrado no mês.")

        return output_path, warnings
