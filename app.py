import streamlit as st
from utils.pdf_extractor import extract_text_from_pdf
from utils.repeated_line_detector import find_repeated_lines
from utils.cleaner import clean_text
from utils.question_parser import extract_questions

st.set_page_config(page_title="Question Paper Analyzer", layout="wide")
st.title("📄 Question Paper Analyzer")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Extracting text..."):
        raw_text = extract_text_from_pdf("temp.pdf")

    with st.expander("Raw Extracted Text"):
        st.text_area("Text", raw_text, height=300)

    candidates = find_repeated_lines(raw_text)
    if candidates:
        st.subheader("Detected Repeated Lines (Header/Footer)")
        remove_lines = st.multiselect("Select lines to auto-remove", candidates)
    else:
        remove_lines = []

    cleaned_text = clean_text(raw_text, remove_lines)
    questions = extract_questions(cleaned_text)

    st.subheader("📌 Extracted Questions")
    if questions:
        for q in questions:
            st.markdown(f"**{q}**")
    else:
        st.info("No questions detected.")
