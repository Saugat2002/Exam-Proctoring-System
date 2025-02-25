from pydub import AudioSegment
import os
import subprocess
# import ffmpeg

def resample(input_path, output_path):
    """
    Resample audio to 16kHz and export as WAV.
    
    Args:
    input_path (str): Path to the input audio file.
    output_path (str): Path to save the resampled audio file.
    
    Returns:
    None
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")
    
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(output_path, format="wav")
    print(f"Resampled {input_path} to {output_path} at 16 kHz.")

# def extract_audio(input_video_path, output_audio_path):
#     print("Input video path: ", input_video_path)
#     print("Output audio path: ", output_audio_path)
#     try:
#         # Input video
#         stream = ffmpeg.input(input_video_path)
        
#         # Extract audio
#         audio = stream.audio
        
#         # Set audio codec and parameters
#         output = ffmpeg.output(audio, output_audio_path,
#                                acodec='pcm_s16le',
#                                ar=16000,
#                                ac=1)
        
#         # Run FFmpeg command
#         ffmpeg.run(output, overwrite_output=True)

        
#         print(f"Audio extracted successfully: {output_audio_path}")
#     except ffmpeg.Error as e:
#         print(f"An error occurred: {e.stderr.decode()}")


def extract_wav_from_mp4(input_video_path, output_audio_path):
    """
    Extracts 16kHz mono WAV audio from an MP4 video using FFmpeg.
    
    Args:
        input_video_path (str): Path to the input MP4 video file.
        output_audio_path (str): Path to save the extracted WAV audio file.
        
    Returns:
        bool: True if the extraction was successful, False otherwise.
    """
    if not os.path.isfile(input_video_path):
        raise FileNotFoundError(f"The file {input_video_path} does not exist.")
    
    if not output_audio_path.endswith('.wav'):
        raise ValueError("Output file must have a .wav extension")
    
    # extract_audio(input_video_path, output_audio_path)
    print(f"Audio extracted successfully and saved to {output_audio_path}")
    
    command = [
        'ffmpeg',
        '-i', input_video_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        output_audio_path,
        '-y'
    ]
    
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return False

# Example usage:
# extract_wav_from_mp4('cheating_detector/audio/data/video/test_video.mp4', 'cheating_detector/audio/data/audio_files/output_audio.wav')
# resample('input_audio.mp3', 'output_audio_resampled.wav')
