import streamlit as st
import utils
import io


st.set_page_config(page_title="ATS Resume & Cover Letter Generator (LLM Powered)", layout="wide")

st.title("ATS Resume & Cover Letter Generator 🤖")
st.markdown("Generate a high-scoring ATS resume and cover letter using AI.")

# Sidebar for Settings
with st.sidebar:
    st.header("Settings")
    model_provider = st.selectbox("Select Model Provider", ["Google Gemini", "OpenAI"])
    api_key = st.text_input("API Key", type="password", help="Enter your API key here.")
    st.info("Get your Gemini API key from Google AI Studio (Free tier available).")

# Main Content
st.header("1. Upload Your Resume")
uploaded_file = st.file_uploader("Upload your current resume (PDF or DOCX)", type=["pdf", "docx"])

resume_text = ""
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".pdf"):
            resume_text = utils.extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            resume_text = utils.extract_text_from_docx(uploaded_file)
        st.success("Resume uploaded successfully!")
        with st.expander("View Extracted Text"):
            st.text_area("Extracted Resume Text", resume_text, height=200)
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")

st.header("2. Job Details")
job_description = st.text_area("Paste Job Description Here", height=300)

# ATS Analysis Section
if resume_text and job_description and api_key:
    if st.button("Analyze Current ATS Score"):
        with st.spinner("Analyzing resume against job description..."):
            try:
                analysis_result = utils.analyze_ats_score(resume_text, job_description, model_provider, api_key)
                st.markdown("### ATS Analysis Result")
                st.markdown(analysis_result)
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

st.header("3. Generate Optimized Documents")

if st.button("Generate Resume & Cover Letter"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    elif not resume_text:
        st.error("Please upload a resume.")
    elif not job_description:
        st.error("Please paste a job description.")
    else:
        with st.spinner(f"Generating content using {model_provider}..."):
            try:
                # Generate Content
                st.session_state['generated_resume'] = utils.generate_resume_content(resume_text, job_description, model_provider, api_key)
                st.session_state['generated_cover_letter'] = utils.generate_cover_letter_content(resume_text, job_description, model_provider, api_key)
                st.success("Documents generated! Review and edit below.")
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")

# Review and Edit Section
if 'generated_resume' in st.session_state:
    st.header("4. Review & Edit")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Optimized Resume")
        edited_resume = st.text_area("Edit Resume Content", st.session_state['generated_resume'], height=600)
        
        resume_docx = utils.generate_docx_from_text(edited_resume)
        st.download_button(
            label="Download Resume (DOCX)",
            data=resume_docx,
            file_name="Optimized_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    with col2:
        st.subheader("Cover Letter")
        edited_cover_letter = st.text_area("Edit Cover Letter Content", st.session_state['generated_cover_letter'], height=600)
        
        cover_letter_docx = utils.generate_docx_from_text(edited_cover_letter)
        st.download_button(
            label="Download Cover Letter (DOCX)",
            data=cover_letter_docx,
            file_name="Cover_Letter.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
