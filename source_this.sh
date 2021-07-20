export P4C=/home/pi/p4pi/p4c/
export RTE_TARGET=build
export RTE_SDK=/home/pi/p4pi/dpdk/
export GRPC=/home/pi/p4pi/grpc/
export P4PI=/home/pi/p4pi/PI/
export GRPCPP=/home/pi/p4pi/P4Runtime_GRPCPP/

sudo ip netns add red
sudo ip netns add blue
sudo ip link add veth0 type veth peer name veth0-1 netns blue
sudo ip link add veth1 type veth peer name veth1-1 netns red
#ip link set veth1-1 netns red

sudo ip netns exec blue ip addr add 10.10.10.1/24 dev veth0-1
sudo ip netns exec blue ip link set dev veth0-1 up
sudo ip netns exec red ip addr add 10.10.10.2/24 dev veth1-1
sudo ip netns exec red ip link set dev veth1-1 up

sudo ip link set dev veth0 up
sudo ip link set dev veth1 up

sudo ethtool -K veth0 tx off
sudo ip netns exec blue ethtool -K veth0-1 tx off
sudo ethtool -K veth1 tx off
sudo ip netns exec red ethtool -K veth1-1 tx off
