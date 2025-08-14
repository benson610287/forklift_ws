import cv2

# Check what GPU modules are available
print("OpenCV version:", cv2.__version__)
print("CUDA enabled:", cv2.cuda.getCudaEnabledDeviceCount() > 0)

# List available GPU functions
gpu_functions = [attr for attr in dir(cv2.cuda) if not attr.startswith('_')]
print("Available GPU functions:", len(gpu_functions))
