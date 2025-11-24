#!/usr/bin/env python3
"""
YOLO Inference Example
This script demonstrates how to run inference with a trained YOLO model on person detection
"""

import os
import cv2
import numpy as np
from ultralytics import YOLO
import time
from pathlib import Path
import argparse
import random


def get_dataset_info():
    """Get person detection dataset information"""
    dataset_path = "/app/python/examples/yolo/person detection detection.v2i.yolov11"

    if os.path.exists(dataset_path):
        print(f"📁 Dataset found at: {dataset_path}")

        # Check for data.yaml
        data_yaml_path = os.path.join(dataset_path, "data.yaml")
        if os.path.exists(data_yaml_path):
            import yaml

            with open(data_yaml_path, "r") as f:
                config = yaml.safe_load(f)
            print(f"📊 Classes: {config['names']}")
            print(f"🔢 Number of classes: {config['nc']}")
            return dataset_path, config

    return dataset_path, None


def load_model(model_path="runs/detect/person_detection_exp/weights/best.pt"):
    """Load YOLO model"""
    # Check if trained model exists
    if not os.path.exists(model_path):
        print(f"❌ Trained model not found: {model_path}")
        print("💡 Please run train_yolo.py first to train a model")
        print("🔄 Using pre-trained YOLOv8n for demonstration...")
        model_path = "yolov8n.pt"

    try:
        model = YOLO(model_path)
        print(f"✅ Model loaded: {model_path}")
        return model
    except Exception as e:
        print(f"❌ Failed to load model: {str(e)}")
        return None


def get_sample_images_from_dataset(dataset_path, num_samples=5):
    """Get sample images from the dataset"""
    sample_images = []

    # Try to get images from test set first
    test_images_path = os.path.join(dataset_path, "test/images")
    val_images_path = os.path.join(dataset_path, "valid/images")
    train_images_path = os.path.join(dataset_path, "train/images")

    # Check each directory for images
    for images_path in [test_images_path, val_images_path, train_images_path]:
        if os.path.exists(images_path):
            image_files = [
                f
                for f in os.listdir(images_path)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ]
            if image_files:
                # Get random sample
                sample_files = random.sample(
                    image_files, min(num_samples, len(image_files))
                )
                for filename in sample_files:
                    full_path = os.path.join(images_path, filename)
                    sample_images.append(full_path)
                break

    return sample_images


