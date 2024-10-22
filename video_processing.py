from moviepy.editor import AudioFileClip, VideoFileClip

def replace_audio_in_video(video_file, new_audio_file):
    video = VideoFileClip(video_file)
    new_audio = AudioFileClip(new_audio_file)
    
    video_with_new_audio = video.set_audio(new_audio)
    output_video_file = "output_video.mp4"
    video_with_new_audio.write_videofile(output_video_file, codec="libx264", audio_codec="aac")
    
    return output_video_file
