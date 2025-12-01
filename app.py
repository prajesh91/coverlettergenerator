import streamlit as st
import utils
import io

# Cache the model loading to prevent reloading on every run
@st.cache_resource
def get_spacy_model():
    return utils.load_spacy_model()

# Pre-load model
get_spacy_model()

st.set_page_config(page_title="ATS Resume & Cover Letter Generator (LLM Powered)", layout="wide")

st.title("ATS Resume & Cover Letter Generator 🤖")
st.markdown("Generate a high-scoring ATS resume and cover letter using AI.")

# Sidebar for Settings
with st.sidebar:
    st.header("Settings")
    model_provider = st.selectbox("Select Model Provider", ["Google Gemini", "OpenAI"])
    api_key = st.text_input("API Key", type="password", help="Enter your API key here.")
    st.info("Get your Gemini API key from Google AI Studio (Free tier available).")

# Two-column layout
col1, col2 = st.columns(2)

with col1:
    st.header("1. Your Profile")
    name = st.text_input("Full Name", "John Doe")
    email = st.text_input("Email", "john@example.com")
    phone = st.text_input("Phone", "123-456-7890")
    summary = st.text_area("Current Professional Summary", "Experienced professional with...")
    experience = st.text_area("Work Experience", "Job Title at Company (Year-Year)\n- Achievement 1")
    education = st.text_area("Education", "Degree at University (Year)")
    skills = st.text_area("Skills (Comma separated)", "Python, Project Management")

with col2:
    st.header("2. Job Details")
    job_title = st.text_input("Job Title")
    company_name = st.text_input("Company Name")
    job_description = st.text_area("Paste Job Description Here", height=400)

if st.button("Generate Documents"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    elif not job_description:
        st.error("Please paste a job description.")
    else:
        with st.spinner(f"Generating content using {model_provider}..."):
            # Prepare Data
            profile_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "summary": summary,
                "experience": experience,
                "education": education,
                "skills": skills
            }
            job_data = {
                "title": job_title,
                "company": company_name,
                "description": job_description
            }

            # Generate Files
            try:
                # Resume
                resume_docx = utils.generate_resume_docx(profile_data, job_data, model_provider, api_key)
                
                # Cover Letter
                cover_letter_docx = utils.generate_cover_letter_docx(profile_data, job_data, model_provider, api_key)
                
                # Download Buttons
                st.subheader("Downloads")
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    st.download_button(
                        label="Download Resume (DOCX)",
                        data=resume_docx,
                        file_name="Optimized_Resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    
                with col_d2:
                    st.download_button(
                        label="Download Cover Letter (DOCX)",
                        data=cover_letter_docx,
                        file_name="Cover_Letter.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                st.success("Documents generated successfully!")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
