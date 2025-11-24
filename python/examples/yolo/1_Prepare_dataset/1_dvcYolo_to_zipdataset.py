import os
import shutil
import subprocess
import random
import glob
import zipfile
import sys
import json
import xml.etree.ElementTree as ET
from PIL import Image

def download_dvc(dvc_files):
    """Download the content of the specified .dvc files using Docker.

    Args:
        dvc_files (list): List of .dvc file names to download.
    """
    current_dir = os.getcwd()
    # Assuming the repo root is the parent of 'projects'
    if 'projects' in current_dir:
        repo_root = current_dir.split('projects')[0].rstrip('/')
        relative_path = os.path.relpath(current_dir, repo_root)
    else:
        relative_path = os.path.basename(current_dir)  # fallback
    for dvc_file in dvc_files:
        dataset_dir = dvc_file.replace('.dvc', '')
        if os.path.exists(dataset_dir):
            print(f"Data for {dvc_file} already exists, skipping download.")
            continue
        if os.path.exists(dvc_file):
            print(f"Descargando {dvc_file}")
            cmd = f"dvc pull {relative_path}/{dvc_file}'"
            subprocess.run(cmd, shell=True, check=True)
        else:
            print(f"Archivo {dvc_file} no encontrado, saltando.")

def detect_task_type(dataset_dirs):
    """Detect the task type (classification or detection) based on the presence of .txt, .json, or .xml files.

    Args:
        dataset_dirs (list): List of dataset directory paths.

    Returns:
        str: 'classification' or 'detection'.
    """
    for dataset_dir in dataset_dirs:
        if os.path.exists(dataset_dir):
            txt_files = glob.glob(os.path.join(dataset_dir, '*.txt'))
            json_files = glob.glob(os.path.join(dataset_dir, '*.json'))
            xml_files = glob.glob(os.path.join(dataset_dir, '*.xml'))
            print(f"En {dataset_dir}: txt_files={len(txt_files)}, json_files={len(json_files)}, xml_files={len(xml_files)}")
            if txt_files or json_files or xml_files:
                return 'detection'
    return 'classification'

def get_image_paths_by_class(dataset_dirs):
    """Collect image paths organized by class for classification.

    Args:
        dataset_dirs (list): List of dataset directory paths.

    Returns:
        dict: Dictionary with class names as keys and lists of image paths as values.
    """
    class_images = {}
    for dataset_dir in dataset_dirs:
        if os.path.exists(dataset_dir):
            # If the directory is numeric, assume all images belong to that class
            if os.path.basename(dataset_dir).isdigit():
                class_name = os.path.basename(dataset_dir)
                if class_name not in class_images:
                    class_images[class_name] = []
                images = glob.glob(os.path.join(dataset_dir, '*.png')) + glob.glob(os.path.join(dataset_dir, '*.jpeg')) + glob.glob(os.path.join(dataset_dir, '*.jpg'))
                class_images[class_name].extend(images)
            else:
                # Search for numeric subfolders
                has_subfolders = False
                for root, dirs, files in os.walk(dataset_dir):
                    for dir_name in dirs:
                        if dir_name.isdigit():  # Assuming numeric classes
                            has_subfolders = True
                            class_path = os.path.join(root, dir_name)
                            if dir_name not in class_images:
                                class_images[dir_name] = []
                            images = glob.glob(os.path.join(class_path, '*.png')) + glob.glob(os.path.join(class_path, '*.jpeg')) + glob.glob(os.path.join(class_path, '*.jpg'))
                            class_images[dir_name].extend(images)
                # If no subfolders, assume all images belong to class '0'
                if not has_subfolders:
                    images = glob.glob(os.path.join(dataset_dir, '*.png')) + glob.glob(os.path.join(dataset_dir, '*.jpeg')) + glob.glob(os.path.join(dataset_dir, '*.jpg'))
                    if images:
                        class_images['0'] = images
    return class_images

