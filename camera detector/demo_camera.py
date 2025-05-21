# # import cv2

# # cap = cv2.VideoCapture(0)  # 0 is usually the default webcam
# # if not cap.isOpened():
# #     print("Error: Camera not found or cannot be accessed")
# # else:
# #     print("Camera is working!")
# #     while True:
# #         ret, frame = cap.read()
# #         if not ret:
# #             break
# #         cv2.imshow('Camera Test', frame)
# #         if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit
# #             break
# #     cap.release()
# #     cv2.destroyAllWindows()
# import cv2
# for i in range(10):
#     cap = cv2.VideoCapture(i)  # 0 is usually the default webcam
#     if not cap.isOpened():
#         print("Error: Camera not found or cannot be accessed")
#         found = True
#         cap.release()
#         break
#     else:
#         print("Camera is working!")
#     if not found:
#         print("No camera detected . Check if your camera is connected and enabled.")    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to grab frame")
#             break  # Exit if the frame cannot be read
#         cv2.imshow('Camera Test', frame)
#         if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit
#             break
#     cap.release()
#     cv2.destroyAllWindows()

# import cv2

# found = False
# for i in range(10):
#     cap = cv2.VideoCapture(i)
#     if cap.isOpened():
#         print(f"✅ Camera detected at index {i}")
#         found = True
#         cap.release()
#         break
#     else:
#         print(f"❌ No camera at index {i}")

# if not found:
#     print("🚫 No cameras detected. Check if your camera is connected and enabled.")


import cv2

cap = cv2.VideoCapture(0)  # Use index 0 as confirmed

if not cap.isOpened():
    print("Error: Camera not found or cannot be accessed")
else:
    print("Camera is working!")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow('Camera Test - Press ESC to Exit', frame)
        
        # Exit on pressing ESC (ASCII 27)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
