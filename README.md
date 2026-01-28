# Lecture Voice AI

Lecture Voice AI is a web application that transcribes lecture audio into text and generates structured study materials such as summaries, quizzes, and flashcards using advanced AI models.

## Problem Statement

Students often miss key points during lectures because it is difficult to listen and take notes simultaneously. This project automates note-taking by converting speech into text and summarizing the material into concise learning resources using AI.

---

## Features

### Speech-to-Text Transcription

The application uses **AssemblyAI** to convert uploaded audio or video lecture files into accurate, time-stamped transcripts. It supports multiple formats including MP3, WAV, M4A, MP4, and more. Transcripts are displayed in a dedicated viewer with syntax highlighting for easy reading.

### Intelligent Lecture Summaries

After transcription, Groq's **Llama 3.3 model** analyzes the lecture content and generates a structured summary highlighting the main topic, 3-5 key points, important concepts, and a conclusion. This helps students quickly grasp the core lecture material.

### Multiple-Choice Quiz Generation

The AI automatically creates **five multiple-choice quiz questions** based on the lecture content. Each question includes four answer options, the correct answer, and a brief explanation. This feature enables active recall and self-testing.

### Flashcard Creator

Generates **exactly ten flashcards** from the lecture transcript, formatted with a question on the first line and answer on the second. Flashcards focus on key definitions, concepts, and relationships, perfect for spaced repetition study sessions.

### Ask Professor AI Chatbot

Students can ask questions about the lecture content through a conversational interface. The chatbot uses the full transcript as context to provide accurate, professor-like explanations and clarifications on any topic from the lecture.

### Downloadable Study Materials

All generated content—transcripts, summaries, quizzes, and flashcards—can be downloaded as timestamped text files. This allows offline study and integration with other note-taking systems.

### Modern Streamlit Interface

Built with **Streamlit** and enhanced with custom CSS, the app features a dark gradient theme, responsive layout, and intuitive tabbed interface (Transcribe, Study Materials, Ask Professor) optimized for student workflows.

---

## Tech Stack

| Component            | Technology              |
|----------------------|-------------------------|
| Programming Language | Python                  |
| Framework            | Streamlit               |
| Speech-to-Text API   | AssemblyAI              |
| Generative AI API    | Groq (Llama 3.3 model)  |
| Styling              | Custom CSS              |
| File Handling        | Python I/O              |

---

## Project Structure


Lecture-Voice-AI/
│
├── app.py                  # Main Streamlit application file
├── requirements.txt        # Dependencies
└── README.md               # Documentation

Installation and Setup
1. Clone the repository
bash
git clone https://github.com/<your-username>/Lecture-Voice-AI.git
cd Lecture-Voice-AI
2. Create a virtual environment
bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Set up API keys
Create a .env file in the project root and add:

text
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
GROQ_API_KEY=your_groq_api_key
You can alternatively assign the keys directly in the script for quick testing, but environment variables are recommended for security.

5. Run the application
bash
streamlit run app.py
Then open the provided local URL (usually http://localhost:8501) in your browser.

How It Works
Upload a lecture file in audio or video format such as .mp3, .wav, .m4a, or .mp4.

The application transcribes the uploaded file using AssemblyAI via its Python SDK.

After transcription completes, you can generate a summary, quiz, or flashcards using the connected LLM through Groq.

You can review and download transcripts and study materials from the Study Materials tab.

The Ask Professor tab lets you ask questions based on the lecture for clarification.

Example Use Case
If you upload a lecture on "Machine Learning Fundamentals," the app can produce a complete transcript, a concise summary of key topics, a short quiz with multiple-choice questions, ten flashcards with core concepts, and explanatory answers to follow-up questions through the Ask Professor feature.

Environment Variables
Variable	Description
ASSEMBLYAI_API_KEY	Required for transcription functionality
GROQ_API_KEY	Required for summary, quiz, and flashcard generation
Future Improvements
Integration with academic schedule systems for automatic lecture handling.

Real-time live transcription for ongoing lectures.

Multi-language support for non-English lectures.

Enhanced analytics on lecture content and study progress.

Author
Developer: Akash G
Role: AI/ML Developer Intern
Organization: SNS College of Technology, ECE Department

Built using Streamlit, AssemblyAI, and Groq.


