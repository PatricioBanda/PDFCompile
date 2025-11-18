import os
from backend.utils.path_utils import join_path, ensure_dir, list_files


class RHScanner:
    def __init__(self, rh_root: str):
        self.rh_root = rh_root

    def scan_month(self, year: str, month_key: str):
        """
        Scan the RH folder year/month but ONLY for groups 2–13.
        Group 14 is reserved for the BASE PDF output.
        Group 1 is ignored.
        """
        results = []

        for group in sorted(os.listdir(self.rh_root), key=lambda x: int(x) if x.isdigit() else 999):
            if not group.isdigit():
                continue

            g = int(group)

            # ignore groups 1 and 14
            if g == 1 or g == 14:
                continue

            # only scan groups 2–13
            if g < 2 or g > 13:
                continue

            month_dir = join_path(self.rh_root, group, month_key)

            if not os.path.isdir(month_dir):
                results.append({
                    "group": group,
                    "month": month_key,
                    "folder": month_dir,
                    "files": [],
                })
                continue

            pdf_files = list_files(month_dir, extension=".pdf")

            results.append({
                "group": group,
                "month": month_key,
                "folder": month_dir,
                "files": pdf_files,
            })

        return {
            "month": month_key,
            "status": "ok",
            "groups": results
        }
