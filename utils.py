import spacy
from collections import Counter
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
import openai
import google.generativeai as genai

# Load Spacy model (Lazy loading)
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

def extract_keywords(text, num_keywords=20):
    """
    Extracts keywords from text using Spacy.
    """
    nlp = load_spacy_model()
    doc = nlp(text)
    keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and not token.is_punct:
            keywords.append(token.text.lower())
    word_freq = Counter(keywords)
    return [word for word, count in word_freq.most_common(num_keywords)]

def call_llm(prompt, model_provider, api_key):
    """
    Calls the specified LLM provider to generate content.
    """
    if model_provider == "OpenAI":
        openai.api_key = api_key
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"
            
    elif model_provider == "Google Gemini":
        genai.configure(api_key=api_key)
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error calling Gemini: {str(e)}"
    
    return "Invalid Model Provider"

def generate_resume_content(profile_data, job_data, model_provider, api_key):
    """
    Generates resume content using LLM.
    """
    prompt = f"""
    You are an expert resume writer. Rewrite the following professional summary and experience to tailor it for the job description provided.
    Ensure you include relevant keywords from the job description to pass ATS systems.
    
    Job Description:
    {job_data['description']}
    
    Candidate Profile:
    Name: {profile_data['name']}
    Summary: {profile_data['summary']}
    Experience: {profile_data['experience']}
    Skills: {profile_data['skills']}
    
    Output Format:
    Provide the output in two sections:
    1. Professional Summary
    2. Experience (bullet points)
    Do not include any other text.
    """
    return call_llm(prompt, model_provider, api_key)

def generate_cover_letter_content(profile_data, job_data, model_provider, api_key):
    """
    Generates cover letter content using LLM.
    """
    prompt = f"""
    You are an expert career coach. Write a persuasive cover letter for the following candidate applying for the specified job.
    
    Job Details:
    Title: {job_data['title']}
    Company: {job_data['company']}
    Description: {job_data['description']}
    
    Candidate Profile:
    Name: {profile_data['name']}
    Email: {profile_data['email']}
    Phone: {profile_data['phone']}
    Summary: {profile_data['summary']}
    Experience: {profile_data['experience']}
    
    The cover letter should be professional, engaging, and highlight why the candidate is a great fit.
    """
    return call_llm(prompt, model_provider, api_key)

def generate_resume_docx(profile_data, job_data, model_provider, api_key):
    """
    Generates a DOCX resume using LLM content.
    """
    # Get LLM content
    llm_content = generate_resume_content(profile_data, job_data, model_provider, api_key)
    
    doc = Document()
    
    # Header
    doc.add_heading(profile_data.get('name', 'Name'), 0)
    doc.add_paragraph(f"{profile_data.get('email', '')} | {profile_data.get('phone', '')}")
    
    # Parse LLM content (Simple split for now, robust parsing would be better)
    # Assuming LLM follows instructions roughly
    doc.add_heading('Optimized Content', level=1)
    doc.add_paragraph(llm_content)
    
    # Education (Static)
    doc.add_heading('Education', level=1)
    doc.add_paragraph(profile_data.get('education', ''))
    
    # Skills (Static + Keywords)
    doc.add_heading('Skills', level=1)
    doc.add_paragraph(profile_data.get('skills', ''))

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

def generate_cover_letter_docx(profile_data, job_data, model_provider, api_key):
    """
    Generates a DOCX cover letter using LLM content.
    """
    llm_content = generate_cover_letter_content(profile_data, job_data, model_provider, api_key)
    
    doc = Document()
    doc.add_paragraph(llm_content)
    
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

def generate_pdf_from_text(text_content):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    
    # Simple text wrapping could be added here
    for line in text_content.split('\n'):
        if y < 40:
            p.showPage()
            y = height - 40
        p.drawString(40, y, line[:90]) # Simple truncation to avoid overflow
        y -= 15
        
    p.save()
    buffer.seek(0)
    return buffer
