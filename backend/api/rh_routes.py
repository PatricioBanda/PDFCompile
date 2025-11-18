from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime
import os

from backend.utils.config_loader import get_settings
from backend.core.automation.rh_scanner import RHScanner
from backend.core.automation.state_manager import StateManager
from backend.core.pdf.merger import PDFMergerEngine

router = APIRouter()

class ScanRequest(BaseModel):
    year: str
    months: List[str]

class JoinRequest(BaseModel):
    year: str
    months: List[str]

def get_rh_root_for_year(year: str) -> str:
    settings = get_settings()
    base_root = settings.get("RH_BASE_ROOT")

    rh_root = os.path.join(base_root, year, "RH")
    rh_root = os.path.normpath(rh_root)
    if not os.path.exists(rh_root):
        raise HTTPException(status_code=400, detail=f"Pasta RH não encontrada: {rh_root}")
    return rh_root


@router.post("/scan")
def scan_months(request: ScanRequest) -> Dict[str, Any]:
    rh_root = get_rh_root_for_year(request.year)
    state_manager = StateManager(rh_root)
    scanner = RHScanner(rh_root, state_manager)

    results = {}

    for month_key in request.months:
        scan_info = scanner.scan_month(request.year, month_key)
        state_manager.update_scan_info(request.year, month_key, scan_info["groups"])
        results[month_key] = scan_info

    return {"year": request.year, "months": results}


@router.post("/join/base")
def join_base(request: JoinRequest):
    rh_root = get_rh_root_for_year(request.year)
    state_manager = StateManager(rh_root)
    merger = PDFMergerEngine(rh_root)

    output = {}

    for month_key in request.months:
        state = state_manager.load_state(request.year, month_key)

        if "groups" not in state:
            raise HTTPException(400, f"Mês {month_key} ainda não foi scaneado.")

        pdf_path, warnings = merger.merge_month(month_key, state["groups"])

        state["base_pdf"] = pdf_path
        state["base_pdf_created"] = datetime.datetime.now().isoformat()
        state["warnings"] = warnings

        state_manager.save_state(request.year, month_key, state)

        output[month_key] = {"pdf": pdf_path, "warnings": warnings}

    return output
