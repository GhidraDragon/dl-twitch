import pickle

def main():
    email_list = []
    with open("extracted_emails.txt", "r") as f:
        for line in f:
            email_list.append(line)
    
    with open("employees.pickle", "rb") as f:
        employees_dict = pickle.load(f)

    for email in email_list:
        email = email.strip()
        employees_dict[email] = 'Someone Affiliated With Twitch Crimes'
    
    with open("employees.pickle", "wb") as f:
        pickle.dump(employees_dict, f)
    
    print(employees_dict)

if __name__ == "__main__":
    main()