def convert_xml_to_txt(dataset_dir):
    """Convert .xml to .txt in YOLO detection format (assuming VOC-like format).

    Args:
        dataset_dir (str): Path to the dataset directory.

    Returns:
        list: List of detected categories.
    """
    xml_files = glob.glob(os.path.join(dataset_dir, '*.xml'))
    if not xml_files:
        return []
    
    categories = set()
    # First pass to collect categories
    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            objects = root.findall('object')
            for obj in objects:
                name_elem = obj.find('name')
                if name_elem is not None and name_elem.text is not None:
                    categories.add(name_elem.text)
        except Exception as e:
            print(f"Error in first pass {xml_file}: {e}")
    
    categories = sorted(list(categories))
    category_to_id = {cat: i for i, cat in enumerate(categories)}
    
    # Second pass to convert
    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except Exception as e:
            print(f"Error parsing {xml_file}: {e}")
            continue
        
        # Get image size
        size = root.find('size')
        if size is None:
            continue
        width_elem = size.find('width')
        height_elem = size.find('height')
        if width_elem is None or height_elem is None or width_elem.text is None or height_elem.text is None:
            continue
        width = int(width_elem.text)
        height = int(height_elem.text)
        
        txt_path = xml_file.replace('.xml', '.txt')
        with open(txt_path, 'w') as f:
            for obj in root.findall('object'):
                name_elem = obj.find('name')
                if name_elem is None or name_elem.text is None:
                    continue
                name = name_elem.text
                class_id = category_to_id[name]
                
                bndbox = obj.find('bndbox')
                if bndbox is None:
                    continue
                try:
                    xmin = float(bndbox.find('xmin').text)
                    ymin = float(bndbox.find('ymin').text)
                    xmax = float(bndbox.find('xmax').text)
                    ymax = float(bndbox.find('ymax').text)
                except (AttributeError, ValueError, TypeError):
                    continue
                
                # Convert to YOLO format
                x_center = (xmin + xmax) / 2 / width
                y_center = (ymin + ymax) / 2 / height
                w = (xmax - xmin) / width
                h = (ymax - ymin) / height
                
                line = f"{class_id} {x_center} {y_center} {w} {h}\n"
                f.write(line)
    
    return sorted(list(categories))

def convert_json_to_txt(dataset_dir):
    """Convert .json to .txt in YOLO segmentation format.

    Args:
        dataset_dir (str): Path to the dataset directory.

    Returns:
        list: List of detected categories.
    """
    json_files = glob.glob(os.path.join(dataset_dir, '*.json'))
    if not json_files:
        return []
    json_file = json_files[0]  # Assume one JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    categories = set()
    json_filenames = set()
    for key, value in data.items():
        json_filenames.add(value['filename'])
        for region in value.get('regions', []):
            categories.add(region['region_attributes']['category'])
    categories = sorted(list(categories))
    category_to_id = {cat: i for i, cat in enumerate(categories)}
    print(f"Imágenes en JSON: {len(json_filenames)}")
    
    for key, value in data.items():
        filename = value['filename']
        img_path = os.path.join(dataset_dir, filename)
        if os.path.exists(img_path):
            regions = value.get('regions', [])
            print(f"Procesando {filename}, regions: {len(regions)}")
            img = Image.open(img_path)
            width, height = img.size
            txt_path = os.path.splitext(img_path)[0] + '.txt'
            try:
                with open(txt_path, 'w') as f:
                    for region in regions:
                        shape = region['shape_attributes']
                        if shape['name'] == 'polygon':
                            xs = shape['all_points_x']
                            ys = shape['all_points_y']
                            category = region['region_attributes']['category']
                            class_id = category_to_id[category]
                            coords = []
                            for x, y in zip(xs, ys):
                                coords.extend([x / width, y / height])
                            line = f"{class_id} " + " ".join(map(str, coords))
                            f.write(line + '\n')
            except PermissionError:
                print(f"Permiso denegado para escribir {txt_path}, saltando.")
    return categories

