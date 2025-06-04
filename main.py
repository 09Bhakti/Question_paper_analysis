from pdf_processing import extract_text_from_pdf
from text_cleaning import find_repeated_lines, clean_text
from question_extraction import extract_questions

def process_pdf(file_path):
    raw_text = extract_text_from_pdf(file_path)
    repeated_lines = find_repeated_lines(raw_text)
    cleaned_text = clean_text(raw_text, repeated_lines)
    questions = extract_questions(cleaned_text)
    return questions
