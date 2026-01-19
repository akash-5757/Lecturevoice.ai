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

# CSS for modern styling
st.markdown("""
<style>
:root {
    --primary: #6366F1;
    --primary-light: #818CF8;
    --primary-lighter: #E0E7FF;
    --secondary: #EC4899;
    --accent: #06B6D4;
    --accent-light: #22D3EE;
    --background: #0F172A;
    --surface: #1E293B;
    --surface-light: #334155;
    --surface-hover: #475569;
    --text-primary: #F1F5F9;
    --text-secondary: #CBD5E1;
    --text-muted: #94A3B8;
    --success: #10B981;
    --error: #EF4444;
}

.main {
    background: linear-gradient(135deg, #0F172A 0%, #1A1F36 100%);
}

h1, h2, h3 {
    color: var(--text-primary);
    font-weight: 700;
}

/* Modern large buttons */
.modern-btn button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 18px 36px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.4) !important;
    border: 2px solid transparent !important;
    height: 64px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.modern-btn button:hover {
    background: linear-gradient(135deg, var(--primary-light) 0%, var(--accent-light) 100%) !important;
    box-shadow: 0 20px 48px rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-4px) scale(1.02) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

.modern-btn button:active {
    transform: translateY(-2px) scale(1.0) !important;
}

/* Generate buttons - even larger */
.generate-btn button {
    padding: 22px 44px !important;
    font-size: 18px !important;
    height: 72px !important;
    border-radius: 20px !important;
    box-shadow: 0 16px 40px rgba(99, 102, 241, 0.5) !important;
}

.generate-btn button:hover {
    box-shadow: 0 24px 60px rgba(99, 102, 241, 0.6) !important;
    transform: translateY(-6px) scale(1.03) !important;
}

/* Download buttons */
.download-btn button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%) !important;
    padding: 14px 28px !important;
    font-size: 15px !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 28px rgba(6, 182, 212, 0.4) !important;
}

.download-btn button:hover {
    box-shadow: 0 16px 40px rgba(6, 182, 212, 0.5) !important;
    transform: translateY(-3px) scale(1.02) !important;
}

/* Chat input styling */
.chat-input input {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%) !important;
    border: 2px solid var(--surface-hover) !important;
    border-radius: 14px !important;
    color: var(--text-primary) !important;
    padding: 16px 20px !important;
    font-size: 15px !important;
    height: 56px !important;
}

.chat-input input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
}

/* Send button for chat */
.send-btn button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%) !important;
    padding: 16px 24px !important;
    font-size: 15px !important;
    border-radius: 14px !important;
    height: 56px !important;
    box-shadow: 0 10px 28px rgba(6, 182, 212, 0.4) !important;
    margin-left: 12px !important;
}

.send-btn button:hover {
    box-shadow: 0 16px 40px rgba(6, 182, 212, 0.5) !important;
    transform: translateY(-3px) !important;
}

.stTextInput input, .stTextArea textarea {
    background-color: var(--surface-light) !important;
    border: 2px solid var(--surface-light) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    padding: 12px !important;
}

.transcript-area textarea {
    background-color: #0A0E27 !important;
    color: #E0F2FE !important;
    font-family: 'Courier New', monospace !important;
    border: 3px solid #06B6D4 !important;
    border-radius: 12px !important;
    padding: 18px !important;
    font-size: 14px !important;
}

.card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 2.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
    box-shadow: 0 24px 72px rgba(99, 102, 241, 0.3);
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-6px);
}

.stSuccess, .stInfo {
    border-radius: 12px !important;
    padding: 18px !important;
    backdrop-filter: blur(12px) !important;
}

[data-testid="stFileUploadDropzone"] {
    border: 3px dashed var(--primary-light) !important;
    border-radius: 16px !important;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(6, 182, 212, 0.05) 100%) !important;
    padding: 24px !important;
}
</style>
""", unsafe_allow_html=True)

# API keys
ASSEMBLYAI_API_KEY = "db53042d34f64c23a815538eab44aa86"
GROQ_API_KEY = "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"

# Setup APIs
try:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    groq_client = Groq(api_key=GROQ_API_KEY)
except:
    st.error("API setup failed")

# All functions (same as before but shorter)
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
    prompt = f"Answer: {question}\nLecture: {transcript_text[:2000]}"
    return call_groq_api(prompt, 500) or "Failed"

# Session state
for key in ['transcript', 'transcript_text', 'summary', 'quiz', 'flashcards', 'chat_history', 'materials_ready']:
    if key not in st.session_state:
        st.session_state[key] = None if key != 'chat_history' and key != 'materials_ready' else []
        if key == 'materials_ready': st.session_state[key] = False

