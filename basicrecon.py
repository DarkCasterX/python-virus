#!/usr/bin/env python3

# Requirements: gobuster, nmap, ffuf, nikto

import os
from os import path
import argparse
from threading import Thread
import xml.etree.ElementTree as ET

banner = """
--------------------------
|    Basicrecon.py       |
--------------------------
Web server initial recon
     **SIMPLIFIED**

-----> GO RECON!!! <------

"""

running_threads = []

#Run Nmap scan
def NmapScan(noprompt, ip):
    print("Running Nmap scan... (Nmap may require sudo privileges)")
    if not path.exists("./nmap"):
        os.mkdir("./nmap")
    os.system(f"sudo nmap -sS -sV -A {ip} -oA nmap/nmap-scan >/dev/null")
    if noprompt is False:
        try:
            choice = input("Display the results of the Nmap scan? (Yes/No)")
            if choice.lower() == "yes":
                os.system("cat ./nmap/nmap-scan.nmap")
        except KeyboardInterrupt:
            print("Keyboard interrupt detected")
        except ValueError:
            print("Bad value")
        except Exception as e:
            print("Error occured", e)

#Run gobuster directory scan
def DirScan(noprompt, dirwordlist, ip, domainname, port):
    if not path.exists("./gobuster"):
        os.mkdir("./gobuster")
    if len(domainname) > 1:
        os.system(f"gobuster dir -u http://{domainname} -w {dirwordlist} -o gobuster/dir-scan-results.txt -q >/dev/null") 
    else:
        if port is not None:    
            os.system(f"gobuster dir -u http://{ip}:{port} -w {dirwordlist} -o gobuster/dir-scan-results.txt -q >/dev/null")
        else:
            os.system(f"gobuster dir -u http://{ip} -w {dirwordlist} -o gobuster/dir-scan-results.txt -q >/dev/null")
    if noprompt is False:
        try:
            choice = input("Display the results of the directory scan()? (Yes/No) ")
            if choice.lower() == "yes":
                os.system("cat gobuster/dir-scan-results.txt")
        except KeyboardInterrupt:
            print("Keyboard interrupt detected")
        except ValueError:
            print("Bad value")
        except Exception as e:
            print("Error occured", e)

#Run gobuster DNS scan
def DNSScan(domain, list, *args, **kwargs):
    print("Running DNS Scan...")
    if not path.exists("./gobuster"):
        os.mkdir("./gobuster")
    try:
        os.system(f"gobuster dns -d {domain} -w {list} -o gobuster/dns-scan-results.txt -q >/dev/null")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected")
    except ValueError:
        print("Bad value")
    except Exception as e:
        print("Error occured", e)

def VHostScan(url, list, *args, **kwargs):
    print("Running VHOST Scan...")
    if not os.path.exists("./gobuster"):
        os.mkdir("./gobuster")
    if not os.path.exists("./ffuf"):
        os.mkdir("./ffuf")
    try:
        os.system(f"gobuster vhost -u {url} -w {list} -o gobuster/vhost-scan-results.txt -q >/dev/null")
        os.system(f"ffuf -s -c -u http://{url} -w {list} -H 'Host: FUZZ.{url}' -t 200 -fl 10 -o ffuf/ffuf-vhost-scan.txt")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected")
    except ValueError:
        print("Bad value")
    except Exception as e:
        print("Error occured", e)

#Run nikto scan
def NiktoScan():
    try:
        host = input("Enter host to run nikto scan on: ")
        os.system(f"nikto -host {host} -output nikto-scan.txt")
    except ValueError:
        print("Bad value")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected")
    except Exception as e:
        print("Error occured", e)

def checkForWebserver(port, noprompt, ip):
    try:
        NmapScan(noprompt, ip)
        if port is None:
            open_ports = []
            tree = ET.parse("./nmap/nmap-scan.xml")
            root = tree.getroot()
            for port_elem in root.iter('port'):
                portno = port_elem.get('portid')
                if portno is not None:
                    open_ports.append(portno)
            
            for open_port in open_ports:
                print(open_port)
                if int(open_port) == 80 or int(open_port) == 443:
                    print("Port 80 or 443 is open, server is likely hosting a web server")
                    return True
                else:
                    return False

        if port is not None:
            print("You specified a port in arguments. Assuming there is a web server running on that port.")
            return True
    except Exception as e:
        print("Error occured", e)
        return False

def webServerScan(is_web_server, noprompt, dirwordlist, ip, domainname, port, args, dnslist):
    if is_web_server == True:
        #Run scans
        try:
            print("Running directory scan...")
            dir_scan = Thread(target=DirScan, args=(noprompt, dirwordlist, ip, domainname, port,), daemon=True)
            running_threads.append(dir_scan)
            
            #Optional scans
            if args.do_dns:
                if dnslist is None:
                    print("No wordlist specified for DNS scan.")
                else:
                    dns_scan = Thread(target=DNSScan, args=(domainname, dnslist))
                    vhost_scan = Thread(target=VHostScan, args=(domainname, dnslist))
                    running_threads.append(dns_scan)
                    running_threads.append(vhost_scan)
            if args.do_nikto:
                nikto_scan = Thread(target=NiktoScan)
                running_threads.append(nikto_scan)
            
            #Start threads
            for thread in running_threads:
                thread.start()

            #Wait for all threads to finish
            for thread in running_threads:
                thread.join()

            print("[!] All scans complete. Check the current directory for the files containing scan results.")
        except Exception as e:
            print("Something went wrong: ", e)
    else:
        print("[!] Host does not have a web server open")

def main():
    #Print banner
    print(banner)

    #Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help="IP address of server to recon")
    parser.add_argument('dirlist', help="Path of directory wordlist you want to use")
    parser.add_argument('-n', '--do-dns', action="store_true", help="do dns scanning")
    parser.add_argument('-k', '--do-nikto', action="store_true", help="run nikto scan")
    parser.add_argument('-t', '--no-prompt', action="store_true", help="Disable unnecessary prompts (yes or no) default: yes")
    parser.add_argument('-s', '--skip-nmap', action="store_true", help="Skip Nmap scan")
    parser.add_argument('-l', '--dns-list', nargs="?", help="wordlist to use for DNS scanning")
    parser.add_argument('-d', '--domain', nargs="?", default="", help="optional domain name to use for scanners default: none")
    parser.add_argument('-p', '--port', nargs='?', default=None, help="Specify port to scan")
    args = parser.parse_args()

    #Store arguments
    ip = args.ip
    dirwordlist = args.dirlist
    noprompt = args.no_prompt
    domainname = args.domain
    dnslist = args.dns_list
    port = args.port

    #Run nmap scan to check if port 80 is open
    if args.skip_nmap is False:
        is_web_server = checkForWebserver(port, noprompt, ip)
        
        #Scan the web server
        webServerScan(is_web_server, noprompt, dirwordlist, ip, domainname, port, args, dnslist)

    else:
        webServerScan(True, noprompt, dirwordlist, ip, domainname, port, args, dnslist)

    
    

if __name__ == "__main__":
    main()