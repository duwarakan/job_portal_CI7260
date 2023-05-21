import os


def read_and_write_files(source_dir, output_file, skip_files=None):
    if skip_files is None:
        skip_files = []

    file_extensions = ['.html', '.css', '.py']
    total_word_count = 0

    with open(output_file, 'w', encoding='utf-8') as output:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file not in skip_files and any(file.endswith(ext) for ext in file_extensions):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        content = input_file.read()
                    word_count = len(content.split())
                    total_word_count += word_count
                    output.write(f"{file}\n")
                    output.write(f"{content}\n")
                    output.write("\n")

    return total_word_count


source_directory = r"C:\Users\duwar\Desktop\Job_final"
output_txt_file = "output.txt"
files_to_skip = ["test_app.py", "get_all_files.py"]

total_word_count = read_and_write_files(source_directory, output_txt_file, files_to_skip)
print(f"Total word count: {total_word_count}")
