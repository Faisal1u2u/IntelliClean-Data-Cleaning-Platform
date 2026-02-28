import os
import matplotlib.pyplot as plt
import seaborn as sns


class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    def generate_summary(self):
        summary = self.df.describe(include="all")
        return summary

    def plot_sales_distribution(self):
        os.makedirs("../reports", exist_ok=True)

        plt.figure()
        sns.histplot(self.df["total_sales"], kde=True)
        plt.title("Sales Distribution")
        plt.xlabel("Total Sales")
        plt.ylabel("Frequency")
        plt.savefig("../reports/sales_distribution.png")
        plt.close()

    def plot_revenue_by_city(self):
        os.makedirs("../reports", exist_ok=True)

        revenue = self.df.groupby("city")["total_sales"].sum()

        plt.figure()
        revenue.plot(kind="bar")
        plt.title("Total Revenue by City")
        plt.ylabel("Revenue")
        plt.savefig("../reports/revenue_by_city.png")
        plt.close()