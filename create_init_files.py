import os

# PASTAS QUE DEVEM TER __init__.py
REQUIRED_PACKAGES = [
    "backend",
    "backend/core",
    "backend/core/automation",
    "backend/core/pdf",
    "backend/services",
    "backend/utils",
    "backend/api",
    "tests",
]

def create_init_files():
    for package in REQUIRED_PACKAGES:
        path = os.path.join(package, "__init__.py")

        # Garantir que a pasta existe
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Criar ficheiro __init__.py se não existir
        if not os.path.exists(path):
            with open(path, "w", encoding="utf8") as f:
                f.write("# Auto-generated to enable Python packages\n")
            print(f"[OK] Created: {path}")
        else:
            print(f"[SKIP] Already exists: {path}")

if __name__ == "__main__":
    print("\n--- Creating __init__.py files for Python packages ---\n")
    create_init_files()
    print("\nDone! All required __init__.py files are now in place.\n")
