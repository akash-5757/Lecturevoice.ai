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

# Premium CSS
st.markdown("""
<style>
:root {
    --primary: #6366F1;
    --primary-light: #818CF8;
    --primary-lighter: #E0E7FF;
    --secondary: #EC4899;
    --accent: #06B6D4;
    --accent-light: #22D3EE;
    --background: #0A0E1F;
    --surface: #1A1F2E;
    --surface-light: #2A2F45;
    --surface-hover: #3A3F55;
    --glass: rgba(255, 255, 255, 0.05);
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --text-muted: #94A3B8;
    --success: #10B981;
    --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main {
    background: linear-gradient(135deg, var(--background) 0%, #1A1F36 50%, #0F172A 100%);
    backdrop-filter: blur(20px);
}

.hero {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
    border-radius: 32px;
    margin: 2rem 0;
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass);
    box-shadow: 0 32px 80px rgba(0, 0, 0, 0.4);
}

.hero h1 {
    font-size: 4.5rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent-light) 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin: 0 0 1rem 0 !important;
    letter-spacing: -0.05em !important;
}

.hero p {
    font-size: 1.5rem !important;
    color: var(--text-secondary) !important;
    max-width: 600px;
    margin: 0 auto !important;
    line-height: 1.6 !important;
}

/* Feature sections */
.feature-section {
    padding: 4rem 2rem;
    text-align: center;
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-radius: 32px;
    margin: 2rem 0;
    border: 1px solid var(--glass);
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(20px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.feature-section:hover {
    transform: translateY(-12px);
    box-shadow: 0 36px 96px rgba(99, 102, 241, 0.3);
    border-color: rgba(99, 102, 241, 0.3);
}

/* Feature title */
.feature-title {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 1.5rem !important;
}

/* Feature subtitle */
.feature-subtitle {
    font-size: 1.3rem !important;
    color: var(--text-muted) !important;
    max-width: 500px;
    margin: 0 auto 3rem auto !important;
}

/* Ultra modern buttons */
.premium-btn {
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent-light) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 24px 48px !important;
    font-weight: 800 !important;
    font-size: 20px !important;
    box-shadow: 0 24px 64px rgba(99, 102, 241, 0.5) !important;
    height: 80px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    position: relative !important;
    overflow: hidden !important;
}

.premium-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.5s;
}

.premium-btn:hover::before {
    left: 100%;
}

.premium-btn:hover {
    background: linear-gradient(135deg, var(--accent-light) 0%, var(--secondary) 100%) !important;
    box-shadow: 0 36px 96px rgba(99, 102, 241, 0.6) !important;
    transform: translateY(-8px) scale(1.05) !important;
}

.premium-btn:active {
    transform: translateY(-4px) scale(1.02) !important;
}

/* Cards and other styles */
.card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-radius: 28px;
    padding: 36px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    border: 1px solid var(--glass);
    margin-bottom: 2.5rem;
    backdrop-filter: blur(20px);
}

.chat-input input {
    background: linear-gradient(135deg, var(--surface-light) 0%, var(--surface-hover) 100%) !important;
    border: 2px solid var(--glass) !important;
    border-radius: 20px !important;
    color: var(--text-primary) !important;
    padding: 20px 24px !important;
    font-size: 16px !important;
    height: 64px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
}

.send-btn button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%) !important;
    padding: 20px 28px !important;
    font-size: 16px !important;
    border-radius: 20px !important;
    height: 64px !important;
    box-shadow: 0 12px 40px rgba(6, 182, 212, 0.4) !important;
    margin-left: 16px !important;
}

.transcript-area textarea {
    background: linear-gradient(135deg, #0A0E27 0%, #1A1F36 100%) !important;
    color: #E0F2FE !important;
    font-family: 'SF Mono', Monaco, monospace !important;
    border: 3px solid rgba(6, 182, 212, 0.5) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    font-size: 15px !important;
    box-shadow: 0 12px 40px rgba(6, 182, 212, 0.2) !important;
}

[data-testid="stFileUploadDropzone"] {
    border: 3px dashed var(--primary-light) !important;
    border-radius: 24px !important;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(6, 182, 212, 0.08) 100%) !important;
    padding: 32px !important;
    backdrop-filter: blur(20px) !important;
}
</style>
""", unsafe_allow_html=True)

# APIs
ASSEMBLYAI_API_KEY = "db53042d34f64c23a815538eab44aa86"
GROQ_API_KEY = "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"

try:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    groq_client = Groq(api_key=GROQ_API_KEY)
except: st.error("API Error")

# Functions (shortened)
def transcribe_audio(file_path):
    try:
        with st.spinner("🔄 Processing..."):
            return aai.Transcriber().transcribe(file_path)
    except: st.error("Transcription failed"); return None

