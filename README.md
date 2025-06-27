# ExampleDCN

## Mininet Setup Notes

### Host-side

#### VirtualBox
import Mininet VM from .ovf file

settings - NAT - Port Forwarding - 2222->22

#### Chsrc
[Instructions](https://github.com/RubyMetric/chsrc)

APT update and install Curl

Curl install Chsrc

change source of Ubuntu (apt) and Python

#### Git
ssh-keygen

public key -> github account

### Client-side

#### VcXsrv
replace XMing suggested officially

#### Putty
localhost:2222

generate ssh key: [Instructions](https://www.cnblogs.com/liuhaitao/p/6339926.html)

enable X11 Forwarding

for Xterm in Mininet CLI, add "-E" to commands: `sudo -E python run.py`

#### VSCode
localhost:2222

generate ssh key -> ~/.ssh/authorized_keys

### !! Learning Mininet
SDN slides, SDN manual, Python API source code


## FRR Setup Notes
simply apt install (no need to add "deb.frrouting.org" source)

### !! Learning FRR
Quagga examples: after installing, lies in `/usr/share/doc/quagga-core/examples/`

[FRR topotests](https://github.com/FRRouting/topotests)

[Sigcomm BGP hijacking](https://github.com/mininet/mininet/wiki/BGP-Path-Hijacking-Attack-Demo)


## Batfish Setup Notes
### Docker (WSL is OK)
follow official setup, but change source at "echo" step: [Instructions](https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/)

change docker registry source; Chsrc's source is currently unavailable: [Instructions](https://blog.csdn.net/c12312303/article/details/146428465)

if using WSL, manually start/restart dockerd

### Batfish
[Instructions](https://pybatfish.readthedocs.io/en/latest/index.html)