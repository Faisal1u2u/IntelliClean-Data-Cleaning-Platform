IntelliClean — Smart Data Cleaning & Analytics Platform

IntelliClean is a professional web-based data cleaning and validation platform built using Python and Streamlit.

It transforms messy datasets into structured, analysis-ready data using automated cleaning, validation checks, and interactive analytics — all in one place.

LIVE APPLICATION

Live Demo:
https://intellclean-data-cleaning-platform.streamlit.app

FEATURES

Automated Data Cleaning

Removes duplicate rows

Standardizes column names

Replaces negative numeric values with NaN (instead of deleting rows)

Fills missing categorical values with "Unknown"

Detects and replaces unrealistic age values (<0 or >100)

Fixes invalid date formats

Drops fully empty rows

Generates a clear cleaning operations report

Interactive Analytics Dashboard

Visual summary of cleaning impact

Bar graph showing affected cells per operation

Before vs After dataset comparison

Data quality scoring

Validation Engine

Detects missing values

Identifies duplicate records

Flags negative numeric entries

Calculates overall data quality score

Export Options

Download cleaned dataset as CSV

Download cleaned dataset as Excel

TECH STACK

Python

Pandas

NumPy

Plotly

Streamlit

OpenPyXL

PROJECT STRUCTURE

IntelliClean-Data-Cleaning-Platform
|
|-- app.py
|-- requirements.txt
|-- .gitignore
|-- README.md

HOW TO RUN LOCALLY

Clone repository
git clone https://github.com/Faisal1u2u/IntelliClean-Data-Cleaning-Platform.git

Go into project folder
cd IntelliClean-Data-Cleaning-Platform

Create virtual environment
python3 -m venv venv

Activate environment
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Run app
streamlit run app.py

WHY THIS PROJECT IS STRONG

This project demonstrates:

Real-world data preprocessing automation

Interactive dashboard development

Error-safe data validation logic

Clean UI design using Streamlit

Cloud deployment using Streamlit Cloud

GitHub version control integration

AUTHOR

Faisal Ahmad
B.Tech CSE
GitHub: https://github.com/Faisal1u2u
