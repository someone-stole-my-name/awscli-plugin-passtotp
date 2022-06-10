# AWS CLI MFA with pass-otp made easy

This plugin enables aws-cli to directly talk to [pass](https://www.passwordstore.org/)
to acquire an OATH-TOTP code using the [pass-otp](https://github.com/tadfisher/pass-otp) extension.

## Installation

`awscli-plugin-passtotp` can be installed from PyPI:
```sh
$ pip install awscli-plugin-passtotp
```

It's also possible to install it just for your user in case you don't have
permission to install packages system-wide:
```sh
$ pip install --user awscli-plugin-passtotp
```

### Configure AWS CLI

To enable the plugin, add this to your `~/.aws/config`:
```ini
[plugins]
# If using aws-cli v2 you must specify the path to where the package was installed.
cli_legacy_plugin_path = /foo/bar/lib/python3.9/site-packages/

passtotp = awscli_plugin_passtotp
```

Also make sure to specify a path to a file in your password-store in the profiles managed by pass:
```ini
[profile myprofile]
role_arn = arn:aws:iam::...
mfa_serial = arn:aws:iam::...
mfa_path = foo/aws/bar
...
```

## Usage

Just use the `aws` command with a custom role and the plugin will do the rest:

```sh
$ aws s3 ls --profile myprofile
2013-07-11 17:08:50 mybucket
2013-07-24 14:55:44 mybucket2
```

---

## Acknowledgements
* Thanks to [@tommie-lie](https://github.com/woowa-hsw0) for the [inspiration for this plugin](https://github.com/tommie-lie/awscli-plugin-yubikeytotp)
