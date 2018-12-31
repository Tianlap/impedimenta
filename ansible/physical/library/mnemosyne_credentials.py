#!/usr/bin/env python
# coding=utf-8
"""Set mnemosyne's sync server credentials.

For basic module development information, see `Ansible module development:
getting started
<https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html>`_.
"""
import pathlib
import sqlite3

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community',
}

DOCUMENTATION = '''
---
module: mnemosyne_credentials

short_description: "Set mnemosyne's sync server credentials."

options:
    username:
        description: The sync server username to set.
        required: true
    password:
        description: The sync server password to set.
        required: true
'''

EXAMPLES = '''
- name: Set mnemosyne's sync server credentials
  mnemosyne_credentials:
    username: Alice
    password: super-secret
  become: true
  become_user: mnemosyne-user
'''

RETURN = '''
A changed status if the credentials were changed.
'''


def main():
    """Set mnemosyne's sync server credentials."""
    argument_spec = {
        'password': {'required': True, 'type': str, 'no_log': True},
        'username': {'required': True, 'type': str},
    }
    module = AnsibleModule(argument_spec=argument_spec)
    db_path = pathlib.Path.home().joinpath('.config/mnemosyne/config.db')
    changed = False
    changed_attrs = []

    for key in ('username', 'password'):
        curr_val = get_attr(db_path, key)
        new_val = module.params[key]
        # Why call repr()? See:
        # https://bugs.launchpad.net/mnemosyne-proj/+bug/1644402
        if curr_val != repr(new_val):
            changed = True
            changed_attrs.append(key)
            set_attr(db_path, key, new_val)

    if changed_attrs:
        message = 'Attributes changed: ' + ', '.join(changed_attrs)
    else:
        message = 'No attributes changed.'
    module.exit_json(changed=changed, message=message)


def get_attr(db_path, attr):
    """Get an attribute from mnemosyne's database.

    :param db_path: The path to mnemosyne's database.
    :param attr: The attribute to get. Either 'username' or 'password'.
    """
    queries = {
        'username': """
            SELECT value
            FROM config
            WHERE key = "remote_access_username"
        """,
        'password': """
            SELECT value
            FROM config
            WHERE key = "remote_access_password"
        """,
    }
    query = queries[attr]
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute(query).fetchone()[0]
    finally:
        conn.close()


def set_attr(db_path, attr, value):
    """Set an attribute in mnemosyne's database.

    :param db_path: The path to mnemosyne's database.
    :param attr: The attribute to set. Either 'username' or 'password'.
    :param value: The new value for the attribute.
    """
    queries = {
        'username': """
            UPDATE config
            SET value = ?
            WHERE key = "remote_access_username"
        """,
        'password': """
            UPDATE config
            SET value = ?
            WHERE key = "remote_access_password"
        """,
    }
    query = queries[attr]
    conn = sqlite3.connect(db_path)
    try:
        # Why call repr()? See:
        # https://bugs.launchpad.net/mnemosyne-proj/+bug/1644402
        with conn:
            conn.execute(query, (repr(value),))
    finally:
        conn.close()


if __name__ == '__main__':
    exit(main())
