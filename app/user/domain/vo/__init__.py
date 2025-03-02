from enum import StrEnum


class OauthProviderTypeEnum(StrEnum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"
    KAKAO = "kakao"
    NAVER = "naver"


class UserRolesEnum(StrEnum):
    Researcher = "researcher"
    Participant = "participant"


class LoginTypeEnum(StrEnum):
    App = "app"
    Web = "web"

    @property
    def is_researcher(self) -> bool:
        return self == LoginTypeEnum.Web

    @property
    def is_participant(self) -> bool:
        return self == LoginTypeEnum.App
