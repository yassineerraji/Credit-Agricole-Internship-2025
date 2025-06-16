# Msty provided an api url to use locally the models downloaded
API_URL = "http://localhost:1000/v1/chat/completions"

MODELS = ["phi4:latest", "command-r:35b-08-2024-q5_1", "llama3.3:latest"]

# What the hell are headers ? 
HEADERS = {"Content-Type" : "application/json", "Authorization" : "Bearer msty-local"}
