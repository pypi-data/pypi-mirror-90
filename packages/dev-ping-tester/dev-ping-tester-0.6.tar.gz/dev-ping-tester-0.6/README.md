# Ping tester

Simple module for ping testing 


## Usage
```bash
pip install dev-ping-tester
```

```python
# For Huawei Device
from dev_ping_tester.Huawei import Huawei


h= Huawei("DeviceName","IP",PORT,"Username","Password","telnet/ssh")
result = h.ping("192.168.0.10",10)
# 192.168.0.10 is destination and 10 is count
```

```python
# For Cisco Device
from dev_ping_tester.Cisco import Cisco


h= Cisco("DeviceName","IP",PORT,"Username","Password","telnet/ssh")
result = h.ping("192.168.0.10",10)
# 192.168.0.10 is destination and 10 is count

```


```python
# For Auto detect Device Type
from dev_ping_tester.AutoDetectDevice import AutoDetectDevice


a= AutoDetectDevice("DeviceName","IP",PORT,"Username","Password","telnet/ssh")
result = a.ping("192.168.0.10",10)
# 192.168.0.10 is destination and 10 is count
results = a.ping(["192.168.0.10","192.168.0.11"],10)
# 192.168.0.10 and 192.168.0.11 are list of IPs to check and 10 is count



```