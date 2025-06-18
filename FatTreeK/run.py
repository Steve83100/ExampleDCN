# Construct an arbitrary k (at most 64) FatTree topology, start network, and run FRR daemons on routers.

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import Switch
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
        self.cmd("/usr/lib/frr/zebra -f ./conf/%s.conf -d -i /tmp/%s_zebra.pid > ./log/%s_zebra-stdout.log 2>&1" % (r, r, r), shell=True)
        self.waitOutput()
        self.cmd("/usr/lib/frr/bgpd -f ./conf/%s.conf -d -i /tmp/%s_bgpd.pid > ./log/%s_bgpd-stdout.log 2>&1" % (r, r, r), shell=True)
        self.waitOutput()
        self.cmd("ifconfig lo up")
        self.waitOutput()

    def stop(self):
        self.deleteIntfs()



class FatTreeK(Topo):
    def build(self, n):
        self.n = n
        n2 = int(n/2) # Convert float to int so that range stops complaining

        hosts = {}
        for i in range(n): # pod number i
            for j in range(n2): # edge router number j
                for k in range(n2): # host number k
                    hosts[f'h{i}_{j}_{k}'] = self.addHost(f'h{i}_{j}_{k}', ip=f'10.{i}.{j}.{(k<<2)+2}/30', defaultRoute=f'via 10.{i}.{j}.{(k<<2)+1}')

        edges = {}
        for i in range(n): # pod number i
            for j in range(n2): # edge router number j
                edge = self.addSwitch(f'e{i}_{j}')
                edges[f'e{i}_{j}'] = edge
                for k in range(n2): # host number k
                    self.addLink(edge, hosts[f'h{i}_{j}_{k}'], intfName1=f'e{i}_{j}--h{i}_{j}_{k}')

        aggrs = {}
        for i in range(n): # pod number i
            for j in range(n2): # aggr router number j
                aggr = self.addSwitch(f'a{i}_{j}')
                aggrs[f'a{i}_{j}'] = aggr
                for k in range(n2): # edge number k
                    self.addLink(aggr, edges[f'e{i}_{k}'], intfName1=f'a{i}_{j}--e{i}_{k}', intfName2=f'e{i}_{k}--a{i}_{j}')

        cores = {}
        for i in range(n2): # set number i
            for j in range(n2): # core router number j
                core = self.addSwitch(f'c{i}_{j}')
                cores[f'c{i}_{j}'] = core
                for k in range(n): # aggr's pod number k
                    self.addLink(core, aggrs[f'a{k}_{i}'], intfName1=f'c{i}_{j}--a{k}_{i}', intfName2=f'a{k}_{i}--c{i}_{j}')



def main():
    os.system("rm -f /tmp/*.log /tmp/*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra bgpd > /dev/null 2>&1")
    net = Mininet(topo=FatTreeK(4), switch=Router, cleanup=True, controller=None)
    net.start()
    CLI(net)
    net.stop()
    os.system("killall -9 zebra bgpd")



if __name__ == "__main__":
    main()