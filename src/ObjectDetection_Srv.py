import socket
import struct
import cv2
import numpy as np

# Replace with actual server IP and port
server_address = ('0.0.0.0', 8081)

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

# Haar cascade detector object declaration
face_cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_fullbody.xml')

# Accept a client connection
print('waiting for a connection...')
client_socket, client_address = server_socket.accept()
print('connected from', client_address)

# Define payload size
payload_size = struct.calcsize("Q")

cv2.namedWindow("face_detection")

# warning message 를 출력할 window 생성
cv2.namedWindow("warning")
# 시작 위치
cv2.moveWindow("warning", 500, 500)
# 임계값 설정
threshold = 3

# Run an infinite loop
while True:
    # Receive the length of the encoded data from the client
    data = b''
    while len(data) < payload_size:
        packet = client_socket.recv(payload_size - len(data))
        if not packet:
            break
        data += packet
    if not data:
        break

    # Extract the length of the encoded data from the received data
    message_size = struct.unpack("Q", data)[0]

    # Receive the encoded data from the client
    data = b''
    while len(data) < message_size:
        packet = client_socket.recv(message_size - len(data))
        if not packet:
            break
        data += packet
    if not data:
        break

    # Decode the received data and display the resulting frame
    frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Create a new empty image for warning window
    warning = np.zeros((200, 700, 3), np.uint8)

    # Calculate percentage
    num_faces = len(faces)
    percent = int(num_faces / threshold * 100)

    # Add the number of detected faces as text to the frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(warning, "Number of people detected: " +
                str(num_faces) + " (" + str(percent) + "%)", (20, 50), font, 1, (0, 255, 0), 2)
    cv2.putText(warning, "Threshold: " + str(threshold),
                (20, 80), font, 1, (255, 255, 255), 2)

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Check if the number of people detected exceeds the threshold
    if num_faces > threshold:
        cv2.putText(warning, "WARNING: Too many people detected!",
                    (20, 110), font, 1, (0, 0, 255), 2)
    else:
        # Clear warning window if no warning is needed
        cv2.putText(warning, "",
                    (20, 110), font, 1, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('warning', warning)

    # If there is a face found
    # Display the face area as a rectangle on the image
    if num_faces:
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (255, 255, 255), 2, cv2.LINE_4)

    cv2.imshow("face_detection", frame)

    # Exit loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the capture and destroy all windows
cv2.destroyAllWindows()
client_socket.close()
server_socket.close()
