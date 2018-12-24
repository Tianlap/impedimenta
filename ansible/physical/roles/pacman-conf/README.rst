pacman-conf
===========

Configure pacman.conf(5) and the files it includes, and schedule maintenance.

When invoked, this role will do the following:

#. Create and delete configuration files in ``/etc/pacman.d/``.
#. Install ``/etc/pacman.conf``. Ensure pacman.conf includes all files in
   ``/etc/pacman.d/*.conf``. This globbing approach is used so that other roles
   may also install custom repositories.
#. Install, start and enable ``update-mirrorlist.{service,timer}``, which use
   `reflector`_ to update ``/etc/pacman.d/mirrorlist``.
#. Start and enable ``paccache.timer``, which uses `paccache`_ to prune cached
   packages.

Variables
---------

No variables are supported. Customization is done via mechanisms like file
templates. This role is not generic across varying environments, and is instead
tightly bound to the author's target environment.

Sample Playbook
---------------

.. code-block:: yaml

    - hosts: all
      roles:
        - pacman-repos

.. _paccache: https://wiki.archlinux.org/index.php/Pacman#Cleaning_the_package_cache
.. _reflector: https://wiki.archlinux.org/index.php/Reflector
