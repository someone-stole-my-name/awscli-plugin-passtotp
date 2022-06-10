from botocore.exceptions import ProfileNotFound
import subprocess
import sys


class PassTotpPrompter(object):
    def __init__(self, mfa_path, original_prompter=None):
        self.mfa_path = mfa_path
        self._original_prompter = original_prompter

    def __call__(self, prompt):
        try:
            pass_result = subprocess.run(
                ["pass", "otp", self.mfa_path], capture_output=True
            )
            token = pass_result.stdout.decode("utf-8").strip()
            return token
        except subprocess.CalledProcessError as e:
            print(e, file=sys.stderr)

        if self._original_prompter:
            return self._original_prompter(prompt)

        return None

def inject_pass_totp_prompter(session, **kwargs):
    try:
        providers = session.get_component("credential_provider")
    except ProfileNotFound:
        return

    config = session.get_scoped_config()
    mfa_path = config.get("mfa_path")
    if mfa_path is None:
        return

    assume_role_provider = providers.get_provider("assume-role")
    original_prompter = assume_role_provider._prompter
    assume_role_provider._prompter = PassTotpPrompter(
        mfa_path, original_prompter=original_prompter
    )
