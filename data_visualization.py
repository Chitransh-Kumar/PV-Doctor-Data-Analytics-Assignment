import pandas as pd
import matplotlib.pyplot as plt

def data_visualization(csv_path, start_date= None, end_date= None):
    """
    This function is used for data visualization based on csv file mentioned and start and end date mentioned (if any)
    
    :param csv_path: File path of the data prepared
    :param start_date: Start date for data visualization (depends on the user) Default= None
    :param end_date: End date for data visualization (depends on the user) Default= None
    """
    
    df= pd.read_csv(csv_path)

    # Converts Date column data-type from Object (string) to Date.
    df['Date']= pd.to_datetime(df['Date'])


    # If start and end date is mentioned then filter the data accordingly
    if start_date is not None:
        start_date= pd.to_datetime(start_date)
        df= df[df['Date']>=start_date]

    if end_date is not None:
        end_date= pd.to_datetime(end_date)
        df= df[df['Date']<=end_date]

    # GHI values color mapping
    def ghi_color(ghi):
        if ghi<2:
            return "navy"
        elif ghi<4:
            return "lightblue"
        elif ghi<6:
            return "orange"
        else:
            return "brown"
    
    df['GHI_Color']= df['GHI'].apply(ghi_color)

    # 30-day moving average
    df['PR_30D_MA']= df['PR'].rolling(window= 30).mean()

    # Budget year calculation 
    # Year starts from July and ends at June
    def budget_year_index(date):
        if date.month >=7:
            return date.year - 2019
        else:
            return date.year - 2019 - 1

    df['Budget_year']= df['Date'].apply(budget_year_index).astype(int)

    # Values as specified in the assignment
    BASE_BUDGET= 73.9 
    YEARLY_DROP= 0.8 

    df['Budget_PR']= BASE_BUDGET - (df['Budget_year'] * YEARLY_DROP)


    # Points above target budget PR
    above_budget= df[df['PR']> df['Budget_PR']]
    total_count_percent= round((len(above_budget) / len(df)) * 100, 2)


    # Graph plotting
    plt.figure(figsize= (14, 7))

    # Scatter plot for PR values with color encoding of corresponding GHI values
    plt.scatter(df['Date'], df['PR'], c= df['GHI_Color'], s= 20, alpha= 0.8, label= 'Daily PR')

    # Plot for 30 day moving average of PR values
    plt.plot(df['Date'], df['PR_30D_MA'], color= 'red', linewidth= 2, label= '30 day moving avg (PR)')

    # Plot for Target Budget PR
    plt.plot(df['Date'], df['Budget_PR'], color= 'darkgreen', linewidth= 2, label= 'Target Budget PR')


    # Summary statistics
    last_7= df['PR'].tail(7).mean()
    last_30= df['PR'].tail(30).mean()
    last_60= df['PR'].tail(60).mean()
    last_90= df['PR'].tail(90).mean()
    last_365= df['PR'].tail(365).mean()
    lifetime= df['PR'].mean()

    summary_text= (
        f"Avg PR (last 7 days): {last_7:.2f}\n"
        f"Avg PR (last 30 days): {last_30:.2f}\n"
        f"Avg PR (last 60 days): {last_60:.2f}\n"
        f"Avg PR (last 90 days): {last_90:.2f}\n"
        f"Avg PR (last 365 days): {last_365:.2f}\n"
        f"Avg PR (Lifetime): {lifetime:.2f}"
    )

    x_pos= df['Date'].max()
    y_pos= df['PR'].min()

    plt.text(
        x_pos, y_pos, 
        summary_text, 
        fontsize= 10,
        verticalalignment= "bottom", 
        horizontalalignment= "right"
    )

    # Above budget PR statistics text
    min_pr= df['PR'].min()
    mid_date= df['Date'].iloc[len(df)//2]

    plt.text(
        mid_date,
        min_pr - 0.5,
        f"Points above target budget PR: {total_count_percent} %",
        horizontalalignment= "center",
        fontsize= 12
    )


    # Graph formatting
    plt.xlabel("Date")
    plt.ylabel("Performance Ratio (%) ")
    plt.title("Performance Ratio Evaluation")

    plt.legend()
    plt.tight_layout()

    plt.savefig("Performance-Ratio-Evaluation.png")
    plt.show()

if __name__=="__main__":
    data_visualization(csv_path="preprocessed_data.csv")