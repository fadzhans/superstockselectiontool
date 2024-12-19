import yfinance as yf
import pandas as pd

# Register a user by saving their email and password
def register_user(email, password):
    with open('users.csv', 'a') as file:
        file.write(f"{email},{password}\n")

# Authenticate user by checking their email and password
def authenticate_user(email, password):
    with open('users.csv', 'r') as file:
        for line in file:
            stored_email, stored_password = line.strip().split(',')
            if email == stored_email and password == stored_password:
                return True
    return False

# Fetch the historical closing prices for a stock
def get_closing_prices(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data  # Return full DataFrame, not just 'Close' column

# Perform analysis on the closing prices
def analyze_closing_prices(data):
    # Perform analysis (example calculations)
    average = data['Close'].mean()  # Directly use 'Close' column of the DataFrame
    percentage_change = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
    highest = data['Close'].max()
    lowest = data['Close'].min()

    # Analysis results as a dictionary
    return {
        'average': average,
        'percentage_change': percentage_change,
        'highest': highest,
        'lowest': lowest
    }

# Save user interaction data to a CSV file
def save_to_csv(data, filename='user_data.csv'):
    print(f"Saving the following data to {filename}:")
    print(data)  # Print the data to be saved
    df = pd.DataFrame([data])  # Create DataFrame from the dictionary
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

# Read and display data from the CSV file
def read_from_csv(filename='user_data.csv'):
    try:
        data = pd.read_csv(filename)
        print("\nPrevious user interactions:")
        print(data)  # Debug print
    except FileNotFoundError:
        print("No previous data found.")
