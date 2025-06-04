import re

# def extract_questions(text):
#     pattern = re.compile(
#         r'(Q\.?\s*\d+|\d+\.)\s+(.*?)'
#         r'(?=\nQ\.?\s*\d+|\n\d+\.|\Z)',
#         re.DOTALL | re.IGNORECASE
#     )
#     matches = pattern.findall(text)
#     questions = []
#     for q_num, body in matches:
#         clean_body = body.strip().replace("\n", " ")
#         questions.append(f"{q_num.strip()} {clean_body}")
#     return questions

def extract_questions(text):
    pattern = re.compile(
        r'(Q\.?\s*\d+|\d+\.)\s+(.*?)'
        r'(?=\nQ\.?\s*\d+|\n\d+\.|\Z)',  # Lookahead for next Q or number or end
        re.DOTALL | re.IGNORECASE
    )

    matches = pattern.findall(text)
    questions = []

    for q_num, body in matches:
        clean_body = ' '.join(body.strip().split())

        # Remove internal question numbers like "Q.1", "1.", etc. at the start of the body
        clean_body = re.sub(r'^(Q\.?\s*\d+|\d+\.)\s+', '', clean_body)

        # Remove excessive whitespace and fix formatting
        clean_body = re.sub(r'\s+', ' ', clean_body).strip()

        # Only skip if it's clearly an instruction header (short and no question-like structure)
        if len(clean_body) < 30 and re.search(r'carry\s+(one|two|\d+)\s+mark', clean_body, re.IGNORECASE):
            continue

        if clean_body:
            questions.append(f"{q_num.strip()}. {clean_body}")

    return questions


