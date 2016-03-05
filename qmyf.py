"""
Usage:
  qmyf.py init <client> <secret> <gpgkeyname> [--gpghomedir=<gpghomedir>] [--gpgbinary=<gpgbinary>]
  qmyf.py auth (bofa|chase) <username> <password>
  qmyf.py inst
  qmyf.py -h | --help | --version

Options:
  --gpghomedir=<gpghomedir>     gnupg home dir [default: ~/.gnupg]
  --gpgbinary=<gpgbinary>       gpgbinary path [default: /usr/local/bin/gpg]
"""
import sys; sys.path.append('lib')
from docopt import docopt
import json, os, sys, getpass
from qmyf import crypt

def _init(arguments):
    config = {'gpghomedir': arguments['--gpghomedir'], 'gpgbinary': arguments['--gpgbinary'], 'gpgkeyname': arguments['<gpgkeyname>']}
    f = open('config.json', 'w')
    data = json.dumps(config)
    f.write(data)
    f.flush(); f.close()

    cred = {'client': arguments['<client>'], 'secret': arguments['<secret>']}
    crypter_util = crypt.Crypt(config)
    cred_data = json.dumps(cred)
    encrypted_cred_data = crypter_util.encrypt(cred_data)

    f = open('plaid.gpg','w')
    f.write(encrypted_cred_data)
    f.flush(); f.close()

def _check_if_init():
    if not os.path.exists('config.json') or not os.path.exists('plaid.gpg'):
        print 'First run '
        print '$ qmyf.py init <client> <secret> <gpgkeyname>'
        sys.exit(0)

def _get_plaid_client(passphrase):
    f = open('config.json', 'r')
    data = f.read()
    f.close()
    config = json.loads(data)

    f = open('plaid.gpg', 'r')
    plaid_config_data_gpg = f.read()
    f.close()

    crypter_util = crypt.Crypt(config)
    plaid_config_data = crypter_util.decrypt(plaid_config_data_gpg, passphrase)
    plaid_config = json.loads(plaid_config_data)

    from plaid import Client
    Client.config({
        'url': 'https://api.plaid.com'
    })

    return Client(client_id=plaid_config['client'], secret=plaid_config['secret'])

def _get_password():
    return getpass.getpass("gpg password: ")

def _auth(arguments):
    _check_if_init()
    _get_password()
    username = arguments['<username>']
    password = arguments['<password>']

    for inst in ['bofa', 'chase']:
        if arguments[inst]:
            client = Client(client_id=plaid_config['client'], secret=plaid_config['secret'])
            try:
                response = client.connect(inst, {
                    'username': username,
                    'password': password
                })
                print(response)
            except e:
                print e

def _inst(arguments):
    passphrase = _get_password()
    client = _get_plaid_client(passphrase)
    institutions = json.loads(client.institutions().content)
    categories = json.loads(client.categories().content)
    print institutions

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.1')
    for func in arguments:
        if arguments[func] and '_'+func in locals():
            locals()['_'+func](arguments)
