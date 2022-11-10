import pyvisa

import pyvisa
import time
import pyvisa_py.protocols.rpc, pyvisa.errors
# from SSH_RU import take_SSH
from fpdf import FPDF

def Run_RM(Inst_Ip, Port):
    # try:
        RM = pyvisa.ResourceManager()
        VSA = RM.open_resource('TCPIP::{0}::inst1::INSTR'.format(Inst_Ip, Port))
        # print(RM.list_opened_resources())
        VSA.read_termination='\n'
        VSA.write_termination='\n'
        VSA.delay = .2
        # VSA.write('*CLS')
        time.sleep(1)
        for _ in range(10):
            try:
                VSA.write('*CLS')
                t = int(time.time())
                Res = VSA.query('*IDN?')
                print('{0} ; VXT2           ; Debug       ; SCPI >> *IDN?'.format(t))
                print('{0} ; VXT2           ; Debug       ; SCPI << {1}'.format(t,Res))
                return VSA, RM
            except Exception as e:
                print('{} Run_RM Function'.format(e))
        return VSA, RM


def VSA_Write_SCPI(INS,Write_List):
    #Write_List = [':INIT:CONT ON',':INST:SEL NR5G',':OUTP:STAT OFF',':FEED:RF:PORT:INP RFIN',':CONF:CHP']
    INS.timeout = 5000
    for CMD in Write_List:
        # if CMD != ':POW:RANG:OPT IMM':
            for _ in range(10):
                try:
                    t = int(time.time())
                    # print('{0} ; VXT2           ; Debug       ; SCPI >> {1}'.format(t,CMD))
                    Res = INS.write(CMD)
                    # print('{0} ; VXT2           ; Debug       ; SCPI << {1}'.format(t,Res))
                    if Res:
                        break
                except Exception as e:
                    print(e,CMD)
        
                

def VSA_Query_SCPI(INS,CMD):
        # INS.timeout = 5000

        try:
            # INS.timeout = None
            Res = INS.query(CMD)
            # print(Res)
            return Res
        except Exception as e:
            return e

if __name__ == "__main__":
    vsa,RM = Run_RM('192.168.1.12','1')
    # print(vsa,RM)
    # Ch_P_Window = [':INIT:CONT ON',':INST:SEL NR5G',':OUTP:STAT OFF',':FEED:RF:PORT:INP RFIN',':CONF:CHP',':POW:RANG:OPT IMM']
    # VSA_Write_SCPI(vsa, Ch_P_Window)
    time.sleep(5)
    vsa.timeout = 5000
    # print(vsa.write(':READ:CHP?'))
    vsa.read_termination='\n'
    # vsa.write_termination='\n'
    # print(vsa.read_bytes(1))
    print(vsa.query(':FETC:CHP?'))
    ACLR_Window = [':INST:SEL NR5G',':INIT:CONT ON',':OUTP:STAT OFF',':FEED:RF:PORT:INP RFIN',':CONF:ACP',':POW:RANG:OPT IMM']
    VSA_Write_SCPI(vsa, ACLR_Window)
    time.sleep(5)
    print(vsa.query(':FETC:ACP?'))
    # vsa.query('*IND?')
    # print(VSA_Query_SCPI(vsa,':*IND?'))
    # print(VSA_Query_SCPI(vsa,':READ:ACP?'))
    vsa.close()
