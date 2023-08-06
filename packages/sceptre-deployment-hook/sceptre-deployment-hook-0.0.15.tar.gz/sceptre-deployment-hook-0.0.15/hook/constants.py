import os
import subprocess

from typing import List


def _getenv(key) -> str:
    return os.getenv(key, "")


def _get_output_subprocess(command: List[str]) -> str:
    return subprocess.run(command, capture_output=True).stdout.decode("utf-8")


GIT_BRANCH_NAME = _getenv("CI_COMMIT_BRANCH")
JOB_ID = _getenv("CI_JOB_ID")
APP_VPC = _getenv("APP_VPC")
AWS_REGION = _getenv("AWS_REGION")
AWS_ACCOUNT_ID = _getenv("AWS_ACCOUNT_ID")
LAST_GIT_COMMIT_MESSAGE = _get_output_subprocess(["git", "log", "-1"])
