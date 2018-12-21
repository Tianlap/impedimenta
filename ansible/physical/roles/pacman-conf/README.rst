pacman-repos
============

Configure pacman.conf(5) and the files it includes. [1]

When invoked, this role will do the following:

#. Create and delete configuration files in ``/etc/pacman.d/``.
#. Install ``/etc/pacman.conf``. Ensure pacman.conf includes all files in
   ``/etc/pacman.d/*.conf``. This globbing approach is used so that other roles
   may also install custom repositories.

Variables
---------

No variables are supported. Customization is done via file templates. This role
is not generic.

Sample Playbook
---------------

.. code-block:: yaml

    - hosts: all
      roles:
        - pacman-repos

.. [1] This role doesn't configure ``/etc/pacman.d/mirrorlist``. This role may
    subsume the ``update-mirrorlist`` role at some point in the future.
