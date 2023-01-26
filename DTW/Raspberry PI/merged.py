import array
import struct
import os
import wave 

def read_loaded_file(audio_path):
    # we are to open the .wav file
    wav_file = wave.open(audio_path, "rb")

    # read audio samples from the audio file
    audio_sample = wav_file.readframes(wav_file.getnframes())
    wav_file.close()

    # convert audio samples into an array
    audio_sample = array.array("h", audio_sample)
    return audio_sample

#------------------------------------------------------------------------------#
audio_sample = read_loaded_file("isigi_ac.wav")

# control measure
if audio_sample is None:
    exit()

# set quantized level - 16 is best 
quantization_level = 16

# quantize the audio sample
quant_audio = audio_sample

for aud in range(len(quant_audio)):
    quant_audio[aud] = int(quant_audio[aud]/(2**15/quantization_level) * (2**15/quantization_level))

encoded_sample = struct.pack("h"*len(quant_audio), *quant_audio)                                          

#encoded_sample = struct.pack("h"*len(quantized_sample), *quantized_sample)

# send encoded audio input to PWM output

import pigpio # initialize pigpio

pi = pigpio.pi()

pwm_pin = 13 # set the pwm output pin 12, 13, 19, 18 etc

pwm_freq = 44000 # ensure the PWM freq matches sample frequency

# start PWM on the pin
pi.set_mode(pwm_pin, pigpio.OUTPUT)
pi.hardware_PWM(pwm_pin, pwm_freq, 0)

# send the encoded audio sample to the PWM output
pi.hardware_PWM(pwm_pin, pwm_freq, int(encoded_sample))


from scipy.fft import fft
# fft to perform a fast fourier on the encoded audio sample
import numpy as np 

# fourirer transform the encoded output
fourirer_trans = fft(encoded_sample)
abs_fourier_trans = fft(encoded_sample)

# extract the fourier_trans values and save as a csv file
np.savetxt("extracted_values.csv", fourirer_trans, delimiter=",")
np.savetxt("extracted_abs_values.csv",abs_fourier_trans,delimiter=",") # get the absolute values also


