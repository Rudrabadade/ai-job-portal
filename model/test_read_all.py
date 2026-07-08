import os

resume_files = os.listdir("resumes")

for file_name in resume_files:

    with open("resumes/" + file_name, "r") as file:
        content = file.read()

    print("File Name:", file_name)
    print(content)
    print("-------------------")