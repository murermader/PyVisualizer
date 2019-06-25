import pyaudio  # Dieses Modul lässt uns auf das Aufnahmegerät zugreifen.
import struct  # Dieses Modul wird benötigt, um die Binärdaten des Audiostreams in Integer umzuwandeln
from scipy.fftpack import fft  # fft = fast fourier transform


def main():
    # Init
    CHUNK = 1024  # Wieviele Samples in einen stream gelesen werden.
    SAMPLE_RATE = 44100  # Die Abtastrate des Aufnahmegeräts, meist 44,1 kHz.
    FORMAT = pyaudio.paInt16  # Die Zahlen sollen als Int16 ausgelesen werden.
    CHANNELS = 1  # Unser Mikrofon nimmt in diesem Fall nur in Mono auf.

    p = pyaudio.PyAudio()
    print(p.get_default_input_device_info())  # .get("name") für nur Name

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK)
    read_stream = stream.read(num_frames=CHUNK)
    int_data = struct.unpack(str(2 * CHUNK) + 'B', read_stream)  # Konvertiert Binärdaten zu Integern (Werte von 0-255)
    int_data_half = int_data[
                    ::2]  # Jeden zweiten Wert nehmen, da jeder zweiter Wert der Audiowelle wieder zu x=0 zurückkehrt.

    # fft_data ist ein numpy ndarray der Länge CHUNK. Jedes Item der stellt eine komplexe Zahl dar.
    # fft_data ist also unser Spektrum, an dem wir auslesen können, wie laut jede Frequenz gespielt wird.
    # Diese Daten können wir benutzen, um unseren Music Visualizer anzusteuern.
    fft_data = fft(int_data_half)

    print(len(fft_data), type(fft_data), type(fft_data[0]), fft_data)
    for array_item in fft_data:
        print("Realteil: " + str(array_item.real) + " Imaginärteil: " + str(array_item.imag))


if __name__ == "__main__":
    main()