# Title
st.markdown("# 🎓 Lecture Voice AI")
st.markdown("**Modern AI for lecture processing**")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["📤 Transcribe", "📚 Materials", "💬 Professor"])

with tab1:
    st.markdown("### Upload & Process")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload audio/video", 
            type=["mp3", "wav", "m4a", "mp4", "avi", "mov"])
    
    if uploaded_file:
        with col2: st.info(f"**{uploaded_file.name}**")
        
        tfile = f"temp_{uploaded_file.name}"
        with open(tfile, "wb") as f: f.write(uploaded_file.getbuffer())
        
        st.markdown('<div class="modern-btn">', unsafe_allow_html=True)
        if st.button("🚀 START TRANSCRIPTION", use_container_width=True, key="transcribe_btn"):
            transcript = transcribe_audio(tfile)
            if transcript:
                st.session_state.transcript = transcript
                st.session_state.transcript_text = transcript.text
                st.success("✅ Done!")
                try: os.remove(tfile)
                except: pass
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.transcript:
            st.markdown("### 📄 Full Transcript")
            st.markdown('<div class="transcript-area">', unsafe_allow_html=True)
            st.text_area("", st.session_state.transcript_text, height=240, disabled=True, key="transcript_area")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.download_button("💾 Download TXT", st.session_state.transcript_text, 
                f"transcript_{datetime.now().strftime('%Y%m%d')}.txt", use_container_width=True)
            
            st.markdown("### ✨ Generate Study Materials")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
                if st.button("📝 SUMMARY", use_container_width=True, key="gen_summary"):
                    st.session_state.summary = generate_summary(st.session_state.transcript_text)
                    st.session_state.materials_ready = True
                    st.success("✅ Summary ready!")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
                if st.button("❓ QUIZ", use_container_width=True, key="gen_quiz"):
                    st.session_state.quiz = generate_quiz(st.session_state.transcript_text)
                    st.session_state.materials_ready = True
                    st.success("✅ Quiz ready!")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
                if st.button("🎴 FLASHCARDS", use_container_width=True, key="gen_flash"):
                    st.session_state.flashcards = generate_flashcards(st.session_state.transcript_text)
                    st.session_state.materials_ready = True
                    st.success("✅ Flashcards ready!")
                st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 📚 Your Study Materials")
    
    if st.session_state.transcript:
        if st.session_state.summary:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### 📝 Lecture Summary")
            st.markdown(st.session_state.summary)
            col1, col2 = st.columns([4, 1])
            with col2:
                st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                st.download_button("💾 Download", st.session_state.summary, 
                    f"summary_{datetime.now().strftime('%Y%m%d')}.txt", 
                    use_container_width=True, key="dl_summary")
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.quiz:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### ❓ Practice Quiz")
            st.markdown(st.session_state.quiz)
            col1, col2 = st.columns([4, 1])
            with col2:
                st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                st.download_button("💾 Download", st.session_state.quiz, 
                    f"quiz_{datetime.now().strftime('%Y%m%d')}.txt", 
                    use_container_width=True, key="dl_quiz")
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.flashcards:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### 🎴 Flashcards")
            st.markdown(st.session_state.flashcards)
            col1, col2 = st.columns([4, 1])
            with col2:
                st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                st.download_button("💾 Download", st.session_state.flashcards, 
                    f"flashcards_{datetime.now().strftime('%Y%m%d')}.txt", 
                    use_container_width=True, key="dl_flash")
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 💬 Ask Professor")
    
    if st.session_state.transcript:
        if st.session_state.chat_history:
            st.markdown("#### Chat")
            for msg in st.session_state.chat_history[-10:]:  # Last 10 messages
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**🤖 Professor:** {msg['content']}")
        
        st.markdown("#### Send message")
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown('<div class="chat-input">', unsafe_allow_html=True)
            question = st.text_input("", placeholder="Ask about lecture or concepts...", key="chat_question", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="send-btn">', unsafe_allow_html=True)
            if st.button("Send ➤", key="send_chat"):
                if question:
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    answer = ask_professor(question, st.session_state.transcript_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="modern-btn">', unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Transcribe first")

# Footer
st.markdown("""
<div style='text-align:center; padding:32px; color:#94A3B8; border-top:1px solid #334155; margin-top:4rem;'>
    <h3 style='color:#A5B4FC; margin:0;'>Lecture Voice AI</h3>
    <p><strong>AssemblyAI + Groq AI</strong> | Student Project 2026</p>
</div>
""", unsafe_allow_html=True)
