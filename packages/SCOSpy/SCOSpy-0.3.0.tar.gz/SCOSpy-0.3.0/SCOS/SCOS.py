#!/usr/bin/python
from bitstring import BitArray
import datetime


def Time(data):
    ret=datetime.datetime(1970,1,1,0,0,0,0)+datetime.timedelta(seconds=BitArray(hex=data[0:8]).uint)+datetime.timedelta(microseconds=BitArray(hex=data[8:16]).uint)
    return ret

s2kDB={
    "PacketType":{
        1: "Telemetry Packet",
        2: "Telecommand Packet",
        3: "Event Packet"
    },
    "SpacecraftID":{
        816: {
            "Spacecraft": "BepiColombo",
            "Band": "X-Band"
        },
        817: {
            "Spacecraft": "BepiColombo",
            "Band": "Ka-Band"
        }
    },
    "TsPolicy":{
        0: "Packet timestamped with creation time",
        1: "Packet timestamped with frame recived time",
        2: "Packet timestamped with SCET"
    },
    "accessFlag":{
        0: "Inserted Packet",
        1: "Updated"
    },
    "dataUnitType": {
        0: "TM Transfer Frame",
        1: "TM Source Packet",
        2: "Internal MCS TM Packet"
    },
    "groundStation":{
        21: "Kourou",
        22: "Perth",
        23: "New Norcia",
        24: "Cebreros",
        25: "Malargue",
        30: "Maspalomas",
        97: "Usuda",
        98: "Uchinoura"
    },
    "mission": {
        816: "BepiColombo"
    },
    "qualifier": {
         "00": "Good",
         "01": "Good",
         "02": "CLCW",
         "10": "Bad",
         "11": "Bad",
         "12": "User Defined Constant",
         "20": "Idle",
         "21": "Idle",
         "22": "Status Consistency Check",
         "32": "Dynamic Misc",
         "42": "Online MIB changes",
         "52": "SPPG",
         "62": "SPID Validity",
         "72": "TPKT Configuration",
         "82": "External Source"
    },
    "simFlag": {
        0: {"flag": "00", "description": "Not Simulated Packet"},
        1: {"flag": "01", "description": "Simulated Packet"}
    },
    "stream": {
        "1"    : "Telecommand Stream",
        "1000" : "VC0 Real-Time Non-Science or Events (online)",
        "1001" : "VC1 Playback Non-Science or Events (online)",
        "1002" : "VC2 Science (online)",
        "1003" : "VC3 File-Transfer (online)",
        "2000" : "VC0 Real-Time Non-Science or Events (offline)",
        "2001" : "VC1 Playback Non-Science or Events (offline)",
        "2002" : "VC1 Playback Non-Science or Events (offline)",
        "2003" : "VC2 Science (offline)",
        "65535": "Internal non Spacecraft Telemetry"
    },
    "timeQuality": {
        0: "Good",
        1: "Inaccurate",
        2: "Bad"
    }
}

class SCOS:

    def __init__(self,data):
        self.CPH=SCOS_CPH(data[0:120])
        if self.CPH.PType.Code == 1:
            self.TMPH=SCOS_TMPH(data[120:152])
            self.Data=data[152:]
            # c = BitArray(hex=hexdata[152:])
            # self.SPH=SPHeader(c[:48])
            # self.Data=PacketData(hexdata)
            # if self.SPH.APID == 807 :
            #     self.out = Decode807(hexdata[184:])
            # elif self.SPH.APID == 801 :
            #     self.out = Decode801(hexdata[184:],self.Data.Service,self.Data.SubService)
        elif self.CPH.PType.Code ==2:
             self.TCPH=SCOS_TCPH(data[120:208],self.CPH.SeqCounter)
             self.Data=data[208:]
        #     c = BitArray(hex=hexdata[208:])
        #     self.SPH=SPHeader(c[:48])
        #     self.SPH=SPHeader_new(hexdata[208:220])
        #     self.Data=TelecommandData(hexdata)
        else:
            print("Not Decoded")

def jsQuery(name, value):
    par1=s2kDB.get(name)
    if par1:
        par2=s2kDB[name].get(value)
        if par2:
            return s2kDB[name][value]
        else:
            return "Not Decoded"
    else:
        return "Attribute Not defined"

    #return s2kDB[name][value]

class SCOS_TCPH:
    def __init__(self,data,SSC):
        self.UplinkTime=Time(data[0:16])
        self.ExecTime=Time(data[16:32])
        self.LUTime=Time(data[32:48])
        self.RequestID=BitArray(hex=data[48:56]).uint
        self.ReqElemIdx=BitArray(hex=data[56:60]).uint
        self.VarAddSz=BitArray(hex=data[60:64]).uint
        self.PUSAPID=BitArray(hex=data[64:68]).uint
        bTemp=BitArray(hex=data[64:68])
        self.PID=int(bTemp.bin[5:12],2)
        self.PCAT=int(bTemp.bin[12:16],2)
        self.PUSSSC=BitArray(hex=data[68:72]).uint
        self.PUSST=BitArray(hex=data[72:74]).uint
        self.PUSSST=BitArray(hex=data[74:76]).uint
        self.PUSAck=BitArray(hex=data[76:78]).uint # # TODO: oggetto per la decodifica del binario solitamente 9 -> 0000 1001. ultimi 4 sono significativi primo (non) richieto ack per accettazione ultimo (non) richiesto ack per esecuzione
        self.UplinkFlag=BitArray(hex=data[78:80]).uint
        self.SourceHost=BitArray(hex=data[80:82]).uint
        self.SourceType=BitArray(hex=data[82:84]).uint
        self.ReqDetFixedSize=BitArray(hex=data[84:88]).uint

