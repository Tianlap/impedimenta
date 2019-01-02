netctl-generic
==============

Install, configure, start and enable netctl network configuration.

Netctl is Arch Linux's home-brew network configuration manager. It's especially
suitable for relatively static hosts, like headless servers. This role does the
following:

1. Install netctl.
2. Install a configuration file for the "external" interface. If the
   configuration file is changed in any way, also update the corresponding
   systemd service file. (This includes initial installation.)

   The profile is called "external" as opposed to "lan" because the interface
   might not actually be attached to a LAN. It could also be attached to a DMZ.
   Or, if the target compuer is a virtual machine, it could be attached to a
   logical network. "External" is a generic term that reasonably covers all of
   these cases.
3. Start and enable each of the systemd services.

Required variables:

* `netctl_generic_external_if`: The name of the "external" network interface.
