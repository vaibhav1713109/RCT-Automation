from functools import reduce
import os
from fpdf import FPDF
directory_path = os.path.dirname(os.path.abspath(__file__))

class PDF(FPDF):
    def header(self):
        # Logo
        self.image(r'{}/vvdn_logo.png'.format(directory_path), 10, 8, 33)
        self.set_text_color(44, 112, 232)
        self.set_font('Arial', 'B', 15)
        # self.set_x(-45)
        # self.set_font('Times', 'B', 12)
        # self.cell(10,10, 'ACLR & POWER', 0, 0, 'C')
        self.set_text_color(0,0,0)
        self.ln(20)

    # Page footer
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(0,0,0)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'L')
        self.set_text_color(44, 112, 232)
        self.set_font('Arial', 'B', 8)
        self.cell(0, 10, 'Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd', 0, 0, 'R')
        self.cell(0,10)
        self.set_text_color(0,0,0)

################# Table Heading ################
def HEADING(PDF,data):
    print('='*100)
    print(data)
    print('='*100)
    PDF.set_font("Times",style = 'BU', size=20)
    PDF.ln(5)
    PDF.set_text_color(112, 112, 112)
    PDF.multi_cell(w=PDF.epw,txt=data,border=0,align='C')
    PDF.set_text_color(0,0,0)
    PDF.ln(5)
    PDF.set_font("Times",style = '',size=12)
    pass


################# Add Front Page ################
def PDF_CAP():
    pdf = PDF()
    pdf.add_page(format=(350,250))
    pdf.set_font("Times", size=9)
    y = int(pdf.epw)
    pdf.image(name=r'{}/Front_Page.png'.format(directory_path), x = None, y = None, w = y, h = 0, type = '', link = '')
    # pdf.ln(50)
    # pdf.set_font("Times",style = 'B', size=15)
    # pdf.multi_cell(w =y,txt='BASE TEST CASE',border=1,align='C')
    pdf.set_font("Times",style = '',size = 9)
    return pdf

def Test_HEADING(PDF,data,*args):
    li = data.split('\n')
    print('-'*100)
    print(data)
    print('-'*100)
    PDF.set_font("Times",style = 'B', size=11)
    PDF.write(5,li[0])
    PDF.ln(6)
    PDF.set_font("Times",style = '',size = 11)
    PDF.write(5,li[1])
    PDF.ln(10)

def render_header(PDF,TABLE_Header,line_height,col_width):
    PDF.set_font("Times",style="B")  # enabling bold text
    for col_name in TABLE_Header:
        m_l_h = PDF.font_size
        PDF.multi_cell(w=col_width, h = line_height, txt = col_name, border=1,
                new_x="RIGHT", new_y="TOP", max_line_height=PDF.font_size,align='C')
    PDF.ln(line_height)
    PDF.set_font(style="")  # disabling bold text

def render_table_data(PDF,TABLE_DATA,line_height,col_width,TABLE_Header):  # repeat data rows
    for row in TABLE_DATA:
        if PDF.will_page_break(line_height):
            render_header(PDF,TABLE_Header,line_height,col_width)
        for datum in row:
            if datum == 'Pass':
                PDF.set_fill_color(105, 224, 113)
            elif datum =='Fail':
                PDF.set_fill_color(235, 52, 52)
            else:
                PDF.set_fill_color(255,255,255)
            PDF.multi_cell(w=col_width, h = line_height, txt = datum, border=1,
                new_x="RIGHT", new_y="TOP", max_line_height=PDF.font_size,align='C',fill=True)
        PDF.ln(line_height)



def add_image(PDF,Images):
    y = int(PDF.epw)
    i = 0
    PDF.add_page(format=(350,250))
    for image in range(len(Images)):
        # if i < len(Images)-1 and i%2 ==0 :
        #     Images[image], Images[image+1] = Images[image+1], Images[image]
        # print(Images)
        if image%2 != 0:
            # PDF.ln()
            PDF.set_y(30)
            PDF.set_font("Times",style = 'B', size=15)
            PDF.multi_cell(w=PDF.epw,txt='Channel {}'.format(Images[image]),border=0,align='C')
            if Images[image] < len(Images)//2:
                PDF.add_page(format=(350,250)) 
            PDF.set_font("Times",style = '', size=11) 
        else:
            PDF.image(Images[image], 20, 40, 300)
            PDF.ln()
            
        
    PDF.set_font("Times",style = '',size = 9)
    pass