import pandas as pd
import streamlit as st
from PIL import Image
import subprocess
import os
import base64
import pickle


# Title of the app
st.title("🌟 AI Model Prediction App 🌟")

# Add custom CSS for improved styling
st.markdown("""
    <style>
    .main {
        background-color: #333333;  /* Light background */
        font-family: 'Arial', sans-serif;  /* Modern font */
    }
    h1 {
        color: #007bff;  /* Primary color for the title */
        font-weight: bold; /* Emphasize title */
    }
    .stButton>button {
        background-color: #007bff; /* Blue color */
        color: white;
        border-radius: 10px; /* Rounded corners */
        padding: 12px 20px; /* More padding for a bigger button */
        font-size: 16px; /* Larger font size */
        transition: background-color 0.3s; /* Smooth transition */
    }
    .stButton>button:hover {
        background-color: #0056b3; /* Darker shade on hover */
    }
    .stFileUploader {
        margin: 20px 0; /* Add margin for spacing */
        border: 2px dashed #007bff; /* Dashed border */
        border-radius: 10px; /* Rounded corners */
        padding: 20px; /* Padding inside uploader */
        background-color: white; /* Background for uploader */
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    }
    .stTextInput>div>input {
        border: 2px solid #007bff; /* Blue border */
        border-radius: 5px; /* Rounded corners */
        padding: 10px; /* Padding inside input */
        font-size: 14px; /* Font size */
    }
    .output-box {
        background-color: #f8f9fa; /* Light background for output */
        border-radius: 10px; /* Rounded corners */
        padding: 20px; /* Padding inside output box */
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    }
    footer {
        text-align: center; /* Centered footer */
        color: #6c757d; /* Light gray color for footer */
        padding: 20px 0; /* Padding for footer */
    }
    </style>
""", unsafe_allow_html=True)



def desc_calc():
    # Performs the descriptor calculation
    bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    os.remove('molecule.smi')

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

def build_model(input_data):
    # Reads in saved regression model
    load_model = pickle.load(open('random_forest_model.pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data[1], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.file_uploader("Choose a file...", type=["csv", "txt"], label_visibility="collapsed")
    st.sidebar.markdown("""
[Example input file](https://raw.githubusercontent.com/dataprofessor/bioactivity-prediction-app/main/example_acetylcholinesterase.txt)
""")
    

# Button to trigger prediction
if st.sidebar.button('Predict'):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)

    st.header('**Original input data**')
    st.write(load_data)

    with st.spinner("Calculating molecular descriptors..."):
        desc_calc()

    # Read in calculated descriptors and display the dataframe
    st.header('**Calculated molecular descriptors**')
    desc = pd.read_csv('X_df.csv')
    st.write(desc)
    st.write(desc.shape)

    # Read descriptor list used in previously built model
    st.header('**Subset of descriptors from previously built models**')
    Xlist = list(pd.read_csv('X_df.csv').columns)
    desc_subset = desc[Xlist]
    st.write(desc_subset)
    st.write(desc_subset.shape)

    # Apply trained model to make prediction on query compounds
    build_model(desc_subset)
else:
    st.info('Upload input data in the sidebar to start!')

# Footer
st.markdown("<footer>© 2024 AI Model Prediction | Designed with ❤️</footer>", unsafe_allow_html=True)