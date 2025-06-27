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

PuttyGen generate ssh key

public key -> ~/.ssh/authorized_keys

private key file -> putty settings

enable X11 Forwarding

add "-E" for Xterm in Mininet CLI

#### VSCode
localhost:2222

generate ssh key -> ~/.ssh/authorized_keys

### !! Learning Mininet
SDN slides, SDN manual, Python API source code


## FRR Setup Notes
simply apt install (no need to add "deb.frrouting.org" source)

### !! Learning FRR
Quagga examples, FRR topotests, Sigcomm BGP hijacking


## Batfish Setup Notes
### Docker (WSL is OK)
follow official setup, but change source at "echo" step.
[Instructions](https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/)

change docker registry source; Chsrc's source is currently unavailable.
[Instructions](https://blog.csdn.net/c12312303/article/details/146428465)

if using WSL, manually start/restart dockerd