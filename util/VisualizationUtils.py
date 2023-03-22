import cv2
from mediapipe import solutions


def solution_process(img, solution):
    """
    Processes an RGB image and returns the pose landmarks on the most prominent person detected
    cv2: BGR, mediapipe: RGB
    TODO: BGR2RGB
    """
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return solution.process(img_RGB)


def index2point(img, landmarks, index):
    img_height, img_width = img.shape[:2]
    landmark = landmarks[index]
    x = int(landmark.x * img_width)
    y = int(landmark.y * img_height)
    return x, y


def put_text2img(image, text, org=(50, 50), font_face=cv2.FONT_HERSHEY_SIMPLEX, font_scale=2, color=(255, 0, 0),
                 thickness=2):
    cv2.putText(img=image,
                text=str(text),
                org=org,
                fontFace=font_face,
                fontScale=font_scale,
                color=color,
                thickness=thickness
                )


def draw_landmarks(image, landmark_list, connections, color=(255, 0, 0), thickness=2):
    point_style = solutions.drawing_styles.DrawingSpec(color=color, thickness=thickness)
    line_style = solutions.drawing_styles.DrawingSpec(color=color, thickness=thickness)

    solutions.drawing_utils.draw_landmarks(
        image=image,
        landmark_list=landmark_list,
        connections=connections,
        landmark_drawing_spec=point_style,
        connection_drawing_spec=line_style
    )
