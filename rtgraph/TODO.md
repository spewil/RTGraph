TODO

<!-- HARCODE TCP SOCKET ACQUISITION -->
- PROBLEMS
    - timestamp should be parsed from the source packet
    - items in the queue aren't properly separated like: [time, [values]]
        - time + vectors of specified length into queue separately
-  draw out the architecture  
    - processes --> queues 
- plot data in chunks for better speed
- let acquisition start and stop while client is running freely-- client should just be producing and sending?
- check frame rate with chunking 
- communicate bi-directionally with the device
- if client stops sending data, stop all processes other than GUI (hit "stop")

- implement with ZMQ for async...? 
    - problem isn't with the streaming, but the plot updates? 

<!-- FIX HARDCODING -->
- change overall class structure so that acquisition devices are run differently 
    - user writes acquisition device subclass 


<!-- RingBuffer -->
- Changing this to a deque for some speedup 

<!-- Multiprocessing.Queue -->
- this seems to be slow, moving data across processes
- Can we subscribe multiple processes to the incoming stream instead? 
    - No... 
- fastest inter-process communication?
    - https://github.com/MagicStack/uvloop 
    - https://github.com/zeromq/pyzmq 
    - Seems that these things are hard to check
        - variables = message size, message type (serializing is slow)
    - conclusion: stick with Queue for now, it's the right abstraction... 
    - future problem: might need multiple queues for 

<!-- PLotting speedup ideas -->
- biggest time hogs:
    - auto-adjusting the range (requires calculations)
    - clearing and replotting the entire graph (clear + plot)
        - can we keep most of the plot intact? 

<!-- NOTES -->
vSignals acquired with sessantaquattro can be read with a WiFi interface using a TCP connection.
A TCP socket have to be opened by the computer (or tablet, smartphone) running OT BioLab or other custom application.
The default port is 45454 but can be changed in custom application by the user.
When sessantaquattro is connected to a WiFi network, it continuously searches for a TCP socket opened on the IP address provided through the internal web page and connect as a client to the socket as soon as it is found.
When the connection through the socked is established, the communication can be started by sending a configuration command that sets the number of channels, the sampling frequency, the detection mode etc...
The server-client role has been chosen to allow the connection of more sessantaquattro to the same PC. Options for the synchronization are available for future implementations.

~~

data_throughput
(64 channels) X (2000 samples / 1 sec) X (16 bits / 1 sample) = 2,048,000bps = 2Mbps= 256kB/s

~~

sockets

bind() associates the socket with its local address [that's why server side binds, so that clients can use that address to connect to server.]
connect() is used to connect to a remote [server] address, that's why is client side, connect [read as: connect to server] is used.
https://stackoverflow.com/questions/12458019/shutting-down-sockets-properly

When you call close it decrements the handle count by one and if the handle count has reached zero then the socket and associated connection goes through the normal close procedure (effectively sending a FIN / EOF to the peer) and the socket is deallocated.
The thing to pay attention to here is that if the handle count does not reach zero because another process still has a handle to the socket then the connection is not closed and the socket is not deallocated.
On the other hand calling shutdown for reading and writing closes the underlying connection and sends a FIN / EOF to the peer regardless of how many processes have handles to the socket. However, it does not deallocate the socket and you still need to call close afterward.
https://stackoverflow.com/questions/409783/socket-shutdown-vs-socket-close

https://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python

packet splitting

https://stackoverflow.com/	questions/37292113/how-can-i-transfer-large-data-over-tcp-socket

