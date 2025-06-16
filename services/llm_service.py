import requests
from config import API_URL, HEADERS

class LocalLLMService:
    def __init__(self, model: str):
        self.api_url = API_URL
        self.model = model
        self.headers = HEADERS

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the local model
        """
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }

            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers
            )

            if response.status_code == 200:
                result = response.json()
                # Extract the response from the chat completion format
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                raise Exception(f"Error from local model: {response.status_code} - {response.text}")
                
        except Exception as e:
            raise Exception(f"Failed to generate response : {str(e)}")

# Create a function to get a new instance with the specified model
def get_llm_service(model: str) -> LocalLLMService:
    return LocalLLMService(model) 
