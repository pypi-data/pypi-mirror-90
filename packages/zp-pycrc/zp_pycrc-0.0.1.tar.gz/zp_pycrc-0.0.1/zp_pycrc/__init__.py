'''

'''
name='zp_pyCRC'
def reverse_data(data,bits=16):
    reverse_table=[0x0,0x8,0x4,0xc,
                   0x2,0xa,0x6,0xe,
                   0x1,0x9,0x5,0xd,
                   0x3,0xb,0x7,0xf]
    if bits==16 :
        data&=0xffff
        return (reverse_table[data&0xf]<<12)+(reverse_table[(data&0xf0)>>4]<<8)+(reverse_table[(data&0xf00)>>8]<<4)+(reverse_table[(data&0xf000)>>12])
    if bits==8:
        data&=0xff
        return (reverse_table[data&0xf]<<4)+(reverse_table[(data&0xf0)>>4])
    
def make_crc_table(poly,reverse_input=False):
    table=[]
    if reverse_input:
        cal_poly=reverse_data(poly) 
        for i in range(256):
            reg=i
            for _ in range(8):
                if reg&0x1 :
                    reg=reg>>1
                    reg^=cal_poly
                else :
                    reg=reg>>1
            table.append(reg)     
    else:
        cal_poly=poly
        for i in range(256):
            reg=(i<<8)
            for _ in range(8):
                if reg&0x8000 :
                    reg=reg<<1
                    reg&=0xffff
                    reg^=cal_poly
                else :
                    reg=reg<<1
            table.append(reg)    
    return table
def cal_crc(data,reg,table,reverse_input,reverse_output):
        if reverse_input:
            for a in data :
                reg=(reg>>8)^table[(reg^a)&0xff]    
        else :
            for a in data :
                reg=((reg&0xff)<<8)^table[((reg>>8)^a)&0xff]   
                
        if reverse_output != reverse_input :
            reg=reverse_data(reg, 16)      
        return reg
class crc16(object):
    def __init__(self,init_reg,poly,reverse_input,reverse_output,xorout_reg):
        self.init_reg=init_reg
        self.xorout_reg=xorout_reg
        self.poly=poly
        self.reverse_input=reverse_input
        self.reverse_output=reverse_output
        self.crc_table=make_crc_table(self.poly,self.reverse_input)
        pass
    def cal(self,data):
        reg=self.init_reg
        reg=cal_crc(data, reg, self.crc_table, self.reverse_input,self.reverse_output)
        reg^=self.xorout_reg
        return reg
    
class crc16_ccitt(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x1021, True,True, 0x0000)
        
class crc16_ccitt_false(crc16):
    def __init__(self):
        crc16.__init__(self, 0xffff,  0x1021, False,False, 0x0000)

class crc16_xmodem(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x1021, False,False, 0x0000)

class crc16_x25(crc16):
    def __init__(self):
        crc16.__init__(self, 0xffff,  0x1021, True,True, 0xffff)  
        
class crc16_ibm(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x8005, True,True, 0x0000) 
        
class crc16_usb(crc16):
    def __init__(self):
        crc16.__init__(self, 0xffff,  0x8005, True,True, 0xffff)
        
class crc16_maxim(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x8005, True,True, 0xffff)
                        
class crc16_modbus(crc16):
    def __init__(self):
        crc16.__init__(self, 0xffff,  0x8005, True,True, 0x0000)

class crc16_dnp(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x3d65, True,True, 0xffff)
              
