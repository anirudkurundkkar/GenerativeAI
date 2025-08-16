import os
import re
import configparser
import PyPDF2
import pdfplumber
import json


pdf_folder = 'D:\GitHubRepository\GenerativeAI\python\Project-5\content'
properties_path = r'D:\GitHubRepository\GenerativeAI\python\Project-5\content\config.properties'
pdf_file_name = 'Chemistry Questions.pdf'
pdf_path = os.path.join(pdf_folder, pdf_file_name)
output_path = 'output.txt'
config_path = r'D:\GitHubRepository\GenerativeAI\python\Project-5\content\config.properties'

config = configparser.ConfigParser()
config.read(config_path)
patterns = config['patterns']

chapter_pattern = re.compile(patterns['chapter_pattern'], re.MULTILINE)
question_pattern = re.compile(patterns['question_block_pattern'], re.MULTILINE | re.DOTALL)
answer_pattern = re.compile(patterns['option_pattern'], re.MULTILINE)

text = ''
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text += page.extract_text() + "\n"

entries = []
chapter_matches = list(chapter_pattern.finditer(text))
question_matches = list(question_pattern.finditer(text))
answer_matches = list(answer_pattern.finditer(text))

for i in range(len(chapter_matches)):
    for i in range(len(question_matches)):
        chapter_name = None
        # Find the nearest previous chapter heading
        for chap in chapter_matches:
            if chap.start() < question_matches[i].start():
                chapter_name = chap.group(1)
            else:
                break
        question = question_matches[i].group(1).strip()
        answer = None
        # Find the nearest answer after the question
        for ans in answer_matches:
            if ans.start() > question_matches[i].end():
                answer = ans.group(1).strip()
                break
        entries.append((chapter_name, question, answer))

