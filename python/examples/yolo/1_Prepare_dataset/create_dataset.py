import os
import glob
import shutil
import cv2
from shapely.geometry import Polygon
import numpy as np
import yaml
from tqdm import tqdm
from datetime import datetime
import time
import pandas as pd


DATASETPATH = "./data/dataset/datasets_joined"

normalization_to = 0
AREA_MIN = 28 * 28

mapper_class = {
    0: 0,  # bollo            ->  bollo
    1: 1,  # roce             ->  roce
    2: 1,  # pintura quitada  ->  roce
    3: 0,  # Deformacion      ->  bollo
    4: 4,  # cristal roto     ->  cristal roto
    5: 5,  # faro roto        ->  faro roto
    6: 1,  # oxido            ->  roce
}


start_time = time.time()


with open(f"{DATASETPATH}/data.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    data_names = data["names"]
    data_names.append("unknown")


for folder in ["clasification", "detector", "segmentation"]:
    for typ in ["train", "val", "test"]:
        if folder == "clasification":
            for class_name in data_names:
                os.makedirs(
                    f"./data/dataset/{folder}/{typ}/{class_name}", exist_ok=True
                )
        else:
            for img_lab in ["images", "labels"]:
                os.makedirs(f"./data/dataset/{folder}/{typ}/{img_lab}", exist_ok=True)


# copy data.yaml into to detector folder and segmentation folder
shutil.copy(f"{DATASETPATH}/data.yaml", "./data/dataset/detector/data.yaml")
shutil.copy(f"{DATASETPATH}/data.yaml", "./data/dataset/segmentation/data.yaml")


def get_datetime():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def save_image_label_detector(image_path, typ, new_lines, label_name):
    shutil.copy(image_path, f"./data/dataset/detector/{typ}/images/")
    with open(f"./data/dataset/detector/{typ}/labels/{label_name}", "w") as f:
        f.writelines(new_lines)


def save_image_label_segmentation(crop_image, label_name, typ, new_lines):
    cv2.imwrite(
        f"./data/dataset/segmentation/{typ}/images/{label_name}.jpg", crop_image
    )

    with open(f"./data/dataset/segmentation/{typ}/labels/{label_name}.txt", "w") as f:
        for line in new_lines:
            f.write(line)
            f.write("\n")


def save_image_clasification(image, filename, typ, class_name):
    cv2.imwrite(f"./data/dataset/clasification/{typ}/{class_name}/{filename}", image)


def save_real_image(image, filename, typ, polygon):
    image = np.array(image)

    polygon_points = [(int(x), int(y)) for x, y in polygon.exterior.coords]
    points = np.array(polygon_points, dtype=np.int32)
    cv2.polylines(image, [points], isClosed=True, color=(255, 0, 255), thickness=2)

    xmin, ymin, xmax, ymax = polygon.bounds
    cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 0, 255), 2)
    cv2.imwrite(f"./data/dataset/real/{typ}/images/{filename}", image)


#####################################################
# create detector dataset and clasification dataset
#####################################################
def xyxy_to_format_yolo(
    xmin, ymin: int, xmax: int, ymax: int, img_width: int, img_height: int
):
    x_center = ((xmin + xmax) / 2) / img_width
    y_center = ((ymin + ymax) / 2) / img_height
    width = (xmax - xmin) / img_width
    height = (ymax - ymin) / img_height

    return x_center, y_center, width, height


def polygon_to_points_for_graph(polygon):
    polygon_points = [(int(x), int(y)) for x, y in polygon.exterior.coords]
    points = np.array(polygon_points, dtype=np.int32)

    return points


# process dataset
fail_count = 0
dataset = []

