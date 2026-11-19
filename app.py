
import os
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM


# =====================================================
# 1. ENVIRONMENT CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ.pop("GOOGLE_API_KEY", None)

st.set_page_config(
    page_title="CODEX AI | Multi-Agent Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CUSTOM FRONTEND DESIGN
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080d1b;
    --cyan: #53e0f5;
    --purple: #a78bfa;
    --muted: #9aabc8;
    --line: rgba(130,164,220,.18);
}

html, body, [data-testid="stAppViewContainer"] {
    background:
    radial-gradient(ellipse at 12% 0%, rgba(40,111,180,.22), transparent 38%),
    radial-gradient(ellipse at 90% 8%, rgba(130,75,210,.17), transparent 32%),
    var(--bg);
    color: #edf5ff;
    font-family: Inter, sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#101a30,#0b1222);
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] * {
    color: #e8f1ff;
}

.block-container {
    max-width: 1380px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f4f8ff !important;
}

.brand {
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: .18em;
    color: var(--cyan);
    margin: .2rem 0 1.3rem;
}

.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--line);
    border-radius: 26px;
    padding: 30px;
    background: linear-gradient(115deg,#12233f,#1a193e);
    box-shadow: 0 18px 65px #0005;
    min-height: 270px;
}

.hero:before {
    content: "";
    position: absolute;
    width: 330px;
    height: 330px;
    right: -80px;
    top: -130px;
    border-radius: 50%;
    border: 1px solid #53e0f52e;
    box-shadow: 0 0 0 28px #53e0f509,
                0 0 0 58px #a78bfa09;
    animation: orbit 18s linear infinite;
}

.hero-kicker {
    color: var(--cyan);
    text-transform: uppercase;
    letter-spacing: .2em;
    font-size: .72rem;
    font-weight: 800;
}

.hero-title {
    font-size: clamp(2rem,4vw,3.5rem);
    line-height: 1.05;
    font-weight: 800;
    color: white;
    margin: .55rem 0;
}

.hero-sub {
    color: #b8c7df;
    max-width: 650px;
    line-height: 1.7;
}

.hero-art {
    position: absolute;
    right: 2%;
    top: 8%;
    width: 30%;
    max-width: 300px;
    border-radius: 22px;
    opacity: .92;
    animation: float 5s ease-in-out infinite;
}

.metric, .agent-card {
    background: linear-gradient(145deg,#15223b,#0f182b);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 17px;
    transition: transform .25s,border-color .25s;
}

.metric:hover, .agent-card:hover {
    transform: translateY(-4px);
    border-color: #53e0f58c;
}

.metric-label {
    color: var(--muted);
    font-size: .76rem;
}

.metric-value {
    color: #f4f8ff;
    font-size: 1.65rem;
    font-weight: 800;
    margin-top: 4px;
}

.agent-card {
    min-height: 112px;
    border-radius: 17px;
    padding: 15px;
}

.agent-icon {
    font-size: 1.45rem;
}

.agent-name {
    color: #f4f8ff;
    font-weight: 700;
    margin-top: 7px;
}

.agent-desc {
    color: var(--muted);
    font-size: .74rem;
    margin-top: 3px;
}

.section-label {
    color: var(--cyan);
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .17em;
    text-transform: uppercase;
    margin: 1.1rem 0 .55rem;
}

.stTextArea textarea {
    background: #0c1528 !important;
    color: #edf5ff !important;
    border: 1px solid #78a0dc4d !important;
    border-radius: 14px !important;
}

.stButton button,
.stFormSubmitButton button,
.stDownloadButton button {
    background: linear-gradient(100deg,#0891b2,#6366f1) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    min-height: 46px;
    transition: all .2s;
    box-shadow: 0 7px 24px #0891b230;
}

.stButton button:hover,
.stFormSubmitButton button:hover,
.stDownloadButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px #6366f14d;
}

[data-testid="stExpander"] {
    background: #111a2ed1;
    border: 1px solid var(--line);
    border-radius: 14px;
}

.live-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #34d399;
    margin-right: 8px;
    animation: pulse 1.5s infinite;
}

