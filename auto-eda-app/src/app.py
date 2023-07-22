import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.title("📊 Automated Data Profiling Report")

file = st.file_uploader("Upload your dataset here", type=["csv", "xlsx"])
if file:
    if file.name.split(".")[1] == "xlsx":
        xl = pd.ExcelFile(file)
        sheet_choice = st.selectbox(
            "The following sheets were found in the Excel file. Choose one sheet",
            (xl.sheet_names),
        )
        if st.button("Generate report"):
            df = pd.read_excel(file, sheet_name=sheet_choice)
            profile_report = ProfileReport(df)
            st.download_button(
                "Download report as HTML file",
                data=profile_report.to_html(),
                file_name="report.html",
            )
            st_profile_report(profile_report, navbar=True, height=1300)
            # profile_report.to_file("report.html")

    else:
        df = pd.read_csv(file)
        profile_report = ProfileReport(df, explorative=True)
        st.download_button(
            "Download report as HTML file",
            data=profile_report.to_html(),
            file_name="report.html",
        )
        st_profile_report(profile_report, navbar=True, height=1300)
        # profile_report.to_file("report.html")
