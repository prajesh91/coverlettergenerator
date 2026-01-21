import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_sample_resume():
    path = "/Users/prajeshpoudyal/Desktop/cover letter/sample_resume.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "John Doe")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, "Software Engineer | Python Expert")
    c.drawString(50, height - 90, "Email: john.doe@example.com")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 120, "Experience")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 140, "Senior Developer at Tech Corp (2020 - Present)")
    c.drawString(50, height - 160, "- Led development of AI-driven tools.")
    c.drawString(50, height - 180, "- Optimized database queries by 40%.")
    
    c.save()
    print(f"Sample resume created at {path}")

if __name__ == "__main__":
    create_sample_resume()
