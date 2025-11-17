from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os

from backend.core.automation.rh_scanner import RHScanner
from backend.core.automation.state_manager import StateManager

router = APIRouter()

# ⚠️ Ajusta este caminho base para a tua estrutura
BASE_RH_ROOT = r"C:\Users\Patricio Vargas\INCENTAHEAD CONSULTING, UNIPESSOAL LDA\INCENTAHEAD - Documentos (1)\4.Projetos\4.3.Execução\0. Afetação Pessoal Empresas\Agix\0. Pasta Partilhada"

class ScanRequest(BaseModel):
    year: str           # "2025"
    months: List[str]   # ["07_2025", "08_2025"]

class ScanResult(BaseModel):
    year: str
    months: Dict[str, Any]


def get_rh_root_for_year(year: str) -> str:
    """
    Constrói o caminho para a pasta RH de um dado ano.
    Ex: BASE/2025/RH
    """
    rh_root = os.path.join(BASE_RH_ROOT, year, "RH")
    if not os.path.exists(rh_root):
        raise HTTPException(status_code=400, detail=f"Pasta RH não encontrada para o ano {year}: {rh_root}")
    return rh_root


@router.post("/scan", response_model=ScanResult)
def scan_months(request: ScanRequest):
    """
    Faz o scan dos grupos 2..13 para os meses indicados e atualiza o state_YYYY.json.
    """
    rh_root = get_rh_root_for_year(request.year)

    scanner = RHScanner(rh_root)
    state_manager = StateManager(rh_root)

    result_by_month: Dict[str, Any] = {}

    for month_key in request.months:
        # garantir estrutura no state
        state = state_manager.load_state(request.year)
        state_manager.ensure_month(state, month_key)
        state_manager.save_state(request.year, state)

        # correr o scanner para o mês
        month_state = scanner.scan_month(request.year, month_key)
        result_by_month[month_key] = month_state

    return ScanResult(
        year=request.year,
        months=result_by_month
    )
from backend.core.pdf.merger import PDFMergerEngine
import datetime

class JoinRequest(BaseModel):
    year: str
    months: List[str]

@router.post("/join/base")
def generate_base_join(request: JoinRequest):

    rh_root = get_rh_root_for_year(request.year)
    state_manager = StateManager(rh_root)
    merger = PDFMergerEngine()

    final_results = {}

    for month_key in request.months:

        output_folder = os.path.join(rh_root, "14", month_key)
        os.makedirs(output_folder, exist_ok=True)

        output_pdf, warnings = merger.merge_month(
            month_key,
            rh_root,
            output_folder
        )

        # atualizar state
        state = state_manager.load_state(request.year)
        state["months"][month_key]["base_join"] = {
            "path": output_pdf,
            "created": datetime.datetime.now().isoformat(),
            "warnings": warnings
        }
        state_manager.save_state(request.year, state)

        final_results[month_key] = {
            "output_pdf": output_pdf,
            "warnings": warnings
        }

    return final_results
from backend.core.pdf.merger import PDFMergerEngine
import datetime

class JoinRequest(BaseModel):
    year: str
    months: List[str]


@router.post("/join/base")
def generate_base_join(request: JoinRequest):
    rh_root = get_rh_root_for_year(request.year)
    state_manager = StateManager(rh_root)
    merger = PDFMergerEngine()

    results = {}

    for month_key in request.months:
        output_folder = os.path.join(rh_root, "14", month_key)
        os.makedirs(output_folder, exist_ok=True)

        output_pdf, warnings = merger.merge_month(
            month_key,
            rh_root,
            output_folder
        )

        # update state
        state = state_manager.load_state(request.year)
        state["months"][month_key]["base_join"] = {
            "path": output_pdf,
            "created": datetime.datetime.now().isoformat(),
            "warnings": warnings
        }
        state_manager.save_state(request.year, state)

        results[month_key] = {
            "pdf": output_pdf,
            "warnings": warnings
        }

    return results
