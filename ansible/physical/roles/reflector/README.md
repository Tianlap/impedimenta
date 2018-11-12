reflector
=========

Periodically update pacman's mirrorlist.

Uses [reflector](https://wiki.archlinux.org/index.php/Reflector). Installs the
following units:

* `update-mirrorlist.service`
* `update-mirrorlist.timer`

Example Playbook
----------------

```yaml
- hosts: all
  roles:
    - reflector
```
