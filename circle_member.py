import json
import os
from datetime import datetime

CIRCLE_MEMBERS_FILENAME = "circle_members.json"
CIRCLE_MEMBERS_PATH = os.path.join(os.getcwd(), CIRCLE_MEMBERS_FILENAME)


class CircleMember:
    def __init__(self, nickname="새 서클원", uid="", arcalive_id="", join_date=None, position="서클원", remark=""):
        self.nickname = nickname
        self.uid = uid
        self.arcalive_id = arcalive_id
        self.join_date = join_date if join_date else datetime.now()
        self.position = position
        self.remark = remark
        self.join_date = join_date.strftime("%Y-%m-%d") if isinstance(join_date, datetime) else join_date

    @property
    def join_period(self):
        result = None
        if self.join_date:
            join_date = datetime.strptime(self.join_date, "%Y-%m-%d")
            today = datetime.now()
            result = (today - join_date).days

        return result

    def to_dict(self):
        """서클원 객체를 딕셔너리로 변환"""
        return {
            "nickname": self.nickname,
            "uid": self.uid,
            "arcalive_id": self.arcalive_id,
            "join_date": self.join_date,
            "position": self.position,
            "remark": self.remark
        }

    @staticmethod
    def from_dict(data):
        """딕셔너리 데이터를 받아서 서클원 객체로 변환"""
        return CircleMember(
            nickname=data["nickname"],
            uid=data["uid"],
            arcalive_id=data["arcalive_id"],
            join_date=data["join_date"],
            position=data["position"],
            remark=data["remark"]
        )


class CircleMemberManager:
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
            self.members = []
            self.load_from_json()

    def add_member(self, member=None):
        """서클원 추가"""
        if member is None:
            member = CircleMember()

        self.members.append(member)
        return member

    def update_member(self, idx, updated_member):
        """서클원의 데이터를 수정"""
        self.members[idx] = updated_member
        self.save_to_json()

    def remove_member(self, idx):
        """서클원 추가"""
        del self.members[idx]

    def save_to_json(self):
        """JSON 파일로 저장"""
        with open(CIRCLE_MEMBERS_PATH, 'w', encoding='utf-8') as f:
            json.dump([member.to_dict() for member in self.members], f, ensure_ascii=False, indent=4)

    def load_from_json(self):
        """JSON 파일에서 데이터 로드"""
        try:
            with open(CIRCLE_MEMBERS_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.members = [CircleMember.from_dict(member) for member in data]
        except FileNotFoundError:
            print(f"{CIRCLE_MEMBERS_PATH} 파일이 존재하지 않습니다.")
            self.members = []

    def get_by_nickname(self, nickname, attribute=None):
        circle_member_manager = CircleMemberManager()
        members: list[CircleMember] = circle_member_manager.members
        member = next((member for member in members if member.nickname == nickname), None)

        if member is None:
            return None
        else:
            return getattr(member, attribute) if attribute else member
