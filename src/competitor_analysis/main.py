#!/usr/bin/env python
import sys
import warnings
import streamlit as st
import os
import time
from datetime import datetime
from competitor_analysis.crew import CompetitorAnalysis
try:
    from competitor_analysis.crew import CompetitorAnalysis
    CREW_AVAILABLE = True
except ImportError:
    CREW_AVAILABLE = False
    st.error("⚠️ CrewAI module not found. Please install the required dependencies.")

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'competitor_name_or_url': competitor_input
    }
    
    try:
        CompetitorAnalysis().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'competitor_name_or_url': competitor_input
    }
    try:
        CompetitorAnalysis().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CompetitorAnalysis().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'competitor_name_or_url': competitor_input
    }
    
    try:
        CompetitorAnalysis().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


# ========== STREAMLIT UI SECTION ==========


# Page configuration
st.set_page_config(
    page_title="Competitor Intelligence Agent",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
    }
    
    .analysis-container {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #90caf9;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 0.5rem 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔍 Competitive Intelligence with CrewAI</h1>', unsafe_allow_html=True)

# Subtitle/Description
st.markdown("""
<div class="subtitle">
This app uses AI agents to analyze your competitors' websites and provide insights.<br>
Enter a competitor's name or URL, and let the agents do the work!
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Main input section
st.markdown("### 📝 Enter Competitor Information")

# Input field
competitor_input = st.text_input(
    "Enter Competitor Name or URL",
    placeholder="e.g., nike.com or Adidas",
    help="You can enter either a company name or a website URL"
)

# Optional: Model selection
with st.expander("⚙️ Advanced Settings (Optional)"):
    model_choice = st.selectbox(
        "Select AI Model",
        ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
        index=0,
        help="Choose the AI model for analysis"
    )
    
    show_agent_details = st.checkbox(
        "Show detailed agent reasoning",
        value=False,
        help="Display step-by-step agent thoughts and actions"
    )

# Action button
if st.button("Run Competitive Analysis 🚀", type="primary"):
    if not competitor_input.strip():
        st.error("⚠️ Please enter a competitor name or URL before running the analysis.")
    elif not CREW_AVAILABLE:
        st.error("⚠️ CrewAI is not properly configured. Please check your installation.")
    else:
        # Validate API key
        if not os.getenv('OPENAI_API_KEY'):
            st.error("⚠️ OpenAI API key not found. Please set your OPENAI_API_KEY environment variable.")
        else:
            try:
                # Show loading spinner
                with st.spinner("🤖 AI agents are analyzing your competitor... This may take a few minutes."):
                    # Initialize the crew
                    crew_instance = CompetitorAnalysis()
                    
                    # Prepare inputs
                    inputs = {"competitor_name_or_url": competitor_input.strip()}
                    
                    # Run the analysis
                    start_time = time.time()
                    results = crew_instance.crew().kickoff(inputs=inputs)
                    end_time = time.time()
                    
                    # Store results
                    st.session_state.analysis_results = results
                    
                    # Add to history
                    st.session_state.analysis_history.append({
                        'competitor': competitor_input.strip(),
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'duration': f"{end_time - start_time:.2f}s",
                        'results': results
                    })
                
                # Success message
                st.markdown("""
                <div class="success-message">
                    ✅ <strong>Analysis Complete!</strong> The AI agents have successfully analyzed your competitor.
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ <strong>Analysis Failed:</strong> {str(e)}<br>
                    Please check your inputs and try again.
                </div>
                """, unsafe_allow_html=True)

# Results section
if st.session_state.analysis_results:
    st.markdown("### 📊 Analysis Results")
    
    # Display results in a nice container
    st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
    
    # Check if results is a string or structured data
    if isinstance(st.session_state.analysis_results, str):
        st.markdown("**Competitive Intelligence Report:**")
        st.markdown(st.session_state.analysis_results)
    else:
        # Handle structured data (if CrewAI returns JSON/dict)
        try:
            if hasattr(st.session_state.analysis_results, 'raw'):
                st.markdown("**Competitive Intelligence Report:**")
                st.markdown(st.session_state.analysis_results.raw)
            else:
                st.markdown("**Competitive Intelligence Report:**")
                st.write(st.session_state.analysis_results)
        except:
            st.markdown("**Raw Analysis Results:**")
            st.code(str(st.session_state.analysis_results), language="text")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download button for results
    if st.button("📥 Download Analysis Report"):
        results_text = str(st.session_state.analysis_results)
        st.download_button(
            label="Download as Text File",
            data=results_text,
            file_name=f"competitive_analysis_{competitor_input.replace(' ', '_')}.txt",
            mime="text/plain"
        )

# Analysis history sidebar
if st.session_state.analysis_history:
    with st.sidebar:
        st.markdown("### 📈 Analysis History")
        for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):  # Show last 5
            with st.expander(f"🏢 {analysis['competitor'][:20]}..."):
                st.write(f"**Time:** {analysis['timestamp']}")
                st.write(f"**Duration:** {analysis['duration']}")
                if st.button(f"View Results", key=f"view_{i}"):
                    st.session_state.analysis_results = analysis['results']
                    st.rerun()

# Info box
st.markdown("""
<div class="info-box">
    <strong>💡 Tips for Better Analysis:</strong><br>
    • Use specific company names (e.g., "Tesla" instead of "car company")<br>
    • Include full URLs with https:// for website analysis<br>
    • The analysis may take 2-5 minutes depending on the complexity<br>
    • Results include market position, strengths, weaknesses, and opportunities
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "Powered by CrewAI and OpenAI | Built with Streamlit 🚀"
    "</div>", 
    unsafe_allow_html=True
)