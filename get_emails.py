#import pytesseract
import os
import re

def find_emails(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # This pattern should match most email addresses
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    emails = re.findall(pattern, content)
    return emails

def main():
    emails_list = []
    for root, dirs, files in os.walk('screenshots/'):
        for file in files:
            fpath = os.path.join(root, file)
            if fpath.endswith('.txt'):
                emails = find_emails(fpath)
                for email in emails:
                    print(email)
                    emails_list.append(email)

    with open("extracted_emails.txt", "w") as f:
        for email in emails_list:
            f.write(f"{email}\n")

if __name__ == "__main__":
    main()