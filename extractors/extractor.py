import logging
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable

from config import ConfigManager, ConfigKeys
from excel import Excel, ExcelColumn
from utils import clova_ocr, window, image, mouse

# 로깅 설정
logging.basicConfig(
    filename="error.log",  # 로그 파일명
    level=logging.ERROR,  # ERROR 레벨 이상의 로그만 기록
    format="%(asctime)s - %(levelname)s - %(message)s",  # 로그 형식 (시간, 로그 레벨, 메시지)
    datefmt="%Y-%m-%d %H:%M:%S"  # 시간 형식
)


class Extractor(ABC):
    def __init__(self, ocr_headers: list[tuple[str, str]], excel_columns: list[ExcelColumn], parent_window=None):
        self.ocr_headers = ocr_headers
        self.excel_columns = excel_columns

    @abstractmethod
    def get_dynamic_ratio(self, hwnd=None):
        pass

    def screenshot(self, hwnd=None):
        """공통 캡쳐 프로세스 구현"""
        return window.screenshot(self.get_dynamic_ratio(hwnd), hwnd)

    def _on_before_export(self, hwnd=None):
        pass

    def _on_after_export(self, hwnd=None):
        pass

    def _on_before_extract(self):
        pass

    def _on_after_extract(self, extracted_text):
        pass

    @staticmethod
    def create_output_directory():
        """결과물 디렉터리 생성"""
        directory_path = os.path.join(os.getcwd(), "output")
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        return directory_path

    def extract(self, parent=None, name=None):
        try:
            config = ConfigManager()
            api_url = config.get([ConfigKeys.CLOVA_API, ConfigKeys.CLOVA_API_URL])
            api_secret_key = config.get([ConfigKeys.CLOVA_API, ConfigKeys.CLOVA_X_OCR_SECRET])

            if not api_url.strip() or not api_secret_key.strip():
                window.show_message("알림", "CLOVA OCR API 설정을 완료하신 뒤 사용하실 수 있습니다.")
                return

            prefix = name + "을 " if name else ""
            result = window.show_message("추출", f"{prefix}진행하시려면 [확인]을 눌러주세요.", window.MB_OKCANCEL)
            if result == 2:
                return

            window_title = config.get(ConfigKeys.WINDOW_TITLE)
            max_scroll = config.get(ConfigKeys.MAX_SCROLLS)
            scroll_repeat = config.get(ConfigKeys.SCROLL_REPEAT)

            hwnd = window.find_window(window_title)
            window.activate_window(hwnd)
            time.sleep(1)

            # 첫 번째 스크린샷 찍기
            first_screenshot = self.screenshot(hwnd)
            first_screenshot_bin = image.binarize_image(first_screenshot)

            # 스크롤 및 이미지 비교
            scroll_count = 0
            prev_y_offset = -1

            _, _, client_width, _, center_x, center_y = window.get_client_area(hwnd)

            while scroll_count < max_scroll:
                mouse.move_mouse(center_x, center_y)
                mouse.scroll_down(scroll_repeat)
                time.sleep(0.8)

                second_screenshot = self.screenshot(hwnd)
                second_screenshot_bin = image.binarize_image(second_screenshot)

                crop_height = int(second_screenshot.shape[0] * 0.2)
                cropped_second_screenshot_bin = second_screenshot_bin[:crop_height, :]

                similarity, location = image.compare_images(first_screenshot_bin, cropped_second_screenshot_bin)

                print(f"🔍 유사도: {similarity}")
                print(f"📍 가장 유사한 위치: {location}")

                if similarity > 0.8:
                    y_offset = location[1]
                    if y_offset == prev_y_offset:
                        print("❌ y_offset이 같아서 반복을 종료합니다.")
                        break
                    else:
                        prev_y_offset = y_offset
                        first_screenshot_bin = image.merge_images(first_screenshot_bin, second_screenshot_bin, location)
                        print("✅ 이미지 병합 성공!")

                scroll_count += 1
                if scroll_count == max_scroll:
                    print("❌ 최대 시도 횟수 도달, 종료합니다.")

            if parent:
                parent.activateWindow()  # 윈도우 활성화
                parent.raise_()  # 윈도우를 맨 위로 올림

            self._on_before_extract()

            _, _, _, _, _, profile_ratio = self.get_dynamic_ratio(hwnd)
            cropped_image = first_screenshot_bin[:, int(client_width * profile_ratio):]

            # resized_image = cv2.resize(cropped_image, (0, 0), fx=0.4, fy=0.4)
            # cv2.imshow("Preview", resized_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            extracted_text = clova_ocr.call_clova_ocr(cropped_image, api_url, api_secret_key)
            print(f"📝 추출된 텍스트: {extracted_text}")

            extracted_text = self._fix_extracted_text(extracted_text)

            self._on_after_extract(extracted_text)

            # 엑셀 저장
            directory = self.create_output_directory()

            today = datetime.now()
            today_date = today.strftime('%Y-%m-%d')
            today_time = today.strftime('%H:%M:%S')

            # 요일을 한국어로 매핑
            weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
            weekday = weekdays[today.weekday()]

            excel_path = os.path.join(directory, f"{today_date}.xlsx")
            headers, data = self._create_excel_data(extracted_text)

            excel = Excel()
            excel.export(path=excel_path,
                         sheet_name=today_date,
                         title=f"{today_date} {today_time} {weekday}",
                         columns=self.excel_columns,
                         data=data)

            # 이미지 저장
            # image_path = os.path.join(directory, f"{today}.jpg")
            # image.save_image(image_path, cropped_image)

            if window.show_message("추출", "추출이 완료되었습니다. 엑셀파일을 실행하시겠습니까?", flag=window.MB_OKCANCEL):
                os.startfile(excel_path)
        except Exception as e:
            logging.error("추출 중 에러 발생", exc_info=True)  # 로그 파일에 오류 기록
            window.show_message("에러", f"목록 추출 실패: {e}", flag=window.MB_ICONERROR)

    def _fix_extracted_text(self, extracted_text):
        return extracted_text

    def _create_excel_data(self, extracted_text=None):
        headers = [excel_header.header for excel_header in self.excel_columns]

        ocr_data = self._split_extracted_text(extracted_text)

        data = []
        for ocr_row in ocr_data:
            row = []
            for excel_header in self.excel_columns:
                value = excel_header.value

                if isinstance(value, Callable):
                    result = value(ocr_row)
                    row.append(result)
                else:
                    row.append(value)

            data.append(row)

        return headers, data

    def _split_extracted_text(self, extracted_text):
        result = []

        # 서클원 정보는 headers의 길이만큼 반복되므로, 이를 기준으로 데이터를 묶음
        for i in range(0, len(extracted_text), len(self.ocr_headers)):
            row = {}
            for j in range(len(self.ocr_headers)):
                value = extracted_text[i + j]
                if value.isdecimal():
                    value = int(value)

                row[self.ocr_headers[j][0]] = value
            result.append(row)

        return result
