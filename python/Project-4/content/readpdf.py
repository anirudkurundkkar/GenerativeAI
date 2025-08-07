import os
import re
import PyPDF2

# Read regex from properties file
def read_regex_from_properties(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('regex='):
                return line.strip().split('=', 1)[1]
    raise ValueError("Regex not found in properties file.")

pdf_folder = 'D:\GitHubRepository\GenerativeAI\python\Project-4\content'
properties_path = r'D:\GitHubRepository\GenerativeAI\python\Project-4\content\config.properties'
pdf_file_name = 'Chemistry Questions.pdf'
pdf_path = os.path.join(pdf_folder, pdf_file_name)
output_path = 'output.txt'


try:
    regex = read_regex_from_properties(properties_path)

    if not os.path.isdir(pdf_folder):
        raise FileNotFoundError(f"Folder '{pdf_folder}' does not exist.")
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file '{pdf_path}' does not exist.")
    if not os.path.isfile(properties_path):
        raise FileNotFoundError(f"Properties file '{properties_path}' does not exist.")

    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    matches = re.findall(regex, text)
    with open(output_path, 'w', encoding='utf-8') as out_file:
        for match in matches:
            out_file.write(match + '\n')

    print(f"Extracted matches written to `{output_path}`.")

except FileNotFoundError:
    print(f"Error: The output file '{output_path}' could not be created or found.")
except Exception as e:
    print(f"An error occurred while writing to '{output_path}': {e}")