def get_image_paths_for_detection(dataset_dirs):
    """Collect image-annotation pairs for detection, converting .json if necessary.

    Args:
        dataset_dirs (list): List of dataset directory paths.

    Returns:
        tuple: (list of (img_path, txt_path) pairs, list of temp dirs, list of categories).
    """
    image_annotation_pairs = []
    temp_dirs = []
    all_categories = set()
    for dataset_dir in dataset_dirs:
        if os.path.exists(dataset_dir):
            # Copy to temp dir with permissions
            temp_dir = dataset_dir + '_temp'
            shutil.copytree(dataset_dir, temp_dir)
            os.chmod(temp_dir, 0o755)
            for root, dirs, files in os.walk(temp_dir):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o755)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o644)
            temp_dirs.append(temp_dir)

            # Convert .json to .txt if present
            categories = convert_json_to_txt(temp_dir)
            all_categories.update(categories)
            
            # Convert .xml to .txt if present
            categories_xml = convert_xml_to_txt(temp_dir)
            all_categories.update(categories_xml)
            
            images = glob.glob(os.path.join(temp_dir, '*.png')) + glob.glob(os.path.join(temp_dir, '*.jpeg')) + glob.glob(os.path.join(temp_dir, '*.jpg'))
            print(f"Imágenes encontradas: {len(images)}")
            for img_path in images:
                base = os.path.splitext(img_path)[0]
                txt_path = base + '.txt'
                # Create empty .txt if it does not exist
                if not os.path.exists(txt_path):
                    try:
                        with open(txt_path, 'w') as f:
                            pass  # Empty
                    except PermissionError:
                        print(f"Permission denied to create {txt_path}")
                        continue
                image_annotation_pairs.append((img_path, txt_path))
    
    return image_annotation_pairs, temp_dirs, sorted(list(all_categories))

def split_data(class_images, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    """Split the data into train, validation, and test sets.

    Args:
        class_images (dict): Dictionary with class names and image paths.
        train_ratio (float): Ratio for training set.
        val_ratio (float): Ratio for validation set.
        test_ratio (float): Ratio for test set.

    Returns:
        tuple: (train_data, val_data, test_data) dictionaries.
    """
    train_data = {}
    val_data = {}
    test_data = {}

    for class_name, images in class_images.items():
        random.shuffle(images)
        n_total = len(images)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)
        n_test = n_total - n_train - n_val

        train_data[class_name] = images[:n_train]
        val_data[class_name] = images[n_train:n_train + n_val]
        test_data[class_name] = images[n_train + n_val:]

    return train_data, val_data, test_data

def organize_folders(split_data, base_dir='yolo_dataset'):
    """Organize files into train/val/test folders with subfolders by class for classification.

    Args:
        split_data (dict): Dictionary with 'train', 'val', 'test' and their data.
        base_dir (str): Base directory for the dataset.
    """
    for split_name, class_data in split_data.items():
        split_dir = os.path.join(base_dir, split_name)
        os.makedirs(split_dir, exist_ok=True)
        for class_name, images in class_data.items():
            class_dir = os.path.join(split_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)
            for img_path in images:
                shutil.copy(img_path, class_dir)

def organize_for_detection(split_data, base_dir='yolo_dataset'):
    """Organize images and annotations into train/val/test folders for detection.

    Args:
        split_data (dict): Dictionary with 'train', 'val', 'test' and their pairs.
        base_dir (str): Base directory for the dataset.
    """
    for split_name, pairs in split_data.items():
        split_dir = os.path.join(base_dir, split_name)
        images_dir = os.path.join(split_dir, 'images')
        labels_dir = os.path.join(split_dir, 'labels')
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        for img_path, txt_path in pairs:
            shutil.copy(img_path, images_dir)
            shutil.copy(txt_path, labels_dir)

