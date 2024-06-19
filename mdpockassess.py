import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def list_replicate_files():
    txt_files = [file for file in os.listdir() if file.endswith(".txt")]
    for i, file in enumerate(txt_files, start=1):
        print(f"{i}) {file}")
    return txt_files

def select_replicates():
    txt_files = list_replicate_files()
    choices = input("Select your single or multi (replicates) txt file(s) [e.g. 1 OR 1,2,3]: ")
    choices = [int(choice.strip()) for choice in choices.split(",")]
    selected_replicates = [txt_files[i-1] for i in choices]
    return selected_replicates

def select_descriptors():
    descriptor_mapping = {
        '1': 'pock_volume',
        '2': 'pock_asa',
        '3': 'hydrophobicity_score',
        '4': 'polarity_score'
    }
    print("\n1) Volume")
    print("2) Solvent Accessible Surface Area")
    print("3) Hydrophobicity Score")
    print("4) Polarity Score")
    choices = input("Select a single or various descriptor(s) you want to plot [e.g. 2 OR 1,2,3,4]: ")
    choices = [descriptor_mapping[choice.strip()] for choice in choices.split(",")]
    return choices

def plot_normalized_descriptors(selected_replicates, selected_descriptors):
    data_frames = [pd.read_csv(replicate_file, delim_whitespace=True) for replicate_file in selected_replicates]

    if len(selected_descriptors) > 1:
        scaler = MinMaxScaler()
        normalized_data_frames = []
        for df in data_frames:
            normalized_df = df.copy()
            for descriptor in selected_descriptors:
                if descriptor in df.columns:
                    normalized_df[descriptor] = scaler.fit_transform(df[[descriptor]])
            normalized_data_frames.append(normalized_df)

        plt.figure(figsize=(10, 6))
        avg_df = pd.concat(normalized_data_frames).groupby('snapshot').mean()

        for descriptor in selected_descriptors:
            if descriptor in avg_df.columns:
                plt.plot(avg_df.index, avg_df[descriptor], label=descriptor)
    elif len(selected_replicates) > 1:
        plt.figure(figsize=(10, 6))
        avg_df = pd.concat(data_frames).groupby('snapshot').mean()

        for descriptor in selected_descriptors:
            if descriptor in avg_df.columns:
                plt.plot(avg_df.index, avg_df[descriptor], label=f"{descriptor} - Average")
    else:
        plt.figure(figsize=(10, 6))
        for df in data_frames:
            for descriptor in selected_descriptors:
                if descriptor in df.columns:
                    plt.plot(df['snapshot'], df[descriptor], label=f"{descriptor}")

    plt.xlabel('Snapshot')
    plt.ylabel('Normalized Value' if len(selected_descriptors) > 1 else 'Value')
    plt.title('Normalized Descriptors' if len(selected_descriptors) > 1 else 'Descriptors')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    selected_replicates = select_replicates()
    selected_descriptors = select_descriptors()
    plot_normalized_descriptors(selected_replicates, selected_descriptors)

