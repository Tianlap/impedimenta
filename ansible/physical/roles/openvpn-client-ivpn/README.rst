openvpn-client-ivpn
===================

Install OpenVPN, and configure for split routing.

When connecting to the VPN, don't accept routes pushed by the server. Instead,
only make traffic with a source address equal to that of the tunnel interface go
through the VPN.

Variables
---------

``openvpn_client_ivpn_username``
    The username that openvpn should use when connecting. Optional, but certain
    tasks are skipped when omitted.

``openvpn_client_ivpn_password``
    The password that openvpn should use when connecting. Optional, but certain
    tasks are skipped when omitted.
