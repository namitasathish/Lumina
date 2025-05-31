import pandas as pd
import os

def clean_sarcasm_dataset(input_path, output_path):
    """
    Cleans the sarcasm dataset by selecting required columns, handling missing values,
    and saving to a new file.
    """
    # Columns to retain
    required_columns = [
        'label', 'comment', 'author', 'subreddit',
        'score', 'ups', 'downs', 'date', 'created_utc', 'parent_comment'
    ]
    
    # Load dataset
    try:
        df = pd.read_csv(input_path)
        print(f"Loaded dataset with shape: {df.shape}")
    except FileNotFoundError:
        print(f"File not found at {input_path}")
        return

    # Keep only required columns
    df = df[required_columns]

    # Drop rows with missing comment or label
    df.dropna(subset=['comment', 'label'], inplace=True)

    # Fill missing parent_comment with empty string
    df['parent_comment'].fillna("", inplace=True)

    # Optional: Reset index
    df.reset_index(drop=True, inplace=True)

    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to: {output_path}")


if __name__ == "__main__":
    # Input and output file paths
    input_csv_path = "datasets/reddit sarcasm/train-balanced-sarcasm.csv"
    output_csv_path = "datasets/clean_sarcasm.csv"

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    clean_sarcasm_dataset(input_csv_path, output_csv_path)
