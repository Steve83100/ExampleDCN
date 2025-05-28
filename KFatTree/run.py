import time
import os
import sys

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, Switch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import irange, natural, naturalSeq


class FatTreeRouter(Switch):

    def __init__(self, name, ip, asn, connections, **params):

        super(FatTreeRouter, self).__init__(**params)
        os.makedirs("./"+name, exist_ok=True)

        zebra_config = f"""hostname {name}
interface lo
 ip address {ip}
 no shutdown
!
line vty
!
"""
        # Since our FatTree exists in 10.0.0.0/8, we can leave out interface configs other than loopback,
        # and Mininet will establish a "eth0" interface with ip 10.0.0.0/8 for us, which is totally enough for use.
        
        bgp_config = f"""hostname {name}
router bgp {asn}
 bgp router-id {ip}
"""
        if name.startswith("Edge"): # Advertise our hosts in LAN
            bgp_config += f" network {ip[:-3]}/24\n"

        # else: # If no hosts connected, just advertise itself
        #     bpg_config += f" network {ip}\n"

        for (ip, asn) in connections:
            bgp_config += f" neighbor {ip} remote-as {asn}\n"
        
        # bgp_config += "\n address-family ipv4 unicast\n"
        
        # # Activate neighbors
        # for neighbor in bgp_data.get('neighbors', []):
        #     bgp_config += f"  neighbor {neighbor['ip']} activate\n"
        
        # bgp_config += " exit-address-family\n!\n\n"

        bgp_config += """
line vty
!
"""

        f = open("./" + name + "/zebra.conf", 'w')
        f.write(zebra_config)
        f.close()
        
        f = open("./" + name + "/bgpd.conf", 'w')
        f.write(bgp_config)
        f.close()

    def config():
        pass
    
    def terminate():
        pass


def buildFatTree(k):
    """Build an arbitrary sized FatTree. Loads bgp daemons onto routers. Maximum k = 254."""

    net = Mininet()

    core_routers = {} # Stores all core routers
    for i in irange(1, k/2): # Set id
        for j in irange(1, k/2): # Core router id inside each Set
            ip = f"10.0.{i}.{j}/32"
            asn = "64512"
            name = f"Core{i}_{j}"
            connections = [( f"10.{n}.0.{i}/32", f"{64600+n}") for n in irange(1, k)]
            # Each Core router within set "set_id" connects to the Aggr routers across all pods with the router_id "set_id"
            # router_connections stores (ip, asn) of the routers connected to this router
            core_router = net.addSwitch(name, cls = FatTreeRouter, ip = ip, asn = asn, connections = connections)
            core_routers[i*k/2 + j] = core_router

    for i in irange(1, k): # Pod id
        pod_aggr_routers = {} # Stores all aggr routers in this pod
        for j in irange(1, k/2): # Create Aggr routers in this pod

            # Create Aggr routers
            ip = f"10.{i}.0.{j}/32"
            asn = f"{64600 + i}"
            name = f"Aggr{i}_{j}"
            connections_to_core = [(f"10.0.{j}.{n}/32", "64512") for n in irange(1, k/2)]
            # Each Aggr router with "router_id" connects to all Core routers in set "router_id"
            connections_to_edge = [(f"10.{i}.{n}.0/32", f"{64700+n}") for n in irange(1, k/2)]
            # Each Aggr router also connects to all Edge routers in the same Pod
            connections = connections_to_core + connections_to_edge
            aggr_router = net.addSwitch(name, cls = FatTreeRouter, ip = ip, asn = asn, connections = connections)
            pod_aggr_routers[j] = aggr_router

            # Link this Aggr router to Core routers
            for n in irange(1, k/2):
                core_router = core_routers[j*k/2 + n]
                net.addLink(aggr_router, core_router)
            
        for j in irange(1, k/2): # Create Edge routers in this pod
            ip = f"10.{i}.{j}.0/32"
            asn = f"{64700 + j}"
            name = f"Edge{i}_{j}"
            connections = [(f"10.{i}.0.{n}/32", f"{64600+i}") for n in irange(1, k/2)]
            # Each Edge router connects to all Aggr routers in the same Pod
            edge_router = net.addSwitch(name, cls = FatTreeRouter, ip = ip, asn = asn, connections = connections)

            # Link this Edge router to Aggr routers in the same pod
            for n in irange(1, k/2):
                net.addLink(edge_router, pod_aggr_routers[n])

            # Create Hosts and link them to Edge router
            for n in irange(1, k/2): # Host id
                Hip = f"10.{i}.{j}.{n}/32"
                Hname = f"Host{i}_{j}_{n}"
                host = net.addHost(Hname, ip = Hip, defaultRoute = f"via {ip}")
                net.addLink(host, edge_router)

    return net

def run(k):
    net = buildFatTree(k)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run(4)