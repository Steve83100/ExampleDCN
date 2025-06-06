from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI

class MyTopo(Topo):
    def build(self):
        # Add switches with STP enabled
        s1 = self.addSwitch('s1', cls=OVSSwitch, stp=True)
        s2 = self.addSwitch('s2', cls=OVSSwitch, stp=True)
        s3 = self.addSwitch('s3', cls=OVSSwitch, stp=True)
        
        # Add hosts and links as usual
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(s2, s3)

# Start the network
topo = MyTopo()
net = Mininet(topo=topo, switch=OVSSwitch, controller=None, cleanup=True)
net.start()
CLI(net)
net.stop()