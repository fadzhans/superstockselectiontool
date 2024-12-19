import yfinance as yf
import pandas as pd
from functions import register_user, authenticate_user, get_closing_prices, analyze_closing_prices, save_to_csv, read_from_csv

# Dictionary to store users (email:password)
users = {}

# Simple registration and login process
def user_registration_login():
    print("Welcome to the Super Stock Selection Tool")
    
    action = input("Do you want to (r)egister or (l)ogin? ").lower()
    email = None  # Declare email variable
    
    if action == 'r':  # Register new user
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        register_user(email, password)
        print("Registration successful!")
    elif action == 'l':  # Login existing user
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        if authenticate_user(email, password):
            print("Login successful!")
        else:
            print("Invalid credentials. Please try again.")
            return None  # Return None if login fails

    return email  # Return email after successful registration or login

# Stock analysis function
def stock_analysis(email):
    if email is None:  # If login failed, stop execution
        return
    while True:
        # Get stock details from the user
        ticker = input("Enter stock ticker (e.g., 1155.KL for Maybank): ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        # Get closing prices
        data = get_closing_prices(ticker, start_date, end_date)
    
        # Analyze the closing prices
        analysis = analyze_closing_prices(data)
    
        if analysis is None:
            print("Error: Analysis failed or invalid data.")
            continue  # Skip to the next iteration if analysis fails
    
        # Unpack tuple
        average, percentage_change, highest, lowest = analysis
    
       # Access the analysis results directly 
        average = analysis['average'].iloc[0]  # Access the first value in the Series
        percentage_change = analysis['percentage_change'].iloc[0]  # Access the first value in the Series
        highest = analysis['highest'].iloc[0]  # Access the first value in the Series
        lowest = analysis['lowest'].iloc[0]  # Access the first value in the Series
        
        # Display analysis results
        print("Stock Analysis:")
        print(f"Average Closing Price: {average}")
        print(f"Percentage Change: {percentage_change}%")
        print(f"Highest Closing Price: {highest}")
        print(f"Lowest Closing Price: {lowest}")
    
        # Save results to CSV
        filename = 'user_data.csv'  # You can change this to your preferred filename
        save_to_csv({
            'email': email, 
            'ticker': ticker, 
            'average': average, 
            'percentage_change': percentage_change, 
            'highest': highest, 
            'lowest': lowest
        }, filename)
    
        # Optionally read saved data
        display_data = input("Do you want to display previous data? (y/n): ").lower()
        if display_data == 'y':
            data = read_from_csv(filename)
            if data is not None:
                print(data)

        # Ask user if they want to continue or quit
        continue_option = input("Do you want to continue another analysis? (y/n): ").lower()
        if continue_option != 'y':
            print("Thank you for using the Super Stock Selection Tool!")
            break  # Exit the loop and end the program

# Main function start
def main():
    email = user_registration_login()  # Get email after registration or login
    if email:  # Proceed with stock analysis if email is valid
        stock_analysis(email)

if __name__ == "__main__":
    main()
