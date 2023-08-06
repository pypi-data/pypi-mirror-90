import subprocess
import math
import os
import time
import sys
import tempfile
import shutil
import uuid
import utils
import random
def find_name(file):
    """
    This function returns the name of the file without an extension
    It accepts one input:
        -> file: string (travis_scott.mp3)

    Returns a string | Ex: 'travis_scott'
    """
    for index in range(len(file)):
        if file[::-1][index] == '.':
            index += 1
            break
    return file[:-index]
def changemd5(file):
    with open(file,'a') as wb:
        wb.write(f"\r\n{uuid.uuid4()}")
def file_types(filename):
    '''
    This function checks for the file type by looping over filename
    in reverse and returning the text of everything behind the "."

    Returns a string value indicating file type (Ex: 'wav', 'mp3')
    and a string value indicating file name (Ex: 'travis_scott', 'harry_styles')
    '''

    for index in range(len(filename)):
        if filename[::-1][index] == '.':
            break
    return filename[-index:], filename[:-index-1]


def add_music(video_file, music_file):
    """
    This function combines video and audio using FFMPEG
    It accepts two inputs:
        -> video_file: string ('video.mp4')
        -> music_file: string ('music.mp3')
    """
    output_file = find_name(music_file) + 'final.mp4'
    cmd = f'ffmpeg -y -i "{video_file}" -i "{music_file}" -c copy -map 0:v:0 -map 1:a:0 "{output_file}"'
    subprocess.call(cmd, shell=True)

def convert_time(time):
    """
    This function converts time in a form of integers to a hh:mm:ss format
    Returns an array | Ex: 01:32:34
    """
    time_list = [60*60,60,1]
    output_list = []

    for i in time_list:
        amount, remainder = divmod(time, i)
        if len(str(amount)) < 2:
            output_list.append(f'0{str(amount)}')
        else:
            output_list.append(str(amount))
        time = remainder
    return ':'.join(output_list)

def concatenate_clips(media_list, root_folder = None):
    """
    This function concatentates a list of media files into one singular clip
    It accepts two inputs:
        -> media_list: array (['travis_scott.mp4', 'post_malone.mp4'])
        -> output_name: string ('output.mp4')
    """
    if len(media_list) == 1:
        return media_list[0]
    if not root_folder:
        root_folder=tempfile.TemporaryDirectory().name
    f_name = os.path.join(root_folder, f'{uuid.uuid4()}-list.txt')
    f = open(f_name, 'w')
    ex = "mp4"
    arr_tmp=[]
    for media in media_list:
        ex = os.path.splitext(media)[1]
        tmp_ts=convert2("ts", media, root_folder)
        f.write(f"file '{tmp_ts}'\n")
        arr_tmp.append(tmp_ts)
    f.close()
    output_name = os.path.join(root_folder, f"{uuid.uuid4()}.ts")
    cmd = f'ffmpeg -y -f concat -safe 0 -i "{f_name}" -c copy "{output_name}"'
    print(cmd)
    subprocess.call(cmd, shell=True)
    for item in arr_tmp:
        os.remove(item)
    os.remove(f_name)
    return output_name
def concatenate_clips_ori(media_list, is_delete=False, root_folder = None):
    """
    This function concatentates a list of media files into one singular clip
    It accepts two inputs:
        -> media_list: array (['travis_scott.mp4', 'post_malone.mp4'])
        -> output_name: string ('output.mp4')
    """
    if len(media_list) == 1:
        return media_list[0]
    if not root_folder:
        root_folder=tempfile.TemporaryDirectory().name
    f_name = os.path.join(root_folder, f'{uuid.uuid4()}-list.txt')
    f = open(f_name, 'w')
    ex = ".mp4"
    arr_tmp=[]
    for media in media_list:
        ex = os.path.splitext(media)[1]
        f.write(f"file '{media}'\n")
        arr_tmp.append(media)
    f.close()
    output_name = os.path.join(root_folder, f"{uuid.uuid4()}{ex}")
    cmd = f'ffmpeg -y -f concat -safe 0 -i "{f_name}" -c copy "{output_name}"'
    print(cmd)
    subprocess.call(cmd,shell=True)
    if is_delete:
        for item in arr_tmp:
            os.remove(item)
    os.remove(f_name)
    return output_name
