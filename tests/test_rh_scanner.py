import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.core.automation.rh_scanner import RHScanner

RH_PATH = r"C:\Users\Patricio Vargas\INCENTAHEAD CONSULTING, UNIPESSOAL LDA\INCENTAHEAD - Documentos (1)\4.Projetos\4.3.Execução\0. Afetação Pessoal Empresas\Agix\0. Pasta Partilhada\2025\RH"

scanner = RHScanner(RH_PATH)

result = scanner.scan_month("2025", "07_2025")

print("\nResultado do scan para 07_2025:")
print(result)
