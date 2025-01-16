from enum import StrEnum


class OauthProviderTypeEnum(StrEnum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"
    KAKAO = "kakao"
    NAVER = "naver"


class UserRoleEnum(StrEnum):
    Researcher = "researcher"
    Participant = "participant"
