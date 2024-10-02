import re

def find_regex_in_file(file_path, pattern):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        matches = re.findall(pattern, content)
        return matches

# Define the file path and regex pattern
file_path = 'countries.txt'
pattern = r'Q\d+'

# Find and print all matches
matches = find_regex_in_file(file_path, pattern)
print(str([f"wd:{id}" for id in matches]).replace("'", "").replace("[", "(").replace("]", ")"))