Release Notes
=============

2.1.12
------

icinga
~~~~~~

The icinga client address was `hostvars[inventory_hostname]['ansible_host']` prior
to 2.1.12. It now is `icinga_client_address` which defaults to `hostvars[inventory_hostname]['ansible_host']`.
It can be used to resolve the following problem:

* The icinga master has a private IP and no public IP
* The icinga master goes through a router with a public IP
* The icinga client has a public IP which is the default for `icinga_client_address`
* The icinga master tries to ping the icinga client public IP but fails because the firewall of the client does not allow ICMP from the router public IP

The `icinga_client_address` of the client is set to the internal IP
instead of the public IP. The ping will succeed because the firewall
allows ICMP from any host connected to the internal network.

Development
~~~~~~~~~~~

* Added basic `support for running tests with libvirt <https://lab.enough.community/main/infrastructure/-/merge_requests/302>`__
  instead of OpenStack.
