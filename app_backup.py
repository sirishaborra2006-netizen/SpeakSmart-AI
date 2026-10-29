import streamlit as st
import whisper
import tempfile
from modules.transcription import transcribe_audio
from modules.analysis import analyze_speech
from modules.charts import create_pie_chart,create_gauge_chart
import matplotlib.pyplot as plt 
from streamlit_mic_recorder import mic_recorder 
import os
from modules.report_generator import generate_pdf
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="SpeakSmart AI",
    page_icon="🎤",
    layout="wide"
)
#css theme

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
[data-testid="stmainBlockContainer"]
{
padding-top:0rem !important;
margin-top:0rem !important;
}
[data-testid="stHeader"] {
background-color: transparent;
height: 0rem;
}
[data-testid="stToolbar"] {
display: none;
}
[data-testid="stSidebar"] {
    background-color: #1E1E2F;
}

h1, h2, h3, p, li {
    color: white !important;
}

.stButton > button {
    background-color: #FF4B4B !important;
    color: white !important;
    border-radius: 10px;
}
.block-container {
max-width: 1200px;
padding-top: 2rem;
padding-bottom:2rem;
}
/* Feature card styling */
.feature-card {
    background: linear-gradient(135deg, #202b5a, #101b3d);
    padding: 22px;
    border-radius: 16px;
    min-height: 145px;
    height: 100%;
    box-sizing: border-box;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 5px 16px rgba(0, 0, 0, 0.18);
}

.feature-card h3 {
    color: white;
    font-size: 21px;
    line-height: 1.35;
    margin-bottom: 12px;
}

.feature-card p {
    color: #e5e7eb;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 0;
}

/* Reduce excess top spacing */
[data-testid="stMainBlockContainer"] {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎤 SpeakSmart AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Speech Analysis",
        "Practice Questions",
        "Reports"
    ]
)
if page!="Speech Analysis":
    st.session_state["show_analysis_charts"] = False

