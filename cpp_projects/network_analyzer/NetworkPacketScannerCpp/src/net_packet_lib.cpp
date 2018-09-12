#include "header/net_packet_lib.h"

net_packet_lib::net_packet_lib(){
}

net_packet_lib::~net_packet_lib(){
}

bool net_packet_lib::state_interface(std::string interface){
    FILE *pipein_fp;
    char readbuf[80];
    bool state = false;
    std::string state_up;
    std::string state_down;
    state_up.append(interface + ": link up");
    state_down.append(interface + ": link down");
    assert ((pipein_fp = popen("dmesg", "r")) != NULL);
    while(fgets(readbuf, 80, pipein_fp)){
        if (strstr(readbuf, state_up.c_str())) {state = true;}
        if (strstr(readbuf, state_down.c_str())) {state = false;}
    }
    pclose(pipein_fp);
    return state;
}


void net_packet_lib::sniffer(std::string interface){
    char *dev;
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t* descr;
    struct bpf_program fp;      /* hold compiled program     */
    bpf_u_int32 maskp;          /* subnet mask               */
    bpf_u_int32 netp;           /* ip                        */
    u_char* args = NULL;
    dev = pcap_lookupdev(errbuf);
    assert(dev != NULL);
    pcap_lookupnet(dev, &netp, &maskp, errbuf);
    descr = pcap_open_live(dev, BUFSIZ, 1, -1, errbuf);
    assert(descr != NULL);
    pcap_loop(descr, atoi(interface.c_str()), callback, args);
    //std::cout << "\nfinished\n";
}

void net_packet_lib::callback(u_char *args, const struct pcap_pkthdr* pkthdr, const u_char* packet){
    net_packet_lib u;
    u_int16_t type = u.handle_ethernet(args, pkthdr, packet);
    if(type == ETHERTYPE_IP){u.handle_IP(args, pkthdr, packet);}
    else if(type == ETHERTYPE_ARP){
        //handle_ARP(args, pkthdr, packet);
    }
    else if(type == ETHERTYPE_REVARP){}
}


u_int16_t net_packet_lib::handle_ethernet (u_char *args, const struct pcap_pkthdr* pkthdr, const u_char* packet){
    u_int caplen = pkthdr->caplen;
    u_int length = pkthdr->len;
    struct ether_header *eptr;  /* net/ethernet.h */
    u_short ether_type;
    assert(caplen >= ETHER_HDRLEN);
    eptr = (struct ether_header *) packet;
    ether_type = ntohs(eptr->ether_type);
    return ether_type;
}

u_char* net_packet_lib::handle_IP(u_char *args, const struct pcap_pkthdr* pkthdr,const u_char* packet){
    const struct ip_protocol* ip;
    u_int length = pkthdr->len;
    u_int hlen,off,version;
    int len;
    ip = (struct ip_protocol*)(packet + sizeof(struct ether_header));
    length -= sizeof(struct ether_header);
    assert(length >= sizeof(struct ip_protocol ));
    len     = ntohs(ip->ip_len);
    hlen    = IP_HL(ip);            /* header length */
    version = IP_V(ip);            /*   ip version  */
    assert(version == 4);
    assert(hlen > 4);
    assert(length >= len);
    struct ether_header *eptr;
    u_short ether_type;
    eptr = (struct ether_header *) packet;
    ether_type = ntohs(eptr->ether_type);
    off = ntohs(ip->ip_off);
    //std::cout << (int)(ip->ip_p) << std::endl;
    if (ip->ip_p == 6){handle_TCP(packet, hlen*4, pkthdr);}
    return NULL;
}

void net_packet_lib::handle_TCP(const u_char* packet, u_int size_ip,const struct pcap_pkthdr* pkthdr){
    const struct tcp_protocol* tcp;
    tcp = (struct tcp_protocol*)(packet +  sizeof(struct ether_header) + size_ip);
    std::cout << "--------TCP---------:" << std::endl
              << " Port src: " << ntohs(tcp->tcp_port_src) << std::endl
              << " port dst: " << ntohs(tcp->tcp_port_dst) << std::endl
              << " seqnum: " << ntohl(tcp->tcp_seqnum) << std::endl;
}
