from datetime import datetime

import hook.constants
hook.constants.AWS_REGION = "eu-central-1"
hook.constants.APP_VPC = "vpc-1234"
hook.constants.AWS_ACCOUNT_ID = "98765432"
hook.constants.JOB_ID = "1"

from sceptre.stack import Stack
from hook.hook import CustomHook


stack_name = "test/stack.yaml"
stack = Stack(
    name=stack_name,
    project_code="test",
    template_path="template/path",
    region="coin-central-1"
)


def test_invoke_lambda():
    start_test = datetime.utcnow()

    def intercept_invoke_lambda(payload):
        assert payload["method"] == "deploy_start"
        assert payload["stack_name"] == stack_name
        assert payload["ci_job_id"] == hook.constants.JOB_ID
        time = datetime.fromisoformat(payload["time"])
        assert start_test < time < datetime.utcnow()
    test_hook = CustomHook("deploy_start", None)
    assert test_hook._function_name == \
           f"arn:aws:lambda:{hook.constants.AWS_REGION}:{hook.constants.AWS_ACCOUNT_ID}:function:sceptre-lifecycle-provider-{hook.constants.APP_VPC}"
    test_hook._invoke_lambda = intercept_invoke_lambda
    test_hook._get_stack = lambda: stack

    test_hook.run()
