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
            # Using gemini-flash-latest as verified with user key
            model = genai.GenerativeModel('gemini-flash-latest')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Return detailed error for debugging
            return f"Error calling Gemini API: {str(e)}"
    
    return "Invalid Model Provider"

from pdfminer.high_level import extract_text

def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file.
    """
    return extract_text(file)

import re

def clean_text(text):
    """
    Removes markdown formatting like **bold**, --, etc.
    """
    # Remove bold/italic markers
    text = re.sub(r'\*\*|__', '', text)
    text = re.sub(r'\*|_', '', text)
    # Remove headers
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove list markers if they are just dashes (optional, but user asked for no --)
    # Keeping bullet points might be good for readability, but user said "no --"
    # Let's just remove double dashes which are often used as separators
    text = re.sub(r'--', '', text)
    return text.strip()

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
    Provide a detailed analysis in plain text. Do NOT use markdown formatting (no bold, no italics, no headers).
    
    Match Score: [Score]/100
    
    Missing Keywords:
    - [Keyword 1]
    - [Keyword 2]
    
    Improvement Suggestions:
    - [Suggestion 1]
    - [Suggestion 2]
    """
    response = call_llm(prompt, model_provider, api_key)
    return clean_text(response)

def generate_resume_content(resume_text, job_description, model_provider, api_key):
    """
    Generates tailored resume content using LLM.
    """
    prompt = f"""
    You are an expert professional resume writer. Rewrite the following resume to tailor it for the job description provided.
    
    CRITICAL INSTRUCTIONS:
    1. Write in a purely human, professional tone. Avoid robotic transitions or overused AI phrases.
    2. Do NOT use any markdown formatting. No bold (**), no italics (*), no headers (#).
    3. Do NOT use double dashes (--).
    4. Target a 90%+ ATS match rate by naturally integrating keywords.
    5. Output ONLY the resume content. No intro/outro.
    
    Job Description:
    {job_description}
    
    Original Resume:
    {resume_text}
    """
    response = call_llm(prompt, model_provider, api_key)
    return clean_text(response)

def generate_cover_letter_content(resume_text, job_description, model_provider, api_key):
    """
    Generates cover letter content using LLM.
    """
    prompt = f"""
    You are an expert career coach. Write a persuasive cover letter based on the candidate's resume and the job description.
    
    CRITICAL INSTRUCTIONS:
    1. Write in a purely human, professional, and engaging tone. 
    2. Avoid generic AI phrases like "I am writing to express my interest". Be more creative and direct.
    3. Do NOT use any markdown formatting. No bold (**), no italics (*).
    4. Do NOT use double dashes (--).
    5. Do not include placeholders like [Your Name] if the information is available in the resume.
    
    Job Description:
    {job_description}
    
    Resume:
    {resume_text}
    """
    response = call_llm(prompt, model_provider, api_key)
    return clean_text(response)

def generate_docx_from_text(text_content):
    """
    Generates a DOCX file from raw text.
    """
    doc = Document()
    # Split by newlines and add as paragraphs
    for line in text_content.split('\n'):
        if line.strip():
            doc.add_paragraph(line.strip())
    
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
