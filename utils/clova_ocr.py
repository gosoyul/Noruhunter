import base64
import json
import time

import cv2
import requests


def encode_image_to_base64(image, ext="jpg"):
    _, buffer = cv2.imencode(f".{ext}", image)
    return base64.b64encode(buffer).decode("utf-8")


def call_clova_ocr(image, api_url, secret_key, format="jpg"):
    headers = {"Content-Type": "application/json", "X-OCR-SECRET": secret_key}
    image_base64 = encode_image_to_base64(image)

    payload = {
        "images": [{"format": format, "name": "ocr_image", "data": image_base64}],
        "lang": "ko",
        "requestId": "string",
        "resultType": "string",
        "timestamp": int(time.time()),
        "version": "V2"
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return parse_ocr_result(response.json())
    else:
        print(f"❌ OCR API 호출 실패: {response.status_code}, 응답: {response.text}")
        return None


def parse_ocr_result(result):
    extracted_text = []
    try:
        for image_data in result.get("images", []):
            for field in image_data.get("fields", []):
                extracted_text.append(field.get("inferText", ""))
    except Exception as e:
        print(f"⚠️ OCR 데이터 파싱 중 오류 발생: {e}")
    return extracted_text
