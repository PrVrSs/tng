



#ifndef NET_PACKET_LIB_H
#define NET_PACKET_LIB_H
#define ETHER_HDRLEN 14

#include <iostream>
#include <pcap.h>
#include <cerrno>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netinet/if_ether.h>
#include <net/ethernet.h>
#include <netinet/ether.h>
#include <netinet/ip.h>
#include <ctime>
#include <pthread.h>
#include <cstring>
#include <vector>
#include <cassert>
#include <cstdlib>

class net_packet_lib
{
private:
    std::string gate_ip;
    std::string gate_mac;
    std::vector<std::string> found_ip;
    std::vector<std::string> found_mac;
    struct tcp_protocol {
        u_short tcp_port_src; /* port source */
        u_short tcp_port_dst; /* port de destination */
        u_long tcp_seqnum; /* numero de sequence */
        u_long tcp_aqunum;
        u_char tcp_res;
        u_char tcp_flags;
    #define TCP_FIN 0x01
    #define TCP_SYN 0x02
    #define TCP_RST 0x04
    #define TCP_PSH 0x08
    #define TCP_ACK 0x10
    #define TCP_URG 0x20
    #define TCP_ECE 0x40
    #define TCP_CWR 0x80
        #define TCP_FLAGS (TH_FIN|TH_SYN|TH_RST|TH_ACK|TH_URG|TH_ECE|TH_CWR)
        u_short tcp_win; /* taille fenetre demandee */
        u_short tcp_crc; /* Checksum */
        u_short tcp_purg; /* pointeur donnees urgentes */
    };

    struct ip_protocol {
        u_int8_t	ip_vhl;		/* header length, version */
    #define IP_V(ip)	((ip->ip_vhl & 0xf0) >> 4)
    #define IP_HL(ip)	(ip->ip_vhl & 0x0f)
        u_int8_t	ip_tos;		    /* type of service */
        u_int16_t	ip_len;		    /* total length */
        u_int16_t	ip_id;		    /* identification */
        u_int16_t	ip_off;		    /* fragment offset field */
    #define	IP_DF 0x4000			/* dont fragment flag */
    #define	IP_MF 0x2000			/* more fragments flag */
    #define	IP_OFFMASK 0x1fff		/* mask for fragmenting bits */
    #define IP_TCP 6
    #define IP_UDP 17
    #define IP_ICMP 1
        u_int8_t	ip_ttl;		/* time to live */
        u_int8_t	ip_p;		/* protocol */
        u_int16_t	ip_sum;		/* checksum */
        struct	in_addr ip_src,ip_dst;	/* source and dest address */
    };

    typedef struct arphdr1 {
        u_int16_t htype;    /* Hardware Type           */
        u_int16_t ptype;    /* Protocol Type           */
        u_char hlen;        /* Hardware Address Length */
        u_char plen;        /* Protocol Address Length */
        u_int16_t oper;     /* Operation Code          */
        u_char sha[6];      /* Sender hardware address */
        u_char spa[4];      /* Sender IP address       */
        u_char tha[6];      /* Target hardware address */
        u_char tpa[4];      /* Target IP address       */
    }arphdr1_t;


public:
    net_packet_lib();
    ~net_packet_lib();
    void sniffer(std::string interface);
    static void callback(u_char *args, const struct pcap_pkthdr* pkthdr, const u_char* packet);
    bool state_interface(std::string interface);
    void handle_TCP(const u_char* packet, u_int size_ip,const struct pcap_pkthdr* pkthdr);
    u_char* handle_IP (u_char *args,const struct pcap_pkthdr* pkthdr,const u_char* packet);
    u_char* handle_ARP (u_char *arg, const struct pcap_pkthdr* pkthdr, const u_char * packet);
    u_int16_t handle_ethernet (u_char* args, const struct pcap_pkthdr* pkthdr, const u_char* packet);

};


#endif // NET_PACKET_LIB_H
