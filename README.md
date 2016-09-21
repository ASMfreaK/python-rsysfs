# python-rsysfs
Simplistic Python SysFS remote interface via `paramiko` sftp.

## Usage
```python    
from rsysfs import Node
from paramiko.client import SSHClient
client = SSHClient()
... #initialize connection to remote host
client.connect(...)
sftp = client.open_sftp()
sys = sysfs.Node(sftp)

for bdev in sys.block:
    print bdev, str(int(bdev.size) / 1024 / 1024) + 'M'
```

