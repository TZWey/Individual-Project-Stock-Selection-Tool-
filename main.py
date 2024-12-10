import function as fp
import re

#guest user email: guest@gmail.com, password: Guest_123456

while True :
    print("************************\n*                      *")
    print("*      Wlecome to      *\n* Stock Selection Tool *\n*        System        *")
    print("*                      *\n************************\n")
    LR=input( "Login(1),Register(2),Exit(3)\n")

    if LR == "1":
        email=input("Email: ").strip()
        password=input("Password: ").strip()
        if fp.authenticate_user(email,password) == True:

            while True:
                filename = email.strip().split("@")[0]
                print("\nSearch stocks and analyze closing prices(1)\nDisplay analysis of closing prices(2)\nLogout(3)")
                print("")
                choice=input("Enter your choice: ")
                if choice == "1":
                    
                    ticker=input("ticker :")

                    print("Enter start and end date in yyyy-mm-dd format")
                    input_start_year=input("start year (yyyy) :").strip()
                    if len(input_start_year)!= 4:
                        print("Invalid input. Please try again.")
                        continue
                    input_start_month=input("start month (mm) :").strip()
                    if len(input_start_month)!= 2:
                        print("Invalid input. Please try again.")
                        continue
                    input_start_day=input("start day (dd) :").strip()
                    if len(input_start_day)!= 2:
                        print("Invalid input. Please try again.")
                        continue
                    
                    input_end_year=input("end year (yyyy) :").strip()
                    if len(input_end_year)!= 4:
                        print("Invalid input. Please try again.")
                        continue
                    input_end_month=input("end month (mm):").strip()
                    if len(input_end_month)!= 2:
                        print("Invalid input. Please try again.")
                        continue
                    input_end_day=input("end day (dd) :").strip()
                    if len(input_end_day)!= 2:
                        print("Invalid input. Please try again.")
                        continue

                    start_date=input_start_year+"-"+input_start_month+"-"+input_start_day
                    end_date=input_end_year+"-"+input_end_month+"-"+input_end_day

                    data = fp.get_closing_prices(ticker, start_date, end_date)
                    
                    if data is None or data.empty:
                        print("No data found for the given ticker and date range.")
                    else:
                        data2 =fp.analyze_closing_prices(data)
                        save_data=input("Do you want to save the data to a CSV file? (y/n) :").strip()
                        if save_data == "y":
                            filename = filename + "_" + ticker
                            fp.save_to_csv(data2, filename)
                            print("***Data saved to a CSV file successfully.***")
                elif choice == "2":
                    fp.read_from_csv(filename)

                elif choice == "3":
                    break
                else:
                    print("Invalid choice. Please try again.")
    elif LR == "2":
        email=input("Email: ").strip()
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            print("Invalid email address. Please try again.\n\n")
            continue
        password=input("Password: ").strip()
        fp.register_user(email, password)
    elif LR == "3":
        break
    else :
        print("Invalid choice. Please try again.")