def overlay(video, image):
    """
    The script uses FFMPEG to overlay an image over a video. It accepts two inputs.
            -> video: string (location of video)
            -> image: string (location of string)

    Example outputs:
            -> Overlay a snow animation over village
            -> Overlay a rain animation over city
    """
    cmd = f'ffmpeg -y -i "{image}" -i "{video}" -filter_complex [1:v]colorkey=0x000000:0.5:0.5[ckout];[0:v][ckout]overlay[out] -map [out] -c:a copy -c:v libx264 "{"_temp" + video}"'
    subprocess.call(cmd, shell=True)
    return "_temp" + video

def clean_file(string):
    """
    This function cleans out unnecessary characters from subprocess.Popen() outputs.
    If an output is a numerical value, it will round it down and return same else
    it will return the string value
    """
    keep_list = [str(num) for num in range(0,10)] + ['.','x']
    for char in string:
        if char not in keep_list:
            string = string.replace(char, "")
    try:
        return math.floor(float(string))
    except:
        return string
def get_duration(file_target):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file_target}'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    return clean_file(str(output))

def convert2(ext,input_file,root_folder):
    file_rs=os.path.join(root_folder,f"{uuid.uuid4()}.{ext}")
    cmd=f'ffmpeg -loglevel panic -fflags +genpts -i "{input_file}" -c copy -bsf:v h264_mp4toannexb -f mpegts "{file_rs}"'
    subprocess.call(cmd, shell=True)
    return file_rs
