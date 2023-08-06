test

校验集装箱号是否正确

'''

'''

import CRC
from CRC import  *
      
def crc16_x25_test(data):
    reg=0xffff
    cal_poly=0x1021
    for i in data:
        reg^=reverse_data(i, 16)
        for _ in range(8) :
            if reg&0x8000 :
                    reg=reg<<1
                    reg&=0xffff
                    reg^=cal_poly
            else :
                    reg=reg<<1
    reg=  reverse_data(reg, 16)            
    reg^=0xffff       
    return reg             
if __name__ == '__main__':
    data=b'\x01\x02\x03\x04\x05'
    print(len(data),data)
    crc=crc16_ccitt()
    print(crc.__class__.__name__,"%04X"%(crc.cal(data)))
    crc=crc16_ccitt_false()
    print(crc.__class__.__name__,"%04X"%(crc.cal(data)))
    crc=crc16_xmodem()
    print(crc.__class__.__name__,"%04X"%(crc.cal(data)))
    crc=crc16_x25()
    print(crc.__class__.__name__,"%04X"%(crc.cal(data)))
    crc=crc16_ibm()
    print(crc.__class__.__name__,"%04X"%(crc.cal(data)))
    crc=crc16_usb()
    print(crc.__class__.__name__,"%04X"%(crc.cal(data)))
    crc=crc16_maxim()
    print(crc.__class__.__name__,"%04X"%(crc.cal(data)))
    crc=crc16_modbus()
    print(crc.__class__.__name__,"%04X"%(crc.cal(data)))
    crc=crc16_dnp()
    print(crc.__class__.__name__,"%04X"%(crc.cal(data)))

    r=crc16_x25_test(data)
    print("crc16_x25_test","%04x"%r)
    pass