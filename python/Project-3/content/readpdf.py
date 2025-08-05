import os
import PyPDF2

pdf_folder = 'D:\GitHubRepository\GenerativeAI\python\Project-3\content'
pdf_file_name = 'Chemistry Questions.pdf'
pdf_path = os.path.join(pdf_folder, pdf_file_name)
output_path = 'output.txt'

try:
    if not os.path.isdir(pdf_folder):
        raise FileNotFoundError(f"Folder '{pdf_folder}' does not exist.")
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file '{pdf_path}' does not exist.")

    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''

        text += reader.pages[0].extract_text()

    try:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(text)
    except FileNotFoundError:
        print(f"Error: The output file '{output_path}' could not be created or found.")
    except Exception as e:
        print(f"An error occurred while writing to '{output_path}': {e}")

except FileNotFoundError as fnf_error:
    print(f"Error: {fnf_error}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")