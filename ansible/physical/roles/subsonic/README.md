subsonic
========

Install, configure, start and enable Subsonic.

In addition:

* Install several transcoders, and ensure the subsonic user can access them.
* Configure periodic backups of Subsonic's database.
* Delete outdated files that might be lying around from previous implementation
  of this role and the `user-subsonic-backup` role.
* Ensure that only the "subsonic" user can access Subsonic's database.
* Add the "subsonic" user to groups `ichimonji10` and `transmission`, so that it
  can view the corresponding users' files.
* Create a podcasts directory.
