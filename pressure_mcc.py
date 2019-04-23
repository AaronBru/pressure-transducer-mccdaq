import time
import ctypes

from mcculw import ul
from mcculw.enums import ULRange, AnalogInputMode
from mcculw.enums import ScanOptions, FunctionType
from mcculw.enums import InterfaceType


class PressureError(Exception):
    pass


class PressureTransducer:

    def __init__(self, rate, ma_count):
        self.rate = rate
        self.board_num = 0
        self.count = rate
        self.ai_chan = 0
        self.ma_count = ma_count
        self.ai_range = ULRange.BIP5VOLTS
        self._prev_count = 0

        if not self._detect_device():
            raise PressureError

        self.scan_opt = ScanOptions.BACKGROUND | ScanOptions.CONTINUOUS | ScanOptions.SCALEDATA
        self.mem_handle = ul.scaled_win_buf_alloc(self.count)
        self.ctypes_arr = ctypes.cast(self.mem_handle, ctypes.POINTER(ctypes.c_double))
        if not self.mem_handle:
            raise PressureError
        ul.a_input_mode(self.board_num, AnalogInputMode.DIFFERENTIAL)

    def _detect_device(self):
        ul.ignore_instacal()
        devices = ul.get_daq_device_inventory(InterfaceType.ANY)
        if len(devices) > 0:
            device = devices[0]
            ul.create_daq_device(self.board_num, device)
            return True
        return False

    def start_acquisition(self):
        ul.a_in_scan(self.board_num, self.ai_chan, self.ai_chan, self.count, self.rate,
                     self.ai_range, self.mem_handle, self.scan_opt)
        self.get_pressure_reading()

    def get_pressure_reading(self):
        status, curr_count, curr_index = ul.get_status(self.board_num, FunctionType.AIFUNCTION)
        self._prev_count = curr_count
        if curr_index == -1:
            return None

        if (curr_index - self.ma_count) < 0:
            start_index = self.count - self.ma_count + curr_index - 1
            avg_list = self.ctypes_arr[start_index:self.count-1] + self.ctypes_arr[:curr_index]
        else:
            avg_list = self.ctypes_arr[curr_index - self.ma_count: curr_index]

        reading = sum(avg_list) / len(avg_list)
        ret_val = 1000 * reading + 11
        return ret_val

    def stop_collection(self):
        ul.stop_background(self.board_num, FunctionType.AIFUNCTION)
        if self.mem_handle:
            ul.win_buf_free(self.mem_handle)
        ul.release_daq_device(self.board_num)


def main():
    try:
        pt = PressureTransducer(10000, 100)
        pt.start_acquisition()

        while True:
            reading = pt.get_pressure_reading()

            if reading is None:
                print("Non-valid reading")
                time.sleep(0.25)
                continue
            print(reading)
            time.sleep(0.25)

    except KeyboardInterrupt:
        pass
    except PressureError:
        print("The pressure transducer could not be initialized.")
    finally:
        pt.stop_collection()


if __name__ == '__main__':
    main()

