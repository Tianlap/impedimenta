borg-backup-users
=================

Configure per-user backups with `Borg`_.

More specifically, do the following:

1.  Install borg.
2.  For each user for whom backups should be configured:

    1.  Install a private SSH key at ``~/.ssh/borg-backup``
    2.  Customize ``~/.ssh/config``.
    3.  Install a script to perform a backup, at
        ``~/.local/bin/borg-backup.sh``.
    4.  Install, start and enable per-user units to periodically call the backup
        script. Note that lingering is *not* enabled.

The Borg repositories on the remote backup host are distinguished by user names.
As a result, multiple users may back up to the same remote backup host.

Example playbook:

.. code-block:: yaml

    - hosts: borg-backup-users-hosts
      roles:
        - borg-backup-users
      vars:
        borg_backup_users_passphrases:
          alice: password
        borg_backup_users_private_keys:
          alice: /path/to/key
        borg_backup_users:
          - local_user: alice
            local_paths:
              - ~/Documents
              - ~/'my other stuff'
            remote_host: borg-host.example.com
            remote_user: borg-user

Variables:

``borg_backup_users``
    Optional, but most tasks are skipped if omitted. A list of users for whom
    backups will be configured. Each list entry is a dict with the following
    keys:

    ``local_user``
        Required. The name of the user for whom backups will be configured.

    ``local_paths``
        Optional, and defaults to ``["~/Documents", "~/Pictures"]``.  The
        paths to back up to the remote Borg repository. These paths are subject
        to Bash's expansion rules. If the paths contain whitespace or other
        interesting characters, consider using single quotes.

    ``remote_host``
        Optional, but some tasks are skipped if omitted. The hostname of the
        host which will host Borg backups.

    ``remote_user``
        Optional, but some tasks are skipped if omitted. The username on the
        remote host who will host borg backups.

``borg_backup_users_passphrases``
    Optional, but some tasks are skipped if omitted. Defaults to an empty dict.
    Maps user names to the passphrases that those users will use when decrypting
    the remote Borg repository.

``borg_backup_users_private_keys``
    Optional, but some tasks are skipped if omitted. Maps user names to paths
    to private SSH keys. These SSH keys are used when SSH-ing into the host that
    hosts Borg repositories.

.. _Borg: https://borgbackup.readthedocs.io/en/stable/
