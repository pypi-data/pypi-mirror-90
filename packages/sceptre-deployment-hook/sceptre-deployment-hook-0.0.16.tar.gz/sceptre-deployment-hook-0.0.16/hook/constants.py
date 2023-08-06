import os
import subprocess

from typing import List


def _getenv(key) -> str:
    return os.getenv(key, "")


def _get_output_subprocess(command: List[str]) -> str:
    return subprocess.run(command, capture_output=True).stdout.decode("utf-8")


GIT_BRANCH_NAME = _getenv("CI_COMMIT_BRANCH")
JOB_ID = _getenv("CI_JOB_ID")
AWS_REGION = _getenv("AWS_REGION")
LAST_GIT_COMMIT_MESSAGE = _get_output_subprocess(["git", "log", "-1"])

AWS_ACCOUNT_ID = '205781933585' if GIT_BRANCH_NAME == "prod" \
    else "737956109553" if GIT_BRANCH_NAME == "test" \
    else "521248050649"

APP_VPC = 'vpc-41e3082a' if GIT_BRANCH_NAME == "prod" \
    else "vpc-c97463a1" if GIT_BRANCH_NAME == "test" \
    else "vpc-cad5d5a2"
