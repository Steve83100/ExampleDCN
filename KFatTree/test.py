#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch
from mininet.link import TCLink
from mininet.util import dumpNodeConnections, irange
from mininet.log import setLogLevel
from mininet.cli import CLI

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

class MyTopo( Topo ):
    
    def build(self):
        # Setup Routers
        r1 = self.addNode('r1', cls = Router)
        r2 = self.addNode('r2', cls = Router)

        # Setup Switches
        s1 = self.addSwitch('s1', cls=LegacySwitch)
        self.addLink(s1, r1, interfName2 = 'r1-eth0', params2 = {'ip': '10.0.1.1/24'})

        # s2 = self.addSwitch('s2', cls=LegacySwitch)
        # self.addLink(s2, r1, params1={'ip': '10.0.2.2/24'}, params2={'ip': '10.0.2.1/24'})
        # self.addLink(s2, r2, params1={'ip': '10.0.2.3/24'}, params2={'ip': '10.0.2.4/24'})
        
        # s3 = self.addSwitch('s3', cls=LegacySwitch)
        # self.addLink(s3, r2, params1={'ip': '10.0.3.2/24'}, params2={'ip': '10.0.3.1/24'})

def perfTest():
    "Create network and run simple performance test"
    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink, cleanup=True)
    net.start()
    # print( "Dumping host connections" )
    # dumpNodeConnections( net.hosts )
    # print( "Testing network connectivity" )
    # net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()