from PyPDF2 import PdfReader
from summarizer import summarize_email
reader = PdfReader("DWM-Lab-Syllabus.pdf")
text = " "
for page in reader.pages :
    text += page.extract_text()
pdf_text_summary = summarize_email(text)
print(pdf_text_summary)