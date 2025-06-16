# compare.py
from dotenv import load_dotenv
from services.llm_service import get_llm_service

load_dotenv()

def compare_documents(old_text: str, new_text: str, model_choice: str) -> str:
    """
    Generates and returns a Markdown comparison between two documents using the local LLM service.
    """
    # Load the comparison prompt
    with open("prompts/compare.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    full_prompt = f"{prompt}\n\nPrevious text :\n\n{old_text}\n\nNew text :\n\n{new_text}"

    try:
        # Get a new LLM service instance with the selected model
        llm_service = get_llm_service(model_choice)
        return llm_service.generate_response(full_prompt).strip()
    except Exception as e:
        return f"❗ Erreur lors de la génération : {e}"

