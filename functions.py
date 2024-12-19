import os
import pandas as pd
import yfinance as yf

def register_user(email, password):
    
    df = pd.read_excel("user.xlsx") 
    df["Email"] = df["Email"].astype(str).str.strip()
    df["Password"] = df["Password"].astype(str).str.strip()

    if email.strip() == "" or password.strip() == "":
        return print("Email or Password cannot be empty.")

    if email.strip() in df["Email"].values:
        return print("Email already registered.")   
    
    new_user = {"Email": email.strip(), "Password": password}
    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)

    df.to_excel("user.xlsx", index=False)
    return print("Register Successful")

def authenticate_user(email, password):

    df = pd.read_excel("user.xlsx")
    df["Email"] = df["Email"].astype(str).str.strip()
    df["Password"] = df["Password"].astype(str).str.strip()

    for i in df.index :
        if email == df.loc[i,"Email"] and  password == df.loc[i,"Password"]:
            print("\n*** Login successful. ***\n\n")
            return True
        
    print("Email or Password error.")
    return False

def get_closing_prices(ticker, start_date, end_date):
    try :
        data = yf.download(ticker, start=start_date, end=end_date)  
        if "Close" in data.columns:
            return data["Close"]
        else:
            print("Error: 'Close' column not found in data.")
            return None
    except :
        return None

def analyze_closing_prices(data):
    average_price = data.mean()

    latest_price = data.iloc[-1]
    price_two_days_ago = data.iloc[-2]

    pct_change = ((latest_price - price_two_days_ago) / price_two_days_ago) * 100
    
    latast_price_date = data.index[-1]
    highest_price_date= data.idxmax()
    lowest_price_date= data.idxmin() 

    highest_price= data.max()
    lowest_price= data.min()

    lowest_date_after_ticker = pd.to_datetime(lowest_price_date.iloc[0]).strftime('%d/%m/%Y')
    highest_date_after_ticker = pd.to_datetime(highest_price_date.iloc[0]).strftime('%d/%m/%Y')

    return {
        'Average Price': average_price, 
        'Percentage Change (%)': (pct_change, latast_price_date),
        'Highest Price': (highest_price, highest_date_after_ticker),
        'Lowest Price': (lowest_price, lowest_date_after_ticker)
    }

def save_to_csv(data, filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    main_folder = os.path.join(current_directory, 'folder_to_save_csv')
    subfolder = os.path.join(main_folder, filename.strip().split("_")[0])

    os.makedirs(subfolder, exist_ok=True)

    if not filename.endswith('.csv'):
        filename = os.path.join(subfolder, filename + '.csv')
    else:
        filename = os.path.join(subfolder, filename)

    formatted_data = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, tuple):
                metric_value = (
                    value[0].values[0] if hasattr(value[0], 'values') else float(value[0])
                )
                date_value = value[1].strftime('%d/%m/%Y') if isinstance(value[1], pd.Timestamp) else str(value[1])
                formatted_data.append([key, metric_value, date_value])
            elif hasattr(value, 'values'):
                formatted_data.append([key, value.values[0], ""])
            else:
                formatted_data.append([key, value, ""])

    df = pd.DataFrame(formatted_data, columns=["Metric", "Value", "Date (if applicable)"])

    df.to_csv(filename, index=False)
    print(f"Data has been saved to {filename}.")

def read_from_csv(filename): 
    current_directory = os.path.dirname(os.path.abspath(__file__))
    main_folder = os.path.join(current_directory, 'folder_to_save_csv')
    subfolder = os.path.join(main_folder, filename)

    if not os.path.exists(subfolder):
        print("No storage information exists")
        return
    
    files = os.listdir(subfolder)
    if not files:
        print("No storage information exists")
    else:
        Storage_List = []
        print("Below as the storage result: ")
        for file in files:
            print(file)
            if file.endswith('.csv'):
                Storage_List.append(file)

        Print_Result = input("Do you want to print the result? (y/n): ")
        if Print_Result == 'y':
            Choose_Result = input("Please choose the result(ticker name example: 1155.KL) you want to print: ").strip()
            matching_files = [file for file in Storage_List if Choose_Result  in file]
            if matching_files:
                for file in matching_files:
                    file_path = os.path.join(subfolder, file)
                    try:
                        df = pd.read_csv(file_path)
                        print(f"\nData from {file}:\n")
                        print(df)
                    except Exception as e:
                        print(f"Failed to read {file}: {e}")
            else:
                print("Invalid input. No matching file found.")