@keyframes float {
    0%,100% {transform: translateY(0)}
    50% {transform: translateY(-13px)}
}

@keyframes orbit {
    to {transform: rotate(360deg)}
}

@keyframes pulse {
    0%,100% {opacity: .55}
    50% {opacity: 1}
}

@media(max-width:800px) {
    .hero {padding: 23px}
    .hero-art {
        opacity: .22;
        width: 48%;
        right: -5%;
        top: 18%;
    }
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">✦ CODEX AI</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Multi-Agent Studio")
    st.caption("Your AI-powered coding team")

    st.divider()

    st.markdown("**WORKSPACE**")
    st.markdown("🤖 Agent dashboard")
    st.markdown("⌨️ Code generation")
    st.markdown("🔍 Code review")
    st.markdown("🧪 Test planning")

    st.divider()

    st.markdown("**TECH STACK**")
    st.caption("Python · Streamlit · CrewAI · Gemini")

    st.markdown(
        '<div style="padding:12px;border:1px solid #82a4dc30;'
        'border-radius:12px;background:#111a2e">'
        '<span class="live-dot"></span><b>Interface loaded</b>'
        '</div>',
        unsafe_allow_html=True
    )


# =====================================================
# 4. HERO SECTION
# =====================================================

hero_image = (
    "https://images.unsplash.com/photo-1677442136019-21780ecad995"
    "?auto=format&fit=crop&w=700&q=85"
)

st.markdown(f"""
<div class="hero">
    <div class="hero-kicker">
        ✦ Autonomous development workspace
    </div>

    <div class="hero-title">
        Build smarter.<br>
        Ship better code.
    </div>

    <div class="hero-sub">
        Five specialized AI agents collaborate to plan,
        generate, review, debug and prepare tests
        for your Python projects.
    </div>

    <img class="hero-art" src="{hero_image}">
</div>
""", unsafe_allow_html=True)


# =====================================================
# 5. DASHBOARD METRICS
# =====================================================

st.markdown(
    '<div class="section-label">Studio overview</div>',
    unsafe_allow_html=True
)

metrics = st.columns(4)

metric_data = [
    ("05", "SPECIALIST AGENTS"),
    ("01", "SEQUENTIAL WORKFLOW"),
    ("AI", "GEMINI ENGINE"),
    ("MD", "EXPORTABLE REPORT")
]

for col, (value, label) in zip(metrics, metric_data):

    with col:

        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# 6. FIVE AGENT CARDS
# =====================================================

st.markdown(
    '<div class="section-label">Meet your AI team</div>',
    unsafe_allow_html=True
)

agents_ui = [
    ("🧭", "Planner", "Breaks requirements into a plan"),
    ("💻", "Developer", "Builds readable Python code"),
    ("🔎", "Reviewer", "Checks logic and quality"),
    ("🛠️", "Debugger", "Finds bugs and suggests fixes"),
    ("🧪", "Tester", "Creates test cases")
]

cols = st.columns(5)

