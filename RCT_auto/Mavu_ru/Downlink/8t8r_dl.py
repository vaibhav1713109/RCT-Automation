########################################################################
## QPAM Downlink Updated
########################################################################

########################################################################
## Import Modules
########################################################################
#! /home/vvdn/Documents/Mavenir_8/Mavenir_8/bin/python
import time , os
from etw.hw_test.rru_init8_etap import main as RRU_main
from require import Genrate_Report, VSA_Configure
from require.Config_func import Enable_1PPS, Conf_CH_P, test_ACLR, test_EVM
from require.VSA_Configure import VSA_Write_SCPI, VSA_Query_SCPI, Run_RM
from etw.hw_test.qpam_trx_disable8_etap import main as Disable_qpam
from tabulate import tabulate
from configparser import ConfigParser
from datetime import datetime


########################################################################
## For reading data from .ini file
########################################################################
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(os.path.abspath(dir_name))
print(dir_name,'8t8r_dl')
configur = ConfigParser()
configur.read('{}\Downlink\Python_Inputs.ini'.format(dir_name))
# print(dir_name)
sample = ConfigParser()
sample.read('{}\sample.ini'.format(dir_name))


########################################################################
## Class Declaration
########################################################################
class DL_Only():

    ########################################################################
    ## Constructor of Class
    ########################################################################
    def __init__(self) -> None:
        self.ip_addr = '192.168.1.10'
        ######## VSA Path Loss ########
        #self.cable_loss = configur.get('Inputs','cable_loss')[1:-1] 
        self.path_loss = sample.get('Section1','cable_loss').split(' ')
        for i in range(len(self.path_loss)):
            self.path_loss[i] = self.path_loss[i]
        print(self.path_loss)
        ######## VSA IP and hislip port ########                
        self.inst_ip, self.port = configur.get('Inputs','InstrumentIp')[1:-1],configur.get('Inputs','InstrumentPort')[1:-1]   
        self.Test_Mod_str = sample.get('Section1','model')
        test_models = {'TM_3.1':'DLTM3DOT1','TM_3.1a':'DLTM3DOT1A'}
        if self.Test_Mod_str in test_models.keys():
            self.Test_M_scpi = test_models[self.Test_Mod_str]
        # self.Test_Mod_str = 'TM_3.1a'
        # self.Test_M_scpi = 'DLTM3DOT1A'
        self.trxAttenation = configur.get('Inputs','trxattenaution')[1:-1]
        self.trxID,self.qpamID = 0,0
        pass


    ########################################################################
    ## Test Execution starts from here
    ########################################################################
    def RUN_DL(self,CH_Ns):
        ########################################################################
        ## Enabling 1PPS in RU
        ########################################################################
        if Enable_1PPS(self.ip_addr,'root','root'):
            print('\n1PPS enabled successfully...')
        else:
            print('\nRU is not Pinging, SSH Connection is not established......')
            return False   



        ########################################################################
        ## Check Vector Analyzer Status
        ########################################################################
        try:
            response = os.system("ping " + self.inst_ip)
            if response != 0:
                print('\nInstrument Ip is not pinging...')
                return False
            ############## Test Weather instruments connect or not ###############
            VSA,RM = VSA_Configure.Run_RM(self.inst_ip,self.port)
            VSA.close()
            # sprint(type(str(Check_VSA_Status)))
            if 'TCPIPInstrument' in str(VSA):
                print('\n\n-------- VSA is connected successfully -------')

        except Exception as e:
            print('\n\n')
            print(e)
            print('\n\n-------- Please open the Vector Analyser application -------\n\n')
            return False


       
        address = "PXI10::0-0.0::INSTR"

        TX_OP_Power = []
        ACLR_VAL = []
        EVM_VAL = []
        PNG_File = {'CH_PW':[], 'ACLR':[], 'EVM':[]}
        
        freqs = sample.get('Section1','frequency').split(' ')
        for i in range(len(freqs)):
            # freqs[i] = freqs[i][1:-1]
            freqs[i] = freqs[i]
        print(freqs)
        for freq in freqs:
            #######################################################################
            # Run ETW script for enable all 8 channel
            ######################################################################
            try:
                print('\n--------------Running ETW to Initialize all Channel--------------')
                etw_out = RRU_main(frequency=str(int(float(freq)*1000000)),testModel=self.Test_Mod_str[3:],trxAttenuation=self.trxAttenation)
                print('\n-------------- ALL Channel are up...--------------')
            except Exception as e:
                print(e)
                return "{}".format(e)
            for CH_N in CH_Ns:
                if CH_N <= 4:
                    self.cable_loss = self.path_loss[0]
                else:
                    self.cable_loss = self.path_loss[1]
                ########################################################################
                ## Start KtmSwitch 
                ########################################################################
                print("------------------Starting the Channel no. {0}---------------------------\n\n\n".format(CH_N))
                # cmd = "KtMSwitch_Cpp_CloseChannel.exe " + address + " " + "p1ch" + str(CH_N)
                cmd = r"{}\Downlink\KtMSwitch_Cpp_CloseChannel.exe {} p1ch{}".format(dir_name,address,CH_N)
                output = os.system(cmd)
                print(output)
                ########## Check the status of RF Switch #############
                if type(output) == int and output != 0:
                    print('-'*50)
                    print('\n\n Please Connect the Type C USB with RF Switch...')
                    print('-'*50)
                    return False
                # input("Please press enter for next channel")
                time.sleep(1)


                ########################################################################
                ## Configure VSA for Channel Power
                ########################################################################
                empty_list = [str(CH_N),freq,'100',self.Test_Mod_str,'-','26','32']
                print("------------------Starting Downlink for CH no. {0}------------------------\n\n".format(CH_N))
                print('VSA Configuration for channel power under process...\n')
                CH_P = Conf_CH_P(CH_N,self.inst_ip, self.port, int(float(freq)*1000000000), '100', self.Test_M_scpi,self.cable_loss)
                print('VSA Configuration for channel power completed...\n')
                if len(CH_P) >= 3:
                    empty_list[4] = CH_P[0]
                    PNG_File['CH_PW'].append(CH_P[-2])
                    PNG_File['CH_PW'].append(CH_N)
                else:
                    break
                TX_OP_Power.append(empty_list)

                
                ########################################################################
                ## Configure VSA for ACLR
                ########################################################################
                empty_list = [str(CH_N),freq,'100',self.Test_Mod_str,'-','-','-','-','<-45']
                print('VSA Configuration for ACLR under process...\n')
                ACLR = test_ACLR(CH_N,self.inst_ip, self.port, int(float(freq)*1000000000), '100', self.Test_M_scpi,self.cable_loss)
                print('VSA Configuration for ACLR completed...\n')
                if len(ACLR) >= 3:
                    empty_list[4] = ACLR[0]
                    empty_list[5] = ACLR[1]
                    empty_list[6] = ACLR[2]
                    empty_list[7] = ACLR[3]
                    PNG_File['ACLR'].append(ACLR[-2])
                    PNG_File['ACLR'].append(CH_N)
                else:
                    break
                ACLR_VAL.append(empty_list)



                ########################################################################
                ## Configure VSA for EVM
                ########################################################################
                empty_list = [str(CH_N),freq,'100',self.Test_Mod_str,'-','<5']
                print('VSA Configuration for EVM under process...\n')
                EVM = test_EVM(CH_N,self.inst_ip, self.port, int(float(freq)*1000000000), '100', self.Test_M_scpi,self.cable_loss)
                print('VSA Configuration for EVM completed...\n')
                if len(EVM) >= 3:
                    empty_list[4] = EVM[0]
                    PNG_File['EVM'].append(EVM[-2])
                    PNG_File['EVM'].append(CH_N)
                else:
                    break
                EVM_VAL.append(empty_list)
                print("------------------Completed Downlink for CH no. {0}------------------------\n\n".format(CH_N))
            ########################################################################
            ## disable all channel 
            ########################################################################
            Disable_qpam()
        print(TX_OP_Power)
        print(ACLR_VAL)
        print(EVM_VAL)
        VSA.close()
        return TX_OP_Power, ACLR_VAL, EVM_VAL,PNG_File

    ########################################################################
    ## Verify the Result of RUN_DL function and genration of PDF report
    ########################################################################
    def Main(self,CH_NOs):

        Result = self.RUN_DL(CH_Ns=CH_NOs)
        if Result:
            PDF = Genrate_Report.Report_Genration(Result,'123',self.Test_Mod_str,CH_NOs)
            s = datetime.now()
            file_name_format = f"{s.hour}_{s.minute}_{s.second}_{s.day}_{s.month}_{s.year}"
            filename = str(CH_NOs[0])+'_'+'3.35'+file_name_format
            # filename = str(CH_NOs[0])+'_'+'3.35'
            PDF.output(r'{}\Downlink\pdf\{}.pdf'.format(dir_name,"Result123"))
            return True
            # if len(Result[0]) == len(Result[1]) == len(Result[2]) == 8:
            #     return True
            # else:
            #     return '{0} Channels are completed\n{1} Channels are left...'.format(len(Result[0]),8-len(Result[0]))

        else:
            return False



if __name__ == "__main__":

    st = time.time()
    # Serial_no = configur.get('Inputs','Serial Number')[1:-1]
    CH_NOs = sample.get('Section1','channel').split(' ')
    # CH_NOs = list(map(int,CH_NOs.split(',')))
    # CH_NOs = int(CH_NOs)
    print(CH_NOs)
    for i in range(len(CH_NOs)):
        # CH_NOs[i] = int(CH_NOs[i][1:-1])
        CH_NOs[i] = int(CH_NOs[i])
    # print(Serial_no)
    DL_obj = DL_Only()
    # DL_obj.RUN_DL(CH_NOs)
    Result = DL_obj.Main(CH_NOs)
    if Result == True:
        print('Test Cases Completed...\n Please save PDF file...')
    elif type(Result) == str:
        print(Result)
    else:
        print('\nTest Case not Completed...')
    en = time.time()
    res = en - st
    print('Time Taken: {}'.format(res))
    print('+'*100)
    pass

        #         pass
        # pass