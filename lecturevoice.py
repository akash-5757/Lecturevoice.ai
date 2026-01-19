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

# Enhanced CSS for bigger tabs and professional chatbot
st.markdown("""
<style>
:root {
    --primary: #6366F1;
    --primary-light: #818CF8;
    --primary-lighter: #E0E7FF;
    --secondary: #EC4899;
    --accent: #06B6D4;
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

/* Bigger tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    height: 60px !important;
    padding: 0 32px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    border-radius: 20px 20px 0 0 !important;
    margin: 0 4px !important;
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%) !important;
    border: 2px solid transparent !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: linear-gradient(135deg, var(--primary-lighter) 0%, var(--primary-light) 100%) !important;
    border-color: var(--primary) !important;
    color: var(--primary) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4) !important;
}

h1, h2, h3 {
    color: var(--text-primary);
    font-weight: 700;
}

.stButton button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 16px 32px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.3s ease !important;
    height: auto !important;
    min-height: 56px !important;
}

.stButton button:hover {
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.4) !important;
    transform: translateY(-3px) !important;
}

/* Extra large buttons for main actions */
.large-btn button {
    padding: 24px 40px !important;
    font-size: 18px !important;
    border-radius: 20px !important;
    box-shadow: 0 20px 48px rgba(99, 102, 241, 0.4) !important;
    min-height: 72px !important;
}

.large-btn button:hover {
    box-shadow: 0 28px 64px rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-4px) !important;
}

.stTextInput input, .stTextArea textarea {
    background-color: var(--surface-light) !important;
    border: 2px solid var(--surface-light) !important;
    border-radius: 16px !important;
    color: var(--text-primary) !important;
    padding: 16px 20px !important;
    font-size: 16px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
}

/* Enhanced transcript area */
.transcript-area {
    background: linear-gradient(135deg, #0A0E27 0%, #1A1F36 100%) !important;
    border: 3px solid var(--accent) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    box-shadow: 0 20px 60px rgba(6, 182, 212, 0.2) !important;
}

.card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-radius: 24px;
    padding: 36px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 2.5rem;
    transition: all 0.4s ease;
}

.card:hover {
    box-shadow: 0 32px 80px rgba(99, 102, 241, 0.3);
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-6px);
}

.download-btn button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%) !important;
    padding: 16px 28px !important;
    font-size: 15px !important;
    border-radius: 16px !important;
    box-shadow: 0 12px 32px rgba(6, 182, 212, 0.3) !important;
    min-height: 56px !important;
}

.download-btn button:hover {
    box-shadow: 0 20px 48px rgba(6, 182, 212, 0.4) !important;
    transform: translateY(-3px) !important;
}

/* Professional Chatbot UI */
.chat-container {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-radius: 24px;
    padding: 32px;
    height: 700px;
    overflow-y: auto;
    border: 2px solid rgba(99, 102, 241, 0.2);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
}

.message {
    margin-bottom: 24px;
    padding: 20px 24px;
    border-radius: 20px;
    max-width: 85%;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 8px;
}

.professor-message {
    background: linear-gradient(135deg, var(--accent) 0%, #0891b2 100%);
    color: white;
    border-bottom-left-radius: 8px;
    box-shadow: 0 8px 24px rgba(6, 182, 212, 0.3);
}

.chat-input-container {
    background: var(--surface);
    padding: 24px;
    border-radius: 24px;
    border: 2px solid rgba(99, 102, 241, 0.2);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.chat-input {
    background: var(--surface-light) !important;
    border: 2px solid var(--surface-light) !important;
    border-radius: 20px !important;
    color: var(--text-primary) !important;
    padding: 20px 24px !important;
    font-size: 16px !important;
    height: 64px !important;
}

.professor-avatar {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

.professor-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--accent), #0891b2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: bold;
    color: white;
}

.stSuccess, .stInfo {
    border-radius: 16px !important;
    padding: 20px !important;
    border-left-width: 6px !important;
}

[data-testid="stFileUploadDropzone"] {
    border: 3px dashed var(--primary-light) !important;
    border-radius: 20px !important;
    background-color: rgba(99, 102, 241, 0.08) !important;
    padding: 48px 32px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--primary) !important;
    background-color: rgba(99, 102, 241, 0.12) !important;
}

/* Scrollbar styling */
.chat-container::-webkit-scrollbar {
    width: 8px;
}
.chat-container::-webkit-scrollbar-track {
    background: var(--surface-light);
    border-radius: 10px;
}
.chat-container::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 10px;
}
.chat-container::-webkit-scrollbar-thumb:hover {
    background: var(--primary-light);
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

# [Keep all your existing functions unchanged - transcribe_audio, call_groq_api, generate_summary, etc.]
def transcribe_audio(file_path):
    try:
        with st.spinner("🔄 Transcribing your lecture audio..."):
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file_path)
            return transcript
    except Exception as e:
        st.error(f"❌ Transcription failed: {str(e)}")
        return None

def call_groq_api(prompt, max_tokens=1500):
    for attempt in range(3):
        try:
            response = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a clear, professional professor explaining things simply for students."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            return None
    return None

def generate_summary(transcript_text):
    prompt = f"""Summarize this lecture transcript clearly:

1. Main Topic
2. Key Points (3-5 bullets)
3. Important Concepts  
4. Conclusion

TRANSCRIPT:
{transcript_text[:2500]}"""
    
    with st.spinner("✍️ Creating detailed summary..."):
        result = call_groq_api(prompt, 1000)
        return result if result else "Summary generation failed. Please try again."

def generate_quiz(transcript_text):
    prompt = f"""Create 5 multiple choice quiz questions from this lecture.

Format each like:
### Question 1: [Title]
[Question text]

A) [option]
B) [option] 
C) [option]
D) [option]

