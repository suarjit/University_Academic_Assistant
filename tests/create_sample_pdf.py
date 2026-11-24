
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

output_path = "data/raw/sample_document.pdf"

pdf = canvas.Canvas(output_path, pagesize=A4)

width, height = A4

pdf.setFont("Helvetica-Bold", 16)
pdf.drawString(50, height - 50, "GREENFIELD UNIVERSITY")

pdf.setFont("Helvetica-Bold", 13)
pdf.drawString(50, height - 85, "Library Policy - 2026-2027")

pdf.setFont("Helvetica", 11)

lines = [
    "The central library is open Monday to Saturday.",
    "Library opening hours are 9:00 AM to 6:00 PM.",
    "Students may borrow up to four books at a time.",
    "The standard borrowing period is 14 days.",
    "Students must return books before the due date.",
    "A late return may result in a library fine.",
    "This is fictional sample information for testing."
]

y = height - 120

for line in lines:
    pdf.drawString(50, y, line)
    y -= 25

pdf.save()

print("Sample PDF created:", output_path)
