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

# CSS for styling
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

h1, h2, h3 {
    color: var(--text-primary);
    font-weight: 700;
}

/* Enhanced Tab Styling - Modern Clean */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin-bottom: 0 !important;
    gap: 0 !important;
    display: flex !important;
    border-bottom: 1px solid var(--surface-light);
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    padding: 16px 32px !important;
    border-radius: 16px 16px 0 0 !important;
    margin: 0 !important;
    transition: all 0.3s ease !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    flex: 1 !important;
    text-align: center !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: var(--surface) !important;
    border-bottom-color: var(--primary-light) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: var(--primary) !important;
    background: var(--surface-light) !important;
    border-bottom-color: var(--primary) !important;
}

/* Clean modern buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px 28px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.3s ease !important;
    height: auto !important;
    min-height: 52px !important;
}

.stButton > button:hover {
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.4) !important;
    transform: translateY(-2px) !important;
}

/* Chat input with Enter support */
.stTextInput input {
    background-color: var(--surface-light) !important;
    border: 2px solid var(--surface-light) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 16px 20px !important;
    font-size: 15px !important;
}

.stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
}

/* Full width transcript */
.transcript-area textarea {
    background-color: #0A0E27 !important;
    color: #E0F2FE !important;
    font-family: 'Courier New', monospace !important;
    border: 3px solid #06B6D4 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    font-size: 15px !important;
    height: 300px !important;
}

.card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 2rem;
    transition: all 0.3s ease;
    height: 100%;
}

.card:hover {
    box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
    transform: translateY(-4px);
}

.download-btn > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%) !important;
    padding: 12px 24px !important;
    font-size: 14px !important;
    border-radius: 10px !important;
}

.stSuccess {
    background-color: rgba(16, 185, 129, 0.15);
    color: #10B981;
    border-left: 4px solid var(--success);
    border-radius: 10px;
    padding: 16px;
}

.stInfo {
    background-color: rgba(99, 102, 241, 0.15);
    color: #A5B4FC;
    border-left: 4px solid var(--primary);
    border-radius: 10px;
    padding: 16px;
}

[data-testid="stFileUploadDropzone"] {
    border: 2px dashed var(--primary-light) !important;
    border-radius: 16px !important;
    background-color: rgba(99, 102, 241, 0.05) !important;
    padding: 40px !important;
}
</style>
""", unsafe_allow_html=True)

# API keys - Keep hidden in production
ASSEMBLYAI_API_KEY = "db53042d34f64c23a815538eab44aa86"
GROQ_API_KEY = "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"

# Setup APIs
try:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    groq_client = Groq(api_key=GROQ_API_KEY)
except:
    st.error("API setup failed")

# Core functions (unchanged)
def transcribe_audio(file_path):
    try:
        with st.spinner("🔄 Transcribing your lecture..."):
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file_path)
            return transcript
    except Exception as e:
        st.error(f"Transcription failed: {str(e)}")
        return None

def call_groq_api(prompt, max_tokens=1500):
    for attempt in range(3):
        try:
            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a clear, professional professor explaining things simply for students."},
                    {"role": "user", "content": prompt}
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
    result = call_groq_api(prompt, 1000)
    return result if result else "Summary generation failed."

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
    result = call_groq_api(prompt, 1500)
    return result if result else "Quiz generation failed."

def generate_flashcards(transcript_text):
    prompt = f"""Create 10 flashcards from this lecture.

**Card 1:**
**Front:** [question/term]
**Back:** [answer]

---

TRANSCRIPT:
{transcript_text[:2500]}"""
    result = call_groq_api(prompt, 1500)
    return result if result else "Flashcards generation failed."

def ask_professor(question, transcript_text):
    prompt = f"""Answer this student question as a professor.
Use the lecture if possible. If not, explain clearly anyway.

LECTURE:
{transcript_text[:2000]}

