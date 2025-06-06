from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, RemoteController
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class FatTree4(Topo):
    def build(self):
        host1_1 = self.addHost('h1_1')
        host1_2 = self.addHost('h1_2')
        host1_3 = self.addHost('h1_3')
        host1_4 = self.addHost('h1_4')
        
        edge1_1 = self.addSwitch('e1_1')
        edge1_2 = self.addSwitch('e1_2')
        
        aggr1_1 = self.addSwitch('a1_1')
        aggr1_2 = self.addSwitch('a1_2') # 删除其中一个 aggr switch
        
        self.addLink(host1_1, edge1_1)
        self.addLink(host1_2, edge1_1)
        self.addLink(host1_3, edge1_2)
        self.addLink(host1_4, edge1_2)
        self.addLink(aggr1_1, edge1_1)
        self.addLink(aggr1_1, edge1_2)
        self.addLink(aggr1_2, edge1_1) # 删除通向其中一个 aggr switch 的 link
        self.addLink(aggr1_2, edge1_2) # 删除通向其中一个 aggr switch 的 link
        
        
        
        # host2_1 = self.addHost('h2_1')
        # host2_2 = self.addHost('h2_2')
        # host2_3 = self.addHost('h2_3')
        # host2_4 = self.addHost('h2_4')
        
        # host3_1 = self.addHost('h3_1')
        # host3_2 = self.addHost('h3_2')
        # host3_3 = self.addHost('h3_3')
        # host3_4 = self.addHost('h3_4')
        
        # host4_1 = self.addHost('h4_1')
        # host4_2 = self.addHost('h4_2')
        # host4_3 = self.addHost('h4_3')
        # host4_4 = self.addHost('h4_4')
        
        
        
        # edge2_1 = self.addSwitch('e2_1')
        # edge2_2 = self.addSwitch('e2_2')
        
        # edge3_1 = self.addSwitch('e3_1')
        # edge3_2 = self.addSwitch('e3_2')
        
        # edge4_1 = self.addSwitch('e4_1')
        # edge4_2 = self.addSwitch('e4_2')
        
        
        
        # aggr2_1 = self.addSwitch('a2_1')
        # aggr2_2 = self.addSwitch('a2_2')
        
        # aggr3_1 = self.addSwitch('a3_1')
        # aggr3_2 = self.addSwitch('a3_2')
        
        # aggr4_1 = self.addSwitch('a4_1')
        # aggr4_2 = self.addSwitch('a4_2')
        
        # core1 = self.addSwitch('c1')
        # core2 = self.addSwitch('c2')
        # core3 = self.addSwitch('c3')
        # core4 = self.addSwitch('c4')
        
        
        
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        # self.addLink(host1_1, edge1_1)
        


topo = FatTree4()
net = Mininet(topo=topo, switch=OVSSwitch, controller=None)
net.start()
CLI(net)
net.stop()