import time
from pinpong.board import gboard,I2C
import math

class BMI160():
    Acc                                 = 0
    Step                                = 1
    BMI160_I2C_INTF                     = 0

    BMI160_OK                           = 0
    BMI160_E_NULL_PTR                   = -1
    BMI160_E_COM_FAIL                   = -2
    BMI160_E_DEV_NOT_FOUND              = -3
    BMI160_E_OUT_OF_RANGE               = -4
    BMI160_E_INVALID_INPUT              = -5
    BMI160_E_ACCEL_ODR_BW_INVALID       = -6
    BMI160_E_GYRO_ODR_BW_INVALID        = -7
    BMI160_E_LWP_PRE_FLTR_INT_INVALID   = -8
    BMI160_E_LWP_PRE_FLTR_INVALID       = -9
    BMI160_E_AUX_NOT_FOUND              = -10
    BMI160_FOC_FAILURE                  = -11
    BMI160_ERR_CHOOSE                   = -12

    BMI160_CHIP_ID_ADDR                 = 0x00
    BMI160_CHIP_ID                      = 0xD1

    def __init__(self, board = None, i2c_addr = 0x69, bus_num=0):
        if isinstance(board, int):
            i2c_addr = board
            board = gboard
        elif board == None:
            board = gboard
        self.i2c_addr = i2c_addr
        self._i2c = I2C(bus_num)

    def begin(self, type, addr):
        self.i2c_init(addr)

    def i2c_init(self, i2c_addr):
        self.i2c_addr = i2c_addr
        self.interface = self.BMI160_I2C_INTF
        return self.i2c_init2()
    
    def i2c_init2(self):
        rslt = self.BMI160_OK
        chip_id = 0
        data = 0
        if rslt == self.BMI160_OK:
            chip_id = self.get_regs(self.BMI160_CHIP_ID_ADDR, 1)
            print(chip_id)
            while True:pass

    def get_regs(self, reg, lens):
        data = self._i2c.readfrom_mem(self.i2c_addr, reg, len)
        return data

    def write16_reg(self, reg, value):
        data = [value >> 8, value]
        self._i2c.writeto_mem(self.i2c_addr, reg, data)
         
    def read16_reg(self, reg, len = 2):
        data = self._i2c.readfrom_mem(self.i2c_addr, reg, len)
        return data[0] << 8 | data[1]
