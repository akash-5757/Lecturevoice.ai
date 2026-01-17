import streamlit as st
import assemblyai as aai
import os
import time
from datetime import datetime
from groq import Groq

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Lecture Voice AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== MODERN PREMIUM THEME CSS =====
st.markdown("""
<style>
:root {
    /* Vibrant Professional Color Palette */
    --primary: #6366F1;
    --primary-light: #818CF8;
    --primary-lighter: #E0E7FF;
    --secondary: #EC4899;
    --secondary-light: #F472B6;
    --accent: #06B6D4;
    --accent-light: #22D3EE;
    
    /* Background & Surface */
    --background: #0F172A;
    --surface: #1E293B;
    --surface-light: #334155;
    --surface-hover: #475569;
    
    /* Text Colors */
    --text-primary: #F1F5F9;
    --text-secondary: #CBD5E1;
    --text-muted: #94A3B8;
    
    /* Status Colors */
    --success: #10B981;
    --success-light: #D1FAE5;
    --warning: #F59E0B;
    --warning-light: #FEF3C7;
    --error: #EF4444;
    --error-light: #FEE2E2;
    --info: #3B82F6;
    --info-light: #DBEAFE;
}

html, body, .main {
    background-color: var(--background);
    background-image: linear-gradient(135deg, #0F172A 0%, #1A1F36 100%);
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    border-bottom: 2px solid var(--surface-light);
}

.stTabs [data-baseweb="tab"] {
    padding: 14px 20px;
    background-color: transparent;
    border-radius: 12px 12px 0 0;
    font-weight: 600;
    color: var(--text-muted);
    border-bottom: 3px solid transparent;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stTabs [aria-selected="true"] [data-baseweb="tab"] {
    color: var(--primary);
    border-bottom-color: var(--primary);
    background-color: rgba(99, 102, 241, 0.1);
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary);
    background-color: rgba(99, 102, 241, 0.05);
}

/* Button Styling */
.stButton button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 14px;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stButton button:hover {
    background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.4);
    transform: translateY(-2px);
}

.stButton button:active {
    transform: translateY(0);
}

/* Input Fields */
.stTextInput input,
.stTextArea textarea,
.stSelectbox select,
.stNumberInput input {
    background-color: var(--surface-light) !important;
    border: 2px solid var(--surface-light) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-size: 14px;
    padding: 12px 14px !important;
    transition: all 0.3s ease;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: var(--text-muted) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stSelectbox select:focus,
.stNumberInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
    outline: none !important;
    background-color: var(--surface) !important;
}

/* Transcript Text Area - Smaller Size */
.transcript-area textarea {
    background-color: #0A0E27 !important;
    color: #E0F2FE !important;
    font-size: 14px !important;
    font-family: 'Courier New', monospace !important;
    border: 3px solid #06B6D4 !important;
    border-radius: 10px !important;
    line-height: 1.6 !important;
    padding: 15px !important;
}

.transcript-area textarea:focus {
    border-color: #0EA5E9 !important;
    box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.4) !important;
}

/* Alert Messages */
.stSuccess {
    background-color: rgba(16, 185, 129, 0.15);
    color: #10B981;
    border-left: 4px solid var(--success);
    border-radius: 10px;
    padding: 16px;
    backdrop-filter: blur(10px);
}

.stInfo {
    background-color: rgba(99, 102, 241, 0.15);
    color: #A5B4FC;
    border-left: 4px solid var(--primary);
    border-radius: 10px;
    padding: 16px;
    backdrop-filter: blur(10px);
}

.stError {
    background-color: rgba(239, 68, 68, 0.15);
    color: #FCA5A5;
    border-left: 4px solid var(--error);
    border-radius: 10px;
    padding: 16px;
    backdrop-filter: blur(10px);
}

.stWarning {
    background-color: rgba(245, 158, 11, 0.15);
    color: #FCD34D;
    border-left: 4px solid var(--warning);
    border-radius: 10px;
    padding: 16px;
    backdrop-filter: blur(10px);
}

/* Text Styling */
.stMarkdown p {
    color: var(--text-secondary);
    line-height: 1.7;
    margin-bottom: 1rem;
    font-size: 15px;
}

.stMarkdown {
    color: var(--text-primary);
}

/* Card Container */
.card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.card:hover {
    box-shadow: 0 16px 48px rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-4px);
}

/* File Uploader */
.stFileUploader {
    border-radius: 12px !important;
}

[data-testid="stFileUploadDropzone"] {
    border: 2px dashed var(--primary-light) !important;
    border-radius: 12px !important;
    background-color: rgba(99, 102, 241, 0.05) !important;
}

/* Divider */
.stDivider {
    border-color: var(--surface-light) !important;
}

/* Radio & Checkbox */
[role="radio"], [role="checkbox"] {
    color: var(--primary) !important;
}

/* Text Area */
.stTextArea textarea {
    background-color: var(--surface-light) !important;
    color: var(--text-primary) !important;
}

.stTextArea textarea:focus {
    border-color: var(--primary) !important;
    background-color: var(--surface) !important;
}

/* Scrollable Container */
.stContainer {
    border-radius: 12px;
}

/* Footer Section */
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 12px;
    padding: 24px;
    border-top: 1px solid var(--surface-light);
    margin-top: 40px;
}

.footer strong {
    color: var(--text-secondary);
}

/* Spinner */
.stSpinner > div {
    border-top-color: var(--primary) !important;
}
</style>
""", unsafe_allow_html=True)

