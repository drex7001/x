import os
from PyPDF2 import PdfReader


def extract_data(input_folder="input", output_folder="output"):
    """
    Extracts text from new PDF files in the input folder and saves the extracted text in the output folder.
    
    Parameters:
        input_folder (str): Path to the folder containing input PDF files.
        output_folder (str): Path to the folder where extracted text files will be saved.
    """

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get lists of files in input and output folders
    input_files = set(f for f in os.listdir(input_folder) if f.endswith(".pdf"))
    output_files = set(f.replace(".txt", ".pdf") for f in os.listdir(output_folder) if f.endswith(".txt"))

    # Find new PDF files that need processing
    new_files = input_files - output_files

    if not new_files:
        print("No new files to process.")
        return

    print(f"Found {len(new_files)} new files to process: {new_files}")

    # Process each new file
    for file_name in new_files:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name.replace(".pdf", ".txt"))

        try:
            # Read the PDF file
            reader = PdfReader(input_file_path)
            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            # Save extracted text to output folder
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Processed and saved: {file_name}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")


if __name__ == "__main__":
    # Specify the paths for input and output folders
    input_folder = "inputs"
    output_folder = "outputs"

    extract_data(input_folder, output_folder)