**Answer:** [letter]
**Explanation:** [brief]

---

TRANSCRIPT:
{transcript_text[:2500]}"""
    
    with st.spinner("📝 Generating quiz questions..."):
        result = call_groq_api(prompt, 1500)
        return result if result else "Quiz generation failed. Please try again."

def generate_flashcards(transcript_text):
    prompt = f"""Create 10 flashcards from this lecture.

**Card 1:**
**Front:** [question/term]
**Back:** [answer]

---

TRANSCRIPT:
{transcript_text[:2500]}"""
    
    with st.spinner("🎴 Creating flashcards..."):
        result = call_groq_api(prompt, 1500)
        return result if result else "Flashcards generation failed. Please try again."

def ask_professor(question, transcript_text):
    prompt = f"""Answer this student question as a professor.

Use the lecture if possible. If not, explain clearly anyway.

LECTURE:
{transcript_text[:2000]}

QUESTION: {question}"""
    
    result = call_groq_api(prompt, 500)
    return result if result else "Professor response failed. Please try again."

# Session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'transcript_text' not in st.session_state:
    st.session_state.transcript_text = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'quiz' not in st.session_state:
    st.session_state.quiz = None
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'materials_ready' not in st.session_state:
    st.session_state.materials_ready = False

# Title
st.markdown("# 🎓 Lecture Voice AI")
st.markdown("**Transform lectures into transcripts and interactive study materials**")
st.markdown("---")

# Bigger Tabs with enhanced spacing
tab1, tab2, tab3 = st.tabs(["📺 **Transcribe Lecture**", "📚 **Study Materials**", "💬 **Ask Professor**"])

# Tab 1 - Upload and transcribe (Enhanced layout)
with tab1:
    st.markdown("### 🚀 Upload & Process Your Lecture")
    
    col1, col2 = st.columns([3, 1], gap="2rem")
    
    with col1:
        uploaded_file = st.file_uploader(
            "🎤 Choose your lecture audio/video file",
            type=["mp3", "wav", "m4a", "mp4", "avi", "mov", "flac", "ogg", "webm"],
            help="Supports most common audio/video formats"
        )
    
    if uploaded_file:
        with col2:
            st.success(f"✅ **{uploaded_file.name}**")
            st.info(f"📏 Size: {uploaded_file.size / (1024*1024):.1f} MB")
        
        temp_file = f"temp_{uploaded_file.name}"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        col_btn1, col_btn2 = st.columns([1,1], gap="1rem")
        with col_btn1:
            if st.button("🎙️ **Start Transcription**", use_container_width=True, key="transcribe"):
                transcript = transcribe_audio(temp_file)
                if transcript:
                    st.session_state.transcript = transcript
                    st.session_state.transcript_text = transcript.text
                    st.success("🎉 **Transcription completed successfully!**")
                    try:
                        os.remove(temp_file)
                    except:
                        pass
        
        if st.session_state.transcript:
            st.markdown("---")
            st.markdown("### 📄 **Full Lecture Transcript**")
            
            st.markdown('<div class="transcript-area">', unsafe_allow_html=True)
            st.text_area(
                "",
                st.session_state.transcript_text,
                height=350,
                disabled=True,
                key="transcript_view"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### ✨ **Generate Study Materials**")
            
            col1, col2, col3 = st.columns(3, gap="1.5rem")
            
            with col1:
                st.markdown('<div class="large-btn">', unsafe_allow_html=True)
                if st.button("📝 **Summary**", use_container_width=True, key="summary_gen"):
                    result = generate_summary(st.session_state.transcript_text)
                    st.session_state.summary = result
                    st.session_state.materials_ready = True
                    st.balloons()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="large-btn">', unsafe_allow_html=True)
                if st.button("❓ **Quiz**", use_container_width=True, key="quiz_gen"):
                    result = generate_quiz(st.session_state.transcript_text)
                    st.session_state.quiz = result
                    st.session_state.materials_ready = True
                    st.balloons()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="large-btn">', unsafe_allow_html=True)
                if st.button("🎴 **Flashcards**", use_container_width=True, key="flash_gen"):
                    result = generate_flashcards(st.session_state.transcript_text)
                    st.session_state.flashcards = result
                    st.session_state.materials_ready = True
                    st.balloons()
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    "💾 **Download Transcript**",
                    st.session_state.transcript_text,
                    f"lecture_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    "text/plain",
                    use_container_width=True,
                    type="primary"
                )
    
    else:
        st.info("👆 **Upload a lecture file to get started**")

# Tab 2 - Study materials (Enhanced cards)
with tab2:
    st.markdown("### 📚 **Your Generated Study Materials**")
    
    if st.session_state.transcript:
        if st.session_state.summary:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📝 **Lecture Summary**")
            st.markdown(st.session_state.summary)
            col1, col2 = st.columns([3, 1])
            with col2:
                st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                st.download_button(
                    "💾 Download",
                    st.session_state.summary,
                    f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    "text/plain",
                    use_container_width=True,
                    key="dl_summary"
                )
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.quiz:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ❓ **Interactive Quiz**")
            st.markdown(st.session_state.quiz)
            col1, col2 = st.columns([3, 1])
            with col2:
                st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                st.download_button(
                    "💾 Download", 
                    st.session_state.quiz,
                    f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    "text/plain",
                    use_container_width=True,
                    key="dl_quiz"
                )
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.flashcards:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🎴 **Flashcards**")
            st.markdown(st.session_state.flashcards)
            col1, col2 = st.columns([3, 1])
            with col2:
                st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                st.download_button(
                    "💾 Download",
                    st.session_state.flashcards,
                    f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    "text/plain",
                    use_container_width=True,
                    key="dl_flash"
                )
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if not st.session_state.summary and not st.session_state.quiz and not st.session_state.flashcards:
            st.info("✨ **Generate materials from the Transcribe tab first**")
    else:
        st.info("📺 **Transcribe a lecture first to unlock study materials**")

# Tab 3 - Professional Chatbot UI
with tab3:
    st.markdown("### 💬 **Ask Professor Anything**")
    st.markdown("*Ask about the lecture content or any related topic*")
    
    if not st.session_state.transcript:
        st.warning("📺 **Please transcribe a lecture first** to enable professor mode")
    else:
        # Professional Chat Container
        st.markdown('<div class="chat-container" id="chat-messages">', unsafe_allow_html=True)
        
        if st.session_state.chat_history:
            for i, msg in enumerate(st.session_state.chat_history):
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="message user-message">
                        <strong>👤 You</strong>
                        <div style="margin-top: 8px; white-space: pre-wrap;">{msg['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="professor-avatar">
                        <div class="professor-icon">👨‍🏫</div>
                        <strong>Professor</strong>
                    </div>
                    <div class="message professor-message">
                        <div style="white-space: pre-wrap;">{msg['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; color: var(--text-muted); padding: 60px 20px;">
                <div style="font-size: 48px; margin-bottom: 24px;">💬</div>
                <h3>Ask your professor anything!</h3>
                <p style="max-width: 400px; margin: 0 auto;">
                    Ask about lecture concepts, request explanations, 
                    or get help with difficult topics.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Chat Input
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        col_input, col_send = st.columns([4, 1], gap="1rem")
        
        with col_input:
            question = st.text_input(
                "",
                placeholder="💭 What would you like to ask about the lecture?",
                label_visibility="collapsed",
                key="chat_input",
                help="Press Enter or click Send"
            )
        
        with col_send:
            send = st.button("📤 Send", use_container_width=True, type="primary")
        
        if send and question.strip():
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("🤔 Professor is thinking..."):
                answer = ask_professor(question, st.session_state.transcript_text)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear Chat Button
        if st.session_state.chat_history:
            if st.button("🗑️ **Clear Chat History**", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94A3B8; padding: 32px; border-top: 2px solid #334155; margin-top: 4rem; border-radius: 24px; background: rgba(30, 41, 59, 0.5);'>
    <h3 style='color: #A5B4FC; margin: 0 0 12px 0;'>🎓 Lecture Voice AI</h3>
    <p style='margin: 0 0 8px 0; font-size: 16px;'><strong>Powered by AssemblyAI + Groq AI</strong></p>
    <p style='margin: 0; font-size: 14px; opacity: 0.8;'>Transforming lectures into interactive learning experiences</p>
</div>
""", unsafe_allow_html=True)
