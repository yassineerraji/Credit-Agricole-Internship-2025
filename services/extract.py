# --- services/extract.py ---
import pymupdf4llm

def extract_text_from_pdf(path) :
    '''
    Optimized version that identifies efficently the structure of the text 
    and provides the markdown version of it, easing the task for the LLM.
    '''
    md_text = pymupdf4llm.to_markdown(path)
    return md_text
   
if __name__ == "__main__" : 
    test_path = "data\docs\ACPR Décision Tunisian Bank.pdf"
    result = extract_text_from_pdf(test_path)
    print(result)




