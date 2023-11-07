import cv2

username = 'admin'
password = 'admin'
port = '1935'
ip = '192.168.0.106'

# Stream
stream = cv2.VideoCapture(f'rtsp://{username}:{password}@{ip}:{port}')

try:
    while True:
        # Read the input live stream
        ret, frame = stream.read()
        height, width, layers = frame.shape
        frame = cv2.resize(frame, (width // 2, height // 2))

        # Show video frame
        cv2.imshow("Camera", frame)

        # Quit when 'x' is pressed
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
except Exception as e:
    print("ERROR:", e)

# Main function
if __name__ == "__main__":
    # Release and close stream
    stream.release()
    cv2.destroyAllWindows()