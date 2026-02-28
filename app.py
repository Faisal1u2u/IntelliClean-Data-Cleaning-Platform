import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

st.set_page_config(page_title="IntelliClean", layout="wide")

# ---------------- THEME STATE ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

top1, top2 = st.columns([9,1])
with top2:
    st.button("🌙" if st.session_state.theme=="dark" else "☀️", on_click=toggle_theme)

# ---------------- COLOR SYSTEM ----------------
if st.session_state.theme == "dark":
    bg = "#000000"
    card = "#1A1A1A"
    text = "#FFFFFF"
else:
    bg = "#F3F4F6"
    card = "#FFFFFF"
    text = "#111111"

# ---------------- GLOBAL CSS ----------------
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
background-color:{bg};
}}
html, body {{
color:{text};
}}
h1, h2, h3, h4, h5, h6, p {{
color:{text} !important;
}}
.upload-wrapper {{
background:{card};
padding:40px;
border-radius:20px;
box-shadow:0 10px 30px rgba(0,0,0,0.1);
text-align:center;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>IntelliClean — Smart Data Cleaning & Analytics</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Transform Raw Data into Structured Intelligence</h4>", unsafe_allow_html=True)

# ---------------- UPLOAD ----------------
c1, c2, c3 = st.columns([2,4,2])
with c2:
    st.markdown("<div class='upload-wrapper'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv","xlsx"])
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PROCESS ----------------
if uploaded_file is not None:

    uploaded_file.seek(0)

    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.lower().endswith(".xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("Unsupported file type.")
            st.stop()

    except Exception as e:
        st.error("File could not be read. Please upload a valid CSV or XLSX file.")
        st.stop()

    page = st.radio("", ["Overview","Cleaning","Analytics","Validation"], horizontal=True)

    # ---------------- OVERVIEW ----------------
    if page == "Overview":
        st.subheader("Raw Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)
        st.write("Dataset Shape:", df.shape)

    # ---------------- CLEANING ----------------
    elif page == "Cleaning":

        if st.button("Start Smart Cleaning"):

            report = []
            df_clean = df.copy()

            # Remove duplicates
            duplicates = df_clean.duplicated().sum()
            df_clean = df_clean.drop_duplicates()
            report.append(["Removed Duplicate Rows", duplicates])

            # Standardize column names
            df_clean.columns = df_clean.columns.str.strip().str.lower().str.replace(" ","_")
            report.append(["Standardized Column Names", len(df_clean.columns)])

            # Convert columns safely to numeric where possible
            for col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors="ignore")

            numeric_cols = df_clean.select_dtypes(include=np.number).columns

            # Detect missing numeric values
            missing_numeric = df_clean[numeric_cols].isna().sum().sum()
            report.append(["Detected Missing Numeric Values", missing_numeric])

            # Fill missing categorical values
            cat_cols = df_clean.select_dtypes(include="object").columns
            missing_cat = df_clean[cat_cols].isna().sum().sum()
            df_clean[cat_cols] = df_clean[cat_cols].fillna("Unknown")
            report.append(["Filled Missing Categorical Values", missing_cat])

            # Replace negative numeric values with NaN
            negative_count = 0
            for col in numeric_cols:
                neg = (df_clean[col] < 0).sum()
                negative_count += neg
                df_clean.loc[df_clean[col] < 0, col] = np.nan
            report.append(["Replaced Negative Numeric Values", negative_count])

            # Handle unrealistic age safely
            if "age" in df_clean.columns and "age" in numeric_cols:
                invalid_age = ((df_clean["age"] < 0) | (df_clean["age"] > 100)).sum()
                df_clean.loc[(df_clean["age"] < 0) | (df_clean["age"] > 100), "age"] = np.nan
                report.append(["Replaced Unrealistic Age Values", invalid_age])

            # Fix invalid dates
            invalid_dates = 0
            for col in df_clean.columns:
                if "date" in col:
                    parsed = pd.to_datetime(df_clean[col], errors="coerce")
                    invalid_dates += parsed.isna().sum()
                    df_clean[col] = parsed
            report.append(["Replaced Invalid Dates", invalid_dates])

            # Drop fully empty rows
            fully_invalid = df_clean.isna().all(axis=1).sum()
            df_clean = df_clean.dropna(how="all")
            report.append(["Dropped Fully Empty Rows", fully_invalid])

            # Display version
            df_display = df_clean.fillna("")

            st.session_state.cleaned = df_clean
            st.session_state.display = df_display
            st.session_state.report = pd.DataFrame(report, columns=["Operation","Cells Affected"])

            st.success("Cleaning Completed Successfully")

            st.subheader("Cleaning Operations Performed")
            st.dataframe(st.session_state.report, use_container_width=True)

            st.subheader("Before vs After")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Before:", df.shape)
                st.dataframe(df.head())
            with col2:
                st.write("After:", df_clean.shape)
                st.dataframe(df_display.head())

            st.markdown("## Download Cleaned Dataset")

            csv_data = df_clean.to_csv(index=False).encode("utf-8")
            st.download_button("Download Cleaned CSV", csv_data, "cleaned_data.csv")

            buffer = io.BytesIO()
            df_clean.to_excel(buffer, index=False, engine="openpyxl")
            st.download_button("Download Cleaned Excel", buffer.getvalue(), "cleaned_data.xlsx")

    # ---------------- ANALYTICS ----------------
    elif page == "Analytics":

        if "report" in st.session_state:
            st.subheader("Cleaning Impact Analysis")

            fig = px.bar(
                st.session_state.report,
                x="Operation",
                y="Cells Affected",
                title="Cells Affected Per Cleaning Operation"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- VALIDATION ----------------
    elif page == "Validation":

        missing = df.isna().sum().sum()
        duplicates = df.duplicated().sum()

        numeric_cols = df.select_dtypes(include=np.number).columns
        negatives = sum((df[col] < 0).sum() for col in numeric_cols)

        validation = pd.DataFrame({
            "Issue":["Missing Values","Duplicate Rows","Negative Values"],
            "Count":[missing,duplicates,negatives]
        })

        st.subheader("Data Quality Issues")
        st.table(validation)

        score = max(0, round(100 - (missing*0.02 + duplicates*0.5), 2))
        st.metric("Overall Data Quality Score", f"{score}/100")