def create_data_yaml(base_dir='yolo_dataset', classes=None):
    """Create data.yaml for YOLO detection.

    Args:
        base_dir (str): Base directory for the dataset.
        classes (list): List of class names.
    """
    if classes is None:
        classes = ['0', '45', '90', '135', '180', '225', '270', '315']  # Adjust according to the project
    yaml_content = f"""train: {os.path.join(base_dir, 'train', 'images')}
val: {os.path.join(base_dir, 'val', 'images')}
test: {os.path.join(base_dir, 'test', 'images')}

nc: {len(classes)}
names: {classes}
"""
    with open(os.path.join(base_dir, 'data.yaml'), 'w') as f:
        f.write(yaml_content)

def create_zip(base_dir='yolo_dataset', zip_name='yolo_dataset.zip'):
    """Create a zip archive of the prepared dataset directory.

    Args:
        base_dir (str): Base directory to zip.
        zip_name (str): Name of the zip file.
    """
    shutil.make_archive(zip_name.replace('.zip', ''), 'zip', base_dir)
    print(f"Zip creado: {zip_name}")

def cleanup(dataset_dirs, temp_dirs=None):
    """Remove the downloaded dataset directories and temporary directories.

    Args:
        dataset_dirs (list): List of dataset directories to remove.
        temp_dirs (list): List of temporary directories to remove.
    """
    all_dirs = dataset_dirs + (temp_dirs or [])
    for d in all_dirs:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"Eliminado: {d}")
            except Exception as e:
                print(f"Error eliminando {d}: {e}")

def main():
    # Choose .dvc files to download
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        target_dir = sys.argv[1]
        os.chdir(target_dir)
        dvc_files = sys.argv[2:] if len(sys.argv) > 2 else glob.glob('*.dvc')
    else:
        dvc_files = sys.argv[1:] if sys.argv[1:] else glob.glob('*.dvc')
        if not dvc_files:
            print("No .dvc files specified, downloading all.")
            dvc_files = glob.glob('*.dvc')

    # Download data
    try:
        download_dvc(dvc_files)
    except subprocess.CalledProcessError:
        print("Download failed, assuming data is already present.")

    # Find dataset directories corresponding to downloaded .dvc files
    dataset_dirs = [f.replace('.dvc', '') for f in dvc_files if os.path.isdir(f.replace('.dvc', ''))]
    print(f"Dataset dirs: {dataset_dirs}")

    # Detect task type
    task_type = detect_task_type(dataset_dirs)
    print(f"Detected task type: {task_type}")

    temp_dirs = []
    if task_type == 'classification':
        # Collect images by class
        class_images = get_image_paths_by_class(dataset_dirs)
        print(f"Class images: {list(class_images.keys())}")

        # Split data
        train_data, val_data, test_data = split_data(class_images)

        # Organize into folders
        organize_folders({'train': train_data, 'val': val_data, 'test': test_data})
    elif task_type == 'detection':
        # Collect image-annotation pairs
        pairs, temp_dirs, categories = get_image_paths_for_detection(dataset_dirs)
        print(f"Image-annotation pairs: {len(pairs)}")
        print(f"Detected classes: {categories}")

        # Split data
        random.shuffle(pairs)
        n_total = len(pairs)
        n_train = int(n_total * 0.8)
        n_val = int(n_total * 0.1)
        n_test = n_total - n_train - n_val

        train_pairs = pairs[:n_train]
        val_pairs = pairs[n_train:n_train + n_val]
        test_pairs = pairs[n_train + n_val:]

        # Organize into folders
        organize_for_detection({'train': train_pairs, 'val': val_pairs, 'test': test_pairs})

        # Create data.yaml
        create_data_yaml(classes=categories)

    # Create zip
    base_dir = 'yolo_dataset'
    create_zip(base_dir=base_dir)

    # Remove the yolo_dataset folder after zipping
    if os.path.exists(base_dir):
        try:
            shutil.rmtree(base_dir)
            print(f"Eliminado: {base_dir}")
        except Exception as e:
            print(f"Error eliminando {base_dir}: {e}")

    # Clean up downloaded directories only
    cleanup(dataset_dirs, temp_dirs)

    print("Process completed: download, conversion, zip, and cleanup.")

if __name__ == '__main__':
    main()