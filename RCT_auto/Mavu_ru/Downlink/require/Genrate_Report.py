from require import Convert_PDF
import os
dir_path = os.path.dirname(__file__)
dir_path = os.path.dirname(dir_path)
print(dir_path,'Generate_repor')

def Report_Genration(Result,sr_n,Test_Mod_str,CH_Ns):
    PDF = Convert_PDF.PDF_CAP()
    PDF.add_page(format=(350, 250))
    PDF.set_font("Times", size=12)
    PDF.set_font_size(float(10))
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5

    ########################################################################
    ## Save Output Data into Text file
    ########################################################################
    # print(Result)
    filename = open('{}\Logs\Result{}.txt'.format(dir_path,sr_n),'w')
    for res in Result[:3]:
        for ress in res:
            for res in ress:
                filename.writelines(str(res))
                filename.writelines(', ')
            filename.writelines('\n')
        filename.writelines('\n')

    ###################################### Test report verdict overview ####################################
    TC_Result = [['1', 'Base station output power'],['2', 'Adjacent Channel Leakage Power Ratio'],['3', 'Modulation quality']]
    Convert_PDF.HEADING(PDF, '\nTest report verdict overview \n')
    table_Header = ['Test Case ID', 'Description']
    # print(tabulate(TC_Result, headers=table_Header, tablefmt='fancy_grid'))
    Convert_PDF.render_header(
        PDF, table_Header, Header_H, PDF.epw / len(table_Header))
    Convert_PDF.render_table_data(
        PDF, TC_Result, line_height, PDF.epw / len(table_Header), table_Header)
    

    ################################### Base station output power- Test results #######################################
    PDF.add_page(format=(350, 250))
    print('\n\n\n')
    CH_POWER_Header = ['Channel No', 'Channel Frequency [GHz]', 'BS Channel Bandwidth BW [MHz]',
                    'Test Channel Model', 'Output Power [dbm]', 'Limit Low [dBm]', 'High Low [dBm]']
    Convert_PDF.HEADING(
        PDF, '\nBase station output power- Test results:\n')
    Convert_PDF.Test_HEADING(
        PDF, '''Test purpose : \nThe test purpose is to verify the accuracy of the maximum carrier output power across the frequency range and under normal and extreme conditions''')
    Convert_PDF.Test_HEADING(
        PDF, 'Test environment : \nNormal and Extreme test conditions.')
    Convert_PDF.Test_HEADING(PDF, 'NR FR1 test model: \n{}'.format(
        Test_Mod_str))
    # print(tabulate(Result[0],headers=CH_POWER_Header, tablefmt='fancy_grid'))
    Convert_PDF.render_header(
        PDF, CH_POWER_Header, line_height, PDF.epw / len(CH_POWER_Header))
    Convert_PDF.render_table_data(
        PDF, Result[0], line_height, PDF.epw / len(CH_POWER_Header), CH_POWER_Header)
    if len(Result[3]['CH_PW'])>0:
        Convert_PDF.add_image(PDF,Result[3]['CH_PW'])
    else:
        print('Screenshot didn\'t capture for Channel Power..')
    
    ################################### Adjacent Channel Leakage Power Ratio (ACLR) - Test results: #######################################
    PDF.add_page(format=(350, 250))
    # print('\n\n\n')
    ACLR_Header = ['Channel No', 'Channel Frequency [GHz]', 'BS Channel Bandwidth BW [MHz]', 'Test Channel Model',
                'Low ACLR [dB]', 'High ACLR [dB]', 'Low 2xBW ACLR [dB]', 'High 2xBW ACLR [dB]', 'ACLR Limit [dB]']
    Convert_PDF.HEADING(PDF, '\n Adjacent Channel Leakage Power Ratio (ACLR) - Test results: \n')
    Convert_PDF.Test_HEADING(PDF, '''Test purpose : \nTo verify that the adjacent channel leakage ratio requirement shall be met as specified by the minimum requirement.''')
    Convert_PDF.Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    Convert_PDF.Test_HEADING(PDF, 'NR FR1 test model: \n{}'.format(Test_Mod_str))
    # print(tabulate(Result[1], headers=ACLR_Header, tablefmt='fancy_grid'))
    Convert_PDF.render_header(PDF, ACLR_Header, line_height, PDF.epw / len(ACLR_Header))
    Convert_PDF.render_table_data(PDF, Result[1], line_height, PDF.epw / len(ACLR_Header), ACLR_Header)
    if len(Result[3]['ACLR'])>0:
        Convert_PDF.add_image(PDF,Result[3]['ACLR'])
    else:
        print('Screenshot didn\'t capture for ACP..')

    #################################  Modulation quality - Test results: #########################################
    PDF.add_page(format=(350, 250))
    print('\n\n\n')
    Convert_PDF.HEADING(PDF, '\n Modulation quality - Test results: \n')
    EVM_Header = ['Channel No', 'Channel Frequency [GHz]', 'BS Channel Bandwidth BW [MHz]',
                'Test Channel Model', 'Measured EVM (RMS) [%]', 'EVM Limit [%]']
    Convert_PDF.Test_HEADING(PDF, '''Test purpose : \nThe test purpose is to verify the modulation quality''')
    Convert_PDF.Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    Convert_PDF.Test_HEADING(PDF, 'NR FR1 test model: \n{}'.format(Test_Mod_str))
    # print(tabulate(Result[2], headers=EVM_Header, stralign='left',maxcolwidths=[10, 10, 10, 10, 10, 10, 10], tablefmt='fancy_grid'))
    Convert_PDF.render_header(PDF, EVM_Header, line_height, PDF.epw / len(EVM_Header))
    Convert_PDF.render_table_data(PDF, Result[2], line_height, PDF.epw / len(EVM_Header), EVM_Header)
    if len(Result[3]['EVM'])>0: 
        Convert_PDF.add_image(PDF,Result[3]['EVM'])
    else:
        print('Screenshot didn\'t capture for Measured EVM..')
    
    
    
    return PDF



########################################################################
## For verify result verdict
########################################################################
# if len(Result) >= 3:
    #     filename = open('Logs\Result{}.txt'.format(sr_n),'w')
    #     for res in Result[:3]:
    #         for res in res:
    #             for res in res:
    #                 filename.writelines(res)
    #                 filename.writelines(', ')
    #             filename.writelines('\n')
    #         filename.writelines('\n')
    #         pass
        
    #     TC_Result = []
    #     CH_Flag = 'Pass'
    #     for Res in Result[0]:
    #         if Res[-1] == 'Fail':
    #             CH_Flag = 'Fail'
    #             break
    #         else:
    #             CH_Flag = 'Pass'
        
    #     TC_Result.append(['1', 'Base station output power', CH_Flag])
    #     ACLR_Flag = 'Pass'
    #     for Res in Result[1]:
    #         if Res[-1] == 'Fail':
    #             ACLR_Flag = 'Fail'
    #             break
    #         else:
    #             ACLR_Flag = 'Pass'
    #     TC_Result.append(['2', 'Adjacent Channel Leakage Power Ratio', ACLR_Flag])

    #     EVM_Flag = 'Pass'
    #     for Res in Result[2]:
    #         if Res[-1] == 'Fail':
    #             EVM_Flag = 'Fail'
    #             break
    #         else:
    #             EVM_Flag = 'Pass'
    #     TC_Result.append(['3', 'Modulation quality', EVM_Flag])
    #     Flag = 'Fail'
    #     if EVM_Flag == ACLR_Flag == CH_Flag == True:
    #         Flag = "Pass"

    #     TC_Result.append(['', 'Overall test verdict', Flag])
