import json
import os


class ConfigKeys:
    """Config 파일의 키 값을 관리하는 클래스"""
    WINDOW_TITLE = "window_title"
    MAX_SCROLLS = "max_scrolls"
    SCROLL_REPEAT = "scroll_repeat"
    CONTRIB_LIMIT = "contrib_limit"
    CLOVA_API = "clova_api"
    CLOVA_X_OCR_SECRET = "x_ocr_secret"
    CLOVA_API_URL = "api_url"


class ConfigManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        """싱글턴 패턴을 구현."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._load_config()

    def _load_config(self):
        """설정 파일을 로드하는 메서드."""
        config_file = "config.json"  # 기본 config 파일
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        else:
            print("설정 파일을 찾을 수 없습니다. 기본 설정을 사용합니다.")
            self._config = self._get_default_config()
            self._save_config()

    def get(self, keys, default=None):
        """키 경로로 값을 가져오는 메서드"""
        if isinstance(keys, str):
            keys = [keys]

        value = self._config
        for key in keys:
            value = value.get(key)
        return default if value is None else value

    def set(self, keys, value):
        """키 경로로 값을 설정하는 메서드"""
        if isinstance(keys, str):
            keys = [keys]

        data = self._config
        for key in keys[:-1]:
            data = data.get(key)
        data[keys[-1]] = value

        self._save_config()

    def _save_config(self):
        """설정을 파일에 저장하는 메서드."""
        with open("config.json", 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=4)

    def __repr__(self):
        """현재 설정을 보기 좋게 출력."""
        return json.dumps(self._config, indent=4, ensure_ascii=False)

    @staticmethod
    def _get_default_config():
        default_config = {
            ConfigKeys.WINDOW_TITLE: "EXILIUM",
            ConfigKeys.MAX_SCROLLS: 20,
            ConfigKeys.SCROLL_REPEAT: 25,
            ConfigKeys.CONTRIB_LIMIT: 270,
            ConfigKeys.CLOVA_API: {
                ConfigKeys.CLOVA_X_OCR_SECRET: "",
                ConfigKeys.CLOVA_API_URL: ""
            },
        }
        return default_config
