import os
import PyPDF2

base_folder = 'D:\GitHubRepository\GenerativeAI\python\Project-2\content'
subfolders = ['one', 'two', 'three']

for subfolder in subfolders:
    folder_path = os.path.join(base_folder, subfolder)
    output_path = os.path.join(folder_path, 'output.txt')
    try:
        if not os.path.isdir(folder_path):
            print(f"Folder '{folder_path}' does not exist. Skipping.")
            continue

        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        if not pdf_files:
            print(f"No PDF file found in '{folder_path}'. Skipping.")
            continue

        pdf_path = os.path.join(folder_path, pdf_files[0])
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''

        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(text)
        print(f"Extracted text written to '{output_path}'.")

    except Exception as e:
        print(f"Error processing folder '{folder_path}': {e}")