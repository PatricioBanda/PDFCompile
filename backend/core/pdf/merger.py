import os
from PyPDF2 import PdfMerger
from backend.utils.path_utils import join_path, ensure_dir, list_files


class PDFMergerEngine:
    def __init__(self, rh_root: str):
        self.rh_root = rh_root

    def merge_month(self, month_key: str):
        """
        Merge PDFs ONLY from groups 2–13 and output to:
        RH/14/base_<month_key>.pdf
        """
        merger = PdfMerger()
        warnings = []

        # collect PDFs from groups 2–13
        for group in range(2, 14):
            group_dir = join_path(self.rh_root, str(group), month_key)

            if not os.path.isdir(group_dir):
                warnings.append(f"Group {group} missing folder {group_dir}")
                continue

            pdfs = list_files(group_dir, extension=".pdf")

            for pdf in pdfs:
                try:
                    merger.append(pdf)
                except Exception as e:
                    warnings.append(f"Error adding {pdf}: {e}")

        # Output folder = RH/14/<month_key>/
        out_dir = join_path(self.rh_root, "14", month_key)
        ensure_dir(out_dir)

        out_pdf = join_path(out_dir, f"base_{month_key}.pdf")

        merger.write(out_pdf)
        merger.close()

        return out_pdf, warnings
