import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# Assuming you have a function to query your RAG model
# Replace this with your actual RAG model query function
def query_rag_model(query):
    # Simulate a delay to represent processing time
    time.sleep(2)
    return f"This is a simulated response for the query: '{query}'"

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Set page config
st.set_page_config(page_title="RAG Model Query", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #4e54c8, #8f94fb);
    }
    .big-font {
        font-size:30px !important;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4e54c8;
        color: #ffffff;
    }
    .stButton>button:hover {
        background-color: #8f94fb;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Load Lottie animation
lottie_url = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"
lottie_json = load_lottieurl(lottie_url)

# App layout
col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.empty()

with col2:
    st.markdown("<h1 style='text-align: center; color: white;'>RAG Model Query Interface</h1>", unsafe_allow_html=True)
    
    # Display Lottie animation
    if lottie_json:
        st_lottie(lottie_json, height=200)
    
    # Search bar
    query = st.text_input("", placeholder="Enter your query here...")
    
    # Search button
    if st.button("Search"):
        if query:
            with st.spinner('Searching...'):
                result = query_rag_model(query)
            st.success("Search complete!")
            st.markdown("<p class='big-font'>Results:</p>", unsafe_allow_html=True)
            st.write(result)
        else:
            st.warning("Please enter a query.")

with col3:
    st.empty()

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0,0,0,0.5);
        color: white;
        text-align: center;
    }
    </style>
    <div class="footer">
        <p>Developed with ❤️ by Your Team</p>
    </div>
    """,
    unsafe_allow_html=True
)