#include "header/net_packet_lib.h"


int main(int argc, char *argv[])
{
    net_packet_lib packet;
    std::string interface = "enp38s0";
    if (packet.state_interface(interface))
        std::cout << interface << ": up\n";
    else
        std::cout << interface << ": down\n";
    packet.sniffer(interface);
    return 0;
}
