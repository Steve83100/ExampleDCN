#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Switch
from mininet.log import setLogLevel
from mininet.cli import CLI
import os
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
        self.cmd("/usr/lib/frr/zebra -f test_conf/%s_zebra.conf -d -i /tmp/%s_zebra.pid > test_log/%s_zebra-stdout 2>&1" % (r, r, r))
        self.waitOutput()
        self.cmd("/usr/lib/frr/bgpd -f test_conf/%s_bgpd.conf -d -i /tmp/%s_bgpd.pid > test_log/%s_bgpd-stdout 2>&1" % (r, r, r), shell=True)
        # manually start the interface 'lo'
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

        self.addLink(h1, r1)
        self.addLink(h2, r2)
        self.addLink(r1, r2)


def main():
    os.system("rm -f /tmp/r*.log /tmp/r*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra bgpd > /dev/null 2>&1")
    os.system('pgrep -f webserver.py | xargs kill -9')
    net = Mininet(topo=MyTopo(), switch=Router, cleanup=True, controller=None)
    net.start()
    CLI(net)
    net.stop()
    os.system("killall -9 zebra bgpd")
    os.system('pgrep -f webserver.py | xargs kill -9')


if __name__ == "__main__":
    main()