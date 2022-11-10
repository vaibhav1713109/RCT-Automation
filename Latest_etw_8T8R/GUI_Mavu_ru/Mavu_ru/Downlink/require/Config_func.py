########################################################################
## Imports
########################################################################

import sys, os
import time, paramiko
from require.VSA_Configure import VSA_Write_SCPI, VSA_Query_SCPI, Run_RM
from require.Take_ScreenShot import ScreeneShot
  

########################################################################
## Enable 1pps 
########################################################################
def Enable_1PPS(RU_IP:str ,RU_UserName:str,RU_Password:str):
    '''Description: It will take three aruguments to take ssh of RU.

        RU_IP : ip address of ru to take ssh of RU.
        RU_UserName : Username of RU {Eg. root}
        RU_Password : Password of RU {Eg. root}'''


    iter1 = 0
    host = RU_IP           ######## Ip Address of RU ########
    flag = False
    while(iter1 < 1):
        iter1 += 1
        response = os.system("ping " + host)

        ############## Check the status of Ping ##############
        if response == 0:
            try:
                print("Pinging ip {0}".format(host))
                port = 22
                username = RU_UserName               ######## Username for login to RU ########
                password = RU_Password               ######## Password for login to RU ########

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port, username, password)
                CMD = 'devmem 0xa01b0014 w 0x1;'
                try:
                    stdin, stdout, stderr = ssh.exec_command(CMD)
                    lines = stdout.readlines()
                except Exception as e:
                    return '{}'.format(e)
                flag = True
                
            except Exception as e:
                flag = False
                print('{}'.format(e))
            return flag

        else :
            print("--------- Not able to ping-----------")
    return flag
   

########################################################################
## Configure VSA and Fetch Output Channel Power
########################################################################
def Conf_CH_P(CH_N,Inst_IP, Inst_Port, frequency, Bandwidth, test_model,Cable_Loss):

    '''Description : It will take 6 arguments and return the channel output power. The functionality of this function is to configure the VSA for output 
                    channel power and fetch the output channel power in dBm...
                    
            Inst_Ip : This is the ip of the instrument by which the test pc is connected.
            Inst_Port : This is the port number by which the RF In/Out is connected.
            frequency : This is the frequency in MHz on which the ouput power should come. {eg. 3500}
            Bandwidth : This is the bandwidth in MHz.
            test_model : The test model for selected modulation. {eg. DLTM3DOT1A/DLTM3DOT1}
            Cable_Loss : This is the path loss for transmit data from Antenna to the VSA. {eg. 40dBm attenautor, 1.5dBm cable_loss, so total loss = -41.5}'''


    ################ SCPI Commands to trigger [Channel Output Power] ####################
    ############ Commands for Configure the VSA ############
    Write_Cmd = [':SYST:PRES:FULL',':INIT:CONT ON',':INST:SEL NR5G',':OUTP:STAT OFF',':FEED:RF:PORT:INP RFIN',':CONF:CHP', 
    ':RAD:STAN:PRES:CARR B{}M'.format(Bandwidth),':RAD:STAN:PRES:FREQ:RANG FR1',':RAD:STAN:PRES:DMOD TDD',':RAD:STAN:PRES:SCS SCS30K', 
    ':RAD:STAN:PRES:RBAL {}'.format(test_model),':RAD:MIMO 0',':RAD:STAN:PRES:DLIN:BS:CAT ALAR',':SENSe:CCARrier:COUNt 1', 
    ':SENSe:CCARrier:CONFig:ALLocation Contiguous',':SENSe:CCARrier:CONFig:ALLocation:NCONtiguous:ABPoint CC0', 
    ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(Bandwidth),':SENSe:CCARrier0:STATe ON',':SENSe:CCARrier0:FREQuency:OFFSet 0MHz', 
    ':SENSe:CCARrier0:SPECtrum NORM',':CCAR:REF {}'.format(frequency),':RAD:STAN:PRES:IMM',':RAD:STAN:DIR DLINK', 
    ':CHP:AVER:STAT 0',':POW:RANG 10',':CHP:SAV ON',':SWE:EGAT:SOUR FRAM',':CORR:BTS:GAIN {}'.format(Cable_Loss),':OUTP:STAT ON',':POW:RANG:OPT IMM']

    ################# Connect The Instrument ##############
    

    try:
        VSA, RM = Run_RM(Inst_IP,Inst_Port)
        ################# Write SCPI For POWER ##############
        VSA_Write_SCPI(VSA, Write_Cmd)
        time.sleep(2)
        VSA.timeout = 5000
        for _ in range(10):
            try:
                Res = VSA.query_ascii_values(':FETC:CHP?')
                print(Res)
                # Output_Power = Res.split(',')
                Output_Power = Res
                freq = str(int(frequency)/1000000000)
                print(freq)
                Filename = ScreeneShot(VSA,'{0}_{1}_CH_P'.format(CH_N,freq))
                output_power = "{:.2f}".format(float(Output_Power[0]))
                ###################### Return Output Channel Power ######################
                if float(output_power) > 26 and float(output_power) < 32:

                    return output_power, Filename,'Pass'
                
                else:
                    return output_power, Filename,'Fail'
            except Exception as e:
                print('{} :FETC:CHP?'.format(e))
        VSA.close()
        


    except Exception as e:
        print('{} CH_PW'.format(e))

