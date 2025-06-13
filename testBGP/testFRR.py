#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Switch
from mininet.log import setLogLevel
from mininet.cli import CLI
import os
from time import sleep
import termcolor as T


def log(s, col="green"):
    # Up to python3
    # print T.colored(s, col)
    print(T.colored(s,col))


class Router(Switch):
    ID = 0
    def __init__(self, name, **kwargs):
        kwargs['inNamespace'] = True
        Switch.__init__(self, name, **kwargs)
        Router.ID += 1
        self.switch_id = Router.ID

    def start(self, controllers):
        r = self.name
        log('Setting up %s...' % r)
        self.cmd("sudo sysctl -w net.ipv4.ip_forward=1")
        self.waitOutput()
        sleep(0.2)
        self.cmd("/usr/lib/frr/zebra -f ./test_conf/%s_zebra.conf -d -i /tmp/%s_zebra.pid > ./test_log/%s_zebra-stdout.log 2>&1" % (r, r, r), shell=True)
        self.waitOutput()
        self.cmd("/usr/lib/frr/bgpd -f ./test_conf/%s_bgpd.conf -d -i /tmp/%s_bgpd.pid > ./test_log/%s_bgpd-stdout.log 2>&1" % (r, r, r), shell=True)
        self.waitOutput()
        self.cmd("ifconfig lo up")
        self.waitOutput()

    def stop(self):
        self.deleteIntfs()


class MyTopo( Topo ):
    def build(self):
        h1 = self.addHost('h1', ip = "10.0.1.1/24", defaultRoute = "via 10.0.1.254")
        h2 = self.addHost('h2', ip = "10.0.2.1/24", defaultRoute = "via 10.0.2.254")

        r1 = self.addSwitch('r1')
        r2 = self.addSwitch('r2')

        self.addLink(r1, r2, intfName1="r1-eth2", intfName2="r2-eth2")
        self.addLink(h1, r1, intfName2="r1-eth1")
        self.addLink(h2, r2, intfName2="r2-eth1")

        # If no intfName was specified, Mininet will by default assign names to links in order.
        # For example in this case, r1's interface would have been: 
        # r1-eth1 : r2
        # r1-eth2 : h1
        # Since the link to r2 was established before the link to h1.
        # But with intfName specified, we can assign names to our desired links, not worrying about order.



def main():
    os.system("rm -f /tmp/r*.log /tmp/r*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra bgpd > /dev/null 2>&1")
    net = Mininet(topo=MyTopo(), switch=Router, cleanup=True, controller=None)
    net.start()
    CLI(net)
    net.stop()
    os.system("killall -9 zebra bgpd")


if __name__ == "__main__":
    main()