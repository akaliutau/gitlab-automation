import os

import gitlab

GITLAB_URL = 'https://gitlab.com'


def main() -> None:
    token = os.environ.get('AUTOMATION_PAT')
    gl = gitlab.Gitlab(GITLAB_URL, private_token=token, timeout=30, ssl_verify=True)
