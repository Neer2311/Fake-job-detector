import streamlit as st
import pickle
import re
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy.sparse import hstack
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="🔍 Job Authenticity Checker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)
hide = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide, unsafe_allow_html=True)

# Custom CSS 
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.2);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .analysis-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e3e8ee;
        margin: 1.5rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .analysis-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.12);
    }
    
    .result-legitimate {
        background: linear-gradient(135deg, #00b894, #00a085);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 184, 148, 0.3);
        animation: slideInUp 0.5s ease;
    }
    
    .result-fake {
        background: linear-gradient(135deg, #e17055, #d63031);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(214, 48, 49, 0.3);
        animation: slideInUp 0.5s ease;
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        margin: 1rem 0;
        border-top: 4px solid #0984e3;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
    }
    
    .sidebar-card {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(116, 185, 255, 0.3);
    }
    
    .info-box {
        background: #e8f4fd;
        border: 1px solid #74b9ff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #0984e3;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #ff6b6b;
    }
    
    .success-box {
        background: #d1edff;
        border: 1px solid #74b9ff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #00b894;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #feca57);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    .footer {
        background: linear-gradient(135deg, #2d3436, #636e72);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin: 3rem 0 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        position: relative;
        z-index: 1;
        display: block !important;
        visibility: visible !important;
    }
    
    .footer h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    .footer p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
        line-height: 1.5;
        color: #ffffff;
    }
    
    .contact-form {
        background: rgba(255, 255, 255, 0.15);
        padding: 1.2rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .contact-form input[type=text], 
    .contact-form input[type=email], 
    .contact-form textarea {
        width: 100%;
        padding: 10px;
        border: 1px solid rgba(102, 126, 234, 0.5);
        border-radius: 6px;
        margin: 6px 0 12px 0;
        background: rgba(255, 255, 255, 0.9);
        font-size: 14px;
    }
    .contact-form textarea {
        min-height: 100px;
    }
    .contact-form button[type=submit] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        width: 100%;
        font-weight: bold;
        margin-top: 8px;
        transition: all 0.3s ease;
    }
    .contact-form button[type=submit]:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

#  NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# cleaning function 
def clean(text):
    text = text.lower()
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s₹$@]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return ' '.join(words)

# risk score function
def risk_score(text):
    text = text.lower()
    score = 0
    if "telegram" in text or "whatsapp" in text: 
        score += 1
    if "₹" in text and any(kw in text for kw in ["per day", "per week", "guaranteed", "earn"]): 
        score += 1
    if "no interview" in text or "no experience" in text: 
        score += 1
    if "visa" in text and "processing fee" in text: 
        score += 1
    return score

# Load models
@st.cache_resource
def load_models():
    try:
        with open('lrmodel.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        try:
            with open('job_scam_model.pkl', 'rb') as f:
                model = pickle.load(f)
            with open('tfidf_vectorizer.pkl', 'rb') as f:
                vectorizer = pickle.load(f)
            return model, vectorizer
        except FileNotFoundError:
            st.error("🚨 Model files not found! Please ensure model.pkl and vectorizer.pkl are in the same directory.")
            return None, None

model, vectorizer = load_models()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-card">
        <h3>🎯 Analysis Center</h3>
        <p>Choose your analysis method and get instant results</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analysis method selection
    analysis_method = st.selectbox(
        "📊 Select Analysis Method",
        ["Direct Text Analysis", "URL Scraping Analysis"],
        index=0
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div class="info-box">
    <h4>💡 Detection Tips</h4>
    <ul style="margin: 0.5rem 0;">
        <li>🚩 Watch for vague descriptions</li>
        <li>💰 Be wary of unrealistic salaries</li>
        <li>⚡ Avoid "urgent hiring" posts</li>
        <li>📧 Check company email domains</li>
        <li>🏢 Verify company addresses</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Contact form section
    st.header("📬 Contact Us")
    st.markdown("""
    <div style="margin-bottom: 0.5rem;">
        Have questions or feedback?<br>
        We'd love to hear from you!
    </div>
    """, unsafe_allow_html=True)
    
    contact_form = """
    <div class="contact-form">
        <form action="https://formsubmit.co/neerajchandel9.nc@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here"></textarea>
            <button type="submit">Send Message</button>
        </form>
    </div>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🔍 Job Authenticity Checker</h1>
    <p>Advanced protection against fraudulent job postings</p>
</div>
""", unsafe_allow_html=True)

# Check if models are loaded
if model is None or vectorizer is None:
    st.stop()

# Main content based on analysis method
if analysis_method == "Direct Text Analysis":
    
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="analysis-card">
            <h2>📝 Job Description Analysis</h2>
            <p>Paste the complete job posting below for advanced authenticity analysis</p>
        </div>
        """, unsafe_allow_html=True)
        

        job_text = st.text_area(
            "Job Description",
            height=350,
            placeholder="""📋 Paste the complete job posting here...

Include:
• Job title and description
• Company information
• Salary details
• Requirements and qualifications
• Contact information
• Application instructions

The more complete the posting, the more accurate the analysis will be.""",
            key="job_text_input",label_visibility="collapsed"
        )
        
        # Analysis button
        analyze_btn = st.button("🚀 Analyze Job Posting", type="primary", use_container_width=True)
        
        if analyze_btn and job_text.strip():
            with st.spinner("🤖 Analyzing the job posting... Please wait"):
                time.sleep(1)  
                
                cleaned_text = clean(job_text)
                
                text_vectorized = vectorizer.transform([cleaned_text])
                
                risk = np.array([[risk_score(job_text)]])
                
                final_input = hstack([text_vectorized, risk])
                
                prediction = model.predict(final_input)[0]
                confidence = model.predict_proba(final_input)[0]
                
                if prediction == 1:  # Fake
                    conf_score = confidence[1] * 100
                    prediction_text = "FAKE JOB DETECTED"
                    result_class = "result-fake"
                    emoji = "🚨"
                    advice = "⚠️ This job posting shows strong indicators of being fraudulent. We recommend avoiding this posting and reporting it if found on job platforms."
                    risk_level = "HIGH" if conf_score > 80 else "MEDIUM"
                else:  # Legitimate
                    conf_score = confidence[0] * 100
                    prediction_text = "LEGITIMATE JOB"
                    result_class = "result-legitimate"
                    emoji = "✅"
                    advice = "✅ This job posting appears to be legitimate based on our analysis. However, always verify company details independently before applying."
                    risk_level = "LOW"
    
    with col2:
        st.markdown("""
        <div class="analysis-card">
            <h3>🎯 Quick Analysis Guide</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
        <h4>🔍 Red Flags to Watch</h4>
        <ul>
            <li>Poor grammar and spelling</li>
            <li>Vague job descriptions</li>
            <li>Unrealistic salary promises</li>
            <li>Pressure to act quickly</li>
            <li>Requests for personal info upfront</li>
            <li>No clear company address</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# Display results if analysis was performed
if analysis_method == "Direct Text Analysis" and 'analyze_btn' in locals() and analyze_btn and job_text.strip():
    
    st.markdown("---")
    
    # Main result display
    st.markdown(f"""
    <div class="{result_class}">
        <h2>{emoji} {prediction_text}</h2>
        <h3>Confidence Score: {conf_score:.1f}%</h3>
        <p style="font-size: 1.1rem; margin-top: 1rem;">Risk Level: {risk_level}</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Confidence gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = conf_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence Level", 'font': {'size': 20}},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#ff6b6b" if prediction == 1 else "#00b894"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#f8f9fa'},
                    {'range': [50, 80], 'color': '#e9ecef'},
                    {'range': [80, 100], 'color': '#dee2e6'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}
            }
        ))
        fig.update_layout(
            height=300,
            font={'color': "darkblue", 'family': "Arial"},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk factors analysis
        risk_factors = []
        text_lower = job_text.lower()
        
        # Enhanced risk factor detection
        if any(word in text_lower for word in ['urgent', 'immediate', 'asap', 'quickly', 'hurry']):
            risk_factors.append("⚡ Urgent hiring language detected")
        if any(word in text_lower for word in ['$', 'salary', 'pay', 'earn']) and any(word in text_lower for word in ['high', 'excellent', 'amazing', 'incredible']):
            risk_factors.append("💰 Unrealistic salary claims")
        if len(re.findall(r'\b[A-Z]{2,}\b', job_text)) > 15:
            risk_factors.append("📢 Excessive capitalization")
        if 'email' in text_lower and any(domain in text_lower for domain in ['gmail', 'yahoo', 'hotmail']):
            risk_factors.append("📧 Personal email domain used")
        if len(job_text.split()) < 50:
            risk_factors.append("📝 Very brief job description")
        if any(word in text_lower for word in ['work from home', 'no experience', 'easy money']):
            risk_factors.append("🏠 Suspicious work arrangement")
        if "telegram" in text_lower or "whatsapp" in text_lower:
            risk_factors.append("📱 Messaging app references")
        if "₹" in text_lower and any(kw in text_lower for kw in ["per day", "per week", "guaranteed", "earn"]):
            risk_factors.append("💰 Suspicious payment promises")
        if "no interview" in text_lower or "no experience" in text_lower:
            risk_factors.append("🎯 No interview/experience claims")
        if "visa" in text_lower and "processing fee" in text_lower:
            risk_factors.append("🌍 Visa processing fee mentions")
        
        st.markdown("### 🔍 Risk Analysis")
        if risk_factors:
            for factor in risk_factors[:4]:  
                st.markdown(f"• {factor}")
            if len(risk_factors) > 4:
                st.markdown(f"• ➕ {len(risk_factors) - 4} more factors detected")
        else:
            st.markdown("• ✅ No obvious red flags detected")
            st.markdown("• ✅ Professional language used")
            st.markdown("• ✅ Detailed job description")
    
    with col3:
        # Text statistics
        word_count = len(job_text.split())
        char_count = len(job_text)
        sentence_count = len([s for s in job_text.split('.') if s.strip()])
        
        st.markdown("### 📊 Text Statistics")
        st.metric("Word Count", word_count)
        st.metric("Characters", char_count)
        st.metric("Sentences", sentence_count)
        
        
        if word_count > 100:
            st.markdown("✅ Detailed description")
        elif word_count > 50:
            st.markdown("⚠️ Moderate detail")
        else:
            st.markdown("❌ Very brief")
    
    # Advice section
    st.markdown("---")
    st.markdown(f"""
    <div class="analysis-card">
        <h3>💡 Our Recommendation</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">{advice}</p>
    </div>
    """, unsafe_allow_html=True)

elif analysis_method == "URL Scraping Analysis":
    
    st.markdown("""
    <div class="analysis-card">
        <h2>🌐 URL-based Job Analysis</h2>
        <p>Enter a job posting URL to automatically extract and analyze the content</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        job_url = st.text_input(
            "🔗 Job Posting URL:",
            placeholder="https://example.com/job-posting-url",
            help="Enter the complete URL of the job posting",label_visibility="collapsed"
        )
        
        if st.button("🌐 Fetch & Analyze", type="primary", use_container_width=True):
            if job_url:
                try:
                    with st.spinner("🌐 Fetching job posting from URL..."):
                        
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                        response = requests.get(job_url, headers=headers, timeout=15)
                        response.raise_for_status()
                        
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        job_text = soup.get_text()
                        
                        lines = (line.strip() for line in job_text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        job_text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        # Limit text length
                        if len(job_text) > 5000:
                            job_text = job_text[:5000] + "..."
                        
                        if job_text and len(job_text.split()) > 10:
                            st.markdown("""
                            <div class="success-box">
                                <h4>✅ Content Successfully Extracted</h4>
                                <p>Job posting content has been fetched and is ready for analysis.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display extracted text in expandable section
                            with st.expander("📄 View Extracted Content", expanded=False):
                                st.text_area("Extracted Job Description:", job_text, height=300, disabled=True)
                            
                            # Analyze the text
                            with st.spinner("🤖 Analyzing extracted content..."):

                                cleaned_text = clean(job_text)
                                 
                                text_vectorized = vectorizer.transform([cleaned_text])
                                
                                risk = np.array([[risk_score(job_text)]])
                                
                                final_input = hstack([text_vectorized, risk])
                                
                                prediction = model.predict(final_input)[0]
                                confidence = model.predict_proba(final_input)[0]
                                
                                if prediction == 1:
                                    conf_score = confidence[1] * 100
                                    st.markdown(f"""
                                    <div class="result-fake">
                                        <h2>🚨 FAKE JOB DETECTED</h2>
                                        <h3>Confidence: {conf_score:.1f}%</h3>
                                        <p>This job posting from the provided URL shows indicators of being fraudulent.</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    conf_score = confidence[0] * 100
                                    st.markdown(f"""
                                    <div class="result-legitimate">
                                        <h2>✅ LEGITIMATE JOB</h2>
                                        <h3>Confidence: {conf_score:.1f}%</h3>
                                        <p>This job posting appears to be legitimate based on our analysis.</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="warning-box">
                                <h4>⚠️ Content Extraction Failed</h4>
                                <p>Could not extract sufficient job content from the provided URL. This could be due to:</p>
                                <ul>
                                    <li>The page requires JavaScript to load content</li>
                                    <li>The URL is protected or requires login</li>
                                    <li>The page structure is not compatible</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                            
                except requests.exceptions.RequestException as e:
                    st.markdown(f"""
                    <div class="warning-box">
                        <h4>❌ Connection Error</h4>
                        <p>Failed to fetch content from the URL: <code>{str(e)}</code></p>
                        <p>Please check if the URL is correct and accessible.</p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="warning-box">
                        <h4>❌ Processing Error</h4>
                        <p>An error occurred while processing the content: <code>{str(e)}</code></p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>🌐 Supported Platforms</h4>
            <p><strong>Works well with:</strong></p>
            <ul>
                <li>✅ Indeed</li>
                <li>✅ LinkedIn Jobs</li>
                <li>✅ Glassdoor</li>
                <li>✅ Monster</li>
                <li>✅ CareerBuilder</li>
                <li>✅ Company websites</li>
            </ul>
            <p><small>⚠️ Some sites may block automated access</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
            <h4>🔒 Privacy Notice</h4>
            <p>We only extract publicly available job posting content. No personal data is stored or transmitted.</p>
        </div>
        """, unsafe_allow_html=True)

# Footer 
st.markdown("---")
st.markdown("""
<div class="footer">
    <h3>🛡️ Stay safe in your job search with advanced machine learning detection</h3>
    <p>⚠️ This tool provides guidance based on analysis. Always verify job postings independently and trust your instincts.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)