import cv2
import os
import time
import threading

# Set dataset directory
datasets = 'datasets'

# Open webcam
webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Function to display live video feed and take user input
def show_camera_and_get_input():
    global sub_data, num_images
    sub_data = ""
    num_images = ""
    input_stage = 0  # 0 for name, 1 for number of images
    user_input = ""
    last_frame = None  # Store last valid frame
    
    while True:
        ret, frame = webcam.read()
        if not ret:
            break
        last_frame = frame.copy()
        
        # Display instructions on the live feed
        if input_stage == 0:
            text = "Enter your name: " + user_input
        else:
            text = "Enter number of images: " + user_input
        
        cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Live Capture', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 27:  # Press 'Esc' to exit
            webcam.release()
            cv2.destroyAllWindows()
            exit()
        elif key == 13:  # Press 'Enter' to submit input
            if input_stage == 0:
                sub_data = user_input
                user_input = ""
                input_stage = 1
            else:
                num_images = int(user_input)
                break
        elif key == 8:  # Press 'Backspace' to delete last character
            user_input = user_input[:-1]
        elif 32 <= key <= 126:  # Handle alphanumeric input
            user_input += chr(key)
    
    return sub_data, num_images, last_frame
display_thread = threading.Thread(target=show_camera_and_get_input, daemon=True)
display_thread.start()
# Get user input on live feed
sub_data, num_images, frame = show_camera_and_get_input()

# Set dataset path
path = os.path.join(datasets, sub_data)
if not os.path.isdir(path):
    os.makedirs(path)

# Display start capture message on last captured frame
cv2.putText(frame, "Press Enter to start capturing...", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2.imshow('Live Capture', frame)
cv2.waitKey(0)  # Wait until user presses Enter

# Capture images
count = 1
while count <= num_images:
    ret, im = webcam.read()
    if not ret:
        print("Error: Failed to capture image.")
        break
    
    # Save image
    cv2.imwrite(f'{path}/{count}.png', im)
    print(f"Saved image {count}/{num_images}")
    count += 1
    
    time.sleep(0.2)  # Small delay to avoid duplicate captures

webcam.release()
cv2.destroyAllWindows()
print("Dataset collection complete!")