# ===== API CONFIGURATION =====
ASSEMBLYAI_API_KEY = "db53042d34f64c23a815538eab44aa86"
GROQ_API_KEY = "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"

# ===== INITIALIZE APIs =====
try:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"❌ API Initialization Error: {str(e)}")

# ===== HELPER FUNCTIONS =====

def transcribe_audio(file_path):
    """Transcribe audio using Assembly AI"""
    try:
        with st.spinner("🔄 Transcribing audio... This may take 1-3 minutes..."):
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file_path)
            return transcript
    except Exception as e:
        st.error(f"❌ Transcription error: {str(e)}")
        return None

def call_groq_api(prompt, max_tokens=1500, retries=3):
    """Call Groq API with retry logic and proper error handling"""
    for attempt in range(retries):
        try:
            # Using llama-3.3-70b-versatile - the new recommended model
            message = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",  # Updated to latest Llama 3.3
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=1
            )
            return message.choices[0].message.content
        
        except Exception as e:
            error_str = str(e).lower()
            
            # Handle rate limiting
            if "rate_limit" in error_str or "429" in error_str:
                if attempt < retries - 1:
                    wait_time = 3 * (attempt + 1)
                    st.warning(f"⏳ API rate limit... waiting {wait_time} seconds (attempt {attempt + 1}/{retries})")
                    time.sleep(wait_time)
                else:
                    st.error("❌ API rate limit exceeded. Please try again in a few moments.")
                    return None
            
            # Handle timeout
            elif "timeout" in error_str or "timed out" in error_str:
                if attempt < retries - 1:
                    wait_time = 3 * (attempt + 1)
                    st.warning(f"⏳ Request timed out... retrying in {wait_time} seconds (attempt {attempt + 1}/{retries})")
                    time.sleep(wait_time)
                else:
                    st.error("❌ Request timed out. Please try again.")
                    return None
            
            # Handle decommissioned model
            elif "decommissioned" in error_str or "no longer supported" in error_str:
                st.error("❌ Model has been deprecated. Using updated model. Please refresh and try again.")
                return None
            
            # Handle authentication errors
            elif "auth" in error_str or "unauthorized" in error_str or "401" in error_str:
                st.error("❌ Authentication failed. Please check your Groq API key.")
                return None
            
            # Handle other errors
            else:
                if attempt < retries - 1:
                    st.warning(f"⚠️ Error occurred, retrying... (attempt {attempt + 1}/{retries})")
                    time.sleep(2)
                else:
                    st.error(f"❌ Error: {str(e)}")
                    return None
    
    return None

def generate_summary_from_transcript(transcript_text):
    """Generate summary using Groq API"""
    try:
        with st.spinner("📝 Generating summary with AI... (< 30 seconds)"):
            prompt = f"""Create a concise, well-structured summary of the following lecture transcript. 
Organize it with clear sections:

1. **Main Topic** - Brief overview
2. **Key Points** - 3-5 essential bullet points
3. **Important Concepts** - Core ideas explained simply
4. **Conclusion** - Summary takeaway

TRANSCRIPT:
{transcript_text[:2500]}

Format with clear markdown headings and bullet points. Be comprehensive but concise."""
            
            response = call_groq_api(prompt, max_tokens=1000)
            if response:
                return response
            else:
                return "⚠️ Failed to generate summary. Please try again."
    
    except Exception as e:
        st.error(f"❌ Error generating summary: {str(e)}")
        return None

