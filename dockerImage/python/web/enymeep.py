from ping3 import ping
from socket import socket
import json

##AVISO PARA NAVEGANTES, SI SE NECESITA ELIMINAR LA VERBOSITY HAY QUE CARGARSE TODOS LOS PRINTS

class PortItem:
    def __init__(self, port,status="?"):
        self.port = port
        self.status = status

class ObjectResult:
    def __init__(self, ip, status="Down"):
        self.ip = ip
        self.status = status
        self.ports = []
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

def scanTarget(ip,ports="22,80,443"):
    # print("bim bim, bam bam, cyka")
    rvalue=None
    ports=ports.split(",")
    portResult=ObjectResult(ip)
    print(f"\n{ip}------")
    for x in range(1,3,1):
        res = ping(ip, timeout=2)
        if res is None:
            continue
        else:
            if res is False:
                print("Too far")
                break
            else:
                rvalue=True
    if rvalue is True:
        portResult.status = "Up"
        c=0
        for port in ports:
            s = socket()
            s.settimeout(2)
            portStatus=PortItem(port,"Closed")
            try:
                socketRes = s.connect((ip,int(port)))
                portStatus.status = "Open"
            except OSError as e:
                if e.errno == 111:
                    pass
                elif e.errno == 113:
                    portResult.status="Unreacheable"
                else:
                    if type(e) == TimeoutError:
                        portStatus.status = "Open"
                    else:
                        print(f"An error has ocurred while scanning port {port}: {e.value}:")
                        print(e)
                        portStatus.status = "Error"
                    c=1
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"An exception has ocurred while scanning port {port}:")
                print(e)
            portResult.ports.append(portStatus)
    else:
        for port in ports:
            portStatus=PortItem(port,"?")
            portResult.ports.append(portStatus)
    print(portResult.to_json())
    return portResult.to_json()
# res = scanTarget("10.227.87.122","22,80,443,3306,2049,2050,902")
# print("Result-----------------------")
# print(res)