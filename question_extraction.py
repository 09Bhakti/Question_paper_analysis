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
        r'(?=\nQ\.?\s*\d+|\n\d+\.|\Z)',  # Lookahead for next Q or end
        re.DOTALL | re.IGNORECASE
    )

    matches = pattern.findall(text)
    questions = []

    for q_num, body in matches:
        # Combine and flatten the question text
        clean_body = ' '.join(body.strip().split())

        # Skip non-question lines like marking instructions
        if re.search(r'carry\s+(one|two|\d+)\s+mark', clean_body, re.IGNORECASE):
            continue
        if len(clean_body.split()) < 5:  # skip very short lines
            continue

        # Remove options like (A)... (B)... etc.
        clean_body = re.sub(r'\([A-D]\)\s.*?(?=(\([A-D]\)|$))', '', clean_body, flags=re.DOTALL)

        # Remove common non-question patterns
        clean_body = re.split(
            r'(?=“|From|Based only|Note:|Select the most appropriate|Which one of|The sum of|Choose the correct|To manufacture|Consider)', 
            clean_body
        )[0].strip()

        # Re-assemble cleaned question
        if clean_body:
            questions.append(f"{q_num.strip()}. {clean_body}")

    return questions

