# qmyf

# About

`qmyf` stands for Query My Financial data.  It is a commandline wrapper for the https://plaid.com/ api.

# Usage
```
Usage:
  qmyf.py init <client> <secret> <gpgkeyname> [--gpghomedir=<gpghomedir>] [--gpgbinary=<gpgbinary>] [--plaid-endpoint=<plaidendpoint>]
  qmyf.py auth <inst>
  qmyf.py mfainit <inst> (phone|email)
  qmyf.py authmfa <inst> <code>
  qmyf.py token <inst>
  qmyf.py (inst|privacy|noprompt|prompt)
  qmyf.py q <inst> <search>
  qmyf.py -h | --help | --version
Options:
  --plaid-endpoint=<plaidendpoint>  endpoint url [default: https://api.plaid.com]
  --gpghomedir=<gpghomedir>         gnupg home dir [default: ~/.gnupg]
  --gpgbinary=<gpgbinary>           gpgbinary path [default: /usr/local/bin/gpg]
```

# Commands

- `init` - initiates configuration file.
- `auth` - adds insitution for authorization i.e. bofa, chase, etc.
- `mfainit` - engages multi-factor authentication (MFA) with institution.
- `token` - print institution access token.
- `inst` - print institutions available for use with plaid.
- `privacy` - prints plaid privacy statement.
- `[no]prompt` - enables/disables password storage in keychain so user doesn't need to continually be prompted for such.
- `q` - query institutional data.
