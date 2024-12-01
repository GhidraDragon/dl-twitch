import pytesseract
import os
import concurrent.futures

def list_folders(path):
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return folders

def get_txt(ss_path):
    png_files = [file for file in os.listdir(f"screenshots/{ss_path}") if file.endswith('.png')]
    for png in png_files:
        text = pytesseract.image_to_string(f"screenshots/{ss_path}/{png}")
        with open(f"screenshots/{ss_path}/{png}_text.txt", "w") as f:
            f.write(text)
            print(f"written screenshots/{ss_path}/{png}_text.txt")

def thread_get_txt(ss_folders, max_threads=30):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(get_txt, fol) for fol in ss_folders]
        concurrent.futures.wait(futures)

def main():
    ss_folders = list_folders('screenshots/')
    thread_get_txt(ss_folders)

if __name__ == "__main__":
    main()