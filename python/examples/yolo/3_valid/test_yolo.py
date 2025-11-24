#!/usr/bin/env python3
"""
YOLO Testing Example
This script demonstrates how to test a trained YOLO model on person detection dataset
"""

import os
import yaml
from ultralytics import YOLO
import json
import time
from pathlib import Path


def get_dataset_config():
    """Get person detection dataset configuration"""
    dataset_path = "/app/python/examples/yolo/person detection detection.v2i.yolov11"
    data_yaml_path = os.path.join(dataset_path, "data.yaml")

    # Update data.yaml with absolute paths
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

        # Count images in test set
        test_images = (
            len(os.listdir(config["test"])) if os.path.exists(config["test"]) else 0
        )
        print(f"📸 Test images: {test_images}")

        return data_yaml_path, config
    else:
        print(f"❌ Dataset not found at: {data_yaml_path}")
        return None, None


def test_yolo_model(model_path="runs/detect/person_detection_exp/weights/best.pt"):
    """Test a YOLO model on person detection test dataset"""
    print("🧪 Starting YOLO testing on person detection dataset...")

    # Get dataset configuration
    data_yaml_path, config = get_dataset_config()
    if not data_yaml_path:
        return None

    # Check if model exists
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        print("💡 Please run train_yolo.py first to train a model")
        print("🔄 Using pre-trained model for demonstration...")
        model_path = "yolov8n.pt"

    # Load model
    try:
        model = YOLO(model_path)
        print(f"✅ Model loaded: {model_path}")
    except Exception as e:
        print(f"❌ Failed to load model: {str(e)}")
        return None

    # Test configuration
    test_params = {
        "data": data_yaml_path,
        "imgsz": 640,
        "batch": 16,
        "device": "cuda" if os.system("nvidia-smi > /dev/null 2>&1") == 0 else "cpu",
        "save_json": True,
        "project": "runs/detect",
        "name": "person_detection_test",
        "conf": 0.25,  # Confidence threshold
        "iou": 0.6,  # IoU threshold
        "max_det": 100,  # Maximum detections per image
    }

    print(f"📊 Testing with parameters: {test_params}")

    try:
        # Start timing
        start_time = time.time()

        # Run testing
        results = model.val(**test_params)

        # End timing
        end_time = time.time()
        inference_time = end_time - start_time

        print("✅ Testing completed successfully!")
        print(f"⏱️  Total inference time: {inference_time:.2f} seconds")

        # Calculate performance metrics
        if hasattr(results, "box"):
            metrics = results.box
            test_results = {
                "model_path": model_path,
                "dataset": "person detection detection.v2i.yolov11",
                "inference_time": inference_time,
                "map50": float(metrics.map50) if hasattr(metrics, "map50") else 0,
                "map50_95": float(metrics.map) if hasattr(metrics, "map") else 0,
                "precision": float(metrics.mp) if hasattr(metrics, "mp") else 0,
                "recall": float(metrics.mr) if hasattr(metrics, "mr") else 0,
                "device": test_params["device"],
                "confidence_threshold": test_params["conf"],
                "iou_threshold": test_params["iou"],
            }

            # Save test results
            os.makedirs("/app/results", exist_ok=True)
            with open("/app/results/person_detection_test_results.json", "w") as f:
                json.dump(test_results, f, indent=2)

            print(
                f"📊 Test results saved to: /app/results/person_detection_test_results.json"
            )
            return test_results

        return results
    except Exception as e:
        print(f"❌ Testing failed: {str(e)}")
        return None


