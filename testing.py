from ultralytics import YOLO
model = YOLO(r"C:\Users\Lund University\Documents\GitHub\bnl-ai\runs\detect\train17\weights\best.pt")
results = model("path/to/your/image.png", conf=0.1)
results[0].show()  # or results[0].save("output.jpg")