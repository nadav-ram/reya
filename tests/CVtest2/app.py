import cv2
from cv2 import threshold


def main():
    cv_logic()


def cv_logic():

    camera = cv2.VideoCapture(0)    # Get camera stream

    while True:
        ret, frame = camera.read()  # ret(bool), frame(np array)
        ret, frame2 = camera.read()

        diff = cv2.absdiff(frame, frame2)
        
        grayscale = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = \
            cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        cv2.imshow("TESTWINDOW", frame)
        key = cv2.waitKey(30)
        if key == 27:               # If ESC is pressed
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
