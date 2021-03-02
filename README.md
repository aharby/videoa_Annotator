# videoa-Annotator
IP_22_Team

For successful operation a user needs:

1. FFMPEG library.
see:http://ffmpeg.org/ffmpeg.html

    ffmpeg install guide: https://www.youtube.com/watch?v=r1AtmY-RMyQ 2:33 minute onwards.

2. Make sure Numpy 1.19.5 or earlier is installed. (For Windows only)


All the needed libraries are already included in the virtual environment attached with the source code.
-------------------------------------------------
Main libraries:
1. Numpy
2. pandas
3. PyQt5
4. scipy
-------------------------------------------------
Operation:
1. Load the Videos and the beep reference from file tab.
2. Load the dataset and the annotation set (AA.csv) from file tab.(please use only csv files with semicolon separator)
3. Press Sync.
4. to add a parameter press add on the left side and type in the parameter name as typed in the dataset (MUST).
5. To graph a parameter over the total length of the dataset press graph button next to the parameter.
6. To annotate, press start button at the desired time stamp, then stop button at the end timestamp, the videos will pause and a new field for the annotation is created.
7. Important: entry field in the annotation must not be empty before saving the project.
-------------------------------------------------

Good luck
