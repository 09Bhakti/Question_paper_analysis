import re

def extract_questions(text):
    pattern = re.compile(
        r'(Q\.?\s*\d+|\d+\.)\s+(.*?)'
        r'(?=\nQ\.?\s*\d+|\n\d+\.|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    matches = pattern.findall(text)
    questions = []
    for q_num, body in matches:
        clean_body = body.strip().replace("\n", " ")
        questions.append(f"{q_num.strip()} {clean_body}")
    return questions
