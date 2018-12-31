workstation
===========

Install and configure a GUI workstation.

Install applications that are useful in a GUI desktop environment. Start and/or
enable several useful services, such as a login manager and CUPS. One notable
side-effect is that the uucp group is created when picocom is installed.

Variables:

``workstation_video_drivers``
    Packages to install to provide video drivers, e.g. ``xf86-video-amdgpu``.
    For more information, see the Arch Wiki page on `hardware video acceleration
    <https://wiki.archlinux.org/index.php/Hardware_video_acceleration>`_.
