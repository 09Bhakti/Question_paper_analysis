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


def clean_text(text):
    # Remove headers like "Q.1 – Q.5 Carry ONE mark Each"
    text = re.sub(r"Q\.?\s*\d+\s*–\s*Q\.?\s*\d+\s*Carry\s+\w+\s+mark[s]?\s+Each", "", text, flags=re.IGNORECASE)

    # Fix encoding issues, unwanted line breaks and spaces
    text = re.sub(r'(?<=\w)-\n(?=\w)', '', text)  # Join hyphenated words split by newline
    text = re.sub(r'\n+', '\n', text)  # Collapse multiple newlines
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces
    text = text.strip()
    return text


def extract_questions(text):
    text = clean_text(text)

    # Match questions starting with Q.1 or 1. etc.
    pattern = re.compile(
        r'(Q\.?\s*\d+|\d+\.)\s+(.*?)(?=Q\.?\s*\d+|\d+\.|$)',  # Lookahead for next Q.2 or 2. or end
        re.DOTALL | re.IGNORECASE
    )

    matches = pattern.findall(text)
    questions = []

    for q_num, body in matches:
        clean_body = body.strip()

        # Remove duplicate inner question numbers like "Q.1", "1.", etc.
        clean_body = re.sub(r'^(Q\.?\s*\d+|\d+\.)\s+', '', clean_body)

        # Remove any remaining junk instructions
        if re.search(r'carry\s+(one|two|\d+)\s+mark', clean_body, re.IGNORECASE):
            continue

        clean_body = re.sub(r'\s+', ' ', clean_body).strip()

        if clean_body:
            questions.append(f"{q_num.strip()}. {clean_body}")

    return questions

