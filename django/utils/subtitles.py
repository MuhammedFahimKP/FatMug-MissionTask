from videos.models import Video,Subtitle

import subprocess

import json

import os 


def extract_subtitles(video:Video):
    input_video = os.path.abspath(video.track.path)
    print(input_video)
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'stream=index:stream_tags=language', 
           '-select_streams', 's', '-of', 'json', input_video]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    
    print(result)
    
    # Parse the ffprobe output (JSON format)
    probe_data = json.loads(result.stdout)
    subtitle_streams = probe_data.get('streams', [])

    # Extract and save each subtitle
    
    language_unknown =  1
    
    for stream in subtitle_streams:
        index = stream['index']
        language = stream['tags'].get('language', 'unknown')
        
        
        if language == 'unknown' :
            
            language = f"{language}-{language_unknown}"
            language_unknown += 1
        
        

        # Output subtitle file
        output_file = f'subtitle_{video.id}_{language}_{index}.srt'
        output_path = os.path.abspath(f'media/subtitles/{output_file}')
        cmd = [
            'ffmpeg', '-i', input_video, 
            '-map', f'0:{index}', 
            output_path
        ]
        subprocess.run(cmd)
        
        save_path = f'media/subtitles/{output_file}'
        # Save subtitle to the database
        Subtitle.objects.create(video_track=video, track_path=save_path, language=language)