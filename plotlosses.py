import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
csv_path = r'c:\Users\Lund University\Documents\GitHub\bnl-ai\out\train_pose-250621_203317\loss_PoseHRNet-W48_288x384.csv'

# Read the CSV file
df = pd.read_csv(csv_path)

# Plot
plt.figure(figsize=(8,5))
plt.plot(df['epoch'], df['average_train_loss'], label='Train Loss')
plt.plot(df['epoch'], df['average_val_loss'], label='Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.title('Train and Validation Loss vs Epoch')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()