aur
===

Package and install software from the AUR, using aurutils.

This role is designed to address the needs of an Arch Linux and Ansible user
who'd like to locally package and install packages from the AUR, using aurutils.
When invoked, this role will:

1. Create a privileged system user dedicated to building packages.
2. Install aurutils.
3. Create a package cache in `/var/cache/pacman/aur/`. Let this cache be owned
   by the user.
4. Create a repository named `aur`, and make `/etc/pacman.conf` include it.
5. Package and install the packages named by the `aur_packages` variable.

This role doesn't allow one to serve packages over a network. Instead, only the
local system may consume compiled packages.

Variables:

* `aur_packages`: Required. The AUR packages to compile.
* `aur_user`: Optional. The name of the local system user that will compile and
  own packages.
* `aur_user_home`: Optional. The AUR user's home directory.

Sample playbook:

```yaml
- hosts: all
  roles:
    - name: aur
      vars:
        aur_packages:
          - systemd-boot-pacman-hook
```