def generate_quiz_from_transcript(transcript_text):
    """Generate quiz questions using Groq API"""
    try:
        with st.spinner("❓ Generating quiz questions with AI... (< 30 seconds)"):
            prompt = f"""Based on this lecture transcript, create 5 multiple-choice questions that test understanding of the key concepts.

Format each question exactly like this:

### Question 1: [Question Title]
**[Full question text]**

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

**Correct Answer:** [Letter]
**Explanation:** [Brief explanation]

---

TRANSCRIPT:
{transcript_text[:2500]}

Focus on key concepts and important details from the lecture. Make questions challenging but fair."""
            
            response = call_groq_api(prompt, max_tokens=1500)
            if response:
                return response
            else:
                return "⚠️ Failed to generate quiz. Please try again."
    
    except Exception as e:
        st.error(f"❌ Error generating quiz: {str(e)}")
        return None

def generate_flashcards_from_transcript(transcript_text):
    """Generate flashcards using Groq API"""
    try:
        with st.spinner("🎴 Generating flashcards with AI... (< 30 seconds)"):
            prompt = f"""Create 10 effective study flashcards based on this lecture transcript.

Format each flashcard exactly like this:

**Card 1:**
**Front:** [Question or term]
**Back:** [Answer or definition]

---

TRANSCRIPT:
{transcript_text[:2500]}

Make flashcards concise and suitable for quick memorization. Cover the most important concepts. Each flashcard should focus on a single concept."""
            
            response = call_groq_api(prompt, max_tokens=1500)
            if response:
                return response
            else:
                return "⚠️ Failed to generate flashcards. Please try again."
    
    except Exception as e:
        st.error(f"❌ Error generating flashcards: {str(e)}")
        return None

def ask_question_about_lecture(question, transcript_text):
    """Ask a question about the lecture using Groq API"""
    try:
        prompt = f"""You are an expert professor assistant answering questions about a lecture. 
Answer the student's question based ONLY on the lecture content provided below.
If the question is not related to the lecture, politely redirect them.

LECTURE CONTENT:
{transcript_text[:2000]}

STUDENT QUESTION: {question}

Provide a clear, concise, and educational answer. Be helpful and thorough."""
        
        response = call_groq_api(prompt, max_tokens=500, retries=2)
        if response:
            return response
        else:
            return "⚠️ Failed to generate response. Please try again."
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ===== SESSION STATE =====
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

# ===== MAIN UI =====
st.markdown("# 🎓 Lecture Voice AI")
st.markdown("**Transform lectures into interactive study materials with AI**")
st.markdown("---")

# ===== TABS =====
tab1, tab2, tab3 = st.tabs(["🎤 Transcribe Lecture", "📚 Study Materials", "🤖 Ask Professor"])

