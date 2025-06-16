# 📘 DynaScrap - Document Analysis Tool

A powerful document analysis tool that leverages local Large Language Models to help users analyze and compare documents efficiently.

## 🚀 Features

- 📄 **Document Summarization**: Generate clear and structured summaries of PDF documents
- 🔍 **Document Comparison**: Compare two versions of documents to identify important changes
- 🤖 **Multiple Model Support**: Choose from different LLM models for processing
- 📊 **User-Friendly Interface**: Clean and intuitive Streamlit interface
- 📥 **Export Options**: Download results in both Markdown and PDF formats

## 🧠 Supported Models

The application supports multiple local LLM models:
- phi4:latest
- command-r:35b-08-2024-q5_1
- llama3.3:latest

## 🚀 Getting Started

### 1. **Clone the repository**
```bash
git clone https://github.com/yassineerraji/Credit-Agricole-Internship-2025.git
```

### 2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Configure the local LLM service**

Ensure you have a local LLM service running at `http://localhost:1000` with the following models available:
- phi4:latest
- command-r:35b-08-2024-q5_1
- llama3.3:latest

## 🧪 Running the Application

### Start the Streamlit interface
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🗂️ Project Structure

```
DynaScrap/
├── app.py                # Main Streamlit application
├── config.py             # Configuration settings
├── main.py              # Testing script
├── requirements.txt     # Python dependencies
├── README.md           # This file
│
├── prompts/            # LLM prompts
│   ├── summarize.txt
│   └── compare.txt
│
├── services/           # Core services
│   ├── llm_service.py  # LLM service interface
│   ├── summarize.py    # Document summarization
│   ├── compare.py      # Document comparison
│   └── extract.py      # PDF text extraction
│
├── assets/            # Static assets
│   └── animation.json # Loading animation
│
├── data/             # Input documents
└── outputs/          # Generated results
    └── results/      # Analysis outputs
```

## 🔐 Security & Best Practices

- All processing is done locally using your own LLM service
- No data is sent to external APIs
- Results are saved locally in the outputs directory

## 🛠️ Technical Details

### Document Processing
- PDF text extraction using PyMuPDF4LLM
- Text processing with local LLM models
- Markdown and PDF export capabilities

### User Interface
- Built with Streamlit
- Responsive design
- Interactive model selection
- Progress indicators and animations

## 👤 Author

**Yassine Erraji**  
Data Scientist – Compliance Department  
Credit Agricole Summer Internship 2025

## 📝 License

This project is licensed under the MIT License for now but may change soon.
