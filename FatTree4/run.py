# Construct k=4 FatTree topology, start network, and run FRR daemons on routers.

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import Switch
from mininet.util import irange
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
        sleep(0.1)
        self.cmd("/usr/lib/frr/zebra -f ./test_conf/%s_zebra.conf -d -i /tmp/%s_zebra.pid > ./test_log/%s_zebra-stdout.log 2>&1" % (r, r, r), shell=True)
        self.waitOutput()
        self.cmd("/usr/lib/frr/bgpd -f ./test_conf/%s_bgpd.conf -d -i /tmp/%s_bgpd.pid > ./test_log/%s_bgpd-stdout.log 2>&1" % (r, r, r), shell=True)
        self.waitOutput()
        self.cmd("ifconfig lo up")
        self.waitOutput()

    def stop(self):
        self.deleteIntfs()



class FatTree4(Topo):
    def build(self):
        cores = {}
        for i in irange(1, 4):
            cores[f'c{i}'] = self.addSwitch(f'c{i}')

        aggrs = {}
        for i in irange(1, 4):
            for j in irange(1, 2):
                aggrs[f'a{i}{j}'] = self.addSwitch(f'a{i}{j}')

        edges = {}
        for i in irange(1, 4):
            for j in irange(1, 2):
                edges[f'e{i}{j}'] = self.addSwitch(f'e{i}{j}')


        host11 = self.addHost('h11')
        host12 = self.addHost('h12')
        host13 = self.addHost('h13')
        host14 = self.addHost('h14')

        host21 = self.addHost('h21')
        host22 = self.addHost('h22')
        host23 = self.addHost('h23')
        host24 = self.addHost('h24')
        
        host31 = self.addHost('h31')
        host32 = self.addHost('h32')
        host33 = self.addHost('h33')
        host34 = self.addHost('h34')
        
        host41 = self.addHost('h41')
        host42 = self.addHost('h42')
        host43 = self.addHost('h43')
        host44 = self.addHost('h44')
        

        
        
        self.addLink(host11, edge11)
        self.addLink(host12, edge11)
        self.addLink(host13, edge12)
        self.addLink(host14, edge12)
        self.addLink(aggr11, edge11)
        self.addLink(aggr11, edge12)
        self.addLink(aggr12, edge11)
        self.addLink(aggr12, edge12)
        
        self.addLink(host21, edge21)
        self.addLink(host22, edge21)
        self.addLink(host23, edge22)
        self.addLink(host24, edge22)
        self.addLink(aggr21, edge21)
        self.addLink(aggr21, edge22)
        self.addLink(aggr22, edge21)
        self.addLink(aggr22, edge22)

        self.addLink(host31, edge31)
        self.addLink(host32, edge31)
        self.addLink(host33, edge32)
        self.addLink(host34, edge32)
        self.addLink(aggr31, edge31)
        self.addLink(aggr31, edge32)
        self.addLink(aggr32, edge31)
        self.addLink(aggr32, edge32)
        
        self.addLink(host41, edge41)
        self.addLink(host42, edge41)
        self.addLink(host43, edge42)
        self.addLink(host44, edge42)
        self.addLink(aggr41, edge41)
        self.addLink(aggr41, edge42)
        self.addLink(aggr42, edge41)
        self.addLink(aggr42, edge42)
        
        self.addLink(aggr11, core1)
        self.addLink(aggr21, core1)
        self.addLink(aggr31, core1)
        self.addLink(aggr41, core1)

        self.addLink(aggr11, core2)
        self.addLink(aggr21, core2)
        self.addLink(aggr31, core2)
        self.addLink(aggr41, core2)
        
        self.addLink(aggr12, core3)
        self.addLink(aggr22, core3)
        self.addLink(aggr32, core3)
        self.addLink(aggr42, core3)
        
        self.addLink(aggr12, core4)
        self.addLink(aggr22, core4)
        self.addLink(aggr32, core4)
        self.addLink(aggr42, core4)



def main():
    os.system("rm -f /tmp/r*.log /tmp/r*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra bgpd > /dev/null 2>&1")
    net = Mininet(topo=FatTree4(), switch=Router, cleanup=True, controller=None)
    net.start()
    CLI(net)
    net.stop()
    os.system("killall -9 zebra bgpd")



if __name__ == "__main__":
    main()