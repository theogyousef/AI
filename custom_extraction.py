import pandas as pd
import py7zr
from tqdm import tqdm

 # taking a 100 instances from each class 
def extract_files_by_class(archive_path, csv_path, output_folder):
    # Load the labels from the CSV
    labels_df = pd.read_csv(csv_path)

    filtered_df = labels_df[labels_df['Class'] == 5]
    grouped_df = filtered_df.head(100)
    # # Filter out Class 4
    # filtered_df = labels_df[labels_df['Class'] != 5]
    #
    # # Group by 'Class' and take the first 100 entries from each group
    # grouped_df = filtered_df.groupby('Class').head(100)

    # Create a list of IDs to extract from the archive, appending '.asm' to each ID
    ids_to_extract = [f"{row['Id']}.bytes" for index, row in grouped_df.iterrows()]
    print("IDs to Extract:", ids_to_extract)  # Debug output to verify the right file names are targeted

    # Extract the specific files from the .7z archive
    with py7zr.SevenZipFile(archive_path, mode='r') as archive:
        all_files = archive.getnames()
        all_files = [filename.replace('train/', '') for filename in all_files]
        print("All Files in Archive:", all_files)  # Debug output to see all file names in the archive

        # Filter to include only those files that are in the ids_to_extract
        files_to_extract = {f: None for f in all_files if f in ids_to_extract}
        print("Files to Extract:", files_to_extract)  # Debug output to see which files will be extracted
        with tqdm(total=len(files_to_extract), desc="Extracting files") as progress:
            if files_to_extract:
                # Map back to original file names with 'train/' for extraction
                original_files_to_extract = ['train/' + f for f in files_to_extract]
                archive.extract(targets=original_files_to_extract, path=output_folder)
                print(f"Extracted Files:{original_files_to_extract}")
            else:
                print("No matching files found for extraction.")


# Specify the path to your .7z file, the CSV file, and the output folder
archive_path = 'train.7z'
csv_path = 'trainLabels.csv'
output_folder = './train_ext'

extract_files_by_class(archive_path, csv_path, output_folder)