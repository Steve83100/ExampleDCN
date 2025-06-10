from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, RemoteController
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class FatTree4(Topo):
    def build(self):
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
        

        edge11 = self.addSwitch('e11', failMode='standalone', stp=True)
        edge12 = self.addSwitch('e12', failMode='standalone', stp=True)
        
        edge21 = self.addSwitch('e21', failMode='standalone', stp=True)
        edge22 = self.addSwitch('e22', failMode='standalone', stp=True)
        
        edge31 = self.addSwitch('e31', failMode='standalone', stp=True)
        edge32 = self.addSwitch('e32', failMode='standalone', stp=True)
        
        edge41 = self.addSwitch('e41', failMode='standalone', stp=True)
        edge42 = self.addSwitch('e42', failMode='standalone', stp=True)


        aggr11 = self.addSwitch('a11', failMode='standalone', stp=True)
        aggr12 = self.addSwitch('a12', failMode='standalone', stp=True)
        
        aggr21 = self.addSwitch('a21', failMode='standalone', stp=True)
        aggr22 = self.addSwitch('a22', failMode='standalone', stp=True)
        
        aggr31 = self.addSwitch('a31', failMode='standalone', stp=True)
        aggr32 = self.addSwitch('a32', failMode='standalone', stp=True)
        
        aggr41 = self.addSwitch('a41', failMode='standalone', stp=True)
        aggr42 = self.addSwitch('a42', failMode='standalone', stp=True)
        

        core1 = self.addSwitch('c1', failMode='standalone', stp=True)
        core2 = self.addSwitch('c2', failMode='standalone', stp=True)
        core3 = self.addSwitch('c3', failMode='standalone', stp=True)
        core4 = self.addSwitch('c4', failMode='standalone', stp=True)
        
        
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


topo = FatTree4()
net = Mininet(topo=topo, switch=OVSSwitch, controller=None, autoSetMacs=True, cleanup=True)
net.start()
CLI(net)
net.stop()