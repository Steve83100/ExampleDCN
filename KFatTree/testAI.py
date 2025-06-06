from mininet.net import Mininet
from mininet.node import Node, RemoteController, Host
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from functools import partial

class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

def run():
    privateDirs = ['/tmp', '']
    host = partial( Host,
                    privateDirs=privateDirs )
    net = Mininet(controller=None, link=TCLink, host=host, cleanup=True)

    info("*** Creating routers\n")
    r1 = net.addHost('r1', cls=LinuxRouter, ip='10.0.1.1/24')
    r2 = net.addHost('r2', cls=LinuxRouter, ip='10.0.2.1/24')
    r3 = net.addHost('r3', cls=LinuxRouter, ip='10.0.3.1/24')

    info("*** Creating hosts\n")
    h1 = net.addHost('h1', ip='10.0.1.100/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', ip='10.0.2.100/24', defaultRoute='via 10.0.2.1')
    h3 = net.addHost('h3', ip='10.0.3.100/24', defaultRoute='via 10.0.3.1')

    info("*** Creating links\n")
    net.addLink(h1, r1)
    net.addLink(h2, r2)
    net.addLink(h3, r3)

    net.addLink(r1, r2)
    net.addLink(r2, r3)
    net.addLink(r3, r1)

    info("*** Starting network\n")
    net.start()

    info("*** Configuring interfaces\n")
    # Manually assign IPs for router-to-router links
    r1.cmd("ifconfig r1-eth1 10.0.12.1/30")
    r2.cmd("ifconfig r2-eth1 10.0.12.2/30")

    r2.cmd("ifconfig r2-eth2 10.0.23.1/30")
    r3.cmd("ifconfig r3-eth1 10.0.23.2/30")

    r3.cmd("ifconfig r3-eth2 10.0.31.1/30")
    r1.cmd("ifconfig r1-eth2 10.0.31.2/30")

    info("*** Starting FRRouting (BGP) on each router\n")
    for router, asn, neighbors in [
        ('r1', 65001, [('10.0.12.2', 65002), ('10.0.31.1', 65003)]),
        ('r2', 65002, [('10.0.12.1', 65001), ('10.0.23.2', 65003)]),
        ('r3', 65003, [('10.0.23.1', 65002), ('10.0.31.2', 65001)]),
    ]:
        node = net.get(router)
        zebra_conf = f"""/tmp/{router}_zebra.conf"""
        bgpd_conf = f"""/tmp/{router}_bgpd.conf"""
        
        with open(zebra_conf, 'w') as f:
            f.write(f"""
hostname {router}
log file /tmp/{router}-zebra.log
""")
        with open(bgpd_conf, 'w') as f:
            f.write(f"""
hostname {router}
router bgp {asn}
  bgp router-id 1.1.1.{asn - 65000}
""")
            for nbr_ip, nbr_asn in neighbors:
                f.write(f"  neighbor {nbr_ip} remote-as {nbr_asn}\n")
            f.write("  network 10.0.1.0/24\n" if router == 'r1' else "")
            f.write("  network 10.0.2.0/24\n" if router == 'r2' else "")
            f.write("  network 10.0.3.0/24\n" if router == 'r3' else "")

        node.cmd(f"/usr/lib/frr/zebra -f {zebra_conf} -d -z /tmp/{router}_zebra.api -i /tmp/{router}_zebra.pid")
        node.cmd(f"/usr/lib/frr/bgpd -f {bgpd_conf} -d -z /tmp/{router}_zebra.api -i /tmp/{router}_bgpd.pid")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    
    for router, asn, neighbors in [
        ('r1', 65001, [('10.0.12.2', 65002), ('10.0.31.1', 65003)]),
        ('r2', 65002, [('10.0.12.1', 65001), ('10.0.23.2', 65003)]),
        ('r3', 65003, [('10.0.23.1', 65002), ('10.0.31.2', 65001)]),
    ]:
        node = net.get(router)
        node.cmd( "killall bgpd staticd zebra" )
        
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