def create_sample_image():
    """Create a sample image with person-like shapes for testing"""
    # Create a sample image with rectangles that could represent people
    image = np.zeros((480, 640, 3), dtype=np.uint8)

    # Add background gradient
    for i in range(480):
        image[i, :] = [i // 3, i // 2, i // 4]

    # Add person-like rectangles (vertical, taller than wide)
    person_rects = [
        (100, 150, 180, 400),  # x1, y1, x2, y2
        (250, 200, 320, 450),
        (400, 120, 470, 380),
        (520, 180, 590, 430),
    ]

    for x1, y1, x2, y2 in person_rects:
        # Draw rectangle with person-like colors
        cv2.rectangle(image, (x1, y1), (x2, y2), (100, 150, 200), -1)
        # Add head
        head_center = ((x1 + x2) // 2, y1 - 15)
        cv2.circle(image, head_center, 12, (200, 180, 150), -1)

    # Add some text
    cv2.putText(
        image,
        "Person Detection Test",
        (150, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
    )

    # Save image
    os.makedirs("/app/test_images", exist_ok=True)
    cv2.imwrite("/app/test_images/person_detection_sample.jpg", image)

    return "/app/test_images/person_detection_sample.jpg"


def run_single_inference(model, image_path, conf_threshold=0.25):
    """Run inference on a single image"""
    print(f"🔍 Running inference on: {os.path.basename(image_path)}")

    try:
        # Start timing
        start_time = time.time()

        # Run inference
        results = model(image_path, conf=conf_threshold)

        # End timing
        end_time = time.time()
        inference_time = end_time - start_time

        print(f"⏱️  Inference time: {inference_time:.3f} seconds")
        print(f"🚀 FPS: {1.0 / inference_time:.1f}")

        # Process results
        for i, result in enumerate(results):
            boxes = result.boxes
            if len(boxes) > 0:
                print(f"👥 Detected {len(boxes)} persons:")
                for j, box in enumerate(boxes):
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())

                    print(
                        f"  Person {j + 1}: Confidence: {confidence:.3f}, "
                        f"Box: [{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]"
                    )
            else:
                print("👥 No persons detected")

        # Save results
        annotated_image = results[0].plot()
        result_filename = f"inference_result_{Path(image_path).stem}.jpg"
        result_path = f"/app/results/{result_filename}"
        os.makedirs("/app/results", exist_ok=True)
        cv2.imwrite(result_path, annotated_image)
        print(f"💾 Result saved to: {result_path}")

        return results, inference_time

    except Exception as e:
        print(f"❌ Inference failed: {str(e)}")
        return None, 0


def run_batch_inference(model, image_paths=None, conf_threshold=0.25):
    """Run inference on multiple images"""
    if image_paths is None:
        # Get sample images from dataset
        dataset_path, _ = get_dataset_info()
        image_paths = get_sample_images_from_dataset(dataset_path, num_samples=5)

    if not image_paths:
        print("❌ No images found for batch inference")
        return []

    print(f"📁 Running batch inference on {len(image_paths)} images")

    results = []
    total_time = 0
    total_detections = 0

    for i, image_path in enumerate(image_paths):
        print(
            f"\n🖼️  Processing image {i + 1}/{len(image_paths)}: {os.path.basename(image_path)}"
        )

        result, inference_time = run_single_inference(model, image_path, conf_threshold)

        if result:
            # Count detections
            num_detections = len(result[0].boxes) if result[0].boxes else 0
            total_detections += num_detections

            results.append(
                {
                    "image": image_path,
                    "result": result,
                    "inference_time": inference_time,
                    "detections": num_detections,
                }
            )
            total_time += inference_time

    if results:
        avg_time = total_time / len(results)
        avg_detections = total_detections / len(results)
        print(f"\n📊 Batch inference summary:")
        print(f"   Total images: {len(results)}")
        print(f"   Total time: {total_time:.3f} seconds")
        print(f"   Average time per image: {avg_time:.3f} seconds")
        print(f"   Average FPS: {1.0 / avg_time:.1f}")
        print(f"   Total persons detected: {total_detections}")
        print(f"   Average persons per image: {avg_detections:.1f}")

    return results


def run_realtime_inference(model, camera_id=0, conf_threshold=0.25):
    """Run real-time inference on camera feed"""
    print(f"📹 Starting real-time person detection on camera {camera_id}")
    print("Press 'q' to quit")

    try:
        # Open camera
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            print(f"❌ Failed to open camera {camera_id}")
            print("💡 Using sample images instead...")
            return run_batch_inference(model)

        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)

        frame_count = 0
        total_time = 0
        total_detections = 0

        while True:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to read frame from camera")
                break

            # Start timing
            start_time = time.time()

            # Run inference
            results = model(frame, conf=conf_threshold, verbose=False)

            # End timing
            end_time = time.time()
            inference_time = end_time - start_time
            total_time += inference_time
            frame_count += 1

            # Count detections
            num_detections = len(results[0].boxes) if results[0].boxes else 0
            total_detections += num_detections

            # Draw results on frame
            annotated_frame = results[0].plot()

            # Add FPS and detection info
            fps = 1.0 / inference_time if inference_time > 0 else 0
            avg_fps = frame_count / total_time if total_time > 0 else 0

            cv2.putText(
                annotated_frame,
                f"FPS: {fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.putText(
                annotated_frame,
                f"Persons: {num_detections}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.putText(
                annotated_frame,
                f"Avg FPS: {avg_fps:.1f}",
                (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            # Display frame
            cv2.imshow("YOLO Person Detection", annotated_frame)

            # Check for quit key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Cleanup
        cap.release()
        cv2.destroyAllWindows()

        if frame_count > 0:
            avg_fps = frame_count / total_time
            avg_detections = total_detections / frame_count
            print(f"\n📊 Real-time inference summary:")
            print(f"   Total frames: {frame_count}")
            print(f"   Total time: {total_time:.3f} seconds")
            print(f"   Average FPS: {avg_fps:.1f}")
            print(f"   Total persons detected: {total_detections}")
            print(f"   Average persons per frame: {avg_detections:.1f}")

    except Exception as e:
        print(f"❌ Real-time inference failed: {str(e)}")
        print("💡 Falling back to batch inference...")
        return run_batch_inference(model)


def main():
    """Main inference function"""
    parser = argparse.ArgumentParser(description="YOLO Person Detection Inference")
    parser.add_argument(
        "--model",
        type=str,
        default="runs/detect/person_detection_exp/weights/best.pt",
        help="Path to YOLO model",
    )
    parser.add_argument(
        "--image", type=str, default=None, help="Path to single image for inference"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Path to directory with images for batch inference",
    )
    parser.add_argument(
        "--camera", type=int, default=None, help="Camera ID for real-time inference"
    )
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument(
        "--samples", type=int, default=5, help="Number of sample images from dataset"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🔍 YOLO Person Detection Inference")
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
        else:
            print("⚠️  GPU not available, using CPU")
    except:
        print("⚠️  PyTorch not available")

    # Get dataset info
    dataset_path, config = get_dataset_info()
    if config:
        print(f"🎯 Detection classes: {config['names']}")

    # Load model
    model = load_model(args.model)
    if not model:
        return

    # Run inference based on arguments
    if args.camera is not None:
        # Real-time inference
        run_realtime_inference(model, args.camera, args.conf)
    elif args.dir:
        # Batch inference on directory
        image_files = [
            os.path.join(args.dir, f)
            for f in os.listdir(args.dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        run_batch_inference(model, image_files, args.conf)
    elif args.image:
        # Single image inference
        run_single_inference(model, args.image, args.conf)
    else:
        # Default: use dataset samples
        print("📝 No specific input, using dataset samples...")

        # Try to get sample images from dataset
        sample_images = get_sample_images_from_dataset(dataset_path, args.samples)

        if sample_images:
            print(f"📸 Using {len(sample_images)} sample images from dataset")
            run_batch_inference(model, sample_images, args.conf)
        else:
            print("📝 No dataset images found, creating sample image...")
            sample_image = create_sample_image()
            run_single_inference(model, sample_image, args.conf)

    print("\n🎉 Person detection inference completed!")
    print("📊 Check /app/results/ for inference results")


if __name__ == "__main__":
    main()
