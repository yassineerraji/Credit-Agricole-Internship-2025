from dotenv import load_dotenv
from services.llm_service import get_llm_service

load_dotenv()

def summarize_document(text: str, model_choice: str) -> str:
    """
    Generates and returns the Markdown summary of the provided text using the local LLM service.
    """
    # Load the summary prompt
    with open("prompts/summarize.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    full_prompt = f"{prompt}\n\nText to summarize:\n\n{text}"

    try:
        # Get a new LLM service instance with the selected model
        llm_service = get_llm_service(model_choice)
        return llm_service.generate_response(full_prompt).strip()
    except Exception as e:
        return f"❗ Erreur lors de la génération : {e}"


