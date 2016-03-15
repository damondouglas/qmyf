"""
Usage:
  qmyf.py init <client> <secret> <gpgkeyname> [--gpghomedir=<gpghomedir>] [--gpgbinary=<gpgbinary>] [--plaid-endpoint=<plaidendpoint>]
  qmyf.py auth <inst>
  qmyf.py (inst|privacy|noprompt|prompt)
  qmyf.py q <inst> <search>
  qmyf.py -h | --help | --version

Options:
  --plaid-endpoint=<plaidendpoint>  endpoint url [default: https://api.plaid.com]
  --gpghomedir=<gpghomedir>         gnupg home dir [default: ~/.gnupg]
  --gpgbinary=<gpgbinary>           gpgbinary path [default: /usr/local/bin/gpg]

"""
import sys; sys.path.append('lib')
from docopt import docopt
import json, os, sys, getpass
from qmyf import crypt
from qmyf import common
from plaid import Client
from plaid import errors as plaid_errors

def _q(arguments):
    inst = arguments['<inst>']
    search = arguments['<search>']
    passphrase = _get_gpg_password()
    crypter_util = crypt.Crypt()
    cached_inst = crypter_util.decrypt_json_from_file('%s.gpg' % inst, passphrase)
    access_token = cached_inst['access_token']
    client = _get_plaid_client(passphrase, access_token=access_token)
    response = client.connect_get()
    data = json.loads(response.content)
    transactions = data['transactions']
    print common.pretty_print_column_names(transactions)
    print common.pretty_print_rows(transactions)

def _privacy(arguments):
    print """
        Privacy Policy can be read at https://plaid.com/legal.
    """

def _prompt(arguments):
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])
    choice = raw_input("Do you want to delete cached password? [Y|n]").lower()
    if choice in yes:
        common.clear_password_cache()
        print "password is no longer cached."

def _noprompt(arguments):
    crypter_util = crypt.Crypt()
    password = _get_gpg_password()
    message = "this is a test"
    encrypted = crypter_util.encrypt(message)
    decrypted = crypter_util.decrypt(encrypted, password)

    if message != decrypted:
        raise Exception("password supplied is not valid")
    else:
        common.cache_password(password)
        print "password is now cached."

# non upgraded accounts should use <plaidendpoint>: https://tartan.plaid.com
def _init(arguments):
    config = {
        'gpghomedir': arguments['--gpghomedir'],
        'gpgbinary': arguments['--gpgbinary'],
        'gpgkeyname': arguments['<gpgkeyname>']
    }
    f = open('config.json', 'w')
    data = json.dumps(config)
    f.write(data)
    f.flush(); f.close()

    cred = {'client': arguments['<client>'], 'secret': arguments['<secret>'], 'plaidendpoint': arguments['--plaid-endpoint']}
    crypter_util = crypt.Crypt()
    crypter_util.encrypt_json_to_file(cred, 'plaid.gpg')

def _check_if_init():
    if not os.path.exists('config.json') or not os.path.exists('plaid.gpg'):
        print 'First run '
        print '$ qmyf.py init <client> <secret> <gpgkeyname>'
        sys.exit(0)

def _get_plaid_client(passphrase, access_token = None):

    f = open('plaid.gpg', 'r')
    plaid_config_data_gpg = f.read()
    f.close()

    crypter_util = crypt.Crypt()
    plaid_config_data = crypter_util.decrypt(plaid_config_data_gpg, passphrase)
    plaid_config = json.loads(plaid_config_data)

    Client.config({
        'url': plaid_config['plaidendpoint']
    })

    return Client(client_id=plaid_config['client'], secret=plaid_config['secret'], access_token=access_token)

def _get_gpg_password():
    return common.get_password()

def _auth(arguments):
    _check_if_init()
    passphrase = _get_gpg_password()
    client = _get_plaid_client(passphrase)
    crypter_util = crypt.Crypt()
    inst = arguments['<inst>']
    username = raw_input("%s username: " % inst)
    password = getpass.getpass("%s password: " % inst)

    if client and username and password and inst:
        try:
            response = client.connect(inst, {
                'username': username,
                'password': password
            })
            if response.ok:
                data = response.content
                if data:
                    data = json.loads(data)
                    access_token = data['access_token']
                    auth_data = {
                        'access_token': access_token,
                        'inst': inst
                    }

                    crypter_util.encrypt_json_to_file(auth_data, "%s.gpg" % inst)
                    print "institution authorization stored in %s.gpg" % inst

        except plaid_errors.UnauthorizedError as e:
            print e

def _inst(arguments):
    passphrase = _get_gpg_password()
    client = _get_plaid_client(passphrase)
    institutions = json.loads(client.institutions().content)
    categories = json.loads(client.categories().content)
    print common.pretty_print_column_names(institutions)
    print common.pretty_print_rows(institutions)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.1')
    for func in arguments:
        if arguments[func] and '_'+func in locals():
            locals()['_'+func](arguments)
