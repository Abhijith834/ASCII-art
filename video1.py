import cv2
import numpy as np
from PIL import Image

# ASCII characters used to build the output
ASCII_CHARS = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]

# Variable to specify the ASCII art width
ascii_width = 100  # You can adjust this value
invert_colors = False  # Variable to toggle color inversion

# Convert each pixel to grayscale
def grayify(image):
    return image.convert("L")

# Resize image according to a new width
def resize_image(image, new_width=ascii_width):
    width, height = image.size
    ratio = height / width / 1.3  # Adjusted aspect ratio for better output
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

# Map the grayscale value to ASCII characters
def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ''.join(ASCII_CHARS[min(pixel * 10 // 256, 9)] for pixel in pixels)
    return ascii_str

# Mouse click event to toggle color inversion
def toggle_inversion(event, x, y, flags, param):
    global invert_colors
    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if click is within the button area
        if 10 <= x <= 110 and 10 <= y <= 40:
            invert_colors = not invert_colors  # Toggle color inversion

def main():
    global invert_colors
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera
    cv2.namedWindow("ASCII Art")
    cv2.setMouseCallback("ASCII Art", toggle_inversion)

    while True:
        ret, frame = cap.read()  # Capture frame-by-frame
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally

        # Convert the captured frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Convert the NumPy array to a PIL image
        img = Image.fromarray(gray_frame)
        # Resize and convert to ASCII using the variable width
        img = resize_image(img)
        ascii_str = pixels_to_ascii(grayify(img))
        img_width = img.width
        ascii_img = [ascii_str[i:i+img_width] for i in range(0, len(ascii_str), img_width)]
        ascii_img = "\n".join(ascii_img)
        
        # Convert the ASCII art to an image
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        ascii_frame = np.zeros((img.height*12, img.width*10), np.uint8)  # Adjusted aspect ratio
        
        # Put the ASCII characters on the image
        y0, dy = 12, 12
        for i, line in enumerate(ascii_img.split('\n')):
            y = y0 + i * dy
            for j, char in enumerate(line):
                cv2.putText(ascii_frame, char, (j*10, y), font, font_scale, 255, thickness, lineType=cv2.LINE_AA)
        
        # Apply color inversion if toggle is on
        display_frame = 255 - ascii_frame if invert_colors else ascii_frame

        # Draw button with inverted colors based on the toggle state
        button_bg_color = 0 if invert_colors else 255  # Background color of the button
        text_color = 255 if invert_colors else 0       # Text color for button label

        # Draw the button
        cv2.rectangle(display_frame, (10, 10), (110, 40), button_bg_color, -1)
        cv2.putText(display_frame, "Invert" if not invert_colors else "Invert", (15, 30), font, 0.6, text_color, 2)
        
        # Show the frame
        cv2.imshow("ASCII Art", display_frame)
        
        # Break if the window is closed
        if cv2.getWindowProperty("ASCII Art", cv2.WND_PROP_VISIBLE) < 1:
            break

        # Option to quit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
