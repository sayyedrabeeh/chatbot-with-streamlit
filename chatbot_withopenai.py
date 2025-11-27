import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

 
st.set_page_config(
    page_title="Dubai Trip Planner - Professional Travel Planning",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

 
st.markdown("""
    <style>
    /* Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Background - Professional Dark */
    .main {
        background-color: #0e1117;
    }
    
    .block-container {
        padding-top: 0rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Professional Banner Overlay */
    .banner-container {
        position: relative;
        margin: -1rem -1rem 0 -1rem;
    }
    
    .banner-overlay {
        position: relative;
        background: linear-gradient(180deg, rgba(14,17,23,0) 0%, rgba(14,17,23,0.8) 100%);
        padding: 3rem 2rem 2rem 2rem;
        margin-top: -6rem;
    }
    
    .banner-title {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .banner-subtitle {
        color: #e0e0e0;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Sidebar Professional Styling */
    [data-testid="stSidebar"] {
        background-color: #1a1d24;
        border-right: 1px solid #2d3139;
        min-width: 300px !important;
        max-width: 350px !important;
    }
    
    /* Force sidebar to be visible */
    [data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0 !important;
        transform: none !important;
    }
    
    /* Sidebar toggle button visibility */
    [data-testid="collapsedControl"] {
        display: block !important;
        color: #4a9eff !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e0e0e0;
        font-size: 0.9rem;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 0.3rem;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #1e2329 0%, #252b35 100%);
        border: 1px solid #2d3139;
        border-radius: 8px;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.8rem 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #252b35 0%, #2d3139 100%);
        border-color: #4a9eff;
    }
    
    .streamlit-expanderContent {
        background: transparent;
        border: none;
        padding: 0.5rem 0 0 0;
    }
    
    [data-testid="stExpander"] {
        background: transparent;
        border: none;
        margin-bottom: 1rem;
    }
    
    [data-testid="stExpander"] p {
        color: #cbd5e1 !important;
    }
    
    /* Info Cards */
    .info-card {
        background: linear-gradient(135deg, #1e2329 0%, #252b35 100%);
        border: 1px solid #2d3139;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        border-color: #4a9eff;
        box-shadow: 0 4px 12px rgba(74, 158, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .info-card h4 {
        color: #4a9eff;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0 0 0.8rem 0;
    }
    
    .info-card h4::before {
        content: "✦";
        margin-right: 0.5rem;
        color: #4a9eff;
    }
    
    .info-card ul {
        margin: 0;
        padding-left: 1.2rem;
        list-style: none;
    }
    
    .info-card li {
        color: #b0b7c3;
        font-size: 0.85rem;
        line-height: 1.8;
        padding-left: 0.5rem;
        position: relative;
    }
    
    .info-card li:before {
        content: "▪";
        position: absolute;
        left: -0.8rem;
        color: #4a9eff;
    }
    
    /* Professional Buttons */
    .stButton button {
        background: linear-gradient(135deg, #2d5a9e 0%, #1e3c72 100%);
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 0.65rem 1rem;
        font-weight: 500;
        font-size: 0.85rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #3d6aae 0%, #2e4c82 100%);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        transform: translateY(-1px);
    }
    
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* Secondary Button */
    .stButton button[kind="secondary"] {
        background: transparent;
        color: #e0e0e0;
        border: 1px solid #3d4450;
    }
    
    .stButton button[kind="secondary"]:hover {
        background-color: #252b35;
        border-color: #4a9eff;
        color: #ffffff;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: #1a1d24;
        border: 1px solid #2d3139;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    [data-testid="stChatMessageContent"] {
        color: #e0e0e0;
        line-height: 1.7;
        font-size: 0.95rem;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: #e0e0e0;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stChatMessageContent"] strong {
        color: #ffffff;
    }
    
    /* Chat Input */
    .stChatInputContainer {
        border-top: 1px solid #2d3139;
        background-color: #0e1117;
        padding: 1.5rem 0 0 0;
    }
    
    .stChatInputContainer textarea {
        background-color: #1a1d24 !important;
        border: 1px solid #2d3139 !important;
        color: #e0e0e0 !important;
        border-radius: 6px;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #4a9eff !important;
        box-shadow: 0 0 0 1px #4a9eff !important;
    }
    
    /* Chat Avatars */
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #2d5a9e 0%, #1e3c72 100%);
    }
    
    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #3d4450 0%, #2d3139 100%);
    }
    
    /* Divider */
    hr {
        border-color: #2d3139;
        margin: 1.5rem 0;
    }
    
    /* Caption/Footer Text */
    .stCaption, caption {
        color: #6c727f !important;
        font-size: 0.75rem;
        text-align: center;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #4a9eff !important;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1d24;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3d4450;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4a9eff;
    }
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

 
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

 
model = genai.GenerativeModel(
    "models/gemini-2.0-flash",  
    system_instruction="""
You are Dubai Ginnee (DG), an expert Dubai trip planner.
You know all Dubai attractions, food spots, hotels, events, and transportation.
Your responses must:
- Start with a friendly DG introduction.
- Stay under 200 words.
- Include follow-up questions.
- Provide day-wise itinerary guidance.
- Be structured and professional.
"""
)
 
def get_responses_from_llm(messages):
   
    try:
         
        gemini_messages = []
        for m in messages:
            if m["role"] == "system":
                continue
            role = "model" if m["role"] == "assistant" else "user"
            gemini_messages.append({
                "role": role,
                "parts": [{"text": m["content"]}]
            })
        
        
        response = model.generate_content(gemini_messages)
        return response.text
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please try again."

 
banner_url = "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1600&h=400&fit=crop&q=80"

 
with st.sidebar:
    st.markdown("### 🏙️ Dubai Ginnee")
    st.markdown("*Professional Travel Consultation*")
    st.markdown("---")
    
    with st.expander("🎯 **OUR SERVICES**", expanded=True):
        st.markdown("""
        <div class="info-card">
            <h4>Planning Services</h4>
            <ul>
                <li>Custom Itinerary Design</li>
                <li>Attraction Recommendations</li>
                <li>Luxury Accommodation</li>
                <li>Dining Reservations</li>
                <li>VIP Transportation</li>
                <li>Local Experience Curation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("⚡ **QUICK START**", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("3-Day Trip", use_container_width=True):
                st.session_state.quick_query = "I need to plan a 3-day business and leisure trip to Dubai"
        with col2:
            if st.button("Hotels", use_container_width=True):
                st.session_state.quick_query = "What are your luxury hotel recommendations in Dubai?"
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Dining", use_container_width=True):
                st.session_state.quick_query = "Recommend fine dining restaurants in Dubai"
        with col4:
            if st.button("Attractions", use_container_width=True):
                st.session_state.quick_query = "What are the must-visit attractions in Dubai?"
    
    with st.expander("🌟 **POPULAR DESTINATIONS**", expanded=False):
        st.markdown("""
        <div class="info-card">
            <h4>Must-Visit Places</h4>
            <ul>
                <li>Burj Khalifa</li>
                <li>Dubai Mall</li>
                <li>Palm Jumeirah</li>
                <li>Dubai Marina</li>
                <li>Gold Souk</li>
                <li>Dubai Frame</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("💡 **TRAVEL TIPS**", expanded=False):
        st.markdown("""
        <div class="info-card">
            <h4>Insider Information</h4>
            <ul>
                <li>Best time: November to March</li>
                <li>Currency: AED (Dirham)</li>
                <li>Dress code: Modest & respectful</li>
                <li>Language: Arabic & English</li>
                <li>Metro: Efficient transport</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📞 **CONTACT INFO**", expanded=False):
        st.markdown("""
        <div class="info-card">
            <ul>
                <li>📧 info@dubaitripplanner.com</li>
                <li>📱 +971 4 XXX XXXX</li>
                <li>🌐 www.dubaitripplanner.com</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("⚙️ **SESSION CONTROL**", expanded=False):
        if st.button("🔄 New Consultation", type="secondary", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Welcome to Dubai Trip Planner! I'm **Dubai Ginnee (DG)**, your dedicated travel planning consultant.\n\nI specialize in creating personalized Dubai experiences, from luxury accommodations to exclusive dining and must-see attractions.\n\nHow may I assist you with your Dubai travel arrangements today?"
                }
            ]
            st.rerun()
    
    st.markdown("---")
    st.caption("© 2024 Dubai Trip Planner\nPowered by Advanced AI")
 
st.markdown('<div class="banner-container">', unsafe_allow_html=True)
st.image(banner_url, use_container_width=True)
st.markdown("""
    <div class="banner-overlay">
        <div class="banner-title">🏙️ Dubai Trip Planner</div>
        <div class="banner-subtitle">Professional AI-Powered Travel Planning Services</div>
    </div>
    </div>
""", unsafe_allow_html=True)

 
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to Dubai Trip Planner! I'm **Dubai Ginnee (DG)**, your dedicated travel planning consultant.\n\nI specialize in creating personalized Dubai experiences, from luxury accommodations to exclusive dining and must-see attractions.\n\nHow may I assist you with your Dubai travel arrangements today?"
        }
    ]

 
if "quick_query" in st.session_state:
    quick_query = st.session_state.quick_query
    del st.session_state.quick_query
    
    st.session_state.messages.append({"role": "user", "content": quick_query})
    response = get_responses_from_llm(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

 
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

 
user_input = st.chat_input("Describe your travel requirements...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("Consulting our travel experts..."):
        response = get_responses_from_llm(st.session_state.messages)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.rerun()