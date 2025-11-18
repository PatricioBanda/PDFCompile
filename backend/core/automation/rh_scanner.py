import os
from backend.utils.path_utils import join_path, list_files

class RHScanner:
    """
    Scans RH/<year>/<group>/<month_key>
    But ignores groups 1 and 14.
    """

    def __init__(self, rh_root: str, state_manager):
        self.rh_root = rh_root
        self.state_manager = state_manager

    def scan_month(self, year: str, month_key: str):
        month_results = {
            "month": month_key,
            "status": "ok",
            "groups": []
        }

        # Only groups 2–13
        allowed_groups = [str(i) for i in range(2, 14)]

        for group in allowed_groups:
            month_dir = join_path(self.rh_root, group, month_key)

            if not os.path.exists(month_dir):
                month_results["groups"].append({
                    "group": group,
                    "month": month_key,
                    "folder": month_dir,
                    "files": []
                })
                continue

            pdf_files = list_files(month_dir, ".pdf")

            month_results["groups"].append({
                "group": group,
                "month": month_key,
                "folder": month_dir,
                "files": pdf_files
            })

        return month_results
