with open("resumes/resume1.txt", "r") as file:
    content = file.read()

lines = content.split("\n")

name = lines[0].replace("Name: ", "")

print(name)