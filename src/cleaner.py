import pandas as pd


class DataCleaner:

    def __init__(self, df):
        self.df = df

    def clean_column_names(self):
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace(" ", "_")
        return self.df

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self.df

    def handle_missing_values(self):

        if "age" in self.df.columns:
            self.df["age"] = pd.to_numeric(self.df["age"], errors="coerce")
            self.df["age"].fillna(self.df["age"].median(), inplace=True)

        if "customer_name" in self.df.columns:
            self.df["customer_name"] = self.df["customer_name"].replace("", "Unknown")
            self.df["customer_name"].fillna("Unknown", inplace=True)

        return self.df

    def standardize_gender(self):
        if "gender" in self.df.columns:
            self.df["gender"] = self.df["gender"].str.strip().str.lower()
        return self.df
    
    def clean_dates(self):
        if "order_date" in self.df.columns:
            self.df["order_date"] = pd.to_datetime(
                self.df["order_date"],
                errors="coerce",
                dayfirst=True
            )
            self.df = self.df.dropna(subset=["order_date"])
        return self.df
    
    def remove_invalid_age(self):
        if "age" in self.df.columns:
            self.df = self.df[(self.df["age"] > 0) & (self.df["age"] < 100)]
        return self.df

    def remove_negative_values(self):
        if "price" in self.df.columns:
            self.df = self.df[self.df["price"] >= 0]

        if "total_sales" in self.df.columns:
            self.df = self.df[self.df["total_sales"] >= 0]

        return self.df

    def remove_outliers(self, column_name):
        if column_name in self.df.columns:
            Q1 = self.df[column_name].quantile(0.25)
            Q3 = self.df[column_name].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            self.df = self.df[
                (self.df[column_name] >= lower_bound) &
                (self.df[column_name] <= upper_bound)
            ]

        return self.df