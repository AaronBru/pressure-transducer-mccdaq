# pressure-transducer-mccdaq
Simple script utilizing mccdaq and UL for Python to read from a pressure transducer.

##Requirements
1. The digital acquisition device used is the USB 1208FS found [here](https://www.mccdaq.com/usb-data-acquisition/USB-1208FS.aspx) 
from mccdaq.
2. The pressure transducer is the PX309-5KG5V, but the code can be changed to read from any transducer that outputs a voltage anywhere between 0 and 5V.
3. This software works with any Python version above 3.  Ensure it is installed on the host.

##Installation
1. Install the binaries for mccdaq and ensure Universal Library installs, found [here](https://www.mccdaq.com/Software-Downloads.aspx).
2. Install the Python bindings for mccdaq.  Open a cmd prompt and ensure pip can be run.
```bash
pip install mcculw
```
3. Referring to the manual [here](https://www.mccdaq.com/pdfs/manuals/USB-1208FS.pdf), connect ground to pins 2 and 3.  Connect the signal to pin 1.
4. The script can be run to show an example of the library usage, but to use, create an instance of the class with the sampling rate and ma_count (moving average sample count).
Then, call start_collection to start collecting samples in the background, and call get_pressure_reading to retrieve an averaged sample. Finally, call stop_collection once
all collection is complete.

##Notes
1. This was calibrated with respect to a signal generator outputting 0 up to 5V. If this is not calibrated correctly, change the values in the script.
2. The digital acquisition device will sample at a supplied rate (up to 50kHz).  The value returned from get_pressure_reading is a moving average, averaged over
a number of samples specified per instance.  For example, if sampling at 10kHz with a ma_count of 100, this will return a reading averaging 100 samples over
10 ms every time get_pressure_reading is called.
