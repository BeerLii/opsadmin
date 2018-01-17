import paramiko
from six import StringIO
from six import string_types

def ssh_key_string_to_obj(text):
    key = None
    try:
        key = paramiko.RSAKey.from_private_key( StringIO(text) )
    except paramiko.SSHException:
        pass

    try:
        key = paramiko.DSSKey.from_private_key( StringIO(text) )
    except paramiko.SSHException:
        pass
    return key


def ssh_pubkey_gen(private_key=None, username='bwei', hostname='localhost'):
    if isinstance(private_key, bytes):
        private_key = private_key.decode("utf-8")
    if isinstance(private_key, string_types):
        private_key = ssh_key_string_to_obj(private_key)
    if not isinstance(private_key, (paramiko.RSAKey, paramiko.DSSKey)):
        raise IOError('Invalid private key')

    public_key = "%(key_type)s %(key_content)s %(username)s@%(hostname)s" % {
        'key_type': private_key.get_name(),
        'key_content': private_key.get_base64(),
        'username': username,
        'hostname': hostname,
    }
    return public_key