def benchmark_model(model_path="runs/detect/person_detection_exp/weights/best.pt"):
    """Benchmark model performance on person detection"""
    print("🏁 Starting model benchmarking on person detection...")

    # Get dataset configuration
    data_yaml_path, config = get_dataset_config()
    if not data_yaml_path:
        return None

    try:
        model = YOLO(model_path)

        # Benchmark on different image sizes
        image_sizes = [320, 416, 512, 640, 832]
        benchmark_results = {}

        for imgsz in image_sizes:
            print(f"📏 Testing image size: {imgsz}x{imgsz}")

            try:
                start_time = time.time()
                # Run a quick inference test
                results = model.val(
                    data=data_yaml_path,
                    imgsz=imgsz,
                    batch=1,
                    device="cuda"
                    if os.system("nvidia-smi > /dev/null 2>&1") == 0
                    else "cpu",
                    verbose=False,
                    conf=0.25,
                    iou=0.6,
                )
                end_time = time.time()

                inference_time = end_time - start_time

                # Extract metrics
                if hasattr(results, "box"):
                    metrics = results.box
                    benchmark_results[imgsz] = {
                        "inference_time": inference_time,
                        "fps": 1.0 / inference_time if inference_time > 0 else 0,
                        "map50": float(metrics.map50)
                        if hasattr(metrics, "map50")
                        else 0,
                        "map50_95": float(metrics.map)
                        if hasattr(metrics, "map")
                        else 0,
                        "precision": float(metrics.mp) if hasattr(metrics, "mp") else 0,
                        "recall": float(metrics.mr) if hasattr(metrics, "mr") else 0,
                    }
                else:
                    benchmark_results[imgsz] = {
                        "inference_time": inference_time,
                        "fps": 1.0 / inference_time if inference_time > 0 else 0,
                        "error": "No metrics available",
                    }

                print(
                    f"⚡ {imgsz}x{imgsz}: {inference_time:.3f}s ({1.0 / inference_time:.1f} FPS)"
                )
                if "map50" in benchmark_results[imgsz]:
                    print(f"📈 mAP50: {benchmark_results[imgsz]['map50']:.3f}")

            except Exception as e:
                print(f"❌ Benchmark failed for size {imgsz}: {str(e)}")
                benchmark_results[imgsz] = {"error": str(e)}

        # Save benchmark results
        os.makedirs("/app/results", exist_ok=True)
        with open("/app/results/person_detection_benchmark.json", "w") as f:
            json.dump(benchmark_results, f, indent=2)

        print(
            "📊 Benchmark results saved to: /app/results/person_detection_benchmark.json"
        )

        # Print summary
        print("\n📊 Benchmark Summary:")
        for size, results in benchmark_results.items():
            if "fps" in results:
                print(
                    f"  {size}x{size}: {results['fps']:.1f} FPS, mAP50: {results.get('map50', 0):.3f}"
                )

        return benchmark_results

    except Exception as e:
        print(f"❌ Benchmarking failed: {str(e)}")
        return None


def analyze_test_set():
    """Analyze the test set characteristics"""
    print("📊 Analyzing person detection test set...")

    dataset_path = "/app/python/examples/yolo/person detection detection.v2i.yolov11"
    test_images_path = os.path.join(dataset_path, "test/images")
    test_labels_path = os.path.join(dataset_path, "test/labels")

    if not os.path.exists(test_images_path):
        print(f"❌ Test images not found: {test_images_path}")
        return

    # Get all test images
    image_files = [
        f
        for f in os.listdir(test_images_path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    print(f"📸 Total test images: {len(image_files)}")

    # Analyze labels if available
    if os.path.exists(test_labels_path):
        total_objects = 0
        images_with_objects = 0

        for image_file in image_files:
            label_file = os.path.splitext(image_file)[0] + ".txt"
            label_path = os.path.join(test_labels_path, label_file)

            if os.path.exists(label_path):
                with open(label_path, "r") as f:
                    lines = f.readlines()
                    num_objects = len(lines)
                    total_objects += num_objects
                    if num_objects > 0:
                        images_with_objects += 1

        print(f"🎯 Images with objects: {images_with_objects}")
        print(f"👥 Total objects in test set: {total_objects}")
        if images_with_objects > 0:
            print(
                f"📊 Average objects per image: {total_objects / images_with_objects:.2f}"
            )

    # Sample some image files for display
    print(f"\n📝 Sample test images:")
    for i, image_file in enumerate(image_files[:5]):
        print(f"  {i + 1}. {image_file}")


def main():
    """Main testing function"""
    print("=" * 60)
    print("🧪 YOLO Person Detection Testing")
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
        print("💡 Please ensure that person detection dataset is available")
        return

    # Analyze test set
    analyze_test_set()

    # Run testing
    print("\n" + "=" * 40)
    test_results = test_yolo_model()

    # Run benchmarking
    print("\n" + "=" * 40)
    benchmark_results = benchmark_model()

    if test_results or benchmark_results:
        print("\n🎉 Person detection testing completed!")
        print("📊 Check /app/results/ for detailed results")
        print("📈 Check runs/detect/person_detection_test/ for validation results")
    else:
        print("\n❌ Testing failed")


if __name__ == "__main__":
    main()
