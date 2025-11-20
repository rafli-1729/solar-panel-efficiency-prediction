import pandas as pd
from pathlib import Path

# To make single time format for merging
def make_timestamp(df) -> pd.Series:  
    if "date_time" not in df.columns:
        raise KeyError("Column 'date_time' not found in dataframe.")
        
    dt = pd.to_datetime(df["date_time"])
    time = dt.dt.strftime("%b %-d, %Y %-I")
    suffix = dt.dt.strftime("%p").str.lower()
    
    timestamp = time + suffix
    
    return pd.to_datetime(timestamp)

# To convert multiple columns in dataframe to single datetime
def columns_to_datetime(df) -> pd.Series:
    return pd.to_datetime(
        df[['Year', 'Month', 'Day', 'Hour', 'Minute']]
    )

# To merge main dataset to multiple feature datasets
def merge_with_features(df, *feature_dfs) -> pd.DataFrame:
    if "Timestamp" not in df.columns:
        raise KeyError("Column 'Timestamp' not found in dataframe.")

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="mixed")
        
    for feature in feature_dfs:
        df = df.merge(feature, on="Timestamp", how="left")
        
    return df

# To load multiple csv file by year
def load_yearly_csv(path, prefix, years) -> pd.DataFrame:
    return pd.concat(
        [pd.read_csv(path / f"{prefix}_{year}.csv") for year in years],
        ignore_index=True
    )

# To convert date time format to submission format
def convert_to_submission(df) -> pd.DataFrame:
    if "Timestamp" not in df.columns:
        raise KeyError("Column 'Timestamp' not found in dataframe.")
        
    dt = pd.to_datetime(df["Timestamp"])
    time = dt.dt.strftime("%b %-d, %Y %-I")
    suffix = dt.dt.strftime("%p").str.lower()

    df['Timestamp'] = time + suffix
    return df

# To add year, month, and day to solar and lunar features
def merge_column_with_timestamp(df, column) -> pd.Series:
    date_str = df['Timestamp'].dt.strftime('%Y-%m-%d')
    combined_str = date_str + ' ' + df[column]

    return pd.to_datetime(combined_str, errors='coerce')
