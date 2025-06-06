#!/usr/bin/env python

#
# test_rip_topo1.py
# Part of NetDEF Topology Tests
#
# Copyright (c) 2017 by
# Network Device Education Foundation, Inc. ("NetDEF")
#
# Permission to use, copy, modify, and/or distribute this software
# for any purpose with or without fee is hereby granted, provided
# that the above copyright notice and this permission notice appear
# in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND NETDEF DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL NETDEF BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
#

"""
test_rip_topo1.py: Testing RIPv2

"""

import os
import re
import sys
import pytest
from time import sleep

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, Host
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Intf

from functools import partial

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fatal_error = ""

class Router(Node):
    def config( self, **params ):
        super(Router, self).config(**params)

        r = self.name
        print("Configure " + r + "\n")
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        # Enable loose reverse path filtering
        self.cmd( 'sysctl net.ipv4.conf.all.rp_filter=2' )

        zebra = "/usr/lib/frr/zebra"
        ripd = "/usr/lib/frr/ripd"

        # # do some mounts bind to make the daemons working
        r = self.name
        self.cmd( "mkdir /tmp/{} && chown frr /tmp/{}".format(r, r) )
        self.cmd( "mount --bind /tmp/{} /var/run/frr".format(r) )
        self.cmd( "mount --bind {} /etc/frr".format(r) )

        # Run the daemons
        self.cmd( "{} -f {}/zebra.conf -d > /tmp/{}/zebra.log 2>&1".format(zebra, r, r) )
        self.waitOutput()

        self.cmd( "{} -f {}/ripd.conf -d > /tmp/{}/ripd.log 2>&1".format(ripd, r, r) )
        self.waitOutput()

    def terminate( self ): 
        r = self.name
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        self.cmd( 'sysctl net.ipv4.conf.all.rp_filter=0' )

        self.cmd( "killall bgpd staticd zebra" )
        self.cmd( "umount /var/run/frr" )
        self.cmd( "umount /etc/frr" )
        self.cmd( "rm -fr /tmp/{}".format(r) )
        super(Router, self).terminate()


class LegacySwitch(OVSSwitch):
    "A Legacy Switch without OpenFlow"
    def __init__(self, name, **params):
        OVSSwitch.__init__(self, name, failMode='standalone', **params)
        self.switchIP = None

#####################################################
##
##   Network Topology Definition
##
#####################################################

class NetworkTopo(Topo):
    "RIP Topology 1"

    def build(self, **_opts):

        # Setup Routers
        router = {}
        #
        # Setup Main Router
        router[1] = self.addNode('r1', cls = Router)
        #
        # Setup RIP Routers
        for i in range(2, 4):
            router[i] = self.addNode('r%s' % i, cls = Router)
        #
        # Setup Switches
        switch = {}
        #
        # On main router
        # First switch is for a dummy interface (for local network)
        switch[1] = self.addSwitch('sw1', cls=LegacySwitch)
        self.addLink(switch[1], router[1], intfName2='r1-eth0')
        #
        # Switches for RIP
        # switch 2 switch is for connection to RIP router
        switch[2] = self.addSwitch('sw2', cls=LegacySwitch)
        self.addLink(switch[2], router[1], intfName2='r1-eth1')
        self.addLink(switch[2], router[2], intfName2='r2-eth0')
        # switch 3 is between RIP routers
        switch[3] = self.addSwitch('sw3', cls=LegacySwitch)
        self.addLink(switch[3], router[2], intfName2='r2-eth1')
        self.addLink(switch[3], router[3], intfName2='r3-eth1')
        # switch 4 is stub on remote RIP router
        switch[4] = self.addSwitch('sw4', cls=LegacySwitch)
        self.addLink(switch[4], router[3], intfName2='r3-eth0')



#####################################################
##
##   Tests starting
##
#####################################################

def run():
    global topo, net

    print("Cleanup old Mininet runs")
    os.system('sudo mn -c > /dev/null 2>&1')

    thisDir = os.path.dirname(os.path.realpath(__file__))
    topo = NetworkTopo()

    net = Mininet(controller=None, topo=topo)
    net.start()

    # Starting Routers
    #
    for i in range(1, 4):
        net['r%s' % i].cmd('/usr/lib/frr/zebra %s/r%s/zebra.conf' % (thisDir, i))
        net['r%s' % i].cmd('/usr/lib/frr/ripd %s/r%s/ripd.conf' % (thisDir, i))

    # For debugging after starting Quagga/FRR daemons, uncomment the next line
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()