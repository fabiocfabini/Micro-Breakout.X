from typing import Tuple, List
import serial

class NCap:
    Y_CHANN:     bytes = b'\x00'
    BTN_A_CHANN: bytes = b'\x01'
    BTN_B_CHANN: bytes = b'\x02'
    BTN_C_CHANN: bytes = b'\x03'
    BTN_D_CHANN: bytes = b'\x04'
    LED_4_CHANN:  bytes = b'\x05'
    LED_5_CHANN:  bytes = b'\x06'
    LED_6_CHANN:  bytes = b'\x07'
    LED_7_CHANN:  bytes = b'\x08'

    channels = [Y_CHANN, BTN_A_CHANN, BTN_B_CHANN, BTN_C_CHANN, BTN_D_CHANN, LED_5_CHANN, LED_5_CHANN, LED_6_CHANN, LED_7_CHANN]

    def __init__(self, port: str, baud_rate: int = 9600):
        self.conn = serial.Serial(port, baud_rate)

    def calibrate(self):
        self.write_value(self.LED_4_CHANN, b'\x01')
        self.write_value(self.LED_5_CHANN, b'\x01')
        self.write_value(self.LED_6_CHANN, b'\x01')
        self.write_value(self.LED_7_CHANN, b'\x01')

        values = []
        for _ in range(500):
            values.append(self.read_value(self.Y_CHANN)[1][0])

        self.write_value(self.LED_4_CHANN, b'\x00')
        self.write_value(self.LED_5_CHANN, b'\x00')
        self.write_value(self.LED_6_CHANN, b'\x00')
        self.write_value(self.LED_7_CHANN, b'\x00')

        return sum(values) / len(values)

    def read_meta(self, debug: bool = False):
        self.conn.write(b'\x00\x00\x01\x02\x00\x02\x01\x00')
        return self.read_stim_response(debug)

    def read_tc(self, channel: bytes, debug: bool = False):
        self.conn.write(b'\x00' + channel + b'\x01\x02\x00\x02\x03\x00')
        return self.read_stim_response(debug)

    def read_value(self, channel: bytes, debug: bool = False):
        self.conn.write(b'\x00' + channel + b'\x03\x01\x00\x01\x00')
        return self.read_stim_response(debug)

    def write_value(self, channel: bytes, value: bytes, debug: bool = False):
        self.conn.write(b'\x00' + channel + b'\x03\x02\x00\x02\x00' + value)
        return self.read_stim_response(debug)

    @staticmethod
    def display_meta(res: List[int]):
        print("META TEDS:")
        print(f"\t      Family : {res[2]}")
        print(f"\t       Class : {res[3]}")
        print(f"\t     Version : {res[4]}")
        print(f"\tTuple Lenght : {res[5]}")
        print(f"\t        UUID : {str(res[8:8+10])[1:-1]}")
        print(f"\tMax Channels : {res[-1]}")

    @staticmethod
    def display_tc(res: List[int], title: str = ""):
        print(f"TC TEDS {title}:")
        print(f"\t          Family  : {res[2]}")
        print(f"\t           Class  : {res[3]}")
        print(f"\t         Version  : {res[4]}")
        print(f"\t    Tuple Lenght  : {res[5]}")
        print(f"\t    Channel Type  : {res[8]}")
        print(f"\t    Channel Units : {str(res[11:11+10])[1:-1]}")
        print(f"\t      Channel Min : {res[23]}")
        print(f"\t      Channel Max : {res[26]}")
        print(f"\t       Data Model : {res[29]}")
        print(f"\tData Model Lenght : {res[32]}")
        print(f"\t    Data Model SB : {res[35]}")

    @staticmethod
    def display_response(res: List[int], title: str = ""):
        print(f"STIM Response: {title}")
        print(f"\tResponse : {str(res)[1:-1]}")

    def read_stim_response(self, debug: bool=False) -> Tuple[int, List[int]]:
        # Read the response from the sensor
        res_code = int.from_bytes(self.conn.read(1), byteorder='big')
        if debug: print("Error code: {}".format(res_code))

        # Read the response length
        res_len = sum([int(b) for b in self.conn.read(2)])
        if debug: print("Response length: {}".format(res_len))

        # Read the response
        res = [int(b) for b in self.conn.read(res_len)]
        if debug: print("Response: {}".format(res))

        # Return the response code and the response
        return res_code, res

if __name__ == "__main__":
    ncap = NCap('/dev/ttyACM0', baud_rate=115200)

    ncap.read_value(b'\x05', True)
