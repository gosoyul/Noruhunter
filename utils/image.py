import cv2
import numpy as np


def binarize_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # _, binary_image = cv2.threshold(gray_image, 175, 255, cv2.THRESH_BINARY)
    return gray_image


def compare_images(img1, img2):
    """두 이미지의 유사도를 비교하는 함수"""
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc  # 정확한 두 개의 값 반환


def merge_images(first_screenshot, second_screenshot, location):
    x_offset, y_offset = location
    first_part = first_screenshot[:y_offset, :]
    return np.vstack((first_part, second_screenshot))


def save_image(image, path):
    """이미지를 파일로 저장"""
    cv2.imwrite(path, image)
    print(f"✅ 이미지 파일 저장 완료: {path}")
