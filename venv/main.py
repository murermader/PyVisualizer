import pyaudio  # Dieses Modul lässt uns auf das Aufnahmegerät zugreifen.
import struct  # Dieses Modul wird benötigt, um die Binärdaten des Audiostreams in Integer umzuwandeln
import numpy as np  # numpy
import matplotlib.pyplot as plt
import sys
from scipy.fftpack import fft  # fft = fast fourier transform


def main():
    chunk = 4096
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()
    p.input_device_index = 7
    stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, output=True, frames_per_buffer=chunk)

    x = np.arange(0, 2 * chunk, 2)
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_ylim(0, 255)
    ax.set_xlim(0, chunk)
    line, = ax.plot(x, np.random.rand(chunk))

    try:
        while True:
            data = stream.read(chunk)
            data_int = np.array(struct.unpack(str(2 * chunk) + 'B', data), dtype='b')[::2] + 128
            line.set_ydata(data_int)
            fig.canvas.draw()
            fig.canvas.flush_events()
    except KeyboardInterrupt:
        print("Das Beenden funktioniert irgendwie noch nicht....")
        sys.exit(0)


if __name__ == "__main__":
    main()
