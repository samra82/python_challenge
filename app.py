# Imports
import streamlit as st 
import pandas as pd
import os
from io import BytesIO
import time


#app setup
st.set_page_config(page_title="Data sweeper" , layout='wide')
# Custom CSS for styling and animations
st.markdown("""
    <style>
    /* General styling */
    .stApp {
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        border-radius: 20px;
        border: 2px solid #4CAF50; /* Green border */
        color: white;
        background-color: #FFB6B9; /* Peach-pink background */
        padding: 8px 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF8C8C; /* Slightly darker peach on hover */
        transform: scale(1.05);
    } 

    .stFileUploader>div>div>div>div {
        border-radius: 20px;
        border: 2px dashed #4CAF50; /* Green dashed border */
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .stFileUploader>div>div>div>div:hover {
        background-color: #f0f0f0;
        transform: scale(1.02);
    }
    .stProgress>div>div>div {
        background-color: #4CAF50;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #4CAF50;
    }
    /* Dark theme specific styling */
    .stApp.dark {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stApp.dark .stButton>button {
        border-color: #4CAF50;
        background-color: #FFB6B9; /* Peach-pink in dark theme */
    }
    .stApp.dark .stButton>button:hover {
        background-color: #FF8C8C;
    }
    .stApp.dark .stFileUploader>div>div>div>div {
        border-color: #4CAF50;
    }
    .stApp.dark .stFileUploader>div>div>div>div:hover {
        background-color: #333333;
    }
    .stApp.dark .stProgress>div>div>div {
        background-color: #4CAF50;
    }
    .stApp.dark .stMarkdown h1, .stApp.dark .stMarkdown h2, .stApp.dark .stMarkdown h3 {
        color: #4CAF50;
    }
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .fadeIn {
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes slideIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .slideIn {
        animation: slideIn 0.5s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)


# Sidebar for additional options
with st.sidebar:
    st.header("Settings")
    st.write("Customize your experience here.")
    theme = st.selectbox("Choose a theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("""
            <style>
            .stApp {
                background-color: #1E1E1E;
                color: #98a6b1;
            }
            </style>
            """, unsafe_allow_html=True)



 # App title and description

st.title("📊 Data Sweaper")
st.write("✨Transform your file between CSV and Excel with build-in data cleaning and visualization!")

uploaded_files = st.file_uploader("upload your files (CSV or Excel):", type=["csv","xlsx"] , accept_multiple_files=True )

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("unsported file type : {file_ext}")
            continue

        #file info display
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:**{file.size/1024}")    

        # 5 rows of data frame
        st.write("Preview the Head of the Data Frame")
        st.dataframe(df.head())

        #data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
           col1, col2 = st.columns(2)
 
           with col1:
                if st.button(f"remove duplicates form {file.name}"):
                   df.drop_duplicates(inplace=True)
                   st.write("Duplicates Removed!")

           with col2:
               if st.button(f"Fill Missing Values For {file.name}"):
                   numeric_cols = df.select_dtypes(include=['number']).columns
                   df[numeric_cols]= df[numeric_cols].fillna(df[numeric_cols].mean())
                   st.write("Missing Values have been Filled!")
                   
        #choose specific columns to keep or convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        #create visualizations
        st.subheader("Data Visualizations")
        if st.checkbox("Show visalization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


        #convert the file csv to excel
        st.subheader("Conversion Options")    
        conversion_type = st.radio(f"Convert {file.name} to :" , ["CSV", "Excel"] , key=file.name)
        if st.button(f"🚀 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer,index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #Download Button
            st.download_button(
                label=f"Download{file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )  
# Progress bar
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)  # Simulate processing time
    progress_bar.progress(i + 1)
st.success("🎉 All Files Processed!")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <p>Made with ❤️ by <a href="https://www.linkedin.com/in/samrashafiq16/" target="_blank">Samra Shafiq</a></p>
    </div>
    """, unsafe_allow_html=True)


            