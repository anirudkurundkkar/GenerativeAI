import os
import re
import mysql.connector
import match
import pymysql
import pymysql.cursors
import configparser
import pdfplumber

pdf_folder = 'D:\GitHubRepository\GenerativeAI\python\Project-5\content'
properties_path = r'D:\GitHubRepository\GenerativeAI\python\Project-5\content\config.properties'
pdf_file_name = 'Chemistry Questions.pdf'
pdf_path = os.path.join(pdf_folder, pdf_file_name)
output_path = 'output.txt'
config_path = r'D:\GitHubRepository\GenerativeAI\python\Project-5\content\config.properties'

try:
    config = configparser.ConfigParser()
    config.read(config_path)
    patterns = config['patterns']
    chapter_pattern = re.compile(patterns['chapter_pattern'], re.MULTILINE)
    question_pattern = re.compile(patterns['question_block_pattern'], re.MULTILINE | re.DOTALL)
    answer_pattern = re.compile(patterns['option_pattern'], re.MULTILINE)

    if not os.path.isdir(pdf_folder):
        raise FileNotFoundError(f"Folder '{pdf_folder}' does not exist.")
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file '{pdf_path}' does not exist.")
    if not os.path.isfile(properties_path):
        raise FileNotFoundError(f"Properties file '{properties_path}' does not exist.")

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


    # Insert each question into MySQL
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Anirud@10302025@$',
                             port= 3306,
                             database='sys',
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chemistry_questions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chapter_name VARCHAR(255),
            question TEXT,
            answer TEXT
            )
        """)
    for chapter, question, answer in entries:
        # Adjust the following line if you have more fields to extract
        cursor.execute("""
                INSERT INTO chemistry_questions (chapter_name, question, answer)
                VALUES (%s, %s, %s)
                """, (chapter, question, answer))
    connection.commit()
    cursor.close()
    connection.close()

    print(f"Extracted questions inserted into MySQL table `chemistry_questions`.")

except FileNotFoundError:
    print(f"Error: The output file '{output_path}' could not be created or found.")
except Exception as e:
    print(f"An error occurred while writing to '{output_path}': {e}")