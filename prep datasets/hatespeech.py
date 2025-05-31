import pandas as pd
import uuid

# Paths
master_path = "../datasets/master_dataset.csv"
labeled_path = "../datasets/labeled_data.csv"
save_path = "../datasets/master_dataset.csv"  # overwrite master

# Load datasets
master_df = pd.read_csv(master_path)
labeled_df = pd.read_csv(labeled_path)

# Map class to toxic categories for labeled_df
# Initialize all toxic-related columns with 0
for col in ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]:
    labeled_df[col] = 0

# Map 'class' to toxic labels
# Hate speech (0) -> toxic=1, severe_toxic=1, identity_hate=1 (optional)
labeled_df.loc[labeled_df["class"] == 0, ["toxic", "severe_toxic", "identity_hate"]] = 1

# Offensive language (1) -> toxic=1, obscene=1
labeled_df.loc[labeled_df["class"] == 1, ["toxic", "obscene"]] = 1

# Neither (2) -> all toxic columns remain 0

# Create 'id' column with unique UUIDs
labeled_df["id"] = [uuid.uuid4().hex[:16] for _ in range(len(labeled_df))]

# Rename tweet to comment_text to match master
labeled_df.rename(columns={"tweet": "comment_text"}, inplace=True)

# Add source column
labeled_df["source"] = "labeled_data"

# Add empty cyberbullying_type column
labeled_df["cyberbullying_type"] = ""

# Select only required columns in order matching master dataset
final_cols = ["id", "comment_text", "toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate", "source", "cyberbullying_type"]

# Ensure master_df has all columns, if not add missing columns with default values
for col in final_cols:
    if col not in master_df.columns:
        if col in ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]:
            master_df[col] = 0
        else:
            master_df[col] = ""

master_df = master_df[final_cols]
labeled_df = labeled_df[final_cols]

# Concatenate dataframes
combined_df = pd.concat([master_df, labeled_df], ignore_index=True)

# Save combined dataframe
combined_df.to_csv(save_path, index=False)

print(f"Combined dataset saved to: {save_path}")
