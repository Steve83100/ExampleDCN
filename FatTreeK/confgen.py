# Generate configuration files for arbitrary k (at most 64) FatTree

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
            asn = f'{64700 + j}' # Edge routers get ASN based only on their number in pod, starting from 64700
            router_id = f'10.{i}.{j}.0' # IP address of its subnet is used as router-id in bgp
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
                intfIP = f'10.{i}.{j}.{(k<<2)+1}/30'
                config_str += f'''
! Connection to {peerName}
interface {intfName}
  ip address {intfIP}
!
'''
            for k in range(n2): # aggr number k
                peerName = f'a{i}_{k}'
                intfName = f'e{i}_{j}--'+ peerName
                intfIP = f'10.{i}.{k+n}.{(j<<2)+2}/30'
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
                peerIP = f'10.{i}.{k+n}.{(j<<2)+1}'
                peerASN = f'{64600 + i}'
                config_str += f'''
  ! Connection to {peerName}
  neighbor {peerIP} remote-as {peerASN}
  neighbor {peerIP} allowas-in
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


    for i in range(n): # pod number i
        for j in range(n2): # aggr router number j
            name = f'a{i}_{j}'
            path = conf_path + "/" + name + ".conf"
            f = open(path, "w")
            asn = f'{64600 + i}' # All aggr routers in the same pod get the same ASN, starting from 64600
            router_id = f'10.{i}.{j+n}.0' # IP address of its subnet is used as router-id in bgp
            config_str = "hostname " + name + '''
password en
enable password en
!

interface lo
  ip address 127.0.0.1/32
!
'''
            for k in range(n2): # edge number k
                peerName = f'e{i}_{k}'
                intfName = f'a{i}_{j}--' + peerName
                intfIP = f'10.{i}.{j+n}.{(k<<2)+1}/30'
                config_str += f'''
! Connection to {peerName}
interface {intfName}
  ip address {intfIP}
!
'''
            for k in range(n2): # core number k, remember aP_A connects to all cS_C with A = S
                peerName = f'c{j}_{k}'
                intfName = f'a{i}_{j}--'+ peerName
                intfIP = f'10.{j+n}.{k}.{(i<<2)+2}/30'
                config_str += f'''
! Connection to {peerName}
interface {intfName}
  ip address {intfIP}
!
'''
            config_str += f'''
router bgp {asn}
  bgp router-id {router_id}
  no bgp ebgp-requires-policy
  no bgp network import-check
'''
            for k in range(n2): # edge number k
                peerName = f'e{i}_{k}'
                peerIP = f'10.{i}.{j+n}.{(k<<2)+2}'
                # peerASN = f'{64600 + i * n2 + k}'
                peerASN = f'{64700 + k}'
                config_str += f'''
  ! Connection to {peerName}
  neighbor {peerIP} remote-as {peerASN}
  neighbor {peerIP} next-hop-self
  neighbor {peerIP} timers 5 5
'''
            for k in range(n2): # core number k, remember aP_A connects to all cS_C with A = S
                peerName = f'c{j}_{k}'
                peerIP = f'10.{j+n}.{k}.{(i<<2)+1}'
                peerASN = '64512'
                config_str += f'''
  ! Connection to {peerName}
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


    for i in range(n2): # set number i
        for j in range(n2): # core router number j
            name = f'c{i}_{j}'
            path = conf_path + "/" + name + ".conf"
            f = open(path, "w")
            asn = '64512' # All core routers get the same ASN 64512
            router_id = f'10.{i+n}.{j}.0' # IP address of its subnet is used as router-id in bgp
            config_str = "hostname " + name + '''
password en
enable password en
!

interface lo
  ip address 127.0.0.1/32
!
'''
            for k in range(n): # aggr's pod number k, remember cS_C connects to all aP_A with A = S
                peerName = f'a{k}_{i}'
                intfName = f'c{i}_{j}--' + peerName
                intfIP = f'10.{i+n}.{j}.{(k<<2)+1}/30'
                config_str += f'''
! Connection to {peerName}
interface {intfName}
  ip address {intfIP}
!
'''
            config_str += f'''
router bgp {asn}
  bgp router-id {router_id}
  no bgp ebgp-requires-policy
  no bgp network import-check
'''
            for k in range(n): # aggr's pod number k, remember cS_C connects to all aP_A with A = S
                peerName = f'a{k}_{i}'
                peerIP = f'10.{i+n}.{j}.{(k<<2)+2}'
                peerASN = f'{64600 + k}'
                config_str += f'''
  ! Connection to {peerName}
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


os.system("rm -f ./conf/*.conf")
genFRR(4)