def call_groq(prompt, tokens=1500):
    for _ in range(3):
        try:
            resp = groq_client.chat.completions.create(
                messages=[{"role": "system", "content": "Professional professor."}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile", max_tokens=tokens, temperature=0.7
            )
            return resp.choices[0].message.content
        except: time.sleep(2)
    return None

# Session state
for k in ['transcript','transcript_text','summary','quiz','flashcards','chat_history','materials_ready']:
    if k not in st.session_state: st.session_state[k] = [] if k=='chat_history' else (False if k=='materials_ready' else None)

# HERO HEADER
st.markdown("""
<div class="hero">
    <h1>Lecture Voice AI</h1>
    <p>Transform your lecture recordings into interactive study materials with cutting-edge AI</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🎤 Transcribe Lecture", "📚 Study Materials", "💬 Professor AI"])

# SECTION 1: TRANSCRIBE
with tab1:
    st.markdown('<div class="feature-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="feature-title">Transcribe & Analyze</h2>')
    st.markdown('<p class="feature-subtitle">Upload any audio/video lecture and get instant AI transcription</p>')
    
    col1, col2 = st.columns([3,1])
    with col1:
        uploaded_file = st.file_uploader("📁 Upload Lecture", 
            type=['mp3','wav','m4a','mp4','avi','mov','flac','ogg','webm'])
    
    if uploaded_file:
        with col2: st.success(f"**{uploaded_file.name}**")
        
        tfile = f"temp_{uploaded_file.name}"
        with open(tfile,"wb") as f: f.write(uploaded_file.getbuffer())
        
        st.markdown('<div class="premium-btn">', unsafe_allow_html=True)
        if st.button("🚀 TRANSCRIBE LECTURE", use_container_width=True):
            transcript = transcribe_audio(tfile)
            if transcript:
                st.session_state.transcript = transcript
                st.session_state.transcript_text = transcript.text
                st.rerun()
                try: os.remove(tfile)
                except: pass
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.transcript:
            st.markdown("### 📄 Complete Transcript")
            st.markdown('<div class="transcript-area">', unsafe_allow_html=True)
            st.text_area("", st.session_state.transcript_text, height=280, disabled=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="premium-btn">', unsafe_allow_html=True)
            st.download_button("💾 SAVE TRANSCRIPT", st.session_state.transcript_text, 
                f"lecture_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<h3 style="color: var(--text-secondary);">✨ Generate Study Materials</h3>')
            col1,col2,col3 = st.columns(3)
            with col1:
                st.markdown('<div class="premium-btn">', unsafe_allow_html=True)
                if st.button("📝 CREATE SUMMARY", use_container_width=True, key="sum_btn"):
                    st.session_state.summary = call_groq_api(f"Summarize lecture:\n{st.session_state.transcript_text[:3000]}")
                    st.session_state.materials_ready = True
                    st.success("✅ Check Study Materials tab!")
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="premium-btn">', unsafe_allow_html=True)
                if st.button("❓ GENERATE QUIZ", use_container_width=True, key="quiz_btn"):
                    st.session_state.quiz = call_groq_api(f"5 quiz questions:\n{st.session_state.transcript_text[:3000]}")
                    st.session_state.materials_ready = True
                    st.success("✅ Check Study Materials tab!")
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="premium-btn">', unsafe_allow_html=True)
                if st.button("🎴 MAKE FLASHCARDS", use_container_width=True, key="flash_btn"):
                    st.session_state.flashcards = call_groq_api(f"10 flashcards:\n{st.session_state.transcript_text[:3000]}")
                    st.session_state.materials_ready = True
                    st.success("✅ Check Study Materials tab!")
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# SECTION 2: MATERIALS
with tab2:
    st.markdown('<div class="feature-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="feature-title">📚 Study Materials</h2>')
    st.markdown('<p class="feature-subtitle">Professional study resources generated instantly from your lecture</p>')
    
    if st.session_state.transcript:
        if st.session_state.summary:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📝 AI Summary")
            st.markdown(st.session_state.summary)
            col1,col2=st.columns([4,1])
            with col2:
                st.markdown('<div class="premium-btn">', unsafe_allow_html=True)
                st.download_button("💾 DOWNLOAD", st.session_state.summary, 
                    f"summary_{datetime.now().strftime('%Y%m%d')}.md", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.quiz:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ❓ Practice Quiz")
            st.markdown(st.session_state.quiz)
            col1,col2=st.columns([4,1])
            with col2:
                st.markdown('<div class="premium-btn">', unsafe_allow_html=True)
                st.download_button("💾 DOWNLOAD", st.session_state.quiz, 
                    f"quiz_{datetime.now().strftime('%Y%m%d')}.md", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.flashcards:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🎴 Flashcards")
            st.markdown(st.session_state.flashcards)
            col1,col2=st.columns([4,1])
            with col2:
                st.markdown('<div class="premium-btn">', unsafe_allow_html=True)
                st.download_button("💾 DOWNLOAD", st.session_state.flashcards, 
                    f"flashcards_{datetime.now().strftime('%Y%m%d')}.md", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# SECTION 3: PROFESSOR
with tab3:
    st.markdown('<div class="feature-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="feature-title">💬 AI Professor</h2>')
    st.markdown('<p class="feature-subtitle">Ask questions about your lecture - instant expert answers</p>')
    
    if st.session_state.transcript:
        if st.session_state.chat_history:
            st.markdown("### Recent Conversation")
            for msg in st.session_state.chat_history[-8:]:
                if msg["role"]=="user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**🤖 Professor:** {msg['content']}")
        
        col1,col2 = st.columns([4,1])
        with col1:
            question = st.text_input("Ask anything about the lecture...", key="prof_question")
        with col2:
            if st.button("➤ SEND", key="prof_send"):
                if question:
                    st.session_state.chat_history.append({"role":"user","content":question})
                    st.session_state.chat_history.append({"role":"assistant","content":call_groq(f"Answer professor style: {question}\nLecture: {st.session_state.transcript_text[:2500]}") or "Processing..."})
                    st.rerun()
        
        st.markdown('<div class="premium-btn">', unsafe_allow_html=True)
        if st.button("🗑️ NEW CONVERSATION", use_container_width=True): st.session_state.chat_history=[]
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<footer style='text-align:center; padding:3rem; color:var(--text-muted); border-top:1px solid var(--glass); margin-top:4rem;'>
    <h3 style='color:var(--primary-light); margin:0;'>Lecture Voice AI</h3>
    <p><strong>Powered by AssemblyAI • Groq AI</strong> | Professional Student Project</p>
</footer>
""", unsafe_allow_html=True)