########################################################################
## Calculate ACLR
########################################################################
def ACLR_CAL(CH_N,INS,freq):
    time.sleep(1)
    INS.timeout = 5000
    for _ in range(10):
        try:
            time.sleep(1)
            Res = INS.query_ascii_values(':FETC:ACP?')
            OUT = Res
            # time.sleep(2)
            Filename = ScreeneShot(INS,'{0}_{1}_ACLR'.format(CH_N,freq))
            # print(str(float(OUT[4])),str(float(OUT[6])),str(float(OUT[8])),str(float(OUT[10])))
            low_aclrA = "{:.2f}".format(float(OUT[4]))
            high_aclrA = "{:.2f}".format(float(OUT[6]))
            low_aclrB = "{:.2f}".format(float(OUT[8]))
            high_aclrB = "{:.2f}".format(float(OUT[10]))
            if float(low_aclrA) < -45 and float(high_aclrA) < -45 and float(low_aclrB) < -45 and float(high_aclrB) < -45:
                return low_aclrA, high_aclrA, low_aclrB, high_aclrB, Filename,'Pass'
            else:
                return low_aclrA, high_aclrA, low_aclrB, high_aclrB, Filename,'Fail'
        
        except Exception as e:
            print('{} ACLR_CAL'.format(e))
    else:
        return 'Timeout expired before operation completed. ACLR_CAL'

########################################################################
## Configure VSA and Fetch Output Channel Power
########################################################################
def test_ACLR(CH_N,Inst_IP, Inst_Port, frequency, Bandwidth, test_model,Cable_Loss):

    '''Description : It will take 6 arguments and return tupple of four ACLR values {Low ACLR, High ACLR, Low 2*BW ACLR, High 2*BW ACLR}. 
                    The functionality of this function is to configure the VSA for Calculating ACLR values and fetch the ACLR values in dBm...
                    
            Inst_Ip : This is the ip of the instrument by which the test pc is connected.
            Inst_Port : This is the port number by which the RF In/Out is connected.
            frequency : This is the frequency in MHz on which the ouput power should come. {eg. 3500}
            Bandwidth : This is the bandwidth in MHz.
            test_model : The test model for selected modulation. {eg. DLTM3DOT1A/DLTM3DOT1}
            Cable_Loss : This is the path loss for transmit data from Antenna to the VSA. {eg. 40dBm attenautor, 1.5dBm cable_loss, so total loss = -41.5}'''

    ############ ACLR SCPI Commands for Configuring VSA ###########
    ACLR = {
    'Writeable' : [':INST:SEL NR5G',':INIT:CONT ON',':OUTP:STAT OFF',':FEED:RF:PORT:INP RFIN',':CONF:ACP', 
    ':RAD:STAN:PRES:CARR B{}M'.format(Bandwidth),':RAD:STAN:PRES:FREQ:RANG FR1',':RAD:STAN:PRES:DMOD TDD',':RAD:STAN:PRES:SCS SCS30K', 
    ':RAD:STAN:PRES:RBAL {}'.format(test_model),':RAD:MIMO 0',':RAD:STAN:PRES:DLIN:BS:CAT ALAR',':SENSe:CCARrier:COUNt 1', 
    ':SENSe:CCARrier:CONFig:ALLocation Contiguous',':SENSe:CCARrier:CONFig:ALLocation:NCONtiguous:ABPoint CC0', 
    ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(Bandwidth),':SENSe:CCARrier0:STATe ON', 
    ':SENSe:CCARrier0:FREQuency:OFFSet 0MHz',':SENSe:CCARrier0:SPECtrum NORM',':CCAR:REF {}'.format(frequency), 
    ':RAD:STAN:PRES:IMM',':INIT:CONT ON',':RAD:STAN:DIR DLINK',':ACP:AVER:STAT 0',':POW:RANG 10', 
    ':ACP:SWE:TIME:AUTO:RUL ACC',':RAD:STAN:DIR DLINK',':RAD:STAN:PRES:DLIN:ACH NR',':ACP:CARR1:PREF:TYPE MPC', 
    ':ACP:CORR:NOIS ON',':RAD:STAN:PRES:IMM',':ACP:SWE:TIME:AUTO:RUL ACC',':RAD:STAN:DIR DLINK', 
    ':RAD:STAN:PRES:DLIN:ACH NR',':ACP:CARR1:PREF:TYPE MPC',':ACP:CORR:NOIS ON',':SWE:EGAT:STATE 1', 
    ':TRIG:FRAM:SYNC RFB',':SWE:EGAT:SOUR FRAM',':SWE:EGAT:LENG 3.7 ms',':SWE:EGAT:DEL 5 ms', 
    ':TRIG:ACP:SOUR IMM',':CORR:BTS:GAIN {}'.format(Cable_Loss),':INIT:CONT ON',':INIT:CONT ON', 
    ':INIT:CONT ON',':INIT:IMM',':DISP:FSCR 0',':OUTP:STAT OFF',':POW:RANG:OPT IMM']
    }
    ACLR_OUT1 = []         ######## For Write scpi output of ACLR
    try:

        ################# Connect The Instrument ##############
        VSA, RM = Run_RM(Inst_IP,Inst_Port)

        ################# Write SCPI For ACLR ##############
        VSA_Write_SCPI(VSA, ACLR['Writeable'])
        time.sleep(2)

        ################# query_ascii_values For ACLR ##############
        freq = str(int(frequency)/1000000000)
        ACLR_OUT = ACLR_CAL(CH_N,VSA,freq)
        VSA.close()
        ###################### Return tuple of Four values of ACLR ######################
        return ACLR_OUT 


    except Exception as e:
        print('{} test_ACLR'.format(e))
        return '{} Test_ACLR'.format(e),'Fail'

