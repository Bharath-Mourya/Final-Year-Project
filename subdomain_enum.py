import socket

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "test", "dev", "api",
    "blog", "admin", "portal", "secure", "vpn",
    "m", "shop", "beta", "staging"
]

def enumerate_subdomains(domain):
    print("\n--- SUBDOMAIN ENUMERATION ---")

    socket.setdefaulttimeout(2)

    found = []

    for sub in COMMON_SUBDOMAINS:
        subdomain = f"{sub}.{domain}"
        try:
            socket.gethostbyname(subdomain)
            print(f"[+] Found: {subdomain}")
            found.append(subdomain)
        except socket.gaierror:
            continue

    if not found:
        print("[!] No common subdomains found.")

    return list(set(found))  # remove duplicates