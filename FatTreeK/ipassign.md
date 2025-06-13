We use Pod-based IP address allocation method.
All interfaces are assigned IP addr within 10.0.0.0/8 based on their pod and position in pod.
Below is an explanation of how IP address are allocated in an n=64 FatTree.

# Basic Principles

## Link connects /31 subnet
A link connects two interfaces. These two interfaces have IP under the same /31 subnet.

This means that the two IPs only differ on the last binary digit, such as 10.0.0.2 and 10.0.0.3.

We assign the lower (last bit = 0) IP to interface "higher" in the network (core > aggr > edge > host).

## Higher machine distributes IP
A higher router has many links down to lower routers.
In a link between an aggr router and an edge router, IP is allocated based on the aggr router's position in the network, not the edge router.

For example, in aggr router a3_6, all links down to edge router begin with "10.3.70" (more later).
You can think of the aggr router "managing" the subnet 10.3.70.0/24.

# Demonstration

## Edge - Host link

For pod P (0~63), edge router E (0~31), there are 32 links down to hosts. These links begin with "10.P.E".

In the link to host k (0~31), edge router side has interface 10.P.E.(k<<1), host side has interface 10.P.E.(k<<1+1).

For example, in pod 3 edge 2, interface 10.3.2.0 connects to host0's 10.3.2.1, interface 10.3.2.2 connects to host1's 10.3.2.3.

## Agge - Edge link

For pod P (0~63), aggr router A (0~31), there are 32 links down to edge routers. These links begin with "10.P.(A+64)".

In the link to edge E (0~31), aggr router side has interface 10.P.(A+64).(E<<1), edge router side has interface 10.P.(A+64).(E<<1+1).

For example, in pod 3 aggr 2, interface 10.3.66.0 connects to edge0's interface 10.3.66.1, interface 10.3.66.2 connects to edge1's 10.3.66.3.

## Core - Aggr link

There are 32*32 core routers in all. We separate them into 32 sets so that both connection and IP allocation is clear and easy.

A core router in set S (0~31) and has number C (0~31) will connect to aggr router A across all pods with A = S. This gives the core router 64 links down to aggr routers.

We give the core router subnet 10.(S+64).C.0/24, and in its link to pod P, core side gets 10.(S+64).C.(P<<1), aggr side gets 10.(S+64).C.(P<<1+1).

For example, in set 4 core 5, interface 10.70.5.0 connects to pod0 aggr's interface 10.3.66.1, interface 10.70.5.2 connects to pod1 aggr's 10.70.5.3.