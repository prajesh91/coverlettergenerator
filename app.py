import streamlit as st
import utils
import io

# Professional UI Setup
st.set_page_config(page_title="ATS Resume & Cover Letter Generator", page_icon="📄", layout="wide")

# Custom CSS for professional look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        height: 50px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h2 {
        color: #34495e;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 10px;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        border: 1px solid #ced4da;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📄 Professional ATS Resume & Cover Letter Generator")
st.markdown("---")

# API Key Handling (Background)
try:
    # Try to get from secrets first
    api_key = st.secrets["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError):
    # Fallback for immediate user testing (if secrets are not yet set on Cloud)
    # This ensures the app works right away for the demo
    api_key = "AIzaSyB8le0r8J12eWzIrkmLVeVdxW3BQ04CKMc"

model_provider = "Google Gemini"

if not api_key:
    st.warning("Please configure the API key to proceed.")
    st.stop()

# Layout using Tabs for cleaner interface
tab1, tab2, tab3 = st.tabs(["1️⃣ Upload & Details", "2️⃣ ATS Analysis", "3️⃣ Generate & Edit"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Current Resume")
        uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
        
        resume_text = ""
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".pdf"):
                    resume_text = utils.extract_text_from_pdf(uploaded_file)
                elif uploaded_file.name.endswith(".docx"):
                    resume_text = utils.extract_text_from_docx(uploaded_file)
                st.success("✅ Resume uploaded successfully!")
            except Exception as e:
                st.error(f"Error extracting text: {str(e)}")
    
    with col2:
        st.subheader("Job Description")
        job_description = st.text_area("Paste the job description here...", height=300)

with tab2:
    st.header("ATS Compatibility Check")
    if resume_text and job_description:
        if st.button("Analyze My Resume", key="analyze_btn"):
            with st.spinner("Auditing your resume against the job description..."):
                try:
                    analysis_result = utils.analyze_ats_score(resume_text, job_description, model_provider, api_key)
                    st.markdown("### 📊 Analysis Result")
                    st.text(analysis_result) # Use text to avoid markdown rendering issues if any remain
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
    else:
        st.info("Please upload a resume and provide a job description in the first tab.")

with tab3:
    st.header("Generate Optimized Documents")
    
    if st.button("✨ Generate Resume & Cover Letter", key="generate_btn"):
        if not resume_text or not job_description:
            st.error("Please complete the 'Upload & Details' tab first.")
        else:
            with st.spinner("Crafting your professional documents..."):
                try:
                    # Generate Content
                    st.session_state['generated_resume'] = utils.generate_resume_content(resume_text, job_description, model_provider, api_key)
                    st.session_state['generated_cover_letter'] = utils.generate_cover_letter_content(resume_text, job_description, model_provider, api_key)
                    st.balloons()
                    st.success("Documents generated successfully! Review and edit below.")
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")

    # Review and Edit Section
    if 'generated_resume' in st.session_state:
        st.markdown("---")
        col_res, col_cov = st.columns(2)
        
        with col_res:
            st.subheader("📝 Optimized Resume")
            edited_resume = st.text_area("Edit Resume Content", st.session_state['generated_resume'], height=600)
            
            resume_docx = utils.generate_docx_from_text(edited_resume)
            st.download_button(
                label="⬇️ Download Resume (DOCX)",
                data=resume_docx,
                file_name="Optimized_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        with col_cov:
            st.subheader("✉️ Cover Letter")
            edited_cover_letter = st.text_area("Edit Cover Letter Content", st.session_state['generated_cover_letter'], height=600)
            
            cover_letter_docx = utils.generate_docx_from_text(edited_cover_letter)
            st.download_button(
                label="⬇️ Download Cover Letter (DOCX)",
                data=cover_letter_docx,
                file_name="Cover_Letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
