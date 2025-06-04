import re
import difflib
from collections import Counter

def find_repeated_lines(raw_text, min_occurrences=3, top_n=3, bottom_n=3, similarity_threshold=0.9):
    pages = re.split(r'^---\s*Page\s*\d+\s*---$', raw_text, flags=re.MULTILINE)
    pages = [p.strip() for p in pages if p.strip()]
    all_candidates = []

    for page in pages:
        lines = [line.strip() for line in page.splitlines() if line.strip()]
        candidates = lines[:top_n] + lines[-bottom_n:]
        for line in candidates:
            normalized = re.sub(r'\d+', '', line.lower()).strip()
            all_candidates.append((normalized, line))

    clusters = {}
    for norm_line, orig_line in all_candidates:
        found = False
        for key in clusters:
            if difflib.SequenceMatcher(None, norm_line, key).ratio() >= similarity_threshold:
                clusters[key].append(orig_line)
                found = True
                break
        if not found:
            clusters[norm_line] = [orig_line]

    repeated_lines = []
    for group in clusters.values():
        if len(group) >= min_occurrences:
            most_common = Counter(group).most_common(1)[0][0]
            repeated_lines.append(most_common)

    return repeated_lines

# def clean_text(raw_text, removals):
#     cleaned_lines = []
#     for line in raw_text.splitlines():
#         line_stripped = line.strip()
#         lower_line = line_stripped.lower()

#         if any(removal.lower() in lower_line for removal in removals):
#             continue
#         if re.match(r'^---\s*page\s*\d+\s*---$', line_stripped, re.IGNORECASE):
#             continue
#         if re.match(r'^page\s*\d+(\s*of\s*\d+)?$', line_stripped, re.IGNORECASE):
#             continue
#         if re.fullmatch(r'\d+', line_stripped):
#             continue
#         if "organizing institute" in lower_line and len(lower_line.split()) <= 8:
#             continue
#         if re.fullmatch(r'(each question|this section).*mark[s]?.*', lower_line):
#             continue
#         if re.fullmatch(r'mark[s]?\s*[:\-]?\s*\d+', lower_line):
#             continue

#         cleaned_lines.append(line_stripped)
#     return "\n".join(cleaned_lines).strip()

import re

def clean_text(raw_text,removals):
    lines = raw_text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    cleaned_lines = []
    for line in lines:
        if re.search(r'^Page \d+ of \d+', line, re.IGNORECASE):
            continue
        if re.search(r'^Organizing Institute', line, re.IGNORECASE):
            continue
        if re.search(r'^Data Science and Artificial Intelligence \(DA\)', line, re.IGNORECASE):
            continue
        if re.search(r'^Q\.\d+\s*–\s*Q\.\d+', line):
            continue
        if re.search(r'Carry\s+(ONE|TWO)\s+mark[s]?', line, re.IGNORECASE):
            continue
        if re.search(r'^--- Page \d+ ---$', line):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()

