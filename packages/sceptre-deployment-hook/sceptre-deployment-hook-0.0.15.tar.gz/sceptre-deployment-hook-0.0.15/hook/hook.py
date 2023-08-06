import inspect
import json
from datetime import datetime

from sceptre.hooks import Hook
from sceptre.plan.actions import StackActions

from hook.constants import GIT_BRANCH_NAME, JOB_ID, AWS_REGION, AWS_ACCOUNT_ID, APP_VPC, LAST_GIT_COMMIT_MESSAGE


class CustomHook(Hook):
    def __init__(self, *args, **kwargs):
        super(CustomHook, self).__init__(*args, **kwargs)
        self._function_name = \
            f"arn:aws:lambda:{AWS_REGION}:{AWS_ACCOUNT_ID}:function:sceptre-lifecycle-provider-{APP_VPC}"

    def run(self):
        """
        run is the method called by Sceptre. It should carry out the work
        intended by this hook.
        """
        # self.argument == "deploy_start" || "deploy_end"
        try:
            stack = self._get_stack()
            self.lambda_handler(self.argument, stack)
        except AssertionError:
            raise
        except Exception as e:
            print(e)
            # just ignore all other errors for now
            pass

    def lambda_handler(self, method: str, stack) -> None:
        payload = {
            "method": method,
            "git_commit_message": LAST_GIT_COMMIT_MESSAGE,
            "git_branch_name": GIT_BRANCH_NAME,
            "stack_name": stack.name,
            "ci_job_id": JOB_ID,
            "time": datetime.utcnow().isoformat()
        }
        self._invoke_lambda(payload)

    def _invoke_lambda(self, payload: dict) -> None:
        self.stack.connection_manager.call(
            "lambda",
            "invoke",
            kwargs={
                "FunctionName": self._function_name,
                "InvocationType": "RequestResponse",
                "Payload": json.dumps(payload)
            },
            region=AWS_REGION
        )

    @staticmethod
    def _get_stack():
        #  Get reference to 'decorated' function in call stack. This is where sceptre hooks are applied.
        #  Moreover, the 'decorated' function has a reference to StackActions containing the correct Stack-instance.
        #  The 'self.stack' in this object is not necessarily the right Stack.
        fr = next(stack for stack in inspect.stack() if stack.function == 'decorated')[0]
        args, _, _, value_dict = inspect.getargvalues(fr)
        instance = value_dict['self'] if len(args) and args[0] == 'self' else None
        return instance.stack if isinstance(instance, StackActions) else None
