import streamlit as st 
import pandas as pd 
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp { 
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("Datasweeper Sterling Integrator By Syeda Zainab Mukhtar")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# File Uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel formats only):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File Details
        st.write(f"Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data For {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include='number').columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

        # Column Selection
        st.subheader("Select Columns To Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            # File Conversion
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.rsplit(".", 1)[0] + ".csv"
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.rsplit(".", 1)[0] + ".xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed successfully!")
