import wave, numpy, subprocess, os

from scipy import signal



class Sync:
    
    def __init__(self, reference_beep_video, face_video ):
        self.ref_vid = reference_beep_video
        self.face_vid = face_video
        
        self.filtered_beep = self.convert_to_wavFile_and_filter(self.ref_vid)
        self.filtered_facecam = self.convert_to_wavFile_and_filter(self.face_vid)

        self.crop_file(self.filtered_beep, self.filtered_facecam, self.face_vid)
            
            #a new file is created with everything before the beep sound cropped out

#To make a synchronization effect. Take this new cropped video of the facecam, play it together with the corresponding 360 camera
#because the 360 camera is already synced with the data set. Only the facecam is out of sync.



    def convert_to_wavFile_and_filter(self, processed_video_file):
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
    

    
    
    def crop_file(self, filtered_beep, filtered_facecam, facecam_video):
        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html
        #take the cross correlation of the two audio files
        corr = signal.correlate(filtered_beep,filtered_facecam, mode = "full")


        corr_abs = abs(corr) #take absolute value of entries in 'corr' array

        max_index_abs = numpy.argmax(corr_abs) #take the index of maximum absolute value in 'corr' array
        #this is the position where the two audio files are most similar

        zero_index = len(corr)/2 - 1 #get the 0th index
        shift = zero_index - max_index_abs # distance from max_index to zero_index

        shift_in_seconds = shift/44000 # (delay in seconds = shift / sampling frequency)
        #sampling frequency given in convert_to_wavFile_and_filter -ar {sampling frequency}

        absolute_shift = round(abs(shift_in_seconds),3) #round to 3 decimals to put in ffmpeg command


        command = "del *wav" #remove all .wav files after getting array info from .wav files
        os.system(command)

        command = f"ffmpeg -y -ss {absolute_shift} -i {facecam_video} -c: copy {facecam_video}_shifted.mp4"
        #crop everything before the beeping sound out, return the cropped video file
        #-c copy :: copy the encoder of input file => do not re-encode the video, it takes alot of time
        subprocess.call(command, shell=True)
        
        self.synced_video= facecam_video+'_shifted.mp4'

    def get_synced_video(self):
        return self.synced_video

