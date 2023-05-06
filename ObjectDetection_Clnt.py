import socket
import struct
import time
import cv2

# Replace with actual server IP and port
server_address = ('192.168.59.93', 8081)

# Define and set the camera object
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 서버 소켓 셋업
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# 무한 루프
while True:
    ret, frame = capture.read()

    # Encode the frame to JPEG format
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, frame_encoded = cv2.imencode('.jpg', frame, encode_param)

    # Get the size of the frame in bytes and pack it into a struct
    data = struct.pack("Q", len(frame_encoded))
    client_socket.sendall(data)

    # Send the frame
    client_socket.sendall(frame_encoded.tobytes())

    # Wait for some time before sending the next frame
    time.sleep(0.03)

# Release the capture object and close all windows
capture.release()
cv2.destroyAllWindows()
