# --- main.py ---
import os
from services.summarize import summarize_document
from services.compare import compare_documents
from services.extract import extract_text_from_pdf


def summarize_flow():
    print("Entrez le chemin du document texte à résumer : ", end="")
    path = input().strip()

    if not os.path.isfile(path):
        print("❌ Fichier introuvable.")
        return

    if path.endswith(".pdf"):
        text = extract_text_from_pdf(path)
    else:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    result = summarize_document(text)
    print(result)


def compare_flow():
    print("Entrez le chemin de l'ancienne version du document : ", end="")
    path1 = input().strip()
    print("Entrez le chemin de la nouvelle version du document : ", end="")
    path2 = input().strip()

    if not os.path.isfile(path1) or not os.path.isfile(path2):
        print("❌ L'un des fichiers est introuvable.")
        return

    if path1.endswith(".pdf"):
        text1 = extract_text_from_pdf(path1)
    else:
        with open(path1, "r", encoding="utf-8") as f:
            text1 = f.read()

    if path2.endswith(".pdf"):
        text2 = extract_text_from_pdf(path2)
    else:
        with open(path2, "r", encoding="utf-8") as f:
            text2 = f.read()

    result = compare_documents(text1, text2)
    print(result)


def main_menu():
    while True:
        print("\n🛡️  Outil de veille sur les Sanctions Internationales")
        print("==========================================")
        print("[1] Résumer un document")
        print("[2] Comparer deux documents")
        print("[3] Quitter")

        choix = input("Choix : ").strip()

        if choix == "1":
            summarize_flow()
        elif choix == "2":
            compare_flow()
        elif choix == "3":
            print("À bientôt ! 👋")
            break
        else:
            print("❌ Choix invalide, réessaie.")


if __name__ == "__main__":
    main_menu()
