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
    pattern = re.compile(r'(Q\.\d+)\s+(.*?)(?=\nQ\.\d+|\Z)', re.DOTALL)
    matches = pattern.findall(text)

    questions = []
    for q_num, body in matches:
        lines = [line.strip() for line in body.strip().splitlines() if line.strip()]
        options = []
        question_lines = []

        for i in range(len(lines) - 1, -1, -1):
            if len(options) >= 4:
                break
            if re.match(r'^(\(?[A-D]?\)?\s*)?[\w\d\-.+/%]+$', lines[i]):
                options.insert(0, lines[i])
            else:
                question_lines = lines[:i+1]
                break
        else:
            question_lines = lines

        questions.append({
            "number": q_num,
            "question": ' '.join(question_lines).strip(),
            "options": options
        })

    return questions