class AccessF:
    def __init__(self,flag):
        self.Code=flag
        self.Description = jsQuery('accessFlag',flag)#DBquery('accessFlag',flag)

class SimFlag:
    def __init__(self,flag):
        self.Code=int(flag,2)
        self.Description = jsQuery('simFlag',self.Code)#DBquery('simFlag',self.Code)

class SCID:
    def __init__(self,code):
        ret = jsQuery("SpacecraftID",code)
        #c = conn.cursor()
        #c.execute("select * from SpacecraftID where id = '%s'" % code)
        #value = c.fetchone()
        if ret == "Not decoded": #s None:
            self.Spacecraft=ret
            self.Band=ret
        else:
            self.Spacecraft = ret["Spacecraft"]
            self.Band = ret['Band']

class GSID:
    def __init__(self,code):
        self.Code=code
        self.Station = jsQuery('groundStation',code)#DBquery('groundStation',code)

class PType:
    def __init__(self,code):
        self.Code=int(code,2)
        self.Station = jsQuery('groundStation',code)#DBquery('PackType',self.Code)

class FilingF:
    def __init__(self,code):
        self.Code = int(code,2)
        if self.Code == 1:
            self.Description = "Packet filed in MSC archive"
        else:
            self.Description = "Packet not filed in MSC archive"

class DistF:
    def __init__(self,code):
        self.Code = int(code,2)
        if self.Code == 1:
            self.Description = "Packet is to be distributed to the MSC application"
        else:
            self.Description = "Packet is not to be distributed to the MSC application"

class TSPolicy:
    def __init__(self,code):
        self.Code = int(code,2)
        self.Description = jsQuery('TsPolicy',self.Code)#DBquery('TsPolicy',self.Code)

class TimeQuality:
    def __init__(self,code):
        self.Code = int(code,2)
        self.Description = jsQuery('timeQuality',self.Code)#DBquery('timeQuality',self.Code)

class StreamID:
    def __init__(self,code):
        self.Code = code
        self.Description = jsQuery('stream',self.Code)#DBquery('stream',self.Code)

class MissionID:
    def __init__(self,code):
        self.Code = code
        self.Description = jsQuery("mission",self.Code)


class SCOS_CPH:
    def __init__(self,data):
        self.CTree=BitArray(hex=data[0:4])
        self.AccessF=AccessF(BitArray(hex=data[4:6]).uint)
        bTemp=BitArray(hex=data[6:8])
        self.SimFlag=SimFlag(bTemp.bin[6:8])
        self.FilingTime=Time(data[8:24])
        self.CreationTime=Time(data[24:40])
        self.CreateID=BitArray(hex=data[40:48]).uint
        self.SCID=SCID(BitArray(hex=data[48:52]).uint)
        self.GSID=GSID(BitArray(hex=data[52:56]).uint)
        self.PSize=BitArray(hex=data[56:64]).uint
        bTemp=BitArray(hex=data[64:66])
        self.PType=PType(bTemp.bin[0:4])
        self.Version=int(bTemp.bin[4:8],2)
        bTemp=BitArray(hex=data[66:68])
        self.FilingFlag=FilingF(bTemp.bin[2:3])
        self.DistFlag=DistF(bTemp.bin[3:4])
        self.TSPolicy=TSPolicy(bTemp.bin[4:6])
        self.TQ=TimeQuality(bTemp.bin[6:8])
        self.StreamID=StreamID(BitArray(hex=data[68:72]).uint)
        self.SeqCounter=BitArray(hex=data[72:80]).uint
        self.SPID=BitArray(hex=data[80:88]).uint
        self.MissionID=MissionID(BitArray(hex=data[96:100]).uint)


class DataUnitType:
    def __init__(self,code):
        self.Code=code
        self.Description= jsQuery('dataUnitType',self.Code)#DBquery('dataUnitType',self.Code)

class RouteID:
    def __init__(self,data):
        bTemp=BitArray(hex=data)
        DUT=int(bTemp.bin[8:12],2)
        Qualif=int(bTemp.bin[12:16],2)
        self.DUT=DataUnitType(DUT)
        self.Qualif=Qualifier(DUT,Qualif)

class Qualifier:
    def __init__(self,dut,code):
        self.Code = code
        #c = conn.cursor()
        ser=str(code)+str(dut)
        self.Descriprion=s2kDB["qualifier"][ser]

class SCOS_TMPH:
    def __init__(self,data):
        self.TPSD=BitArray(hex=data[8:16]).uint
        self.RouteID=RouteID(data[16:20])
        self.PUSAPID=BitArray(hex=data[20:24]).uint
        self.PUSSSC=BitArray(hex=data[24:28]).uint
        self.PUSST=BitArray(hex=data[28:30]).uint
        self.PUSSST=BitArray(hex=data[30:32]).uint
