import os

PROJECT_STRUCTURE = [
    "frontend",
    "frontend/css",
    "frontend/js",
    "frontend/assets",
    "frontend/assets/icons",
    "backend",
    "backend/api",
    "backend/core",
    "backend/core/pdf",
    "backend/core/automation",
    "backend/services",
    "backend/utils",
    "backend/config",
    "tests",
    "scripts",
    "docs"
]

FILES = {
    "frontend/index.html": "<!-- HTML UI root -->",
    "frontend/css/main.css": "/* main style */",
    "frontend/js/app.js": "// app entry",
    "frontend/js/dragdrop.js": "// drag & drop logic",
    "frontend/js/preview.js": "// pdf preview logic",
    "frontend/js/editor.js": "// page editor",
    "frontend/js/api.js": "// frontend-backend API calls",

    "backend/main.py": "print('Backend placeholder running')",
    "backend/api/pdf_routes.py": "# PDF API endpoints",
    "backend/api/rh_routes.py": "# RH automation endpoints",
    "backend/api/system_routes.py": "# System utilities endpoints",

    "backend/core/pdf/loader.py": "class PDFLoader:\n    pass",
    "backend/core/pdf/renderer.py": "class PDFRenderer:\n    pass",
    "backend/core/pdf/editor.py": "class PDFEditor:\n    pass",
    "backend/core/pdf/merger.py": "class PDFMerger:\n    pass",

    "backend/core/automation/rh_scanner.py": "class RHScanner:\n    pass",
    "backend/core/automation/rh_validator.py": "class RHValidator:\n    pass",
    "backend/core/automation/rh_report.py": "class RHReport:\n    pass",
    "backend/core/automation/rh_compiler.py": "class RHCompiler:\n    pass",

    "backend/services/pdf_service.py": "class PDFService:\n    pass",
    "backend/services/rh_service.py": "class RHService:\n    pass",

    "backend/utils/file_utils.py": "# file utilities",
    "backend/utils/path_utils.py": "# path utilities",
    "backend/utils/logger.py": "# logger system",
    "backend/utils/config_loader.py": "# config loader",

    "backend/config/settings.json": "{}",
    "backend/config/rh_structure.json": "{}",
    "backend/config/defaults.json": "{}",

    "tests/test_pdf_engine.py": "",
    "tests/test_rh_automation.py": "",
    "tests/test_api.py": "",
    "tests/test_ui.py": "",

    "scripts/batch_compile.py": "# batch automation script",
    "scripts/rebuild_thumbnails.py": "# rebuild thumbnails",

    "docs/architecture.md": "# Architecture Documentation",
    "docs/api_reference.md": "# API Reference",
    "docs/setup_guide.md": "# Setup Guide",
    "docs/roadmap.md": "# Roadmap",

    "requirements.txt": "",
    "README.md": "# RH Document Compiler",
    ".env.example": "API_KEY="
}

def create_project():
    for folder in PROJECT_STRUCTURE:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

    for path, content in FILES.items():
        with open(path, "w", encoding="utf8") as f:
            f.write(content)
        print(f"Created file: {path}")

if __name__ == "__main__":
    create_project()
    print("\nProject structure created successfully.")