########################################################################
## Calculate EVM
########################################################################
def EVM_CAL(CH_N,INS,freq):
    time.sleep(1)
    INS.timeout = 5000
    for _ in range(10):
        try:
            time.sleep(3)
            INS.timeout = 5000
            CMD = ':FETCh:EVM000001?'
            Res = INS.query_ascii_values(CMD)
            # OUT = Res.split(',')
            OUT = Res
            # time.sleep(2)
            Filename = ScreeneShot(INS,'{0}_{1}_EVM'.format(CH_N,freq))
            captured_evm = "{:.2f}".format(float(OUT[1]))
            if float(captured_evm) < 5:
                return captured_evm, Filename,'Pass'
            else:
                return captured_evm, Filename,'Fail'
        except Exception as e:
            # INS.close()
            print('{} EVM_CAL'.format(e))
    else:
        return 'Timeout expired before operation completed. EVM_CAL'

########################################################################
## Configure VSA and Fetch Output Channel Power
########################################################################
def test_EVM(CH_N,Inst_IP, Inst_Port, frequency, Bandwidth, test_model,Cable_Loss) -> str:

    '''Description : It will take 6 arguments and return the measured EVM. 
                    The functionality of this function is to configure the VSA for Calculating EVM value and fetch the EVM value...
                    
            Inst_Ip : This is the ip of the instrument by which the test pc is connected.
            Inst_Port : This is the port number by which the RF In/Out is connected.
            frequency : This is the frequency in MHz on which the ouput power should come. {eg. 3500}
            Bandwidth : This is the bandwidth in MHz.
            test_model : The test model for selected modulation. {eg. DLTM3DOT1A/DLTM3DOT1}
            Cable_Loss : This is the path loss for transmit data from Antenna to the VSA. {eg. 40dBm attenautor, 1.5dBm cable_loss, so total loss = -41.5}'''
            

    ############ EVM SCPI Commands for Configuring VSA ###########
    EVM = {
    'Writeable' : [':INST:SEL NR5G', ':INIT:CONT OFF', ':OUTP:STAT OFF', ':FEED:RF:PORT:INP RFIN', ':CONF:EVM', ':RAD:STAN:PRES:CARR B{}M'.format(Bandwidth), 
    ':RAD:STAN:PRES:FREQ:RANG FR1', ':RAD:STAN:PRES:DMOD TDD', ':RAD:STAN:PRES:SCS SCS30K', ':RAD:STAN:PRES:RBAL {}'.format(test_model), 
    ':RAD:MIMO 0', ':RAD:STAN:PRES:DLIN:BS:CAT ALAR', ':SENSe:CCARrier:COUNt 1', ':SENSe:CCARrier:CONFig:ALLocation Contiguous', 
    ':SENSe:CCARrier:CONFig:ALLocation:NCONtiguous:ABPoint CC0', ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(Bandwidth), 
    ':SENSe:CCARrier0:STATe ON', ':SENSe:CCARrier0:FREQuency:OFFSet 0MHz', ':SENSe:CCARrier0:SPECtrum NORM', ':CCAR:REF {}'.format(frequency), 
    ':RAD:STAN:PRES:IMM', ':INIT:CONT OFF', ':RAD:STAN:DIR DLINK', ':EVM:AVER:STAT 0', ':POW:RANG 10', 
    ':EVM:CCAR0:DC:PUNC ON', ':SWE:EGAT:STATE 0', ':TRIG:EVM:SOUR IMM', 
    ':RAD:STAN:PRES:RBAL {}'.format(test_model), ':RAD:STAN:PRES:IMM', ':RAD:MIMO 0', ':EVM:CCAR0:PROF:PDSC:AUTO OFF', 
    ':EVM:AVER:STAT 0', ':POW:RANG 10', ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(Bandwidth), ':SENSe:CCARrier0:STATe ON', 
    ':SENSe:CCARrier0:FREQuency:OFFSet 0MHz', ':SENSe:CCARrier0:SPECtrum NORM', ':CCAR:REF {}'.format(frequency), 'EVM:CCAR0:PHAS:COMP:AUTO OFF' ,'EVM:CCAR0:PHAS:COMP:FREQ 0GHz', ':EVM:CCAR0:DC:PUNC ON', 
    ':DISP:EVM:VIEW NORM;', ':DISP:EVM:WIND5:DATA FRES;', ':DISP:EVM:WIND1:DATA MTIM;', ':DISP:EVM:WIND1:Y:PDIV 0.275;',
    ':CORR:BTS:GAIN {}'.format(Cable_Loss), ':EVM:AVER:COUN?', ':EVM:AVER:COUN 1', ':INIT:CONT ON', ':POW:RANG:OPT IMM' ]
    }
    EVM_OUT1 = []          ######## For Write scpi output of EVM
    try:

        ################# Connect The Instrument ##############
        VSA, RM = Run_RM(Inst_IP, Inst_Port)

        ################# Write SCPI For ACLR ##############
        VSA_Write_SCPI(VSA, EVM['Writeable'])
        time.sleep(2)
        ################# query_ascii_values For EVM ##############
        
        freq = str(int(frequency)/1000000000)
        Measured_EVM = EVM_CAL(CH_N,VSA,freq)
        VSA.close()
        ###################### Return Measured EVM ######################
        return Measured_EVM


    except Exception as e:
        print('{} test_EVM'.format(e))
        return '{} test_EVM'.format(e), 'Fail'