# Home
# Home
if page == "Home":
    st.markdown("""
    <div style="
        width: 100%;
        box-sizing: border-box;
        background: linear-gradient(135deg, #667eea, #4834d4);
        padding: 55px 25px;
        border-radius: 22px;
        color: white;
        text-align: center;
        margin-bottom: 28px;
    ">
        <h1 style="font-size: 42px; margin-bottom: 12px;">
            🎤 SpeakSmart AI
        </h1>
        <h3>Your Personal AI Communication Coach</h3>
        <p style="font-size: 17px;">
            Improve Confidence | Reduce Filler Words | Get AI Feedback
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ✨ Features")
    st.caption("Everything you need to improve your speaking skills.")

    col1, col2, col3 = st.columns(3,gap="large")

    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🎙️ Speech to Text</h3>
        <p>Convert your speech into text for analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>🔎 Filler Word Detection</h3>
        <p>Identify unnecessary filler words.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>📊 Confidence Analysis</h3>
        <p>Review confidence and speaking metrics.</p>
        </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3,gap="large")

    with col4:
        st.markdown("""
        <div class="feature-card">
        <h3>⏱️ WPM Tracking</h3>
        <p>Measure your speaking speed.</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-card">
        <h3>💡 AI Suggestions</h3>
        <p>Get suggestions to improve communication.</p>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="feature-card">
        <h3>📄 PDF Reports</h3>
        <p>Generate a downloadable speech report.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("👈 Select Speech Analysis from the sidebar to get started.")


# =========================
# Speech Analysis Page
# =========================
if page == "Speech Analysis":

    st.title("🎤 Speech Analysis")

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        key="recorder",
        format="wav"
    )

    if audio:
        os.makedirs("uploads",exist_ok=True)
        with open("uploads/recorded_audio.wav", "wb") as f:
            f.write(audio["bytes"])
        st.success("Recording saved successfully!")
       
        transcript = transcribe_audio(
            "uploads/recorded_audio.wav"
        )
        
        results = analyze_speech(transcript)
        st.session_state["results"] = results
        st.session_state["transcript"] = transcript
        st.session_state["show_analysis_charts"] = True

        st.subheader("📄 Transcript")
        st.write(transcript)

        st.subheader("📊 Results")

        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.metric("Total Words", results["total_words"])
        col2.metric("Filler Words", results["filler_count"])
        col3.metric("Confidence", f"{results['confidence_score']}%")
        col4.metric("WPM", results["wpm"])
        col5.metric("Duration", f"{results['speech_duration']} sec")

    uploaded_file = st.file_uploader(
        "Upload Audio File",
        type=["wav", "mp3"]
    )
    if uploaded_file is not None:

     st.success("Audio uploaded successfully!")
     st.audio(uploaded_file)

     with open("uploads/audio_file.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())

     with st.spinner("Analyzing speech..."):

        transcript = transcribe_audio(
            "uploads/audio_file.wav"
        )
        

        results = analyze_speech(
            transcript
        )
        st.session_state["results"]=results
        st.session_state["transcript"]=transcript
        st.session_state["show_analysis_charts"] = True
        st.subheader("📄 Transcript")
        st.write(transcript)

        # Results
        st.subheader("📊 Results")

        col1, col2, col3, col4,col5 = st.columns(5)

        col1.metric("Total Words", results["total_words"])
        col2.metric("Filler Words", results["filler_count"])
        col3.metric("Confidence", f"{results['confidence_score']}%")
        col4.metric("WPM", results["wpm"])
        col5.metric("Duration",f"{results['speech_duration']}sec")

                            # AI Suggestions
        st.subheader("💡 AI Suggestions")

     for suggestion in results["suggestions"]:
       st.write("✅", suggestion)
    if (
    "results" in st.session_state
    and st.session_state.get("show_analysis_charts", False)
):

      results = st.session_state["results"]

      st.markdown(
        "<h2 style='text-align:center;'>📊 Charts</h2>",
        unsafe_allow_html=True
    )

      pie_fig = create_pie_chart(
        results["total_words"],
        results["filler_count"]
    )

      gauge_fig = create_gauge_chart(
        results["confidence_score"]
    )

      col1, col2 = st.columns(2)

      with col1:
        st.pyplot(pie_fig,
        clear_figure=True)
      with col2:
        st.pyplot(gauge_fig,
        clear_figure=True)                  

    else:
        st.info("Record or upload audio to generate charts.")
                            
elif page == "Practice Questions":

        st.title("🎯 Practice Questions")

        category = st.selectbox(
            "Select Category",
            [
                "Self Introduction",
                "Interview",
                "Group Discussion",
                "Public Speaking"
            ],
            key="practice_category"
        )

        difficulty = st.selectbox(
            "Select Difficulty",
            ["Beginner", "Intermediate", "Advanced"],
            key="practice_difficulty"
        )

        questions = {
            "Self Introduction": {
                "Beginner": [
                    "Tell me about yourself.",
                    "What are your hobbies?",
                    "What are your strengths?",
                    "Where are you from?",
                    "What are your career goals?"
                ],
                "Intermediate": [
                    "How has your education prepared you for your career?",
                    "Describe a project you are proud of.",
                    "What makes you different from other candidates?",
                    "How do you handle challenges?",
                    "What skills are you currently improving?"
                ],
                "Advanced": [
                    "How would you present your professional identity in one minute?",
                    "Describe a major setback and what you learned from it.",
                    "How do your long-term goals align with your values?",
                    "What impact do you want to make in your field?",
                    "How would you explain your biggest achievement to a recruiter?"
                ]
            },
            "Interview": {
                "Beginner": [
                    "Why should we hire you?",
                    "What are your strengths and weaknesses?",
                    "Why do you want this job?",
                    "What are your career goals?",
                    "What do you know about our company?"
                ],
                "Intermediate": [
                    "Describe a challenge you solved.",
                    "Tell me about a time you worked in a team.",
                    "How do you handle constructive feedback?",
                    "Describe a mistake and what you learned.",
                    "How do you prioritize multiple tasks?"
                ],
                "Advanced": [
                    "Describe a decision you made with incomplete information.",
                    "How would you handle disagreement with your manager?",
                    "Tell me about a time you influenced a team without authority.",
                    "How would you respond to an unexpected project failure?",
                    "What would you do if a project deadline became impossible to meet?"
                ]
            },
            "Group Discussion": {
                "Beginner": [
                    "Is technology helpful for students?",
                    "Should students participate in sports?",
                    "Is teamwork important?",
                    "Are books better than videos for learning?",
                    "Should college students do internships?"
                ],
                "Intermediate": [
                    "Impact of AI on jobs.",
                    "Should social media have age restrictions?",
                    "Does online education work as well as classroom learning?",
                    "Is remote work better than office work?",
                    "Can technology reduce educational inequality?"
                ],
                "Advanced": [
                    "Can economic growth and environmental protection coexist?",
                    "Should AI-generated content be regulated?",
                    "Does social media strengthen or weaken democracy?",
                    "How should society balance privacy and public safety?",
                    "Will automation increase or reduce economic inequality?"
                ]
            },
            "Public Speaking": {
                "Beginner": [
                    "Importance of time management.",
                    "My role model.",
                    "Why is communication important?",
                    "Benefits of reading books.",
                    "My vision for the future."
                ],
                "Intermediate": [
                    "Role of technology in education.",
                    "Women empowerment.",
                    "How can students manage stress?",
                    "The importance of financial literacy.",
                    "How can young people protect the environment?"
                ],
                "Advanced": [
                    "Can failure be more valuable than success?",
                    "How should leaders build trust during a crisis?",
                    "Does artificial intelligence improve human creativity?",
                    "What responsibilities come with freedom of speech?",
                    "How can society make technological progress more inclusive?"
                ]
            }
        }

        st.subheader(f"📝 {category} Questions")

        selected_questions = questions[category][difficulty]

        for i, question in enumerate(selected_questions, start=1):
            st.write(f"{i}. {question}")

elif page == "Reports":
    st.title("📄 Reports")

    results = st.session_state.get("results")
    transcript = st.session_state.get("transcript", "")

    if results is None:
        st.info("Please analyze a speech first to generate your report.")
    else:
        st.subheader("📋 Speech Analysis Summary")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Words", results.get("total_words", 0))
        col2.metric("Filler Words", results.get("filler_count", 0))
        col3.metric("Confidence", f'{results.get("confidence_score", 0)}%')
        col4.metric("WPM", results.get("wpm", 0))
        duration=results.get("speech_duration", 0)
        col5.metric("Duration", f'{float(duration or 0):.0f}sec')    
        st.subheader("📝 Transcript")
        if transcript:
            st.write(transcript)
        else:
            st.info("Transcript is not available.")

        st.subheader("💡 AI Suggestions")
        for suggestion in results.get("suggestions", []):
            st.write(f"• {suggestion}")

        st.divider()
        st.subheader("📥 Download Your Report")

        from modules.report_generator import generate_pdf

        if st.button("Generate PDF Report", key="reports_page_pdf_button"):
            pdf_file = generate_pdf(results, transcript)

            with open(pdf_file, "rb") as file:
                pdf_data = file.read()

            st.download_button(
                label="Download PDF Report",
                data=pdf_data,
                file_name="SpeakSmart_AI_Report.pdf",
                mime="application/pdf",
                key="reports_page_pdf_download"
            )