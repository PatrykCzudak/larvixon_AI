from moviepy.editor import VideoFileClip, clips_array


def cut_video(input_video_path="GP032995.MP4"):
    
    output_video_left_path = "GP032995_1.MP4"
    output_video_right_path = "GP032995_2.MP4"

    video = VideoFileClip(input_video_path)

    width, height = video.size

    video_left = video.crop(x1=0, y1=0, x2=width, y2=height//2)
    video_right = video.crop(x1=0, y1=height//2, x2=width, y2=height)

    video_left.write_videofile(output_video_left_path, codec='libx264')
    video_right.write_videofile(output_video_right_path, codec='libx264')