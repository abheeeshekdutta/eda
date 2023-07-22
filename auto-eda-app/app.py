import streamlit as st
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling.utils.cache import cache_zipped_file
from ydata_profiling.utils.cache import cache_file


def get_data(file_source: str, file_uploaded) -> pd.DataFrame:
    """
    This function prepares the data as per the given user inputs and returns a pandas dataframe

    Args:
        file_source (str): Source of the data.
        file_uploaded : The file object if there was an upload.

    Returns:
        pd.DataFrame: Resulting DataFrame object of the data created
    """
    if file_source == "UCI Bank Marketing Dataset":
        try:
            file_name = cache_zipped_file(
                "bank-full.csv",
                "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip",
            )
            df = pd.read_csv(file_name, sep=";")
            st.success(f"{file_source} loaded successfully", icon="✅")
            return df
        except Exception as e:
            st.write("❌ Error in loading sample data")
            st.write(e)
            return None

    elif file_source == "NASA Meteorite Dataset":
        try:
            file_name = cache_file(
                "meteorites.csv",
                "https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD",
            )
            # Set a seed for reproducibility
            np.random.seed(7331)
            df = pd.read_csv(file_name)
            # Note: Pandas does not support dates before 1880, so we ignore these for this analysis
            df["year"] = pd.to_datetime(df["year"], errors="coerce")
            # Example: Constant variable
            df["source"] = "NASA"
            # Example: Boolean variable
            df["boolean"] = np.random.choice([True, False], df.shape[0])
            # Example: Mixed with base types
            df["mixed"] = np.random.choice([1, "A"], df.shape[0])
            # Example: unhashable column
            df["unhashable"] = [[1]] * df.shape[0]
            # Example: Highly correlated variables
            df["reclat_city"] = df["reclat"] + np.random.normal(scale=5, size=(len(df)))
            # Example: Duplicate observations
            duplicates_to_add = pd.DataFrame(df.iloc[0:10].copy())
            df = pd.concat([df, duplicates_to_add], ignore_index=True)

            st.success(f"{file_source} loaded successfully", icon="✅")
            return df
        except Exception as e:
            st.write("❌ Error in loading sample data")
            st.write(e)
            return None

    elif file_source == "csv":
        try:
            df = pd.read_csv(file_uploaded)
            st.success("CSV file loaded successfully.", icon="✅")
            return df
        except Exception as e:
            st.write("❌ Error in loading CSV file.")
            st.write(e)
            return None

    elif file_source == "excel":
        try:
            xl = pd.ExcelFile(file_uploaded)
            sheet_choice = st.selectbox(
                "The following sheets were found in the Excel file. Choose one sheet",
                (xl.sheet_names),
            )
            df = pd.read_excel(file_uploaded, sheet_name=sheet_choice)
            st.success("Excel file loaded successfully.", icon="✅")
            return df
        except Exception as e:
            st.write("❌ Error in loading Excel file/sheet.")
            st.write(e)
            return None


def generate_report(df_retrieved: pd.DataFrame, file_source: str, report_title: str):
    """
    This function generates the Pandas Profiling report for the created dataframe object

    Args:
        df_retrieved (pd.DataFrame): Pandas DataFrame for which report needs to be created.
        file_source (str): Source of the data.
        report_title (str): Title of the resulting report.
    """

    if st.button("Generate report", key=f"gen_report_uploaded_{file_source}"):
        profile_report = ProfileReport(
            df_retrieved, explorative=True, title=report_title
        )
        st.download_button(
            "Download report as HTML file",
            data=profile_report.to_html(),
            file_name="report.html",
        )
        st_profile_report(profile_report, navbar=True, height=1300)


if __name__ == "__main__":
    st.title("📊 Automated Data Profiling Report")

    tab1, tab2 = st.tabs(["Use CSV/Excel file", "Use sample dataset"])

    with tab1:
        file = st.file_uploader("Upload your dataset here", type=["csv", "xlsx"])
        if file:
            if file.name.split(".")[1] == "xlsx":
                df = get_data(file_source="excel", file_uploaded=file)
                generate_report(
                    df,
                    file_source="excel",
                    report_title="Profile Report for Excel file",
                )
            else:
                df = get_data(file_source="csv", file_uploaded=file)
                generate_report(
                    df, file_source="csv", report_title="Profile Report for CSV file"
                )

    with tab2:
        st.markdown(
            body="""
                    - [NASA Meteorite Dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) - This comprehensive data set from The Meteoritical Society contains information on all of the known meteorite landings
                    - [UCI Bank Marketing Dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing) - The data is related with direct marketing campaigns (phone calls) of a Portuguese banking institution.
                """
        )
        option = st.selectbox(
            "Choose sample dataset",
            ("NASA Meteorite Dataset", "UCI Bank Marketing Dataset"),
        )

        if option == "UCI Bank Marketing Dataset":
            df = get_data(file_source="UCI Bank Marketing Dataset", file_uploaded=None)
            generate_report(
                df,
                file_source="UCI Bank Marketing Dataset",
                report_title="Profile Report of the UCI Bank Marketing Dataset",
            )
        elif option == "NASA Meteorite Dataset":
            df = get_data(file_source="NASA Meteorite Dataset", file_uploaded=None)
            generate_report(
                df,
                file_source="NASA Meteorite Dataset",
                report_title="Profile Report of the NASA Meteorite Dataset",
            )
