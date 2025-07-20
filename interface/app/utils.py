import os

def delete_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"[INFO] Arquivo removido: {path}")
    except Exception as e:
        print(f"[ERRO] Falha ao remover {path}: {e}")

