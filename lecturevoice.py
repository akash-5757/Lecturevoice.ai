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

.stButton button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
    transition: all 0.3s ease;
}

.stButton button:hover {
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.4);
    transform: translateY(-2px);
}

.stTextInput input, .stTextArea textarea {
    background-color: var(--surface-light) !important;
    border: 2px solid var(--surface-light) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    padding: 12px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
}

.transcript-area textarea {
    background-color: #0A0E27 !important;
    color: #E0F2FE !important;
    font-family: 'Courier New', monospace !important;
    border: 3px solid #06B6D4 !important;
    border-radius: 10px !important;
    padding: 15px !important;
}

.card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 1.5rem;
}

.card:hover {
    box-shadow: 0 16px 48px rgba(99, 102, 241, 0.25);
    border-color: rgba(99, 102, 241, 0.4);
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

# Transcribe function
def transcribe_audio(file_path):
    try:
        with st.spinner("Transcribing audio..."):
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file_path)
            return transcript
    except Exception as e:
        st.error(f"Transcription failed: {str(e)}")
        return None

# Call Groq API
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

# Generate summary
def generate_summary(transcript_text):
    prompt = f"""Summarize this lecture transcript clearly:

1. Main Topic
2. Key Points (3-5 bullets)
3. Important Concepts  
4. Conclusion

TRANSCRIPT:
{transcript_text[:2500]}"""
    
    with st.spinner("Creating summary..."):
        result = call_groq_api(prompt, 1000)
        return result if result else "Summary failed. Try again."

# Generate quiz
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
    
    with st.spinner("Creating quiz..."):
        result = call_groq_api(prompt, 1500)
        return result if result else "Quiz failed. Try again."

# Generate flashcards
def generate_flashcards(transcript_text):
    prompt = f"""Create 10 flashcards from this lecture.

**Card 1:**
**Front:** [question/term]
**Back:** [answer]

---

TRANSCRIPT:
{transcript_text[:2500]}"""
    
    with st.spinner("Creating flashcards..."):
        result = call_groq_api(prompt, 1500)
        return result if result else "Flashcards failed. Try again."

# Ask professor
def ask_professor(question, transcript_text):
    prompt = f"""Answer this student question as a professor.

Use the lecture if possible. If not, explain clearly anyway.

LECTURE:
{transcript_text[:2000]}

QUESTION: {question}"""
    
    result = call_groq_api(prompt, 500)
    return result if result else "Response failed. Try again."

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

# Title
st.markdown("# Lecture Voice AI")
st.markdown("Convert lectures to transcripts and study materials")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["Transcribe Lecture", "Study Materials", "Ask Professor"])

# Tab 1 - Upload and transcribe
with tab1:
    st.markdown("## Upload lecture")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose audio/video file",
            type=["mp3", "wav", "m4a", "mp4", "avi", "mov", "flac", "ogg", "webm"]
        )
    
    if uploaded_file:
        with col2:
            st.info(f"Selected: {uploaded_file.name}")
        
        temp_file = f"temp_{uploaded_file.name}"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Start transcription", use_container_width=True):
            transcript = transcribe_audio(temp_file)
            if transcript:
                st.session_state.transcript = transcript
                st.session_state.transcript_text = transcript.text
                st.success("Transcription done!")
                try:
                    os.remove(temp_file)
                except:
                    pass
        
        if st.session_state.transcript:
            st.markdown("### Transcript")
            
            st.markdown('<div class="transcript-area">', unsafe_allow_html=True)
            st.text_area(
                "",
                st.session_state.transcript_text,
                height=220,
                disabled=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.download_button(
                "Download transcript",
                st.session_state.transcript_text,
                f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True
            )
            
            st.markdown("### Create materials")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Summary", use_container_width=True):
                    result = generate_summary(st.session_state.transcript_text)
                    st.session_state.summary = result
                    if "failed" not in result.lower():
                        st.success("Summary ready - check Study Materials tab")
                        st.rerun()
            
            with col2:
                if st.button("Quiz", use_container_width=True):
                    result = generate_quiz(st.session_state.transcript_text)
                    st.session_state.quiz = result
                    if "failed" not in result.lower():
                        st.success("Quiz ready - check Study Materials tab")
                        st.rerun()
            
            with col3:
                if st.button("Flashcards", use_container_width=True):
                    result = generate_flashcards(st.session_state.transcript_text)
                    st.session_state.flashcards = result
                    if "failed" not in result.lower():
                        st.success("Flashcards ready - check Study Materials tab")
                        st.rerun()
    
    else:
        st.info("Upload a file to start")

# Tab 2 - Study materials
with tab2:
    st.markdown("## Study materials")
    
    if st.session_state.transcript:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Summary")
        if st.session_state.summary:
            st.markdown(st.session_state.summary)
            st.download_button(
                "Download",
                st.session_state.summary,
                f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True
            )
        else:
            st.info("Create summary in Transcribe tab")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Quiz")
        if st.session_state.quiz:
            st.markdown(st.session_state.quiz)
            st.download_button(
                "Download",
                st.session_state.quiz,
                f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True
            )
        else:
            st.info("Create quiz in Transcribe tab")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Flashcards")
        if st.session_state.flashcards:
            st.markdown(st.session_state.flashcards)
            st.download_button(
                "Download",
                st.session_state.flashcards,
                f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True
            )
        else:
            st.info("Create flashcards in Transcribe tab")
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("Transcribe a lecture first")

# Tab 3 - Ask professor
with tab3:
    st.markdown("## Ask professor")
    st.markdown("Ask about the lecture or related topics")
    
    if not st.session_state.transcript:
        st.info("Transcribe a lecture first")
    else:
        if st.session_state.chat_history:
            st.markdown("### Chat")
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**Professor:** {msg['content']}")
        else:
            st.markdown("No messages yet")
        
        st.markdown("### Your question")
        
        with st.form("chat_form"):
            question = st.text_input("", placeholder="What was the main topic?")
            send = st.form_submit_button("Send")
        
        if send and question:
            st.session_state.chat_history.append({"role": "user", "content": question})
            answer = ask_professor(question, st.session_state.transcript_text)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()
        
        if st.button("Clear chat"):
            st.session_state.chat_history = []
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94A3B8; padding: 24px; border-top: 1px solid #334155;'>
    <h3 style='color: #A5B4FC; margin-top: 0;'>Lecture Voice AI</h3>
    <p><strong>Made with AssemblyAI + Groq</strong></p>
</div>
""", unsafe_allow_html=True)
