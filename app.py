import streamlit as st
import utils
import io

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()  # Do not continue running script

# Professional UI Setup
st.set_page_config(
    page_title="Free AI ATS Resume & Cover Letter Generator | Optimize Your Career",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://aistudio.google.com/app/apikey',
        'Report a bug': None,
        'About': "# Professional AI Career Suite\nOptimize your resume and generate persuasive cover letters instantly."
    }
)

# Custom CSS for HeyOrbi-inspired look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600;700&display=swap');

    :root {
        --primary-bg: #0A0A0A;
        --accent-color: #FF4D2D;
        --text-main: #FFFFFF;
        --text-muted: #A1A1AA;
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    .stApp {
        background-color: var(--primary-bg);
        color: var(--text-main);
        font-family: 'Instrument Sans', sans-serif;
    }

    /* Centered Hero Section */
    .hero-container {
        text-align: center;
        padding: 60px 20px;
        max-width: 900px;
        margin: 0 auto;
    }

    h1 {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(to bottom, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px !important;
        letter-spacing: -0.02em !important;
    }

    h2, h3 {
        color: var(--text-main) !important;
        font-weight: 600 !important;
    }

    p, .stMarkdown {
        color: var(--text-muted);
        font-size: 1.1rem;
    }

    /* Glassmorphism Cards */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div {
        # background: var(--glass-bg);
        # border: 1px solid var(--glass-border);
        # border-radius: 16px;
        # padding: 1.5rem;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--accent-color) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        width: 100%;
        height: auto !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -10px var(--accent-color);
        opacity: 0.9;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: var(--glass-bg);
        border-radius: 8px 8px 0px 0px;
        border: 1px solid var(--glass-border);
        padding: 0 20px;
        color: var(--text-muted);
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--glass-border) !important;
        color: var(--text-main) !important;
        border-bottom: 2px solid var(--accent-color) !important;
    }

    /* Inputs */
    /* Inputs - High Contrast for Readability */
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        color: #000000 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 1px var(--accent-color) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F0F0F;
        border-right: 1px solid var(--glass-border);
    }

    /* Gradient Blur Background */
    .gradient-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 10% 10%, rgba(255, 77, 45, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 90% 90%, rgba(0, 123, 255, 0.05) 0%, transparent 40%);
        z-index: -1;
    }
</style>
<div class="gradient-bg"></div>
""", unsafe_allow_html=True)

# SEO Header & Hero
st.markdown("""
    <div class="hero-container">
        <h1>Your AI-Powered Career Edge</h1>
        <p>Stop guessing. Start winning. Optimize your resume for ATS, generate high-converting cover letters, and unlock career insights in seconds.</p>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

# API Key Handling
with st.sidebar:
    st.header("Settings")
    st.markdown("Enter your Gemini API key below to enable AI features.")
    
    api_key = st.text_input(
        "Gemini API Key", 
        type="password",
        help="Get your key at https://aistudio.google.com/app/apikey"
    )
    
    if not api_key:
        st.info("💡 Tip: You can get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).")
        st.warning("⚠️ API Key missing. Please provide it to proceed.")
        st.stop()

