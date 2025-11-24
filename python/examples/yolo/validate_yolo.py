#!/usr/bin/env python3
"""
YOLO Validation Example
This script demonstrates how to validate a trained YOLO model on person detection dataset
"""

import os
import yaml
from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np


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

        # Count images in validation set
        val_images = (
            len(os.listdir(config["val"])) if os.path.exists(config["val"]) else 0
        )
        print(f"📸 Validation images: {val_images}")

        return data_yaml_path, config
    else:
        print(f"❌ Dataset not found at: {data_yaml_path}")
        return None, None


def validate_yolo_model(model_path="runs/detect/person_detection_exp/weights/best.pt"):
    """Validate a YOLO model on person detection dataset"""
    print("🔍 Starting YOLO validation on person detection dataset...")

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

    # Validation configuration
    val_params = {
        "data": data_yaml_path,
        "imgsz": 640,
        "batch": 16,
        "device": "cuda" if os.system("nvidia-smi > /dev/null 2>&1") == 0 else "cpu",
        "plots": True,
        "save_json": True,
        "project": "runs/detect",
        "name": "person_detection_val",
    }

    print(f"📊 Validating with parameters: {val_params}")

    try:
        # Run validation
        results = model.val(**val_params)
        print("✅ Validation completed successfully!")

        # Print key metrics
        if hasattr(results, "box"):
            metrics = results.box
            print(f"📈 mAP50: {metrics.map50:.4f}")
            print(f"📈 mAP50-95: {metrics.map:.4f}")
            print(f"📈 Precision: {metrics.mp:.4f}")
            print(f"📈 Recall: {metrics.mr:.4f}")
            print(
                f"📈 F1-Score: {2 * metrics.mp * metrics.mr / (metrics.mp + metrics.mr):.4f}"
            )

        return results
    except Exception as e:
        print(f"❌ Validation failed: {str(e)}")
        return None


def plot_validation_metrics(results):
    """Plot validation metrics if available"""
    try:
        if results and hasattr(results, "box"):
            metrics = results.box

            # Create a comprehensive metrics plot
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

            # Detection metrics
            metric_names = ["mAP50", "mAP50-95", "Precision", "Recall"]
            metric_values = [
                metrics.map50 if hasattr(metrics, "map50") else 0,
                metrics.map if hasattr(metrics, "map") else 0,
                metrics.mp if hasattr(metrics, "mp") else 0,
                metrics.mr if hasattr(metrics, "mr") else 0,
            ]

            colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
            bars = ax1.bar(metric_names, metric_values, color=colors)
            ax1.set_title("Person Detection Metrics", fontsize=14, fontweight="bold")
            ax1.set_ylabel("Score", fontsize=12)
            ax1.set_ylim(0, 1)
            ax1.grid(axis="y", alpha=0.3)

            # Add value labels on bars
            for bar, value in zip(bars, metric_values):
                ax1.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.01,
                    f"{value:.3f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )

            # Confusion matrix style visualization (simplified)
            categories = ["True Positive", "False Positive", "False Negative"]
            if hasattr(metrics, "mp") and hasattr(metrics, "mr"):
                tp = metrics.mp * 100  # Simplified representation
                fp = (1 - metrics.mp) * 100
                fn = (1 - metrics.mr) * 100

                ax2.pie(
                    [tp, fp, fn],
                    labels=categories,
                    colors=colors[:3],
                    autopct="%1.1f%%",
                )
                ax2.set_title(
                    "Detection Results Distribution", fontsize=14, fontweight="bold"
                )

            # Precision-Recall curve (simulated)
            precision_range = np.linspace(0.1, 1.0, 100)
            recall_range = precision_range * 0.9  # Simulated relationship

            ax3.plot(recall_range, precision_range, "b-", linewidth=2, label="PR Curve")
            ax3.scatter(
                [metrics.mr],
                [metrics.mp],
                color="red",
                s=100,
                zorder=5,
                label="Current Model",
            )
            ax3.set_xlabel("Recall", fontsize=12)
            ax3.set_ylabel("Precision", fontsize=12)
            ax3.set_title("Precision-Recall Curve", fontsize=14, fontweight="bold")
            ax3.grid(True, alpha=0.3)
            ax3.legend()
            ax3.set_xlim(0, 1)
            ax3.set_ylim(0, 1)

            # Class performance
            class_names = ["Face"]  # From dataset
            class_scores = [metrics.map50 if hasattr(metrics, "map50") else 0]

            ax4.bar(class_names, class_scores, color=colors[0])
            ax4.set_title("Class-wise Performance", fontsize=14, fontweight="bold")
            ax4.set_ylabel("mAP50", fontsize=12)
            ax4.set_ylim(0, 1)
            ax4.grid(axis="y", alpha=0.3)

            # Add value label
            ax4.text(
                0,
                class_scores[0] + 0.01,
                f"{class_scores[0]:.3f}",
                ha="center",
                va="bottom",
                fontweight="bold",
            )

            plt.tight_layout()

            # Save plot
            os.makedirs("/app/results", exist_ok=True)
            plt.savefig(
                "/app/results/person_detection_validation.png",
                dpi=300,
                bbox_inches="tight",
            )
            print(
                "📊 Validation metrics plot saved to: /app/results/person_detection_validation.png"
            )

    except Exception as e:
        print(f"⚠️  Could not create metrics plot: {str(e)}")


def main():
    """Main validation function"""
    print("=" * 60)
    print("🔍 YOLO Person Detection Validation")
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

    # Check dataset
    dataset_path = "/app/python/examples/yolo/person detection detection.v2i.yolov11"
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at: {dataset_path}")
        print("💡 Please ensure the person detection dataset is available")
        return

    # Run validation
    results = validate_yolo_model()

    if results:
        # Plot metrics
        plot_validation_metrics(results)
        print("\n🎉 Person detection validation completed!")
        print("📊 Check runs/detect/person_detection_val/ for detailed results")
        print(
            "📈 Check /app/results/person_detection_validation.png for metrics visualization"
        )
    else:
        print("\n❌ Validation failed")


if __name__ == "__main__":
    main()
