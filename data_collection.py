import os
import pandas as pd
from datetime import datetime

def data_preprocessing(base_data_path, output_csv):
    """
    This function takes file path as input and Name of output .csv file as input and saves output csv file.
    
    :param base_data_path: File path (for original data)
    :param output_csv: Name of desired output .csv file
    """

    pr_root_path= os.path.join(base_data_path, "PR")
    ghi_root_path= os.path.join(base_data_path, "GHI")

    records= []

    for month in sorted(os.listdir(pr_root_path)):
        
        pr_month_path= os.path.join(pr_root_path, month)
        ghi_month_path= os.path.join(ghi_root_path, month)

        if not os.path.isdir(pr_month_path):
            continue

        if not os.path.isdir(ghi_month_path):
            continue

        for file in sorted(os.listdir(pr_month_path)):

            pr_file_path= os.path.join(pr_month_path, file)
            ghi_file_path= os.path.join(ghi_month_path, file)

            pr_df= pd.read_csv(pr_file_path)
            ghi_df= pd.read_csv(ghi_file_path)

            pr_date= pd.to_datetime(pr_df.iloc[:, 0])
            
            pr_values= pr_df.select_dtypes(include= "number").iloc[:, 0]
            ghi_values= ghi_df.select_dtypes(include= "number").iloc[:, 0]

            for date, pr_value, ghi_value in zip(pr_date, pr_values, ghi_values):
                records.append({
                    "Date": date.date(),
                    "GHI": ghi_value,
                    "PR": pr_value,
                })

    final_df= pd.DataFrame(records)

    final_df.sort_values("Date", inplace= True)
    
    final_df.to_csv(output_csv, index= False)

    return final_df

if __name__=="__main__":

    # Base file path location -> Depends on the file path 
    base_path= r"C:\Users\chitr\OneDrive\Desktop\Project\data\data"

    # Output file name
    output_csv= "preprocessed_data.csv"

    df= data_preprocessing(base_data_path= base_path, output_csv= output_csv)

    print("Rows: ", len(df))