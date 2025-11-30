from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO(r"C:\Users\Lund University\Documents\GitHub\bnl-ai\pretrained stuff\yolo11x.pt")  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(
        data=r"C:\Users\Lund University\Documents\GitHub\bnl-ai\top_detection\config.yaml",
        epochs=100,
        imgsz=640
    )