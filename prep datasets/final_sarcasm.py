import pandas as pd

# Load Sarcasm.csv and keep only 'tweet' and 'sarcasm' columns
sarcasm_df = pd.read_csv(r'datasets/Sarcasm.csv', usecols=['tweet', 'sarcasm'])

# Load clean_sarcasm.csv and keep only 'comment' and 'label' columns
clean_df = pd.read_csv(r'datasets/clean_sarcasm.csv', usecols=['comment', 'label'])

# Rename columns in clean_df to match sarcasm_df
clean_df.rename(columns={'comment': 'tweet', 'label': 'sarcasm'}, inplace=True)

# Combine the two DataFrames
combined_df = pd.concat([sarcasm_df, clean_df], ignore_index=True)

# Save the combined dataset
combined_df.to_csv('datasets/combined_sarcasm1.csv', index=False)

print("Final sarcasm dataset saved to 'datasets/combined_sarcasm1.csv'")

