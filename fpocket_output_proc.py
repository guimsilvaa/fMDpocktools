import os

def process_file(input_file):
    # Define the dictionary to hold pocket data
    pocket_data = {}

    # Open and read the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Process each line in the file
    current_pocket = None
    for line in lines:
        if line.startswith("Pocket"):
            # Extract the pocket number
            current_pocket = int(line.split()[1])
            pocket_data[current_pocket] = {}
        elif ":" in line:
            # Split the line into property and value
            property_name, value = line.split(":", 1)
            # Store property and value in the dictionary
            pocket_data[current_pocket][property_name.strip()] = value.strip()

    # Transpose the data
    transposed_data = {prop: [] for prop in pocket_data[1]}  # Use properties from the first pocket
    for pocket_number, properties in pocket_data.items():
        for prop, value in properties.items():
            transposed_data[prop].append(value)

    # Processed file name
    processed_file = input_file.replace("_info.txt", "_processed.txt")

    # Write processed data to the new file
    with open(processed_file, 'w') as f:
        # Write column headers
        f.write("pocket_number\t")
        for prop in transposed_data:
            f.write(f"{prop}\t")
        f.write("\n")
        # Write data rows
        for i in range(len(transposed_data["Score"])):
            f.write(f"{i+1}\t")
            for prop, values in transposed_data.items():
                f.write(f"{values[i]}\t")
            f.write("\n")

    print(f"Processed file '{processed_file}' created.")

def main():
    # List all files with names ending with '_info.txt' in current directory and subdirectories
    info_files = [os.path.join(root, filename)
                  for root, _, filenames in os.walk('.')
                  for filename in filenames
                  if filename.endswith('_info.txt')]

    # If no files found, inform the user and exit
    if not info_files:
        print("No files with names ending with '_info.txt' found.")
        return

    # Print the list of found files
    print("List of files ending with '_info.txt':")
    for idx, file in enumerate(info_files):
        print(f"{idx + 1}. {file}")

    # Prompt user to choose a file
    while True:
        choice = input("Enter the number corresponding to the file you want to process: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(info_files):
                chosen_file = info_files[choice - 1]
                process_file(chosen_file)
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        else:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