# ===== TAB 1: UPLOAD & TRANSCRIBE =====
with tab1:
    st.markdown("## Upload Your Lecture")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📁 Choose an audio or video file",
            type=["mp3", "wav", "m4a", "mp4", "avi", "mov", "flac", "ogg", "webm"],
            help="Supports audio and video files up to 2GB"
        )
    
    if uploaded_file:
        with col2:
            st.info(f"✅ {uploaded_file.name}", icon="📋")
        
        # Save uploaded file temporarily
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Transcribe button
        if st.button("🎤 Start Transcription", use_container_width=True, key="transcribe_btn"):
            transcript_obj = transcribe_audio(temp_file_path)
            if transcript_obj:
                st.session_state.transcript = transcript_obj
                st.session_state.transcript_text = transcript_obj.text
                st.success("✅ Transcription complete!", icon="✨")
                # Clean up temp file
                try:
                    os.remove(temp_file_path)
                except:
                    pass
        
        # Show transcript if available
        if st.session_state.transcript:
            st.markdown("---")
            st.markdown("### 📝 Your Lecture Transcript")
            st.markdown("**🔤 Full text of your lecture:**")
            
            st.markdown('<div class="transcript-area">', unsafe_allow_html=True)
            st.text_area(
                "Transcript:",
                st.session_state.transcript_text,
                height=200,
                disabled=True,
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download transcript
            st.download_button(
                label="💾 Download Transcript (TXT)",
                data=st.session_state.transcript_text,
                file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            st.markdown("### Generate Study Materials")
            st.success("⚡ Powered by Groq AI (Llama 3.3) - Ultra-fast responses (< 30 seconds)", icon="✨")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📝 Summary", use_container_width=True, key="summary_btn"):
                    summary_result = generate_summary_from_transcript(st.session_state.transcript_text)
                    st.session_state.summary = summary_result
                    if summary_result and not summary_result.startswith("⚠️"):
                        st.rerun()
            
            with col2:
                if st.button("❓ Quiz", use_container_width=True, key="quiz_btn"):
                    quiz_result = generate_quiz_from_transcript(st.session_state.transcript_text)
                    st.session_state.quiz = quiz_result
                    if quiz_result and not quiz_result.startswith("⚠️"):
                        st.rerun()
            
            with col3:
                if st.button("🎴 Flashcards", use_container_width=True, key="flash_btn"):
                    flashcards_result = generate_flashcards_from_transcript(st.session_state.transcript_text)
                    st.session_state.flashcards = flashcards_result
                    if flashcards_result and not flashcards_result.startswith("⚠️"):
                        st.rerun()
            
            if st.session_state.summary or st.session_state.quiz or st.session_state.flashcards:
                st.success("✨ Materials ready! Check the Study Materials tab", icon="🎉")
    
    else:
        st.info("👆 Upload an audio or video file to begin transcription", icon="ℹ️")

# ===== TAB 2: STUDY MATERIALS =====
with tab2:
    st.markdown("## Study Materials")
    
    if st.session_state.transcript:
        # Summary Section
        st.markdown("### 📝 Summary")
        
        if st.session_state.summary:
            st.markdown(st.session_state.summary)
            st.download_button(
                "💾 Download Summary",
                st.session_state.summary,
                f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                key="download_summary",
                use_container_width=True
            )
        else:
            st.info("Generate a summary from the Transcribe Lecture tab", icon="📋")
        
        st.markdown("")
        st.divider()
        st.markdown("")
        
        # Quiz Section
        st.markdown("### ❓ Quiz")
        
        if st.session_state.quiz:
            st.markdown(st.session_state.quiz)
            st.download_button(
                "💾 Download Quiz",
                st.session_state.quiz,
                f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                key="download_quiz",
                use_container_width=True
            )
        else:
            st.info("Generate a quiz from the Transcribe Lecture tab", icon="📋")
        
        st.markdown("")
        st.divider()
        st.markdown("")
        
        # Flashcards Section
        st.markdown("### 🎴 Flashcards")
        
        if st.session_state.flashcards:
            st.markdown(st.session_state.flashcards)
            st.download_button(
                "💾 Download Flashcards",
                st.session_state.flashcards,
                f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                key="download_flashcards",
                use_container_width=True
            )
        else:
            st.info("Generate flashcards from the Transcribe Lecture tab", icon="📋")
    
    else:
        st.info("📌 Upload and transcribe a lecture in the Transcribe Lecture tab to view study materials", icon="ℹ️")

# ===== TAB 3: CHATBOT =====
with tab3:
    st.markdown("## Ask Your Professor")
    st.markdown("Ask questions about your lecture and get instant answers")
    
    if not st.session_state.transcript:
        st.info("📌 Upload a lecture in the Transcribe Lecture tab to start asking questions", icon="ℹ️")
    
    else:
        # Chat display
        st.markdown("### 💬 Conversation")
        
        if len(st.session_state.chat_history) > 0:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"**👤 You:** {message['content']}")
                else:
                    st.markdown(f"**🤖 Professor:** {message['content']}")
        else:
            st.markdown("*Your conversation will appear here...*")
        
        st.markdown("")
        
        # Input area
        st.markdown("### Ask a Question")
        
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_question = st.text_input(
                "Type your question:",
                key="chat_input",
                placeholder="e.g., What was the main topic covered?",
                label_visibility="collapsed"
            )
        
        with col2:
            ask_btn = st.button("Send 💬", key="send_btn", use_container_width=True)
        
        if ask_btn and user_question:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })
            
            # Get AI response
            response = ask_question_about_lecture(user_question, st.session_state.transcript_text)
            
            # Add AI response to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
            
            st.rerun()
        
        st.markdown("")
        
        # Clear chat button
        if st.button("Clear Conversation 🗑️", key="clear_btn", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# ===== FOOTER =====
st.markdown("---")

st.markdown("""
<div class="footer">
    <h3 style="color: #A5B4FC; margin-top: 0;">🎓 Lecture Voice AI</h3>
    <p><strong>Powered by Assembly AI (Speech-to-Text) & Groq AI (Ultra-Fast Processing)</strong></p>
    <p style="font-size: 11px; margin-top: 10px; color: #10B981;">✅ 100% FREE - No credit card required - Ultra-fast responses (Llama 3.3)</p>
</div>
""", unsafe_allow_html=True)
