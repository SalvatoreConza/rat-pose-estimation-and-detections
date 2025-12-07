"""
CVAT_to_CSV.py

This script converts CVAT XML annotations into a CSV file containing
keypoint coordinates and bounding box information for each labeled image.

Usage:
    python CVAT_to_CSV.py <cvat_annotation.xml>

Arguments:
    <cvat_annotation.xml>: Path to the CVAT XML annotation file.

Output:
    - A CSV file with the same basename as the input XML file.
    - If the output CSV already exists, an incremental number is added to the filename.

CSV Format:
    filename, nose-x, nose-y, ears_midpoint-x, ears_midpoint-y, ..., bbox_tl-x, bbox_tl-y, bbox_br-x, bbox_br-y

Notes:
    - Only images with labels (keypoints or bounding boxes) are considered.
    - Keypoint labels are dynamically extracted from the XML file.
    - Keypoints with the attribute outside="1" will have empty coordinates in the CSV.
"""

import xml.etree.ElementTree as ET
import csv
import os
import sys
import glob
import tqdm

def parse_cvat_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    annotations = []
    keypoints = set()
    
    for image in root.findall(".//image"):
        filename = image.get("name")
        annotation = {"filename": filename}
        has_labels = False
        
        for skeleton in image.findall(".//skeleton"):
            for point in skeleton.findall(".//points"):
                label = point.get("label")
                if point.get("outside") == "1":
                    annotation[f"{label}-x"] = ""
                    annotation[f"{label}-y"] = ""
                else:
                    coords = point.get("points").split(",")
                    if len(coords) == 2:
                        annotation[f"{label}-x"] = float(coords[0])
                        annotation[f"{label}-y"] = float(coords[1])
                        has_labels = True
                keypoints.add(label)
        
        for box in image.findall(".//box"):
            annotation["bbox_tl-x"] = float(box.get("xtl"))
            annotation["bbox_tl-y"] = float(box.get("ytl"))
            annotation["bbox_br-x"] = float(box.get("xbr"))
            annotation["bbox_br-y"] = float(box.get("ybr"))
            has_labels = True
        
        if has_labels:
            annotations.append(annotation)
    
    return annotations, sorted(keypoints)

def save_to_csv(xml_file, annotations, keypoints, include_image_path=False):

    csv_basename = os.path.splitext(xml_file)[0] + "_converted.csv"
    counter = 1
    output_csv = csv_basename
    while os.path.exists(output_csv):
        output_csv = f"{os.path.splitext(xml_file)[0]}_{counter}.csv"
        counter += 1
    # TODO: check the sorted didnt mess up the order of the keypoints
    headers = ["filename"] + [f"{kp}-{axis}" for kp in sorted(keypoints) for axis in ("x", "y")] + ["bbox_tl-x", "bbox_tl-y", "bbox_br-x", "bbox_br-y"]
    
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for ann in annotations:
            if include_image_path:
                ann["filename"] = os.path.relpath(os.path.join(os.path.dirname(xml_file), "images", ann["filename"]),start=os.path.abspath(".."))
            writer.writerow(ann)

def main():
    if len(sys.argv) != 2:
        print("Usage: python CVAT_to_CSV.py <cvat_annotation.xml>")
    
    input_dir = sys.argv[1]
    # Find all XML files in the input directory and its subdirectories
    xml_files = glob.glob(os.path.join(input_dir, os.path.join("**","*.xml")), recursive=True)
    print(f"Found {len(xml_files)} XML files in {input_dir}")
    
    # xml_file = sys.argv[1]
    for _, xml_file in tqdm.tqdm(enumerate(xml_files), desc="Converting XML files"):
        annotations, keypoints = parse_cvat_xml(xml_file)
        save_to_csv(xml_file, annotations, keypoints, include_image_path=True)

if __name__ == "__main__":
    main()
    