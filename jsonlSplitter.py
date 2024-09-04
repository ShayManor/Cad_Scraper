import os
import json


def split_jsonl_file(input_file, max_size_mb=512):
    output_files = []
    file_count = 1
    current_size = 0
    output_file = None

    max_size_bytes = max_size_mb * 1024 * 1024

    with open(input_file, 'r') as infile:
        for line in infile:
            if current_size == 0:
                # Create a new output file
                output_file_name = f"{os.path.splitext(input_file)[0]}_part{file_count}.jsonl"
                output_file = open(output_file_name, 'w')
                output_files.append(output_file_name)
                print(f"Creating {output_file_name}")

            line_size = len(line.encode('utf-8'))
            if current_size + line_size > max_size_bytes:
                # Close the current file and start a new one
                output_file.close()
                file_count += 1
                current_size = 0
                output_file_name = f"{os.path.splitext(input_file)[0]}_part{file_count}.jsonl"
                output_file = open(output_file_name, 'w')
                output_files.append(output_file_name)
                print(f"Creating {output_file_name}")

            output_file.write(line)
            current_size += line_size

        # Close the last file if it was opened
        if output_file:
            output_file.close()

    print(f"Finished splitting the file into {file_count} parts.")
    return output_files


# Example usage:
input_file = '/users/shay/PycharmProjects/cadScraper/Data/finalData.jsonl'  # Replace with your JSONL file path
split_jsonl_file(input_file)
