from PyPDF2 import PdfReader

# Path to the PDF file
pdf_path = 'your_file.pdf'

reader = PdfReader(pdf_path)
text = ""

for page in reader.pages:
    text += page.extract_text()

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print("Text extracted and saved to output.txt")