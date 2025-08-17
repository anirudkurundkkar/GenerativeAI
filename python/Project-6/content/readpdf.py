import sys
import re
import pdfplumber
import configparser

config_path = r'D:\GitHubRepository\GenerativeAI\python\Project-6\content\config.properties'
pdf_file = r'D:\GitHubRepository\GenerativeAI\python\Project-6\content\Chemistry Questions.pdf'

def extract_chapter_questions(pdf_path, chapter_name):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    config = configparser.ConfigParser()
    config.read(config_path)
    patterns = config['patterns']
    chapter_regex = re.compile(patterns['chapter'], re.MULTILINE)
    question_regex = re.compile(patterns['question'], re.MULTILINE | re.DOTALL)

    # Find all chapter headings with their positions
    chapters = [(m.group(1).strip(), m.start()) for m in chapter_regex.finditer(text)]

    # Find the location of the requested chapter
    chapter_start = None
    chapter_end = None
    for idx, (chap, pos) in enumerate(chapters):
        if chap.lower() == chapter_name.lower():
            chapter_start = pos
            if idx + 1 < len(chapters):
                chapter_end = chapters[idx + 1][1]
            else:
                chapter_end = len(text)
            break

    if chapter_start is None:
        print(f"Chapter '{chapter_name}' not found.")
        sys.exit(1)

    # Get text of the requested chapter only
    chapter_text = text[chapter_start:chapter_end]

    # Extract all questions from the chapter text
    questions = question_regex.findall(chapter_text)

    return questions


if __name__ == "__main__":

    chapter_name = input()

    questions = extract_chapter_questions(pdf_file, chapter_name)
    if questions:
        print(f"Questions from chapter '{chapter_name}':\n")
        for idx, q in enumerate(questions, 1):
            print(f"{q}")
    else:
        print(f"No questions found in chapter '{chapter_name}'.")