for col, (emoji, name, description) in zip(cols, agents_ui):

    with col:

        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-icon">{emoji}</div>
                <div class="agent-name">{name}</div>
                <div class="agent-desc">{description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# 7. USER INPUT AND FILE UPLOAD
# =====================================================

st.markdown(
    '<div class="section-label">Start a new analysis</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.45, 1], gap="large")

with left:

    st.subheader("Your coding brief")

    st.caption(
        "Paste a requirement or Python code, "
        "or upload a .py/.txt file."
    )

    with st.form("code_review_form"):

        requirements = st.text_area(
            "1. Paste your requirement or Python code:",
            height=220,
            placeholder=(
                "Example: Create a Python program that accepts "
                "marks in five subjects, calculates total and "
                "average, and displays a grade.\n\n"
                "You can also paste existing Python code here."
            )
        )

        uploaded_file = st.file_uploader(
            "2. Or upload a Python/code file",
            type=["py", "txt"],
            help="Upload a .py or .txt file."
        )

        submitted = st.form_submit_button(
            "🚀 Run AI Analysis",
            use_container_width=True
        )

    if st.button("🧹 Clear input", use_container_width=True):

        st.session_state["requirements_input"] = ""
        st.rerun()


with right:

    st.subheader("Your AI workspace")

    st.image(
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e"
        "?auto=format&fit=crop&w=900&q=80",
        caption="Your AI-powered development team",
        use_container_width=True
    )

    st.caption(
        "Your agents work in sequence. "
        "Their outputs appear below."
    )


# =====================================================
# 8. GEMINI API CONFIGURATION
# =====================================================

if not GEMINI_API_KEY:

    st.error("Gemini API key not found.")

    st.info(
        "Add GEMINI_API_KEY=your_key to the .env file "
        "inside this project folder."
    )

    st.stop()


llm = LLM(
    model="gemini/gemini-3.5-flash-lite",
    api_key=GEMINI_API_KEY,
    temperature=0.2,
    max_tokens=1500,
    timeout=60
)


# =====================================================
# 9. CREATE FIVE AI AGENTS AND TASKS
# =====================================================

def build_crew(user_requirements):

    planner = Agent(
        role="Software Project Planner",
        goal="Analyze requirements and prepare a development plan.",
        backstory="Experienced software planner who breaks tasks into practical steps.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=1
    )

    developer = Agent(
        role="Python Developer",
        goal="Generate complete and readable Python code.",
        backstory="Expert Python developer focused on clear, maintainable code.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=1
    )

    reviewer = Agent(
        role="Code Reviewer",
        goal="Find syntax, logic, security and quality issues.",
        backstory="Careful senior reviewer who explains issues clearly.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=1
    )

    debugger = Agent(
        role="Python Debugger",
        goal="Correct problems and provide final improved code.",
        backstory="Expert debugger who fixes bugs without changing requirements.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=1
    )

    tester = Agent(
        role="Software Tester",
        goal="Prepare test cases and expected results.",
        backstory="QA engineer who designs normal, invalid and edge-case tests.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=1
    )

    # PLANNER TASK

    planning_task = Task(
        description=f"""
        Analyze these requirements:

        {user_requirements}

        Give the objective, main features
        and short development steps.

        Keep under 100 words.
        """,
        expected_output="A concise development plan.",
        agent=planner
    )

    # DEVELOPER TASK

    development_task = Task(
        description="""
        Use the requirements and plan to write
        the complete Python program.

        Include necessary imports, input validation
        and readable variable names.

        Return complete source code in a Python code block.
        """,
        expected_output="Complete Python source code.",
        agent=developer,
        context=[planning_task]
    )

    # REVIEWER TASK

    review_task = Task(
        description="""
        Review the generated code for:

        1. Syntax errors
        2. Logical bugs
        3. Security issues
        4. Code quality

        List issues and improvements concisely.
        """,
        expected_output="A concise code review.",
        agent=reviewer,
        context=[development_task]
    )

    # DEBUGGER TASK

    debugging_task = Task(
        description="""
        Use the generated code and review findings.

        Explain important fixes and provide
        corrected complete code.

        If no corrections are needed, say so clearly.
        """,
        expected_output="Debugging report and corrected code.",
        agent=debugger,
        context=[development_task, review_task]
    )

    # TESTER TASK

    testing_task = Task(
        description="""
        Prepare at least five test cases.

        Include normal, invalid and edge-case inputs
        with expected results.

        Do not claim tests were executed.

        Finish with a short quality summary.
        """,
        expected_output="Test plan with expected results and summary.",
        agent=tester,
        context=[development_task, debugging_task]
    )

    crew = Crew(
        agents=[
            planner,
            developer,
            reviewer,
            debugger,
            tester
        ],
        tasks=[
            planning_task,
            development_task,
            review_task,
            debugging_task,
            testing_task
        ],
        process=Process.sequential,
        verbose=False
    )

    return crew


# =====================================================
# 10. RUN AI WORKFLOW
# =====================================================

if submitted:

    uploaded_text = ""

    if uploaded_file is not None:

        try:

            uploaded_text = uploaded_file.getvalue().decode("utf-8-sig")

        except UnicodeDecodeError:

            st.error(
                "The uploaded file must be UTF-8 encoded."
            )

            st.stop()

    # Combine pasted text and uploaded file

    if requirements.strip() and uploaded_text.strip():

        final_requirements = (
            requirements.strip()
            + "\n\nUploaded file: "
            + uploaded_file.name
            + "\n\nFile contents:\n"
            + uploaded_text
        )

    elif uploaded_text.strip():

        final_requirements = (
            "Please analyze the following uploaded file: "
            + uploaded_file.name
            + "\n\n"
            + uploaded_text
        )

    else:

        final_requirements = requirements.strip()

    if not final_requirements:

        st.warning(
            "Please paste a requirement/code sample "
            "or upload a .py/.txt file first."
        )

        st.stop()

    st.divider()

    st.subheader("⚡ Agent workflow")

    progress = st.progress(
        0,
        text="Preparing your AI team..."
    )

    status = st.empty()

    result = None

    agent_names = [
        "Planner",
        "Developer",
        "Reviewer",
        "Debugger",
        "Tester"
    ]

    # Retry temporary Gemini 503 errors

    for attempt in range(1, 4):

        try:

            crew = build_crew(final_requirements)

            status.info(
                f"Attempt {attempt}/3 — "
                "AI agents are working sequentially."
            )

            with st.spinner(
                "Gemini is processing your workflow..."
            ):

                result = crew.kickoff()

            progress.progress(
                100,
                text="Workflow completed!"
            )

            status.success(
                "All five agents completed their tasks."
            )

            break

        except Exception as exc:

            message = str(exc)
            lower = message.lower()

            temporary = (
                "503" in message
                or "unavailable" in lower
                or "temporarily" in lower
            )

            if temporary and attempt < 3:

                wait_seconds = attempt * 5

                status.warning(
                    f"Gemini returned a temporary 503. "
                    f"Retrying in {wait_seconds} seconds..."
                )

                time.sleep(wait_seconds)

            else:

                progress.empty()

                status.error(
                    "The workflow could not be completed."
                )

                if "429" in message or "resource_exhausted" in lower:

                    st.warning(
                        "Gemini quota or rate limit reached. "
                        "Check your Google AI Studio usage."
                    )

                elif temporary:

                    st.warning(
                        "Gemini is still unavailable. "
                        "Please try again later."
                    )

                elif "404" in message:

                    st.warning(
                        "The selected model may not be available "
                        "to your API key."
                    )

                elif "401" in message or "403" in message:

                    st.warning(
                        "Check your API key and permissions."
                    )

                with st.expander("Technical error details"):

                    st.code(message)

                st.stop()

    # =================================================
    # 11. DISPLAY RESULTS
    # =================================================

    if result is not None:

        st.success(
            "Your AI analysis is ready!"
        )

        outputs = getattr(
            result,
            "tasks_output",
            []
        )

        report = (
            "# CODEX AI — Multi-Agent Code Review Report\n\n"
        )

        if outputs:

            for index, output in enumerate(outputs):

                name = (
                    agent_names[index]
                    if index < len(agent_names)
                    else f"Agent {index + 1}"
                )

                raw = str(
                    getattr(output, "raw", output)
                )

                report += (
                    f"## {name} Agent\n\n"
                    f"{raw}\n\n"
                )

                with st.expander(
                    f"🤖 {name} Agent",
                    expanded=(index == 1)
                ):

                    st.markdown(raw)

        else:

            report += str(result)

            st.markdown(str(result))

        # DOWNLOAD REPORT

        st.divider()

        st.download_button(
            label="📥 Download Complete Report",
            data=report,
            file_name="CODEX_AI_Review_Report.md",
            mime="text/markdown",
            use_container_width=True
        )

        st.caption(
            "The Tester agent prepares test cases. "
            "This application does not execute generated "
            "code or run pytest."
        )


# =====================================================
# 12. FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#8294b4;
        font-size:.8rem;
    ">
        ✦ CODEX AI · Built with Python, Streamlit,
        CrewAI & Google Gemini
    </div>
    """,
    unsafe_allow_html=True
)
