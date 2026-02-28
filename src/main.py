from data_loader import load_data
from cleaner import DataCleaner
from analyzer import DataAnalyzer
from report_generator import ReportGenerator
import os
import logging


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_path = os.path.join(BASE_DIR, "Reports")

    os.makedirs(reports_path, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(reports_path, "project_log.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True
    )

    logging.info("Project execution started.")
    file_path = "../data/raw/retail_sales_raw.csv"

    df = load_data(file_path)

    if df is not None:

        cleaner = DataCleaner(df)

        df = cleaner.clean_column_names()
        df = cleaner.remove_duplicates()
        df = cleaner.handle_missing_values()
        df = cleaner.standardize_gender()
        df = cleaner.clean_dates()
        df = cleaner.remove_invalid_age()
        df = cleaner.remove_negative_values()
        df = cleaner.remove_outliers("price")
        df = cleaner.remove_outliers("total_sales")

        df.to_csv("../data/cleaned/retail_sales_cleaned.csv", index=False)
        analyzer = DataAnalyzer(df)

        summary = analyzer.generate_summary()
        summary.to_csv("../Reports/summary_statistics.csv")

        analyzer.plot_sales_distribution()
        analyzer.plot_revenue_by_city()
        report = ReportGenerator(df, summary)
        report.generate_pdf()

        logging.info("Data cleaning completed and saved.")


if __name__ == "__main__":
    main()