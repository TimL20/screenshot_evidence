import uuid
import hmac, hashlib, base64
from functions import *
import mss
from PIL import Image
import xml.etree.cElementTree as ET
version = "Test 0.1"

def TakeScreenShot():
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[0])
        HostName = getHostname()
        Times = getTimes()
        TimeZone = Times["timezone"]
        Times = Times["times"]
        NetInfo = getNetInfos()
        DNS = GetDNSServers()
        HostsFile = GetHostsFile()
        root = ET.Element("screenshot_evidence")
        ET.SubElement(root,"HostName").text = HostName
        PicID = str(uuid.uuid1()).replace("-","")
        FileFunctionsPY = open("functions.py", "r")
        hmacFunctionsPY = hmac.new(PicID.encode(), msg=FileFunctionsPY.read().encode(), digestmod=hashlib.sha3_512).hexdigest()
        FileMainPY = open("main.py", "r")
        hmacMainPY = hmac.new(PicID.encode(), msg=FileMainPY.read().encode(),digestmod=hashlib.sha3_512).hexdigest()
        xml_Software = ET.SubElement(root, "Software", {"Name": "Python Demo SSE", "Version": version})
        ET.SubElement(xml_Software, "File", {"Name": "functions.py"}).text = hmacFunctionsPY
        ET.SubElement(xml_Software, "File", {"Name": "main.py"}).text = hmacMainPY

        ET.SubElement(root,"PicID").text = PicID
        xml_Times = ET.SubElement(root, "ExtTimes",{"timezone": TimeZone})
        for server, EXTtime in Times.items():
            ET.SubElement(xml_Times, "Time",{"Server": server}).text = str(EXTtime)
        XML_DNS = ET.SubElement(root, "DNS_Servers")
        for Server in DNS:
            ET.SubElement(XML_DNS, "Server", {"IP": Server, "Function": "DNS"})
        XML_HostsFile = ET.SubElement(root, "HostsFile")
        for ip, Names in HostsFile.items():
            xml_client = ET.SubElement(XML_HostsFile, "Client", {"IP": ip})
            for name in Names:
                ET.SubElement(xml_client, "name").text = name
        XML_NetWorkHarware = ET.SubElement(root, "NetWorkHarware")
        for InterfaceName, InterfaceMeta in NetInfo.items():
            ThisInterface = ET.SubElement(XML_NetWorkHarware, "Interface",{"Name": InterfaceName, "MAC": InterfaceMeta["mac"]})

        tree = ET.ElementTree(root)
        tree.write("test.xml")
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img.save("test.png")

TakeScreenShot()
