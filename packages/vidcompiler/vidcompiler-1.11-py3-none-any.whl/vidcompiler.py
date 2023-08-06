
import ffmpeg_wrapper
from ffmpeg_wrapper import Media,changemd5
import shutil,tempfile,os

def replace_sound(video_file, audio_file, start_time, is_revert):
    media = Media(video_file)
    rs=media.replace_sound(audio_file, start_time, is_revert)
    tmp_folder = tempfile.gettempdir()
    new_rs=os.path.join(tmp_folder,os.path.basename(rs))
    shutil.move(rs,new_rs)
    changemd5(new_rs)
    media.cleanup()
    return new_rs
def cut_video(video_file,begin,duration):
    media = Media(video_file)
    rs = media.cut_video(begin, duration)
    tmp_folder = tempfile.gettempdir()
    new_rs = os.path.join(tmp_folder, os.path.basename(rs))
    shutil.move(rs, new_rs)
    changemd5(new_rs)
    media.cleanup()
    return new_rs