if __name__ == "__main__":

    ######### Configuration of RU ###############
    # Enable_PPs = Enable_1PPS(RU_IP ,RU_UserName,RU_Password)                                        ##### True /False
    # intialize_fpga = Initialize_FPGA_TRX(Channel_No, frequency, trxAttenautaion, Test_model)        ##### True /False
    st = time.time()
    for _ in range(1):
        ######### Configuration of VSA ###############
        Power = Conf_CH_P('1','192.168.1.12','1', '3350000000', '100', 'DLTM3DOT1A','-45.5')                     ###### it will return value in string (Eg. 24.37)
        print(Power)
        # # time.sleep(5)
        Acp = test_ACLR('1','192.168.1.12','1', '3350000000', '100', 'DLTM3DOT1A','-45.5')                      ###### it will return tuple of 4 values (Eg. (-44.3,-44.3,-44.3,-44.3))
        print(Acp)
        # time.sleep(5)
        Evm = test_EVM('1','192.168.1.12','1', '3350000000', '100', 'DLTM3DOT1A','-45.5')                        ###### it will return in string (Eg. 2.5)
        print(Evm)
    en = time.time()
    res = en - st
    print('Time Taken: {}'.format(res))
    # print('{0}\n{1}\n{2}'.format(Power,Acp,Evm))
    pass