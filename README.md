# python-virus
I'm not an exploit dev. Just kicking some tires

# Short description

The tcp-listener opens a socket on a port, and upon accepting a connection, sends a bunch of data to it. By default, it sends a short batch script that's basically a fork bomb on Windows.

The tcp-connect would ideally be installed on another machine, downloads the data, and stores it into a file. In actual use, malware wouldn't print on the victim's end, but I'm still testing and debugging the code. This isn't meant to be used anyway, just getting a feel for malware dev
