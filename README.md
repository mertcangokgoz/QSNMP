# TODO List

- [X] API Endpoint Json
- [X] API Sorgularının yapılması
- [X] SNMP için sorguların yazılması
- [X] SNMP ile alınan verilerin insancıllaştırılması
- [X] Kullanıcı bilgilerinin veritabanında tutulması (postgresql)
- [X] Hostname / IP ekleme, silme işlevleri
- [X] IP ve Host bilgilerinin veritabanında tutulması (postgresql)
- [X] Ajax Sorgularının Yazılması
- [X] Karşılaştırmaların yapılması
- [X] Google Chart ile görselleştirme
- [X] Kodun düzenlenmesi okunabilirlik arttırma
- [x] Güvenlik düzenlemeleri
- [X] Testlerin yapılması
- [X] Hataların Çözülmesi(login alanı, minör buglar(görsellik,hata mesajları))


# Test Makina

### Makina 1

**IP :** 138.68.108.208

**OS :** Centos 7

### Makina 2

**IP :** 178.62.94.188

**OS :** Debian 8

# Gerekliler şimdilik

```
sudo apt install build-essential python-dev python3-pip
pip3 install -t lib -r requirements.txt
```

# Örnek SNMP

```python
from easysnmp import Session
#https://easysnmp.readthedocs.io/en/latest/index.html
session = Session(hostname='138.68.108.208', community='public', version=2)
oid = {'sys':'.1.3.6.1.2.1.1.1.0'}
result = {}
for k in oid:
        result[k] = session.get(oid[k]).value
print(result)
```

# SNMP MIB OID

```
Load

1 minute Load: .1.3.6.1.4.1.2021.10.1.3.1

5 minute Load: .1.3.6.1.4.1.2021.10.1.3.2

15 minute Load: .1.3.6.1.4.1.2021.10.1.3.3



CPU

percentage of user CPU time: .1.3.6.1.4.1.2021.11.9.0

raw user cpu time: .1.3.6.1.4.1.2021.11.50.0

percentages of system CPU time: .1.3.6.1.4.1.2021.11.10.0

raw system cpu time: .1.3.6.1.4.1.2021.11.52.0

percentages of idle CPU time: .1.3.6.1.4.1.2021.11.11.0

raw idle cpu time: .1.3.6.1.4.1.2021.11.53.0

raw nice cpu time: .1.3.6.1.4.1.2021.11.51.0



Memory Statistics



Total Swap Size: .1.3.6.1.4.1.2021.4.3.0

Available Swap Space: .1.3.6.1.4.1.2021.4.4.0

Total RAM in machine: .1.3.6.1.4.1.2021.4.5.0

Total RAM used: .1.3.6.1.4.1.2021.4.6.0

Total RAM Free: .1.3.6.1.4.1.2021.4.11.0

Total RAM Shared: .1.3.6.1.4.1.2021.4.13.0

Total RAM Buffered: .1.3.6.1.4.1.2021.4.14.0



Disk Statistics

The snmpd.conf needs to be edited. Add the following (assuming a machine with a single / partition):

disk / 100000 (or)

includeAllDisks 10% for all partitions and disks
The OIDs are as follows

Path where the disk is mounted: .1.3.6.1.4.1.2021.9.1.2.1

Path of the device for the partition: .1.3.6.1.4.1.2021.9.1.3.1

Total size of the disk/partion (kBytes): .1.3.6.1.4.1.2021.9.1.6.1

Available space on the disk: .1.3.6.1.4.1.2021.9.1.7.1

Used space on the disk: .1.3.6.1.4.1.2021.9.1.8.1

Percentage of space used on disk: .1.3.6.1.4.1.2021.9.1.9.1

Percentage of inodes used on disk: .1.3.6.1.4.1.2021.9.1.10.1

System Uptime: .1.3.6.1.2.1.1.3.0
```
