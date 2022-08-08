import cv2
import time

# camera includes all manipulation of color detection

# width: 480; height: 640

# crop a captured image
def crop():
    # read image
    img = cv2.imread('test2.jpg')

    # Cropping an image
    cropped_image = img[200:370, 270:480]    # note: height, width

    # Display cropped image
    # cv2.imshow("cropped", cropped_image)

    # store cropped image
    cv2.imwrite("Cropped Image.jpg", cropped_image)

    # if cv2.waitKey(0) & 0xFF == ord('c'):
        # cv2.imwrite("Cropped Image2.jpg", cropped_image)
        # cv2.destroyAllWindows()


# main function
def take_pic():
    cap = cv2.VideoCapture(1)
    count = 0
    if not (cap.isOpened()):
        print("Could not open video device")

    result = True

    # store the third frame
    while (result):
        time.sleep(1)
        ret, frame = cap.read()

        if count == 3:
            cv2.imwrite("test2.jpg", frame)
            result = False
        else:
            count += 1

    # crop the image taken
    crop()
    cap.release()
    cv2.destroyAllWindows()


    # while (True):
    #     # Capture frame-by-frame
    #     ret, frame = cap.read()
    #
    #     # Display the resulting frame
    #
    #     cv2.imshow('frame', frame)
    #
    #     if cv2.waitKey(1) & 0xFF == ord('s'):
    #         cv2.imwrite("test2.jpg", frame)
    #         crop()
    #         break
    #     # Waits for a user input to quit the application
    #     # if cv2.waitKey(1) & 0xFF == ord('q'):
    #         # break
    #
    # cap.release()
    # cv2.destroyAllWindows()
