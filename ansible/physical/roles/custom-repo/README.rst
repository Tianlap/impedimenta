Custom Repository
=================

Create and serve a repository of custom packages.

When invoked, this role will do the following:

#. Create a privileged system user dedicated to compiling packages.
#. Install aurutils 2.y.
#. Create a repository, and list it in pacman.conf(5). It would be better if the
   latter step could be omitted, but see the `discussion`_ below.
#. Download and compile several packages, and place them into the repository.
#. Configure systemd to automatically update the repository.

The repository and its contents aren't automatically made available. The
repository must be made available through some other means (such as via nginx).

.. WARNING:: aurutils is installed via the `aurutils-git`_ package.

Variables
---------

All variables are optional, due to having default values.

``custom_repo_path_prefix``
    The directory within which the repository will be created.

``custom_repo_name``
    The name of the repository being created. Consider using a limited set of
    characters for this name, like ``[a-zA-Z-_]+``, as it will be used when
    modifying pacman.conf(5), when generating filesystem path names, and more.

``custom_repo_path``
    The full path to the repository. Derived from ``custom_repo_path_prefix``
    and ``custom_repo_name``.

``custom_repo_db``
    The full path to the repository's database file. Derived from
    ``custom_repo_path``.

``custom_repo_packages``
    The packages to download, compile, and place in the repository. Defaults to
    an empty list.

``custom_repo_auto_update``
    Should the repository's packages automatically be updated when a new AUR
    package is released?

``custom_repo_user``
    The privileged system user who compiles packages. Not named
    ``custom_repo_packager`` because the term "packager" is closely associated
    with living, breathing human beings who do things like sign off on packages.

``custom_repo_user_home``
    The privileged system user's home directory.

Sample Playbook
---------------

.. code-block:: yaml

    - hosts: webservers
      roles:
        - name: custom-repo
          vars:
            custom_repo_name: ichi-public
            custom_repo_packages:
              - entr
              - systemd-boot-pacman-hook

Discussion
----------

For a recipe for compiling a package to a repository on a once-off basis (as
opposed to through Ansible), see the aur-build(1) man page.

To remove package "foo" from a repository named "custom", execute something like
this:

.. code-block:: sh

    # Remove "foo" from the database listing.
    sudo -u custom-repo-user repo-remove \
        /srv/packages.example.com/arch-linux/custom/custom.db.tar.xz foo

    # Remove "foo" packages from the filesystem.
    rm -f /srv/packages.example.com/arch-linux/custom/foo-*

    # Refresh pacman's database, so it knows about "foo" being removed from
    # "custom."
    pacman -Sy --config /etc/pacman.d/custom.conf

----

Consider the following use case:

    I want to compile AUR packages A and B and add them to a custom repository.
    A (make)depends on B, and B (make)depends on official packages. I don't want
    to locally install A or B. Instead, I want to make them availble to other
    hosts over the network.

How can this be accomplished? Repository management can be done with the
``repo-*`` executables as provided by core/pacman. And B can be compiled with
tools like makechrootpkg(1) as provided by extra/devtools. But there are several
pain points:

* If compiling A, one must start by installing B.
* If A or B are updated on the AUR, then the corresponding local packages won't
  automatically be updated.

aurutils addresses these pain points, though with some twists. The most curious
one is that pacman.conf(5) must contain an entry for each repository being
managed. While the reason is unknown to me, I think this requirement exists for
one the following reason: When compiling A, one of the first steps will be to
install B, and this can only be done if pacman.conf(5) lists a repository that
provides B.

The marriage to pacman.conf(5) creates risk. Imagine that the custom repository
contains a custom version of a package already provided by the official
repositories. In this case, the build server could inadvertently install the
custom package. No solution is currently known, beyond "be careful about what
you package."

One could try working around this issue by creating a custom pacman
configuration file that references the target custom repository, and asking the
various aurutils to use it when compiling packages:

.. code-block:: sh

    #!/usr/bin/env bash
    # coding=utf-8
    set -euo pipefail

    root="$(realpath custom)"
    mkdir "${root}"
    repo-add "${root}/custom.db.tar.xz"

    cp /usr/share/devtools/pacman-extra.conf pacman-custom.conf
    echo '[custom]' >> pacman-custom.conf
    echo 'SigLevel = Optional TrustAll' >> pacman-custom.conf
    echo "Server = file://${root}" >> pacman-custom.conf

    aur sync \
        --chroot \
        --database custom \
        --root "$(realpath custom)" \
        --pacman-conf pacman-custom.conf \
        entr

However, this fails for reasons that are unclear to me. At this time, the best
available solution is "be careful about what you package."

If one does wish to install an AUR package on the build server, it's advisable
to **NOT** list the custom repository as a ``CacheDir`` in pacman.conf(5). Doing
this will save disk space, but a simple ``pacman -Sc`` (or ``-Scc``) can blow
away packages in a cache.

.. _aurutils-git: https://aur.archlinux.org/packages/aurutils-git/