class Media:
    def __init__(self, media_file, root_folder=None):
        self.ori_folder,self.ori_file= os.path.split(media_file)
        if not root_folder:
            self.root_dir = tempfile.TemporaryDirectory()
            self.root_folder = self.root_dir.name
        else:
            self.root_folder=root_folder
        self.ori_file=f'{uuid.uuid4()}.mp4'
        self.file = os.path.join(self.root_folder, self.ori_file)
        if os.path.splitext(media_file)[1] == ".mp4":
            shutil.copy(media_file, self.file)
        else:
            cmd=f'ffmpeg -y -i "{media_file}" -c copy "{self.file}"'
            subprocess.call(cmd, shell=True)
    def __str__(self):
        return self.file
    def inject(self, start_time, video_file):
        splice_root_folder, arr_spilce=self.splice(0, start_time)
        shutil.copy(video_file,os.path.join(splice_root_folder, os.path.basename(video_file)))
        arr_spilce.insert(1, os.path.join(splice_root_folder, os.path.basename(video_file)))
        return concatenate_clips(arr_spilce, self.root_folder)
    def replace_sound(self, audio_file, start_time="start,mid,end",is_revert=False):
        audio_len=get_duration(audio_file)
        vid_len=self.duration()
        if audio_len > vid_len:
            start_time=0
        elif not start_time.isdigit():
            if start_time=="start":
                start_time=0
            if start_time=="mid":
                start_time=int(random.randint(int(vid_len/2), int(vid_len*2/3)))
                if start_time+audio_len > vid_len:
                    start_time=vid_len-audio_len
            if start_time=="end":
                start_time = vid_len - audio_len
        else:
            start_time=int(start_time)
            if is_revert:
                start_time=vid_len-start_time-audio_len
            if start_time<0:
                start_time=0
            #number
        
        if start_time ==0:
            print("replace all")
            file_rs = os.path.join(self.root_folder, f"{uuid.uuid4()}-tmp-replace.avi")
            cmd = f'ffmpeg -i "{self.file}" -i "{audio_file}" -map 0:v -map 1:a -c copy -shortest "{file_rs}"'
            subprocess.call(cmd, shell=True)
        else:
            splice_root_folder, arr_spilce=self.splice(0,start_time)
            video_tmp = arr_spilce[1]
            media_tmp= Media(video_tmp)
            folder_tmp1, arr_spilce_tmp1 = media_tmp.splice(0,audio_len)
            tmp_file_replace=os.path.join(self.root_folder,f"{uuid.uuid4()}-tmp-replace.avi")
            cmd=f'ffmpeg -i "{arr_spilce_tmp1[0]}" -i "{audio_file}" -map 0:v -map 1:a -c copy -shortest "{tmp_file_replace}"'
            subprocess.call(cmd, shell=True)
            arr_spilce_tmp1[0] = tmp_file_replace
            part1_replace = concatenate_clips(arr_spilce_tmp1, self.root_folder)
            arr_spilce[1] = part1_replace
            media_tmp.cleanup()
            file_rs = concatenate_clips(arr_spilce,self.root_folder)
        return file_rs




    def cut_video(self, begin="end-10",duration=5):
        vid_len = self.duration()
        if begin.isdigit():
            start_time=int(begin)
        else:
            if "end" in begin:
                start_time=vid_len-int(begin.replace("end-",""))-duration
        if start_time < 0:
            start_time = 0
        arr_save=[]
        file_tmp=self.file
        if start_time > 0 :
            arr_tmp = self.split(start_time)
            arr_save.append(arr_tmp[0])
            file_tmp=arr_tmp[1]
        media_tmp=Media(file_tmp)
        arr_tmp=media_tmp.split(duration)
        if len(arr_tmp) > 1:
            arr_save.append(arr_tmp[1])
        rs_vid = concatenate_clips_ori(arr_save,True,self.root_folder)
        last_file = os.path.join(self.root_folder, f"{uuid.uuid4()}-cut-done"+os.path.basename(rs_vid))
        shutil.move(rs_vid,last_file)
        media_tmp.cleanup()
        return last_file
    def cleanup(self):
        self.root_dir.cleanup()

    def duration(self, file_target=None):
        """
        This function uses FFMPEG to parse through a video/music file and returns the duration of the file
        into Python using subprocess.Popen()

        It then calls function clean_file to convert the output into an integer that represents seconds
        Returns an integer | Ex: 251
        """
        if not file_target:
            file_target=self.file
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file_target}'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = proc.communicate()[0]

        return clean_file(str(output))

    def size(self):
        """
        This function uses FFMPEG to parse through an image/video file and returns the size (width & height) of the file
        into Python using subprocess.Popen()

        It then calls function clean_file to convert the output into integers representing width & height.
        Returns an array of two integers | Ex: [720,320]
        """
        cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=height,width -of csv=s=x:p=0 {self.file}'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = proc.communicate()[0]

        size =  clean_file(str(output))
        dimension_list = size.split('x')

        return [int(num) for num in dimension_list]

    def set_size(self, size_list):
        """
        This function uses FFMPEG to set the dimensions of a video/file according to the user's preferences.
        It accepts an array [width,  height] and uses those dimensions to resize the file
        It outputs '_temp' + self.file and points self.file to the newly generated file
        """
        width = size_list[0]
        height = size_list[1]
        cmd = f'ffmpeg -y -i "{self.file}" -s {width}x{height} -c:a copy "{"_temp" + self.file}"'
        subprocess.call(cmd, shell=True)

        self.file = f'_temp{self.file}'

    def subclip(self, start_time, end_time, target_name=None):
        """
        This function uses FFMPEG to create a "subclip" out of the original video clip
        It accepts three inputs:
                -> start_time: int
                -> end_time: int
                -> target_name: string
        The script uses function convert_time to convert numerical integers into the hh/mm/ss string format
        It then uses the output to cut the correct segment out of the original video
        """
        duration = end_time - start_time
        start_time = convert_time(start_time)
        time = convert_time(end_time)

        if target_name:
            cmd = f'ffmpeg -y -ss {start_time} -i "{self.file}" -t {time} -map 0 -vcodec copy -acodec copy "{target_name}"'
            subprocess.call(cmd, shell=True)
            self.file = target_name
        else:
            cmd = f'ffmpeg -y -ss {start_time} -i "{self.file}" -t {time} -map 0 -vcodec copy -acodec copy "{"_temp" + self.file}"'
            subprocess.call(cmd, shell=True)
            self.file = '_temp' + self.file

    def splice(self, start_time, duration):
        start_time = convert_time(start_time)
        uuid.uuid4()
        folder_tmp=f"splice-{uuid.uuid4()}"
        folder_tmp=os.path.join(self.root_folder,folder_tmp)
        os.makedirs(folder_tmp)
        file_rs=f'_temp_%5d_{self.ori_file}'
        file_rs=os.path.join(folder_tmp,file_rs)
        cmd = f'ffmpeg -loglevel panic -ss {start_time} -i "{self.file}" -vcodec copy -acodec copy -f segment -segment_time {duration} -reset_timestamps 1 -y "{file_rs}"'
        print(cmd)
        subprocess.call(cmd, shell=True)
        splice_list = utils.files_in_folder(folder_tmp)
        return folder_tmp, splice_list
    def split(self,sptime):
        folder_tmp, splice_list = self.splice(0,sptime)
        if len(splice_list) < 3:
            return splice_list
        arrRs=[]
        arrRs.append(splice_list.pop(0))
        arrRs.append( concatenate_clips_ori(splice_list,True,self.root_folder))
        return arrRs


    def set_duration(self, duration, target_name=None):
        """
        This function uses FFMPEG to create a new video that adheres to the time duration set by the user
        It accepts two inputs
                -> duration: int
                -> target_name: string
        It uses the convert_time function to convert numerical integers into the hh/mm/ss string format
        It then uses that output to cut the correct segment out of the end of the original video
        """
        start_time = convert_time(0)
        time = convert_time(duration)

        if target_name:
            cmd = f'ffmpeg -y -ss {start_time} -i "{self.file}" -t {time} -map 0 -vcodec copy -acodec copy "{target_name}"'
            subprocess.call(cmd, shell=True)
            self.file = target_name
        else:
            cmd = f'ffmpeg -y -ss {start_time} -i "{self.file}" -t {time} -map 0 -vcodec copy -acodec copy "{"_temp" + self.file}"'
            subprocess.call(cmd, shell=True)
            self.file = '_temp' + self.file

    def loop(self, target_duration):
        """
        This function uses FFMPEG to loop the original user video until it meets the duration set by the user
        It accepts one input:
                -> target_duration: int

        The script divides target_duration with the duration of the video and rounds the number up, arriving at the amount
        of times the video has to "repeat" in order for the combined duration to be at or greater than the target_duration

        Then, using command line arguments, the script will copy the original video "repeat" amount of times and adds the names
        of the copied videos into a text file. That text file is then fed into a FFMPEG command which will then concatenate all the videos
        listed within the file into a singular video
        """
        curr = self.duration()

        if target_duration > curr:
            repeat = math.ceil(target_duration/curr)
            f = open('list.txt','w')
            for i in range(repeat):
                extension, name = file_types(self.file)
                f.write(f"file '{name}{i}.{extension}'\n")
            f.close()

            cmd = f'ffmpeg -y -f concat -safe 0 -i list.txt -c copy {"_temp" + self.file}'
            subprocess.call(cmd, shell=True)
            self.file = '_temp' + self.file

            #cleaning copied files
            os.remove('list.txt')

        self.set_duration(target_duration)

    def convert(self, extension):
        """
        The script uses FFMPEG to convert video files.
        It accepts one input:
            -> extension: string (.mp3, .mp4, ect.)
        """
        cmd = f'ffmpeg -y -i "{self.file}" "{find_name(self.file) + extension}"'
        subprocess.call(cmd, shell=True)
        self.file = find_name(self.file) + extension
