import os
import glob
import shutil
import tempfile
import zipfile
from collections import defaultdict

import numpy as np
import pandas as pd
from tqdm import tqdm
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("datasets.csv")

datasets_list = df["name"].tolist()
datasets_list = [x for x in datasets_list if isinstance(x, str)]


print(f"Datasets to join: {datasets_list}")

print("*" * 50)

with tempfile.TemporaryDirectory() as tmpdirname:
    os.makedirs(f"{tmpdirname}/datasets/", exist_ok=True)

    datasets_names = defaultdict(list)

    all_info_datasets = {}

    categories_list = []

    for dataset in tqdm(datasets_list, desc="Extracting datasets"):
        folder = os.path.join(tmpdirname, dataset[:-4])
        os.makedirs(folder, exist_ok=True)

        with zipfile.ZipFile(dataset, "r") as zip_ref:
            zip_ref.extractall(folder)

        # valid if into of f"{tmpdirname}/datasets/" there aren't data.yaml file, if not, copy it
        if not os.path.exists(f"{tmpdirname}/datasets/data.yaml"):
            shutil.copy(
                f"{folder}/data.yaml",
                f"{tmpdirname}/datasets/data.yaml",
            )

        if os.path.exists(f"{folder}/data.yaml"):
            with open(f"{folder}/data.yaml", "r", encoding="utf-8") as f:
                datasets_names_ = yaml.safe_load(f)
                datasets_names_ = datasets_names_["names"]

                datasets_names[dataset.split(".")[0]] = datasets_names_

        TOTAL_IMAGES = 0
        for train_test_valid in ["train", "test", "val"]:
            files_list = glob.glob(f"{folder}/{train_test_valid}/images/*")
            TOTAL_IMAGES += len(files_list)

        all_info_datasets[os.path.basename(dataset)] = {
            "total_images": TOTAL_IMAGES,
            "histogram": defaultdict(int),
        }

    for train_test_valid in ["train", "test", "val"]:
        for images_labels in ["images", "labels"]:
            os.makedirs(
                f"{tmpdirname}/datasets/{train_test_valid}/{images_labels}",
                exist_ok=True,
            )

    real_names = []
    for dataset_id, dataset in tqdm(enumerate(datasets_list), total=len(datasets_list)):
        dataset_name = dataset[:-4]

        NAMES_FOUND = True
        if dataset_id == 0:
            # capture the names of the dataset
            real_names = datasets_names[dataset_name]
        elif dataset_id > 0:
            # evaluate if the names of the datasets are the same
            # all names of the real_names must be in the names_datasets[dataset_name]
            # with same order
            # it's possible that the names_datasets[dataset_name] has more names than real_names

            dataset_names = datasets_names[dataset_name]

            for name_index, name in enumerate(dataset_names):
                real_name_index = real_names.index(name) if name in real_names else -1
                if real_name_index != name_index:
                    NAMES_FOUND = False
                    break

        if not NAMES_FOUND:
            # print(f"Error: the names of the dataset {dataset_name} are different")
            continue

        # print(f"Joining dataset {dataset_name}")

        for train_test_valid in ["train", "test", "val"]:
            for images_labels in ["images", "labels"]:
                files_list = glob.glob(
                    f"{tmpdirname}/{dataset_name}/{train_test_valid}/{images_labels}/*"
                )

                for file in tqdm(
                    files_list, desc=f"Copying {dataset_name}", leave=False
                ):
                    dirname = os.path.dirname(file)
                    FILENAME = f"{dataset_name}_{os.path.basename(file)}"

                    shutil.copy(
                        file,
                        f"{tmpdirname}/datasets/{train_test_valid}/{images_labels}/{FILENAME}",
                    )
                    # print(
                    #     f"Copy {file} to {tmpdirname}/datasets/{train_test_valid}/"
                    #     f"{images_labels}/{filename}"
                    # )

                    if images_labels == "labels":
                        with open(file, "r") as f:
                            data_lines = f.readlines()

                            for data_line in data_lines:
                                data_line = data_line.strip()
                                if data_line:
                                    data_line = data_line.split(" ")
                                    data_class = int(data_line[0])

                                    if data_class not in categories_list:
                                        categories_list.append(data_class)

                                    all_info_datasets[os.path.basename(dataset)][
                                        "histogram"
                                    ][data_class] += 1

    shutil.copy("datasets.csv", f"{tmpdirname}/datasets/datasets.csv")

    # graph the histogram
    if True:
        fig, axs = plt.subplots(1, 2, figsize=(12, 12))

        labels = list(all_info_datasets.keys())
        sizes = [all_info_datasets[label]["total_images"] for label in labels]
        sizes = [round(x / sum(sizes) * 100, 2) for x in sizes]

        indexes = range(len(labels))

        categories_sum = defaultdict(int)

        data_values_list = []
        for label_id, label in enumerate(labels):

            category_data_dict = {"id": label_id, "dataset": label}

            for category in categories_list:
                if category not in all_info_datasets[label]["histogram"]:
                    VALUE = 0
                else:
                    VALUE = all_info_datasets[label]["histogram"][category]

                categories_sum[category] += VALUE

                category_data_dict[category] = categories_sum[category]

            data_values_list.append(category_data_dict)

        data_df = pd.DataFrame(data_values_list, index=indexes, columns=categories_list)
        data_df.to_csv(f"{tmpdirname}/datasets/data.csv")
        data_df.to_csv("data.csv")

        # left graph
        colors_list = sns.color_palette("pastel")[0 : len(labels)]
        axs[0].pie(
            sizes, labels=indexes, colors=colors_list, autopct="%1.1f%%", startangle=140
        )
        axs[0].set_title("Images distribution")

        # righ graph
        sns.lineplot(data=data_df, palette="tab10", linewidth=2.5, ax=axs[1])
        axs[1].set_title("Categories distribution")
        axs[1].set_xlabel("Categories")
        axs[1].set_ylabel("Count of categories")

        plt.subplots_adjust(wspace=0.5)
        plt.savefig(f"{tmpdirname}/datasets/datasets_joined.png")
        shutil.copy(f"{tmpdirname}/datasets/datasets_joined.png", "datasets_joined.png")

    # compress the datasets path into a zip file with the name "datasets.zip"
    # in the directory where the script is executed

    print("*" * 50)
    print("Compressing datasets into a zip file")

    CWD = os.getcwd()

    os.chdir(tmpdirname)

    shutil.make_archive("datasets_joined", "zip", "datasets")

    os.chdir(CWD)
    shutil.move(f"{tmpdirname}/datasets_joined.zip", "datasets_joined.zip")

    print("Done")
