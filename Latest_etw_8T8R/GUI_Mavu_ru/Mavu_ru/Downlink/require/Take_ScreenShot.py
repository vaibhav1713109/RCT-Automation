from datetime import datetime
import time,os
dir_path = os.path.dirname(__file__)
dir_path = os.path.dirname(dir_path)
print(dir_path,'Take_Screenshot')

def ScreeneShot(VSA,filename):
    s = datetime.now()
    # file_name_format = f"{s.hour}_{s.minute}_{s.second}_{s.day}_{s.month}_{s.year}"
    filePathInstr = r"c:\temp\hcopy_dev.png"
    filePathPc = r"{}\Screenshot\{}.png".format(dir_path,filename)
    # file path on instrument
    # IP_ADDR = '192.168.1.12'    		##### Ip of VXT
    # RM = pyvisa.ResourceManager()
    # VSA = RM.open_resource('TCPIP0::{}::inst{}::INSTR'.format(IP_ADDR))
    time.sleep(5)
    VSA.write(f':MMEM:STOR:SCR "{filePathInstr}"')
    # VSA.timeout = 5000
    # ask for file data from instrument
    fileData = bytes(VSA.query_binary_values(f'MMEM:DATA? "{filePathInstr}"', datatype='s'))
    # save data in file on local hard drive
    newFile = open(filePathPc, "wb")
    newFile.write(fileData)
    newFile.close()
    # VSA.close()
    # print(filename)
    return filePathPc
