#!/usr/bin/env python3
"""
YOLO Training Example
This script demonstrates how to train a YOLO model using the person detection dataset
"""

import os
import yaml
from ultralytics import YOLO
from pathlib import Path


def get_dataset_config():
    """Get the person detection dataset configuration"""
    dataset_path = "/app/python/examples/yolo/person detection detection.v2i.yolov11"
    data_yaml_path = os.path.join(dataset_path, "data.yaml")

    # Update the data.yaml with absolute paths
    if os.path.exists(data_yaml_path):
        with open(data_yaml_path, "r") as f:
            config = yaml.safe_load(f)

        # Update paths to absolute paths
        config["train"] = os.path.join(dataset_path, "train/images")
        config["val"] = os.path.join(dataset_path, "valid/images")
        config["test"] = os.path.join(dataset_path, "test/images")

        print(f"📁 Dataset found at: {dataset_path}")
        print(f"📊 Classes: {config['names']}")
        print(f"🔢 Number of classes: {config['nc']}")

        # Count images in each split
        train_images = (
            len(os.listdir(config["train"])) if os.path.exists(config["train"]) else 0
        )
        val_images = (
            len(os.listdir(config["val"])) if os.path.exists(config["val"]) else 0
        )
        test_images = (
            len(os.listdir(config["test"])) if os.path.exists(config["test"]) else 0
        )

        print(f"📸 Training images: {train_images}")
        print(f"📸 Validation images: {val_images}")
        print(f"📸 Test images: {test_images}")

        return data_yaml_path, config
    else:
        print(f"❌ Dataset not found at: {data_yaml_path}")
        return None, None


def train_yolo_model():
    """Train a YOLO model with person detection dataset"""
    print("🚀 Starting YOLO training on person detection dataset...")

    # Get dataset configuration
    data_yaml_path, config = get_dataset_config()
    if not data_yaml_path:
        return None

    # Load a pre-trained YOLO model
    model = YOLO("yolov8n.pt")  # nano version for faster training

    # Training configuration
    training_params = {
        "data": data_yaml_path,
        "epochs": 50,  # Increased for better training
        "imgsz": 640,
        "batch": 16,
        "name": "person_detection_exp",
        "save": True,
        "plots": True,
        "device": "cuda" if os.system("nvidia-smi > /dev/null 2>&1") == 0 else "cpu",
        "patience": 20,  # Early stopping
        "save_period": 10,  # Save every 10 epochs
        "lr0": 0.01,  # Learning rate
        "optimizer": "AdamW",
        "augment": True,  # Data augmentation
        "mosaic": 1.0,  # Mosaic augmentation
        "mixup": 0.1,  # Mixup augmentation
    }

    print(f"📊 Training with parameters: {training_params}")

    try:
        # Start training
        results = model.train(**training_params)
        print("✅ Training completed successfully!")
        print(f"📁 Results saved to: runs/detect/person_detection_exp")

        # Print training metrics
        if hasattr(results, "results_dict"):
            metrics = results.results_dict
            print(f"📈 Final mAP50-95: {metrics.get('metrics/mAP50-95(B)', 'N/A')}")
            print(f"📈 Final mAP50: {metrics.get('metrics/mAP50(B)', 'N/A')}")

        return results
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        return None


def main():
    """Main training function"""
    print("=" * 60)
    print("🎯 YOLO Person Detection Training")
    print("=" * 60)

    # Check if ultralytics is available
    try:
        import ultralytics

        print(f"✅ Ultralytics version: {ultralytics.__version__}")
    except ImportError:
        print("❌ Ultralytics not found. Install with: pip install ultralytics")
        return

    # Check GPU availability
    try:
        import torch

        if torch.cuda.is_available():
            print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
            print(
                f"📊 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB"
            )
        else:
            print("⚠️  GPU not available, using CPU")
    except:
        print("⚠️  PyTorch not available")

    # Check dataset
    dataset_path = "/app/python/examples/yolo/person detection detection.v2i.yolov11"
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at: {dataset_path}")
        print("💡 Please ensure the person detection dataset is available")
        return

    # Run training
    results = train_yolo_model()

    if results:
        print("\n🎉 Person detection training completed!")
        print("📊 Check runs/detect/person_detection_exp/ for results")
        print("🔍 Use validate_yolo.py to evaluate the trained model")
        print("🎯 Use inference_yolo.py to test the model on new images")
    else:
        print("\n❌ Training failed")


if __name__ == "__main__":
    main()
