from typing import Tuple, List
import serial

class NCap:
    X_CHANN: bytes = b'\x00'
    Y_CHANN: bytes = b'\x01'
    S_CHANN: bytes = b'\x02'
    LED6_CHANN: bytes = b'\x03'
    LED7_CHANN: bytes = b'\x04'

    def __init__(self, port: str, baud_rate: int = 9600):
        self.conn = serial.Serial(port, baud_rate)

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