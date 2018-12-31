btrfs-subvolume
===============

Periodically create and delete snapshots of btrfs subvolumes.

Snapshots of each subvolume are made alongside the subvolumes themselves. For
example, if there are subvolumes at `/mnt/btrfs/home` and `/mnt/btrfs/srv/ftp`,
then snapshots will be created with names of the form
`/mnt/btrfs/home-${timestamp}` and `/mnt/btrfs/srv/ftp-${timestamp}`. Timestamps
are in ISO 8601 datetime format.

Example playbook:

```yaml
- hosts: all
  roles:
  - name: btrfs-subvolume
    vars:
      btrfs_subvolumes:
      - {path: /mnt/btrfs/home}
      - {path: /mnt/btrfs/srv/ftp, days: 5, weeks: 2}
```

Variables:

* `btrfs_subvolumes` Optional, defaults to an empty list. A list of objects,
  where each object contains some information about a subvolume to manage. The
  following attributes may appear in each object. If empty, only a few
  preliminary tasks are executed, such as installing btrfs-progs.
  * `path` Required. The path to a subvolue, relative to `btrfs_path`.
  * `days` Optional, defaults to 14. How many days may will old snapshots be
    retained? Only has an effect when `delete` is true.
  * `weeks` Optional, defaults to 8. How many weeks will old snapshots be
    retained? Only has an effect when `delete` is true.
  * `snapshot` Optional, defaults to true. Whether to install subvolume snapshot
    code.
  * `delete` Optional, defaults to true. Whether to instsall subvolume deletion
    code.

For more information on `days` and `weeks`, see the `btrfs-subvolume-delete.py`
script installed by this role.
