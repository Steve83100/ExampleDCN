#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections, irange
from mininet.log import setLogLevel
from mininet.cli import CLI


class FatTreeTopo( Topo ):
    "Fat Tree topology of radix k."

    def build( self, k = 4, **_opts):
        """k: number of switches
           n: number of hosts per switch"""
        self.k = k

        # core_routers = {}
        # for i in irange(1, int(k/2)): # Set id
        #     for j in irange(1, int(k/2)): # Core router id inside each Set
        name = f"Core{0}_{0}"
        core_router = self.addSwitch(name)
        # core_routers[i*k/2 + j] = core_router

        for i in irange(1, k): # Pod id
            # pod_aggr_routers = {} # Stores all aggr routers in this pod
            # for j in irange(1, int(k/2)): # Create Aggr routers in this pod

            # Create Aggr router
            name = f"Aggr{i}_{0}"
            aggr_router = self.addSwitch(name)
            # pod_aggr_routers[j] = aggr_router

            # # Link this Aggr router to Core routers
            # for n in irange(1, int(k/2)):
            #     core_router = core_routers[j*k/2 + n]
            self.addLink(aggr_router, core_router)
            
            for j in irange(1, int(k/2)): # Create Edge routers in this pod
                name = f"Edge{i}_{j}"
                edge_router = self.addSwitch(name)

                # Link this Edge router to Aggr routers in the same pod
                # for n in irange(1, int(k/2)):
                self.addLink(edge_router, aggr_router)

                # Create Hosts and link them to Edge router
                for n in irange(1, int(k/2)): # Host id
                    # Hip = f"10.{i}.{j}.{n}/32"
                    Hname = f"Host{i}_{j}_{n}"
                    host = self.addHost(Hname)
                    self.addLink(host, edge_router)

        # lastSwitch = None
        # for i in irange( 1, k ):
        #     # Add switch
        #     switch = self.addSwitch( 's%s' % i )
        #     # Add hosts to switch
        #     for j in irange( 1, n ):
        #         host = self.addHost( genHostName( i, j ) )
        #         self.addLink( host, switch )
        #     # Connect switch to previous
        #     if lastSwitch:
        #         self.addLink( switch, lastSwitch )
        #     lastSwitch = switch

def run():
    "Create network and run simple performance test"
    topo =FatTreeTopo(k = 4)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, cleanup = True)
    net.start()
    # print( "Dumping host connections" )
    # dumpNodeConnections( net.hosts )
    # print( "Testing network connectivity" )
    # net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()