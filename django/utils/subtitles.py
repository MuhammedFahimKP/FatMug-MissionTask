
import os
import subprocess
import json
from io import StringIO

import webvtt

from videos.models import Video, Subtitle



def extract_subtitles(video: Video) -> bool | None:
    
    #getting video from the path
    input_video = os.path.abspath(video.track.path)

    # Run ffprobe to get subtitle stream information
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 
        'stream=index:stream_tags=language', '-select_streams', 
        's', '-of', 'json', input_video
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    
    #handling subprocess error
    if result.returncode != 0:
        return None

    # Parse the ffprobe command  output
    probe_data = json.loads(result.stdout)
    subtitle_streams = probe_data.get('streams', [])

    if not subtitle_streams:
        return False

    language_unknown = 1

    for stream in subtitle_streams:
        index = stream['index']
        language = stream.get('tags', {}).get('language', 'unknown')

        if language == 'unknown':
            language = f"{language}-{language_unknown}"
            language_unknown += 1

        # Use ffmpeg to extract subtitle stream to memory
        cmd = [
            'ffmpeg', '-i', input_video, 
            '-map', f'0:{index}', '-c:s', 'webvtt', '-f', 'webvtt', '-'
        ]
        ffmpeg_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if ffmpeg_process.returncode != 0:
            return None

        # Subtitle data is now in memory (ffmpeg_process.stdout)
        subtitle_data = ffmpeg_process.stdout.decode('utf-8')

        # Save the subtitle data directly into the Subtitle model's TextField
        subtitle_instance = Subtitle(
            video_track=video,  # Changed to `video` (assumed relation)
            language=language,
            subtitle_text=subtitle_data  # Store subtitle text here
        )
        subtitle_instance.save()

    return True




def get_timeline_by_subtile_phrase(video:Video,query:str) -> list[dict[str,str]] | None:
    

    
    #cating an emptylist to store the timelines
    
    
    results = []
    
    subtitles = Subtitle.objects.filter(video_track=video)
    
    if not  subtitles.exists():
        return None 
    # Fetch all subtitles
        # Regex pattern to match VTT timestamps (e.g., 00:00:01.000 --> 00:00:05.000)
   
    for subtitle in subtitles:
        
         # Create a file-like object from the VTT content
        vtt_file = StringIO(subtitle.subtitle_text)

        # Load the VTT data from the file-like object
        captions = webvtt.read_buffer(vtt_file)
        
        

        # Iterate through each caption
        for caption in captions:
            # Check if the word is present in the splited capition text  (case-insensitive)
            if query.lower() in caption.text.lower().split():
                # Append the start and end time of the caption containing the word
                results.append(caption.start)

    
        
    return results


