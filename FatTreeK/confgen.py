# Generate configuration files for arbitrary k FatTree

from mininet.util import irange
import os

def genCisco(n, conf_path = "./confCisco"):
    for i in irange(1, n):
        pass

def genFRR(n, conf_path = "./conf"):
    n2 = int(n/2) # Convert float to int so that range stops complaining

    for i in range(n): # pod number i
        for j in range(n2): # edge router number j
            name = f'e{i}_{j}'
            path = conf_path + "/" + name + ".conf"
            f = open(path, "w")
            asn = '0'
            router_id = f'10.{i}.{j}.0' # IP address of the first interface is used as router-id in bgp.
            subnet = f'10.{i}.{j}.0/24'
            config_str = "hostname " + name + '''
password en
enable password en
!

interface lo
  ip address 127.0.0.1/32
!
'''
            for k in range(n2): # host number k
                peerName = f'h{i}_{j}_{k}'
                intfName = f'e{i}_{j}--' + peerName
                intfIP = f'10.{i}.{j}.{k<<1}/31'
                config_str += f'''
! Connection to {peerName}
interface {intfName}
  ip address {intfIP}
!
'''
            for k in range(n2): # aggr number k
                peerName = f'a{i}_{k}'
                intfName = f'e{i}_{j}--'+ peerName
                intfIP = f'10.{i}.{k+64}.{(j<<1)+1}/31'
                config_str += f'''
! Connection to {peerName}
interface {intfName}
  ip address {intfIP}
!
'''
            config_str += f'''
router bgp {asn}
  bgp router-id {router_id}
  address-family ipv4 unicast
    network {subnet}
  exit-address-family
  no bgp ebgp-requires-policy
  no bgp network import-check
'''
            for k in range(n2): # aggr number k
                peerName = f'a{i}_{k}'
                peerIP = f'10.{i}.{k+64}.{j<<1}'
                peerASN = '0'
                config_str += f'''
  neighbor {peerIP} remote-as {peerASN}
  neighbor {peerIP} next-hop-self
  neighbor {peerIP} timers 5 5
'''
                
            config_str += '''
!debug bgp as4
!debug bgp events
!debug bgp filters
!debug bgp fsm
!debug bgp keepalives
debug bgp updates
debug bgp neighbor-events

!
'''
            f.write(config_str)
            f.close()

#     aggrs = {}
#     for i in range(n): # pod number i
#         for j in range(n2): # aggr router number j
#             name = f'a{i}_{j}'
#             path = conf_path + "/" + name + ".conf"
#             f = open(path, "w")
#             config_str = "hostname " + name + '''
# password en
# enable password en
# !

# interface lo
#   ip address 127.0.0.1/32
# !
# '''
#             for k in range(n2): # edge number k
#                 peerName = f'e{i}_{k}'
#                 intfName = f'a{i}_{j}--' + peerName
#                 self.addLink(aggr, edges[f'e{i}_{k}'], intfName2=f'e{i}_{k}--a{i}_{j}')
#             for k in range(n2): # core number k
#                 self.addLink(core, aggrs[f'a{k}_{i}'], intfName1=f'c{i}_{j}--a{k}_{i}', intfName2=f'a{k}_{i}--c{i}_{j}')

#     cores = {}
#     for i in range(n2): # set number i
#         for j in range(n2): # core router number j
#             core = self.addSwitch(f'c{i}_{j}')
#             cores[f'c{i}_{j}'] = core
#             for k in range(n): # aggr's pod number k
#                 self.addLink(core, aggrs[f'a{k}_{i}'], intfName1=f'c{i}_{j}--a{k}_{i}', intfName2=f'a{k}_{i}--c{i}_{j}')

genFRR(4)