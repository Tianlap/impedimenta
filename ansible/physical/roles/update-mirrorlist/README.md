update-mirrorlist
=================

Periodically update pacman's mirrorlist.

Install the following units:

* `update-mirrorlist.service`
* `update-mirrorlist.timer`

These units use [reflector](https://wiki.archlinux.org/index.php/Reflector).

Example Playbook
----------------

```yaml
- hosts: all
  roles:
    - update-mirrorlist
```
