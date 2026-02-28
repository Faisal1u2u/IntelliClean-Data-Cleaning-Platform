import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="IntelliClean", layout="wide")

st.title("IntelliClean — Smart Data Cleaning & Analytics")
st.subheader("Transform Raw Data into Structured Intelligence")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:
        # Always reset pointer
        uploaded_file.seek(0)

        file_name = uploaded_file.name.lower()

        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx"):
            # Read file safely into memory
            file_bytes = uploaded_file.read()
            df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")

        else:
            st.error("Unsupported file format.")
            st.stop()

        st.success("File loaded successfully!")

        st.write("### Preview")
        st.dataframe(df.head())

        # -------------------------
        # CLEANING SECTION
        # -------------------------

        if st.button("Start Smart Cleaning"):

            df_clean = df.copy()

            # 1. Standardize column names
            df_clean.columns = (
                df_clean.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
            )

            # 2. Remove duplicate rows
            df_clean = df_clean.drop_duplicates()

            # 3. Fill missing numeric with blank
            for col in df_clean.select_dtypes(include="number").columns:
                df_clean[col] = df_clean[col].fillna("")

            # 4. Fill missing categorical with Unknown
            for col in df_clean.select_dtypes(include="object").columns:
                df_clean[col] = df_clean[col].fillna("Unknown")

            # 5. Remove negative numeric values (replace with blank)
            for col in df_clean.select_dtypes(include="number").columns:
                df_clean.loc[df_clean[col] < 0, col] = ""

            st.success("Cleaning Completed!")

            st.write("### Cleaned Data Preview")
            st.dataframe(df_clean.head())

            # Download button
            csv = df_clean.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Cleaned CSV",
                csv,
                "cleaned_data.csv",
                "text/csv"
            )

    except Exception as e:
        st.error("File could not be read. Please upload a valid CSV or XLSX file.")
        st.stop()