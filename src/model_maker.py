#!/usr/bin/env python3

import os
import sys
import json
import tensorflow as tf

assert tf.__version__.startswith('2')

from mediapipe_model_maker import object_detector


def main(args):
    
    # Bringing in dataset from example
    train_dataset_path = "/mediapipe_model_maker/datasets/android_figurine/train"
    validation_dataset_path = "/mediapipe_model_maker/datasets/android_figurine/validation"

    # Verifying dataset content
    with open(os.path.join(train_dataset_path, "labels.json"), "r") as f:
        labels_json = json.load(f)
    for category_item in labels_json["categories"]:
        print(f"{category_item['id']}: {category_item['name']}")

    # Get data here - could be in COCO or PASCAL VOC format
    # Initialize dataset
    train_data = object_detector.Dataset.from_coco_folder(train_dataset_path, cache_dir="/tmp/od_data/train")
    validation_data = object_detector.Dataset.from_coco_folder(validation_dataset_path, cache_dir="/tmp/od_data/validation")
    print("train_data size: ", train_data.size)
    print("validation_data size: ", validation_data.size)

    # Retrain the model
    # Set retraining options: could be MobileNet-V2 or MobileNet-MultiHW-AVG
    spec = object_detector.SupportedModels.MOBILENET_MULTI_AVG
    hparams = object_detector.HParams(export_dir='exported_model')
    options = object_detector.ObjectDetectorOptions(
        supported_model=spec,
        hparams=hparams)
    # Run retraining
    model = object_detector.ObjectDetector.create(
        train_data=train_data,
        validation_data=validation_data,
        options=options)
    # Evaluate model performance
    loss, coco_metrics = model.evaluate(validation_data, batch_size=4)
    print(f"Validation loss: {loss}")
    print(f"Validation coco metrics: {coco_metrics}")

    # Export the model
    model.export_model()


if __name__ == '__main__':
    main(sys.argv)