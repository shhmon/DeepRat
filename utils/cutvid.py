from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

start = 9
end = 23
cams = ['A', 'B', 'C', 'D']

for cam in cams:
	ffmpeg_extract_subclip(f'calibration_cam-{cam}.mkv', start, end, targetname=f'calibration_cam-{cam}X.mkv')