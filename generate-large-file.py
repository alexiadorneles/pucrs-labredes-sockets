# Generate content for the text file (repeat a string to make it large)
content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 1000

# File path
file_path = "large_file.txt"

# Write content to the file
with open(file_path, "w") as file:
    file.write(content)

print(f"File '{file_path}' generated successfully.")
