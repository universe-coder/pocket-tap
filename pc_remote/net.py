"""Pick the PC address the phone should use.

With a VPN on, the route to the internet goes through the VPN adapter, so
"the address used for outgoing traffic" is the VPN one and the phone cannot
reach it. Instead list every adapter and rank home-network addresses first.
"""

import ipaddress
import socket

# Adapter name fragments of VPN and virtual adapters (lowercase).
VIRTUAL_HINTS = (
    "vpn", "wireguard", "wg", "tun", "tap", "amnezia", "outline", "openvpn",
    "nekoray", "hiddify", "v2ray", "xray", "clash", "sing-box", "singbox",
    "tailscale", "zerotier", "hamachi", "radmin", "proton", "nord",
    "vethernet", "virtualbox", "vmware", "docker", "wsl", "hyper-v",
    "loopback", "utun", "ppp",
)

# Ranges that VPN / TUN clients use for their own adapters.
VPN_NETWORKS = [ipaddress.ip_network(n) for n in (
    "100.64.0.0/10",   # CGNAT: Tailscale, some VPN providers
    "198.18.0.0/15",   # TUN mode of Clash, sing-box, Hiddify, v2rayN
    "26.0.0.0/8",      # Radmin VPN
    "25.0.0.0/8",      # Hamachi
)]


def score(ip, adapter=""):
    """Lower is better; None means never offer this address."""
    try:
        addr = ipaddress.IPv4Address(ip)
    except ValueError:
        return None
    if addr.is_loopback or addr.is_link_local or addr.is_unspecified or addr.is_multicast:
        return None
    if any(addr in net for net in VPN_NETWORKS):
        rank = 50
    elif addr in ipaddress.ip_network("192.168.0.0/16"):
        rank = 0
    elif addr in ipaddress.ip_network("172.16.0.0/12"):
        rank = 10
    elif addr in ipaddress.ip_network("10.0.0.0/8"):
        rank = 20
    else:
        rank = 60  # public address: almost certainly not the home LAN
    name = adapter.lower()
    if any(hint in name for hint in VIRTUAL_HINTS):
        rank += 100
    return rank


def _adapters():
    """Yield (adapter name, IPv4) for every adapter that is up."""
    try:
        import psutil
    except ImportError:
        psutil = None
    if psutil is not None:
        stats = psutil.net_if_stats()
        for name, addrs in psutil.net_if_addrs().items():
            if name in stats and not stats[name].isup:
                continue
            for a in addrs:
                if a.family == socket.AF_INET:
                    yield name, a.address
        return
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            yield "", info[4][0]
    except OSError:
        pass
    # Connecting a UDP socket sends nothing; it only picks the outgoing interface.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("192.168.0.1", 1))
            yield "", s.getsockname()[0]
        except OSError:
            pass


def candidate_ips(adapters=None):
    """Addresses the phone might reach, best first, as (ip, adapter name)."""
    best = {}
    for name, ip in (adapters if adapters is not None else _adapters()):
        s = score(ip, name)
        if s is not None and (ip not in best or s < best[ip][0]):
            best[ip] = (s, name)
    return [(ip, name) for ip, (s, name) in sorted(best.items(), key=lambda kv: kv[1][0])]
