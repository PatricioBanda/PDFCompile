import sys
import os

# ADICIONA O PATH DO PROJETO
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# IMPORTAÇÃO CORRETA
from backend.core.automation.state_manager import StateManager

# CAMINHO REAL PARA A TUA PASTA RH
RH_PATH = r"C:\Users\Patricio Vargas\INCENTAHEAD CONSULTING, UNIPESSOAL LDA\INCENTAHEAD - Documentos (1)\4.Projetos\4.3.Execução\0. Afetação Pessoal Empresas\Agix\0. Pasta Partilhada\2025\RH"

sm = StateManager(RH_PATH)

state = sm.load_state("2025")
sm.ensure_month(state, "07_2025")
sm.save_state("2025", state)

print("DONE")
