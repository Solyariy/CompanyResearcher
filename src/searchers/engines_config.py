from pydantic_settings import BaseSettings, SettingsConfigDict
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class GoogleConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="google_engine_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    key: str | None = None
    cx: str | None = None
    url: str | None = None

    def build_url(self):
        return (f"{self.url}"
                f"lr=lang_en&"
                f"sort=date&"
                f"num=10&"
                f"key={self.key}&"
                f"cx={self.cx}&"
                f"q=")


class GoogleAlertsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="google_alerts_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    url: str | None = None
    project_id: str | None = None
    quota_count_id: str | None = None
    key_path: str | None = None

    def get_params(self) -> dict[str, str | dict[str, str]]:
        return {
            "url": self.__build_url(),
            "headers": self.__build_headers()
        }

    def __build_url(self) -> str:
        return self.url.format(project_id=self.project_id, policy_id=self.quota_count_id)

    def __build_headers(self) -> dict[str, str]:
        SCOPES = ["https://www.googleapis.com/auth/monitoring.read"]
        credentials = service_account.Credentials.from_service_account_file(
            self.key_path, scopes=SCOPES
        )
        credentials.refresh(Request())
        return {
            "Authorization": f"Bearer {credentials.token}"
        }
