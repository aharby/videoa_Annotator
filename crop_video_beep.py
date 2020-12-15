import wave, numpy, subprocess, os

from scipy import signal





def convert_video_to_wavFile(processed_video_file):
    #http://ffmpeg.org/ffmpeg.html
    #ffmpeg install guide: https://www.youtube.com/watch?v=r1AtmY-RMyQ 2:33 minute onwards
    command = f"ffmpeg -y -i {processed_video_file} -ac 2 -ar 44100 -vn {processed_video_file}_waveform.wav" #generate .wav file from video file
    #-y :: answer yes / -n :: answer no. Answer 'yes' to confirm for overwrite
    #-i :: input file
    #-ac :: number of audio channels
    #-ar :: audio sampling frequency
    #-vn :: blocks all video streams
    subprocess.call(command, shell=True)

    #https://stackoverflow.com/questions/16778878/python-write-a-wav-file-into-numpy-float-array/16779030
    #line 23 to 35 :: answer by user "Matthew Walker" (https://stackoverflow.com/users/562930/matthew-walker)

    #read file to get buffer                                                                                               
    inputfile = wave.open(f"{processed_video_file}_waveform.wav")
    #inputfile_01 = wave.open(f"{reference_sound}")
    samples = inputfile.getnframes()
    audio = inputfile.readframes(samples) #convert .wav files into readable integers

    #convert buffer to float32 using numpy                                                                                 
    audio_as_np_int16 = numpy.frombuffer(audio, dtype=numpy.int16)
    audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)

    #normalise float32 array so that values are between -1 and +1                                             
    max_int16 = 2**15
    audio_normalised = audio_as_np_float32 / max_int16

    #use filter of choice. This case uses Butterworth Filter.
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
    sos = signal.butter(10, [2500,4600], 'bp',fs=samples*0.5 , output='sos') #bandpass filter between 2.5 & 4.6 Hkz
    #use sosfiltfilt because second-order-sections is recommended in the instruction manual:
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html#scipy.signal.filtfilt
    audio_filtered = signal.sosfiltfilt(sos, audio_normalised)

    return audio_filtered


video_file_01 = input("Please type in directory of reference beep file (including . extension)\n")
#video_file_01 = "reference_gopro_beep_02.mp4"
audio_normalised_01 = convert_video_to_wavFile(video_file_01)

video_file_02 = input("Please type in directory of video to crop (including . extension)\n")
#video_file_02 = "GOPR0279_0_to_60s.MP4"
audio_normalised_02 = convert_video_to_wavFile(video_file_02)

#https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html
#take the cross correlation of the two audio files
corr = signal.correlate(audio_normalised_01,audio_normalised_02, mode = "full")


corr_abs = abs(corr) #take absolute value of entries in 'corr' array

max_index_abs = numpy.argmax(corr_abs) #take the index of maximum absolute value in 'corr' array
#this is the position where the two audio files are most similar

zero_index = len(corr)/2 - 1 #get the 0th index
shift = zero_index - max_index_abs # distance from max_index to zero_index

shift_in_seconds = shift/44000 # (delay in seconds = shift / sampling frequency)
#sampling frequency given in convert_video_to_wavFile -ac {sampling frequency}

absolute_shift = round(abs(shift_in_seconds),3) #round to 3 decimals to put in ffmpeg command


command = "del *wav" #remove all .wav files after getting array info from .wav files
os.system(command)

command = f"ffmpeg -y -ss {absolute_shift} -i {video_file_02} -c: copy {video_file_02}_shifted.mp4"
#crop everything before the beeping sound out, return the cropped video file
#-c copy :: copy the encoder of input file => do not re-encode the video, it takes alot of time
subprocess.call(command, shell=True)


###########prints below are for debugging purposes################

print(corr.size) #size of cross correlation array

print(max_index_abs)
# max absolute value of cross correlation array
# index of max value. This is the position where the two audio files are most similar
print(shift) # distance from max_index to zero_index

print(shift_in_seconds) # (delay in seconds = shift / sampling frequency)

print(absolute_shift)