#!/usr/bin/env python

import os
import sys
import random
import shutil


def main(args):
    # Initializing paths and image/annotation files
    images_path = "/mediapipe_model_maker/datasets/voc_2012/images/"
    annotations_path = "/mediapipe_model_maker/datasets/voc_2012/Annotations/"
    train_images_path = "/mediapipe_model_maker/datasets/voc_2012/train/images/"
    train_annotations_path = "/mediapipe_model_maker/datasets/voc_2012/train/Annotations/"
    val_images_path = "/mediapipe_model_maker/datasets/voc_2012/val/images/"
    val_annotations_path = "/mediapipe_model_maker/datasets/voc_2012/val/Annotations/"
    extras_path = "/mediapipe_model_maker/datasets/voc_2012/extras/"

    num_files_images = file_count(images_path)
    num_files_annotations = file_count(annotations_path)
    image_files_full = os.listdir(images_path)
    image_files = list(range(len(image_files_full)))
    ext1 = list(range(len(image_files_full)))
    for idx in range(len(image_files)):
        image_files[idx], ext1[idx] = os.path.splitext(image_files_full[idx])
    annotations_files_full = os.listdir(annotations_path)
    annotations_files = list(range(len(annotations_files_full)))
    ext2 = list(range(len(annotations_files_full)))
    for index in range(len(annotations_files)):
        annotations_files[index], ext2[index] = os.path.splitext(annotations_files_full[index])

    # Get images and annotations files to have the same files
    # Add extensions before moving files here ***
    if num_files_annotations > num_files_images:
        for file in annotations_files:
            if file not in image_files:
                src1 = os.path.join(annotations_path, file + "." + "xml")
                dest1 = os.path.join(extras_path, file + "." + "xml")
                shutil.move(src1, dest1)
    elif num_files_annotations < num_files_images:
        for file in image_files:
            if file not in annotations_files:
                src2 = os.path.join(images_path, file + "." + "jpg")
                dest2 = os.path.join(extras_path, file + "." + "jpg")
                shutil.move(src2, dest2)

    # Check image and annotation file numbers again
    num_files_images = file_count(images_path)
    num_files_annotations = file_count(annotations_path)

    # Randomly sort out 20% for validation only if there are the same number
    # of image and annotation files
    if num_files_images == num_files_annotations:
        # Get the number of validation files needed
        num_val = int(0.2*num_files_images)

        # Generate a random assortment of numbers corresponding to the
        # validation files that will be taken out
        val_selects = generate_rand(num_val, 0, num_files_images)

        # Take out the random files for validation
        image_files = os.listdir(images_path)
        image_files = sorted(image_files)
        annotations_files = os.listdir(annotations_path)
        annotations_files = sorted(annotations_files)

        val_images = []
        val_annotations = []
        for i in range(num_val):
            image = image_files[val_selects[i] - 1]
            val_images.append(image)
            annotation = annotations_files[val_selects[i] - 1]
            val_annotations.append(annotation)

        # Use the remaining images and annotations for training
        train_images = []
        train_annotations = []
        for j in range(len(image_files)):
            if j in val_selects:
                continue
            else:
                train_images.append(image_files[j])
                train_annotations.append(annotations_files[j])

        # Move the images and annotations files into the corresponding
        # directories
        # move_files(val_images, images_path, val_images_path)
        # move_files(val_annotations, annotations_path, val_annotations_path)
        # move_files(train_images, images_path, train_images_path)
        # move_files(train_annotations, annotations_path, train_annotations_path)

        try:
            # Make sure the destination directory exists, and make it if needed
            os.makedirs(val_images_path, exist_ok=True)

            # Move each file corresponding to the file_list to the destination
            # directory
            for file_name in val_images:
                source_path = os.path.join(images_path, file_name)
                destination_path = os.path.join(val_images_path, file_name)
                shutil.move(source_path, destination_path)

            print(f"Files moved from '{images_path}' to '{val_images_path}'")
        except FileNotFoundError:
            print("Directory not found.")
        except Exception as e:
            print(f"Error: {e}")

        try:
            # Make sure the destination directory exists, and make it if needed
            os.makedirs(val_annotations_path, exist_ok=True)

            # Move each file corresponding to the file_list to the destination
            # directory
            for file_name in val_annotations:
                source_path = os.path.join(annotations_path, file_name)
                destination_path = os.path.join(val_annotations_path, file_name)
                shutil.move(source_path, destination_path)

            print(f"Files moved from '{annotations_path}' to '{val_annotations_path}'")
        except FileNotFoundError:
            print("Directory not found.")
        except Exception as e:
            print(f"Error: {e}")

        try:
            # Make sure the destination directory exists, and make it if needed
            os.makedirs(train_images_path, exist_ok=True)

            # Move each file corresponding to the file_list to the destination
            # directory
            for file_name in train_images:
                if file_name in val_images:
                    print("Bad")
                source_path = os.path.join(images_path, file_name)
                destination_path = os.path.join(train_images_path, file_name)
                shutil.move(source_path, destination_path)

            print(f"Files moved from '{images_path}' to '{train_images_path}'")
        except FileNotFoundError:
            print("Directory not found.")
        except Exception as e:
            print(f"Error: {e}")

        try:
            # Make sure the destination directory exists, and make it if needed
            os.makedirs(train_annotations_path, exist_ok=True)

            # Move each file corresponding to the file_list to the destination
            # directory
            for file_name in train_annotations:
                source_path = os.path.join(annotations_path, file_name)
                destination_path = os.path.join(train_annotations_path, file_name)
                shutil.move(source_path, destination_path)

            print(f"Files moved from '{annotations_path}' to '{train_annotations_path}'")
        except FileNotFoundError:
            print("Directory not found.")
        except Exception as e:
            print(f"Error: {e}")



    else:
        print("The number of annotation files and image files do not match.")


def file_count(directory_path):
    try:
        # Get the list of files in the directory
        files = os.listdir(directory_path)

        # Filter out any folders
        files = [file for file in files if \
                 os.path.isfile(os.path.join(directory_path, file))]
        
        # Return the number of files
        return len(files)
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
        return None
    

def generate_rand(length, start, end):
    random_numbers = [random.randint(start, end) for _ in range(int(length))]
    return random_numbers


def move_files(file_list, source_dir, destination_dir):
    try:
        # Make sure the destination directory exists, and make it if needed
        os.makedirs(destination_dir, exist_ok=True)

        # Move each file corresponding to the file_list to the destination
        # directory
        for file_name in file_list:
            source_path = os.path.join(source_dir, file_name)
            destination_path = os.path.join(destination_dir, file_name)
            shutil.move(source_path, destination_path)

        print(f"Files moved from '{source_dir}' to '{destination_dir}'")
    except FileNotFoundError:
        print("Directory not found.")
    except Exception as e:
        print(f"Error: {e}")
    

if __name__ == "__main__":
    main(sys.argv)