from pandas.io.json import json_normalize
import json
import os
import getpass
import keyring

PASSWORD_KEY = "gpg"

def clear_password_cache():
    keyring.delete_password(PASSWORD_KEY, PASSWORD_KEY)

def cache_password(password):
    keyring.set_password(PASSWORD_KEY, PASSWORD_KEY, password)

def get_password():
    password = keyring.get_password(PASSWORD_KEY, PASSWORD_KEY)
    if not password:
        password = getpass.getpass("gpg password: ")

    return password

def normalize(data_as_json):
    return json_normalize(data_as_json)

def _normalize(data_as_json):
    if len(data_as_json) > 0:
        return json.loads(normalize(data_as_json).to_json())

def extract_columns(data_as_json):
    if len(data_as_json) > 0:
        return _normalize(data_as_json).keys()


def pretty_print_column_names(data_as_json):
    if len(data_as_json) > 0:
        columns = extract_columns(data_as_json)
        return "\t".join(columns)

def pretty_print_rows(data_as_json):
    columns = extract_columns(data_as_json)
    data = _normalize(data_as_json)
    rows = []
    if data:
        n = len(data[columns[0]])
        for i in xrange(n):
            row_data = []
            for c in columns:
                token = str(data[c][str(i)])
                if token[0] == '[':
                    token = ''
                row_data.append(token)
            rows.append("\t".join(row_data))

    return "\n".join(rows)