QUESTION: {question}"""
    result = call_groq_api(prompt, 500)
    return result if result else "Response failed."

# Session state
if 'transcript' not in st.session_state:
    st.session_state.update({
        'transcript': None,
        'transcript_text': None,
        'summary': None,
        'quiz': None,
        'flashcards': None,
        'chat_history': [],
        'question': ''
    })

# Title Section
col_title1, col_title2 = st.columns([2, 1])
with col_title1:
    st.markdown("# 🎓 Lecture Voice AI")
with col_title2:
    st.markdown("**Convert lectures to study materials instantly**")

st.divider()

# Three-column main layout
col1, col2, col3 = st.columns(3)

# Left Column - Transcribe
with col1:
    st.markdown("### 🎙️ Upload & Transcribe")
    
    uploaded_file = st.file_uploader(
        "Choose audio/video file",
        type=["mp3", "wav", "m4a", "mp4", "avi", "mov", "flac", "ogg", "webm"],
        help="Supports most common audio/video formats"
    )
    
    if uploaded_file:
        st.info(f"📁 **{uploaded_file.name}** selected")
        
        temp_file = f"temp_{uploaded_file.name}"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("🚀 **Start Transcription**", use_container_width=True):
            transcript = transcribe_audio(temp_file)
            if transcript:
                st.session_state.transcript = transcript
                st.session_state.transcript_text = transcript.text
                st.success("✅ **Transcription Complete!**")
                try:
                    os.remove(temp_file)
                except:
                    pass
    
    if st.session_state.transcript:
        st.markdown("### 📄 Full Transcript")
        st.markdown('<div class="transcript-area">', unsafe_allow_html=True)
        st.text_area(
            "",
            st.session_state.transcript_text,
            height=350,
            disabled=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.download_button(
            "💾 Download Transcript",
            st.session_state.transcript_text,
            f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "text/plain",
            use_container_width=True
        )

# Middle Column - Generate Materials (One-click)
with col2:
    st.markdown("### ⚡ Generate Study Materials")
    
    if st.session_state.transcript:
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("📝 **Summary**", use_container_width=True):
                st.session_state.summary = generate_summary(st.session_state.transcript_text)
                st.success("✅ Summary ready!")
        
        with col_b:
            if st.button("❓ **Quiz**", use_container_width=True):
                st.session_state.quiz = generate_quiz(st.session_state.transcript_text)
                st.success("✅ Quiz ready!")
        
        col_c, col_d = st.columns(2)
        
        with col_c:
            if st.button("🎴 **Flashcards**", use_container_width=True):
                st.session_state.flashcards = generate_flashcards(st.session_state.transcript_text)
                st.success("✅ Flashcards ready!")
        
        st.markdown("---")
        st.markdown("**📥 Download your materials below 👇**")
    else:
        st.info("👆 **Upload & transcribe first**")

# Right Column - Study Materials Display
with col3:
    st.markdown("### 📚 Your Study Materials")
    
    if st.session_state.summary:
        with st.container(height=250):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### 📝 **Lecture Summary**")
            st.markdown(st.session_state.summary)
            st.download_button(
                "💾 Download",
                st.session_state.summary,
                f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True,
                type="secondary"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.quiz:
        with st.container(height=250):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### ❓ **Quiz Questions**")
            st.markdown(st.session_state.quiz)
            st.download_button(
                "💾 Download",
                st.session_state.quiz,
                f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True,
                type="secondary"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.flashcards:
        with st.container(height=250):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### 🎴 **Flashcards**")
            st.markdown(st.session_state.flashcards)
            st.download_button(
                "💾 Download",
                st.session_state.flashcards,
                f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True,
                type="secondary"
            )
            st.markdown('</div>', unsafe_allow_html=True)

# Chat Section - Bottom Full Width
st.markdown("---")
st.markdown("## 💬 Ask Professor Anything")

if not st.session_state.transcript:
    st.warning("👆 **Transcribe a lecture first** to ask context-aware questions")
else:
    # Chat History
    if st.session_state.chat_history:
        st.markdown("### 📜 Conversation")
        for msg in st.session_state.chat_history[-6:]:  # Show last 6 messages
            if msg["role"] == "user":
                st.markdown(f"**👤 You:** {msg['content']}")
            else:
                st.markdown(f"**👨‍🏫 Professor:** {msg['content']}")
    
    # Chat Input with Enter support
    st.markdown("### 💭 Your Question")
    question_col1, question_col2 = st.columns([1, 0.15])
    
    with question_col1:
        question = st.text_input(
            "",
            placeholder="What was the main topic? Press Enter to send...",
            value=st.session_state.question,
            key="chat_input",
            on_change=lambda: None  # Handled by session state
        )
    
    with question_col2:
        if st.button("➤", key="send_button", use_container_width=True):
            if question.strip():
                st.session_state.chat_history.append({"role": "user", "content": question})
                with st.spinner("Professor is thinking..."):
                    answer = ask_professor(question, st.session_state.transcript_text)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.session_state.question = ""
                st.rerun()
    
    # Handle Enter key press
    if st.session_state.question != question:
        st.session_state.question = question
        if question.strip() and st.button("➤", key="send_enter", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Professor is thinking..."):
                answer = ask_professor(question, st.session_state.transcript_text)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.session_state.question = ""
            st.rerun()

if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94A3B8; padding: 32px; border-top: 1px solid #334155;'>
    <h3 style='color: #A5B4FC; margin: 0;'>Lecture Voice AI</h3>
    <p><strong>Powered by AssemblyAI + Groq AI</strong> | Made for students</p>
</div>
""", unsafe_allow_html=True)