# Layout using Tabs for cleaner interface
tab1, tab2, tab3, tab4, tab5 = st.tabs(["1️⃣ Upload & Details", "2️⃣ ATS Analysis", "3️⃣ Generate Documents", "4️⃣ Career Insights", "5️⃣ Interview Preparation"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Resume")
        if 'resume_text' not in st.session_state:
            st.session_state['resume_text'] = ""
            
        resume_input_method = st.radio("Resume Input Method", ["Upload File", "Paste Text"], key="resume_method")
        
        if resume_input_method == "Upload File":
            uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith(".pdf"):
                        st.session_state['resume_text'] = utils.extract_text_from_pdf(uploaded_file)
                    elif uploaded_file.name.endswith(".docx"):
                        st.session_state['resume_text'] = utils.extract_text_from_docx(uploaded_file)
                    st.success("✅ Resume uploaded successfully!")
                except Exception as e:
                    st.error(f"Error extracting text: {str(e)}")
        else:
            st.session_state['resume_text'] = st.text_area("Paste your resume text here...", value=st.session_state['resume_text'], height=250)
        
        resume_text = st.session_state['resume_text']
    
    with col2:
        st.subheader("Job Description")
        jd_input_method = st.radio("Input Method", ["Paste Text", "Provide URL"])
        
        if jd_input_method == "Provide URL":
            with st.expander("💡 Scraping Tips", expanded=True):
                st.info("Major job boards (LinkedIn, Indeed) often block automated tools. If fetching fails, please copy-paste the text manually.")

        if 'job_description' not in st.session_state:
            st.session_state['job_description'] = ""

        if jd_input_method == "Paste Text":
            st.session_state['job_description'] = st.text_area("Paste the job description here...", value=st.session_state['job_description'], height=250)
            if 'fetched_jd' in st.session_state:
                del st.session_state['fetched_jd'] # Clear fetched JD if switching to paste
        else:
            jd_url = st.text_input("Job Description URL (LinkedIn, Indeed, etc.)")
            if jd_url:
                if st.button("Fetch Job Description"):
                    with st.spinner("Extracting job details..."):
                        try:
                            st.session_state['job_description'] = utils.extract_text_from_url(jd_url)
                            st.success("✅ Job details extracted successfully!")
                            st.session_state['fetched_jd'] = st.session_state['job_description']
                        except Exception as e:
                            st.error(f"❌ {str(e)}")
                            st.info("If the link is blocked, switch to 'Paste Text' and copy the description manually.")
            
            if 'fetched_jd' in st.session_state:
                st.session_state['job_description'] = st.text_area("Review Extracted Job Description", st.session_state['fetched_jd'], height=200)
            elif not jd_url: # If URL is empty, clear JD
                pass # Keep current state
        
        job_description = st.session_state['job_description']


with tab2:
    st.header("ATS Compatibility Check")
    if resume_text and job_description:
        if st.button("Analyze My Resume", key="analyze_btn"):
            with st.spinner("Auditing your resume against the job description..."):
                try:
                    analysis_result = utils.analyze_ats_score(resume_text, job_description, api_key)
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
                    st.session_state['generated_resume'] = utils.generate_resume_content(resume_text, job_description, api_key)
                    st.session_state['generated_cover_letter'] = utils.generate_cover_letter_content(resume_text, job_description, api_key)
                    st.session_state['interview_questions'] = utils.generate_interview_questions(resume_text, job_description, api_key)
                    st.session_state['career_insights'] = utils.generate_career_insights(resume_text, job_description, api_key)
                    st.session_state['screening_questions'] = utils.generate_screening_questions(resume_text, job_description, api_key)
                    st.session_state['final_interview_questions'] = utils.generate_final_interview_questions(resume_text, job_description, api_key)
                    st.balloons()
                    st.success("Documents & complete interview suite generated successfully!")
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



with tab4:
    st.header("📈 Market Analysis & Career Growth")
    st.markdown("""
        **Unlock your professional potential.** Our AI analyzes industry trends, salary data, and career pathways to give you a strategic advantage.
    """)
    if 'career_insights' in st.session_state:
        st.text_area("Personalized Insights", st.session_state['career_insights'], height=600)
    else:
        st.info("Complete the document generation in the 'Generate Documents' tab to unlock your career insights.")

with tab5:
    st.header("🎯 Interview Preparation Suite")
    st.markdown("""
        **Master your interview.** We've generated a comprehensive set of questions tailored to your resume and this specific job. 
        Use the feedback tool below to practice your answers.
    """)
    
    if 'screening_questions' in st.session_state:
        with st.expander("📋 Initial Recruitment Screening", expanded=True):
            st.info("Recruiter-level questions to verify your core alignment and basics.")
            st.text_area("Screening Questions & Answer Outlines", st.session_state['screening_questions'], height=300)
            
        with st.expander("💡 Technical & Industry Expertise", expanded=False):
            st.info("In-depth questions about your skills and industry-standard practices.")
            st.text_area("Expertise Deep Dive & Answer Outlines", st.session_state['interview_questions'], height=400)

        with st.expander("🏆 Final Round & Cultural Fit", expanded=False):
            st.info("Scenario-based questions for hiring managers.")
            st.text_area("Selection Committee Questions & Answer Outlines", st.session_state['final_interview_questions'], height=300)
            
        st.markdown("---")
        st.subheader("🎤 Mock Interview Practice")
        st.markdown("Paste a question from above and your draft answer to get professional coaching.")
        
        practice_q = st.text_input("Interview Question")
        practice_a = st.text_area("Your Answer", height=150)
        
        if st.button("Get Expert Feedback"):
            if practice_q and practice_a:
                with st.spinner("Analyzing your response..."):
                    try:
                        feedback = utils.provide_interview_feedback(practice_q, practice_a, job_description, api_key)
                        st.markdown("### 📝 Coaching Feedback")
                        st.text(feedback)
                    except Exception as e:
                        st.error(f"Feedback failed: {str(e)}")
            else:
                st.warning("Please provide both a question and your answer.")
    else:
        st.info("Complete the document generation in the 'Generate Documents' tab to unlock your interview prep.")

# SEO Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #A1A1AA; padding: 40px 0;">
        <h4>The Ultimate AI Career Toolkit</h4>
        <p style="font-size: 0.9rem;">
            Designed for modern professionals. Powered by advanced LLMs to beat Applicant Tracking Systems (ATS) and land more interviews. 
            Built for privacy and professional excellence.
        </p>
    </div>
""", unsafe_allow_html=True)