for typ in tqdm(["train", "val", "test"], desc="Processing dataset", unit="dataset"):
    imageslist = glob.glob(f"{DATASETPATH}/{typ}/images/*")
    labelslist = glob.glob(f"{DATASETPATH}/{typ}/labels/*")

    for image_path in tqdm(
        imageslist, desc=f"Processing {typ} images", unit="images", leave=False
    ):
        image_name = os.path.basename(image_path)
        label_name = os.path.splitext(image_name)[0] + ".txt"
        label_folder = os.path.dirname(image_path).replace("images", "labels")

        if not os.path.join(label_folder, label_name) in labelslist:
            fail_count += 1
            continue

        label_index = labelslist.index(os.path.join(label_folder, label_name))
        label_path = labelslist[label_index]

        image = cv2.imread(image_path)
        image_width, image_height = image.shape[1], image.shape[0]

        classification_new_lines = []
        segmentation_new_lines = []
        with open(label_path, "r") as f:
            lines = f.readlines()

            for i, annotation in enumerate(lines):
                class_id, *segmentation_points = map(float, annotation.strip().split())

                try:
                    class_id = mapper_class[int(class_id)]
                    class_name = data_names[class_id]
                except:
                    class_name = "unknown"

                if True:
                    # convert segmentation points to yolo format bounding box
                    points_array = np.array(segmentation_points, np.float32)
                    points_array_normalized = points_array.reshape((-1, 2))
                    points_array = (
                        points_array_normalized * np.array([image_width, image_height])
                    ).astype(np.int32)

                    original_polygon = Polygon(points_array)
                    xmin, ymin, xmax, ymax = original_polygon.bounds
                    polygon_points = [
                        (int(x), int(y)) for x, y in original_polygon.exterior.coords
                    ]

                    x_center, y_center, width, height = xyxy_to_format_yolo(
                        xmin, ymin, xmax, ymax, image_width, image_height
                    )
                    yolo_data = (
                        f"{normalization_to} {x_center} {y_center} {width} {height}\n"
                    )

                    dataset.append(
                        {
                            "image_path": image_path,
                            "label_path": label_path,
                            "class_id": class_id,
                            "class_name": class_name,
                            "image_center": (image_width / 2, image_height / 2),
                            "width": image_width,
                            "height": image_height,
                            "yolo_data": yolo_data,
                            "area": original_polygon.area,
                            "polygon_points": polygon_points,
                            "bbox": (xmin, ymin, xmax, ymax),
                        }
                    )

                    cropped_image = image[int(ymin) : int(ymax), int(xmin) : int(xmax)]
                    crop_width, crop_height = (
                        cropped_image.shape[1],
                        cropped_image.shape[0],
                    )

                    if crop_width * crop_height < AREA_MIN:
                        continue

                    polygon_coords = np.array(polygon_points, dtype=np.int32)
                    transformed_coords = [
                        (x - xmin, y - ymin) for x, y in polygon_coords
                    ]
                    cropped_image_transformed_polygon = Polygon(transformed_coords)

                    cropped_image_width, cropped_image_height = (
                        cropped_image.shape[1],
                        cropped_image.shape[0],
                    )
                    cropped_image_points = polygon_to_points_for_graph(
                        cropped_image_transformed_polygon
                    )
                    cropped_image_points_normalized = cropped_image_points / np.array(
                        [cropped_image_width, cropped_image_height]
                    )
                    cropped_image_points_normalized_list = (
                        cropped_image_points_normalized.flatten().tolist()
                    )

                    segmentation_new_lines.append(
                        f"{class_id} {' '.join(map(str, cropped_image_points_normalized_list))}"
                    )

                classification_new_lines.append(yolo_data)

                save_image_clasification(
                    cropped_image,
                    f"{os.path.splitext(image_name)[0]}_{i}.jpg",
                    typ,
                    class_name,
                )

                save_image_label_segmentation(
                    cropped_image,
                    f"{os.path.splitext(image_name)[0]}_{i}",
                    typ,
                    segmentation_new_lines,
                )

        save_image_label_detector(image_path, typ, classification_new_lines, label_name)


dataset = pd.DataFrame(dataset)
dataset.to_csv("./data/dataset/dataset.csv", index=False)


end_time = time.time()

elapsed_time = end_time - start_time

results = {
    "datetime": get_datetime(),
    "fail_count": fail_count,
    "elapsed_time": f"{elapsed_time:.2f} seconds",
}

with open("./data/dataset/results.yaml", "w") as f:
    yaml.dump(results, f)
