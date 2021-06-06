
class SettingsDto:
    def __init__(self, chromium_drive: str,
                 waitfortime: int, post_host: str, dingtalk_url: str,
                 code_username: str, code_password: str, code_id: str):
        self.chromium_drive: str = chromium_drive
        self.waitfortime: int = waitfortime
        self.post_host: str = post_host
        self.dingtalk_url: str = dingtalk_url

        self.code_username: str = code_username
        self.code_password: str = code_password
        self.code_id: str = code_id
