# ATS Resume & Cover Letter Generator 🤖

A Streamlit application that uses LLMs (Google Gemini or OpenAI) to generate ATS-optimized resumes and cover letters based on a job description.

## Features

- **ATS Optimization**: Tailors your resume summary and experience to match job descriptions.
- **Cover Letter Generation**: Creates persuasive cover letters customized for the specific role.
- **Multi-Provider Support**: Choose between Google Gemini (Free tier available) or OpenAI.
- **DOCX Export**: Download your generated documents in editable Word format.
- **Secure Access**: Password-protected login to ensure private usage.

## Setup

1.  **Clone the repository** (or unzip the downloaded file).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You may need to install the Spacy language model separately if it doesn't download automatically:*
    ```bash
    python -m spacy download en_core_web_sm
    ```
3.  **Configure Secrets**:
    Create a `.streamlit/secrets.toml` file with your API keys and app password:
    ```toml
    GEMINI_API_KEY = "your_gemini_api_key"
    password = "your_app_password"
    ```
4.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Usage

1.  Enter your API Key (Google Gemini or OpenAI).
2.  Fill in your profile details (Name, Experience, etc.).
3.  Paste the Job Description you are applying for.
4.  Click **Generate Documents**.
5.  Download your optimized Resume and Cover Letter.

## License

MIT
