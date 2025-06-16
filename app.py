# app.py
import streamlit as st
import os
from streamlit_lottie import st_lottie
import datetime
from io import BytesIO
import json

from services.extract import extract_text_from_pdf
from services.summarize import summarize_document
from services.compare import compare_documents

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# A nice function to have an animation during the waiting time for both tasks.
def load_lottie(filepath : str) :
    with open(filepath, "r", encoding="utf-8") as f :
        return json.load(f)

lottie_loader = load_lottie("assets/animation.json")

# --- Page config & title ---
st.set_page_config(page_title="🛡️ DynaScrap (Beta)", layout="centered")
st.title("🛡️ Outil de Veille sur les Sanctions Internationales")
st.markdown("---")

# --- Inject CSS to style Markdown rendering ---
st.markdown(
    """
    <style>
    /* ensure long words wrap and manual line-breaks are honored */
    div[data-testid="stMarkdownContainer"] p {
        white-space: pre-wrap !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        text-align: justify;
        line-height: 1.6;
        font-size: 16px;
        margin-bottom: 1.2em;
    }
    /* center headings and add spacing */
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3 {
        text-align: center;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    /* center text inside all Streamlit buttons */
    .stButton > button, .stDownloadButton > button {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 0.3em 1em !important;
        line-height: 1.2 !important;
    }
    /* specific rule for the 'Générer la synthèse' button */
    .stButton > button:contains('Générer la synthèse') {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 0.3em 1em !important;
        line-height: 1.2 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Utility to save & display Markdown + download button ---
def save_and_display(content: str, prefix: str) :
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm")
    md_path = f"outputs/results/{prefix}_{timestamp}.md"
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)

    st.success("✅ Résultat généré avec succès :")
    st.markdown(content)
    st.download_button(
        "📥 Télécharger le résumé Markdown",
        data=content,
        file_name=os.path.basename(md_path),
        mime="text/markdown",
    )

# --- Choose a task ---
choice = st.radio(
    "Sélectionnez une tâche :",
    ["📄 Synthétiser un document", "📑 Comparer deux documents"],
    index=0,
)

# --- Choose a model ---
if choice:
    model_choice = st.selectbox(
        "Choisissez le modèle à utiliser :",
        ["phi4:latest", "command-r:35b-08-2024-q5_1", "llama3.3:latest"],
    )

# --- Résumer un document ---
if choice == "📄 Synthétiser un document":
    uploaded_file = st.file_uploader("Importez un document PDF à résumer :", type=["pdf"])
    if uploaded_file and st.button("Générer la synthèse"): # 📌
        # save temp PDF
        with open("temp_doc.pdf", "wb") as f:
            f.write(uploaded_file.read())
        extracted_text = extract_text_from_pdf("temp_doc.pdf")

        # Spinner while calling the local model
        with st.spinner("🕗 Génération de la synthèse en cours…"):
            loader_placeholder = st.empty()
            with loader_placeholder:
                st_lottie(lottie_loader, height=200, loop=True)
            summary_md = summarize_document(extracted_text, model_choice)
            loader_placeholder.empty()

        # Show & save Markdown
        save_and_display(summary_md, prefix="synthese")

        # --- PDF generation in‐memory ---
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=18,
        )
        styles = getSampleStyleSheet()
        story = []

        # Split on double-newline to get paragraphs/blocks
        for block in summary_md.split("\n\n"):
            text = block.strip()
            if not text:
                continue
            # Detect markdown headings
            if text.startswith("# "):
                story.append(Paragraph(text[2:], styles["Heading1"]))
            elif text.startswith("## "):
                story.append(Paragraph(text[3:], styles["Heading2"]))
            else:
                # Replace single newlines with <br/> so ReportLab respects line breaks
                story.append(
                    Paragraph(text.replace("\n", "<br/>"), styles["BodyText"])
                )
            story.append(Spacer(1, 0.2 * inch))

        doc.build(story)
        buffer.seek(0)
        pdf_bytes = buffer.read()

        # Download button for PDF
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm")
        st.download_button(
            "📄 Télécharger le résumé en PDF",
            data=pdf_bytes,
            file_name=f"synthese_{timestamp}.pdf",
            mime="application/pdf",
        )

# --- Comparer deux documents (unchanged for now) ---
elif choice == "📑 Comparer deux documents":
    col1, col2 = st.columns(2)
    with col1:
        old_file = st.file_uploader("Ancienne version du document :", type=["pdf"], key="old")
    with col2:
        new_file = st.file_uploader("Nouvelle version du document :", type=["pdf"], key="new")

    if old_file and new_file and st.button("📌 Comparer les deux documents"):
        with open("temp_old.pdf", "wb") as f:
            f.write(old_file.read())
        with open("temp_new.pdf", "wb") as f:
            f.write(new_file.read())

        old_text = extract_text_from_pdf("temp_old.pdf")
        new_text = extract_text_from_pdf("temp_new.pdf")

        with st.spinner("🕗 Analyse comparative en cours…"):
            loader_placeholder = st.empty()
            with loader_placeholder:
                st_lottie(lottie_loader, height=200, loop=True)
            comparison_md = compare_documents(old_text, new_text, model_choice)
            loader_placeholder.empty()

        save_and_display(comparison_md, prefix="comparaison")
