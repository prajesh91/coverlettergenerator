from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
import openai
import google.generativeai as genai


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

from pdfminer.high_level import extract_text

def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file.
    """
    return extract_text(file)

def extract_text_from_docx(file):
    """
    Extracts text from a DOCX file.
    """
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def analyze_ats_score(resume_text, job_description, model_provider, api_key):
    """
    Analyzes the resume against the job description and provides an ATS score.
    """
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) scanner. 
    Analyze the following resume against the job description.
    
    Job Description:
    {job_description}
    
    Resume:
    {resume_text}
    
    Output Format:
    Provide a detailed analysis in the following format:
    
    **Match Score**: [Score]/100
    
    **Missing Keywords**:
    - [Keyword 1]
    - [Keyword 2]
    
    **Improvement Suggestions**:
    - [Suggestion 1]
    - [Suggestion 2]
    """
    return call_llm(prompt, model_provider, api_key)

def generate_resume_content(resume_text, job_description, model_provider, api_key):
    """
    Generates tailored resume content using LLM.
    """
    prompt = f"""
    You are an expert resume writer. Rewrite the following resume to tailor it for the job description provided.
    Ensure you include relevant keywords from the job description to pass ATS systems.
    Target a 90%+ match rate.
    
    Job Description:
    {job_description}
    
    Original Resume:
    {resume_text}
    
    Output Format:
    Provide the full content of the new resume. 
    Do not include any introductory or concluding remarks. 
    Just the resume content.
    """
    return call_llm(prompt, model_provider, api_key)

def generate_cover_letter_content(resume_text, job_description, model_provider, api_key):
    """
    Generates cover letter content using LLM.
    """
    prompt = f"""
    You are an expert career coach. Write a persuasive cover letter based on the candidate's resume and the job description.
    
    Job Description:
    {job_description}
    
    Resume:
    {resume_text}
    
    The cover letter should be professional, engaging, and highlight why the candidate is a great fit.
    Do not include placeholders like [Your Name] if the information is available in the resume.
    """
    return call_llm(prompt, model_provider, api_key)

def generate_docx_from_text(text_content):
    """
    Generates a DOCX file from raw text.
    """
    doc = Document()
    for line in text_content.split('\n'):
        doc.add_paragraph(line)
    
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
