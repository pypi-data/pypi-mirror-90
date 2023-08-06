from moviepy.editor import *
import os


class Converter:
    
    def __init__(self, media_path, out_folder):
        """[summary]

        Args:
            media_path ([type]): [description]
            out_folder ([type]): [description]
        """        
        self.media_path = media_path
        self.out_folder = out_folder
        self.media_name = media_path.split('/')[-1]

    
    def convert_to_wav(self):
        if self.media_path.split('.')[-1]=='mp4':
            videoclip = VideoFileClip(self.media_path)
            audioclip = videoclip.audio
            try:
                audioclip.write_audiofile(f'{self.out_folder}/{self.media_name[:-4]}.wav')
            except OSError:
                raise Exception
            audioclip.close()
            videoclip.close()

    
    def convert_to_mp3(self):
        print(self.media_path[-3:])
        if self.media_path[-3:]=='mp4':
            videoclip = VideoFileClip(self.media_path)
            audioclip = videoclip.audio
            try:
                audioclip.write_audiofile(f'{self.media_path[:-4]}.mp3')
            except OSError:
                raise Error
            audioclip.close()
            videoclip.close()

        
