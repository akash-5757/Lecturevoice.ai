import streamlit as st
import assemblyai as aai
import os
import time
from datetime import datetime
from groq import Groq

st.set_page_config(
    page_title="Lecture Voice AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern professional design
st.markdown("""
<style>
:root {
    --primary: #4F46E5;
    --primary-light: #7C3AED;
    --primary-gradient: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
    --secondary: #EC4899;
    --accent: #06B6D4;
    --accent-light: #22D3EE;
    --background: #0F0F23;
    --surface: #1A1A2E;
    --surface-light: #2D2D44;
    --surface-hover: #3A3A5A;
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --text-accent: #A5B4FC;
    --success: #10B981;
    --error: #EF4444;
    --glass: rgba(255, 255, 255, 0.05);
}

.main {
    background: linear-gradient(135deg, #0F0F23 0%, #1A1A2E 50%, #16213E 100%);
}

/* Hero Header - Center Aligned & Professional */
.hero-header {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
    border-radius: 32px;
    margin: 2rem 0;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.hero-title {
    font-size: 4.5rem !important;
    font-weight: 800 !important;
    background: var(--primary-gradient) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 1.5rem !important;
    line-height: 1.1 !important;
    letter-spacing: -0.02em !important;
}

.hero-subtitle {
    font-size: 1.6rem !important;
    color: var(--text-secondary) !important;
    font-weight: 400 !important;
    max-width: 800px;
    margin: 0 auto !important;
    line-height: 1.6 !important;
}

/* Feature Cards - Full Width Canvas Division */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
    margin: 4rem 0;
}

.feature-card {
    background: linear-gradient(145deg, var(--surface), var(--surface-light));
    border-radius: 28px;
    padding: 3.5rem 2.5rem;
    text-align: center;
    height: 300px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(16px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--primary-gradient);
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

.feature-card:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 32px 80px rgba(79, 70, 229, 0.3);
    border-color: rgba(79, 70, 229, 0.3);
}

.feature-card:hover::before {
    transform: scaleX(1);
}

.feature-icon {
    font-size: 4rem !important;
    margin-bottom: 1.5rem !important;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.feature-title {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin-bottom: 1rem !important;
}

.feature-desc {
    color: var(--text-secondary) !important;
    font-size: 1.1rem !important;
    line-height: 1.6 !important;
    margin-bottom: 2rem;
}

/* Ultra Modern Buttons */
.hero-btn, .feature-btn {
    background: var(--primary-gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 20px 48px !important;
    font-weight: 700 !important;
    font-size: 1.2rem !important;
    box-shadow: 0 20px 40px rgba(79, 70, 229, 0.4) !important;
    height: 68px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    position: relative;
    overflow: hidden;
}

.hero-btn:hover, .feature-btn:hover {
    box-shadow: 0 28px 60px rgba(79, 70, 229, 0.5) !important;
    transform: translateY(-6px) scale(1.05) !important;
}

.hero-btn:active, .feature-btn:active {
    transform: translateY(-2px) !important;
}

/* Clean Professional Footer */
.pro-footer {
    text-align: center;
    padding: 3rem 2rem;
    margin-top: 6rem;
    color: var(--text-secondary);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(26, 26, 46, 0.8);
    backdrop-filter: blur(20px);
    border-radius: 24px 24px 0 0;
}

.pro-footer h3 {
    color: var(--text-accent) !important;
    font-size: 1.8rem !important;
    margin-bottom: 0.5rem !important;
}

/* Rest of your existing styles... */
.modern-btn button, .generate-btn button, .download-btn button, .send-btn button {
    border-radius: 16px !important;
}

.card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
""", unsafe_allow_html=True)

# API keys (unchanged)
ASSEMBLYAI_API_KEY = "db53042d34f64c23a815538eab44aa86"
GROQ_API_KEY = "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"

# Setup APIs (unchanged)
try:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    groq_client = Groq(api_key=GROQ_API_KEY)
except:
    st.error("API setup failed")

# All your existing functions remain the same...
def transcribe_audio(file_path):
    try:
        with st.spinner("Transcribing..."):
            transcriber = aai.Transcriber()
            return transcriber.transcribe(file_path)
    except Exception as e:
        st.error(f"Transcription failed: {str(e)}")
        return None

def call_groq_api(prompt, max_tokens=1500):
    for i in range(3):
        try:
            response = groq_client.chat.completions.create(
                messages=[{"role": "system", "content": "Clear professor explaining simply."}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except:
            if i < 2: time.sleep(2)
    return None

def generate_summary(transcript_text):
    prompt = f"Summarize: {transcript_text[:2500]}"
    return call_groq_api(prompt, 1000) or "Failed"

def generate_quiz(transcript_text):
    prompt = f"5 quiz questions: {transcript_text[:2500]}"
    return call_groq_api(prompt, 1500) or "Failed"

def generate_flashcards(transcript_text):
    prompt = f"10 flashcards: {transcript_text[:2500]}"
    return call_groq_api(prompt, 1500) or "Failed"

def ask_professor(question, transcript_text):
    prompt = f"Answer: {question}\\nLecture: {transcript_text[:2000]}"
    return call_groq_api(prompt, 500) or "Failed"

# Session state (unchanged)
for key in ['transcript', 'transcript_text', 'summary', 'quiz', 'flashcards', 'chat_history', 'materials_ready']:
    if key not in st.session_state:
        st.session_state[key] = None if key != 'chat_history' and key != 'materials_ready' else []
        if key == 'materials_ready': st.session_state[key] = False

# NEW HERO HEADER - Center Aligned & Professional
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">Lecture Voice AI</h1>
    <p class="hero-subtitle">Transform lectures into interactive study materials with cutting-edge AI</p>
    <div style="margin-top: 2.5rem;">
        <button class="hero-btn" onclick="window.location.href='#transcribe'">🚀 Start Transcribing</button>
    </div>
</div>
""", unsafe_allow_html=True)

# NEW FEATURE SECTIONS - Canvas Dividing Cards
st.markdown('<div class="feature-grid">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card" id="transcribe">
        <div class="feature-icon">📤</div>
        <h3 class="feature-title">Transcribe Lectures</h3>
        <p class="feature-desc">Upload audio/video files and get instant, accurate transcripts</p>
        <button class="feature-btn">Start Now →</button>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card" id="materials">
        <div class="feature-icon">📚</div>
        <h3 class="feature-title">Generate Materials</h3>
        <p class="feature-desc">Auto-create summaries, quizzes, and flashcards instantly</p>
        <button class="feature-btn">View Materials →</button>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card" id="professor">
        <div class="feature-icon">💬</div>
        <h3 class="feature-title">Ask Professor</h3>
        <p class="feature-desc">Interactive AI professor answers all your lecture questions</p>
        <button class="feature-btn">Chat Now →</button>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# Your existing tabs content (keep exactly the same)
tab1, tab2, tab3 = st.tabs(["📤 Transcribe", "📚 Materials", "💬 Professor"])

# ... [Keep ALL your existing tab1, tab2, tab3 content exactly the same] ...

# NEW CLEAN FOOTER
st.markdown("""
<div class="pro-footer">
    <h3>Powered by</h3>
    <p><strong>AssemblyAI</strong> + <strong>Groq AI</strong></p>
</div>
""", unsafe_allow_html=True)
