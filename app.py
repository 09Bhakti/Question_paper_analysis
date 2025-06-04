import streamlit as st
from main import process_pdf
from text_cleaning import clean_text
from question_extraction import extract_questions

st.title("📄 Question Paper Analyzer")

uploaded_file = st.file_uploader("Upload a question paper PDF", type="pdf")

if uploaded_file:
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.info("Processing uploaded file...")
    result = process_pdf("uploaded.pdf")

    st.subheader("Extracted Questions:")
    for i, q in enumerate(result, 1):
        st.markdown(f"**{q}**")
