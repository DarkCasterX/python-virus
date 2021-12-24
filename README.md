# python-virus

I'm not an exploit dev. Just kicking some tires

## Short description

The tcp-listener opens a socket on a port, and upon accepting a connection, sends a bunch of data to it. By default, it sends a short batch script that's basically a fork bomb on Windows.

The tcp-connect would ideally be installed on another machine, downloads the data, and stores it into a file. In actual use, malware wouldn't print on the victim's end, but I'm still testing and debugging the code. This isn't meant to be used anyway, just getting a feel for malware dev

Basicrecon.py is a web server scanner that I made to make HackTheBox machines a little quicker. I simply used python to automate running Nmap, gobuster, ffuf and nikto, which are scripts that I find myself using against nearly every easy/medium box. I think it's cool that it's multithreaded as well, allowing it to run all these scans simultaneously and simply dumping all the data in files for you to analyze and read. The options and switches might be a bit clunky, but that doesn't matter so much right now. For the most part, if anyone stumbles upon this script and sees potential in it, I'm hoping you'd recommend scanning tools to support for this script, and also any other recon/enumeration features that would also be convenient. Maybe when I get better at web scraping, I can add some original web page analysis features to make this script that much more effective.
