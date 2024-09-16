

from django.shortcuts import render
from django.views import View
from django.http import Http404

from utils.subtitles import extract_subtitles 

from .forms import VideoUploadForm

from .models import Video,Subtitle


# Create your views here.



def index(request): 
    return render(request=request,template_name='single_video.html')



class VideoUploadListView(View):
    
    #view for handling video upload and listing video 
    
    def get(self,request):
        
        form = VideoUploadForm()
        context = {
            'form':form
        }
        
        return render(request=request,template_name='upload_video.html',context=context)
    
    
    def post(self,request):
        
        form  =  VideoUploadForm(data=request.POST,files=request.FILES) 
        
        
        if form.is_valid():
            
            
            print('is_valid')
            
            video     = request.FILES['video_file']
            video_obj = Video(track=video)
            video_obj.save()
            
        
        print(form.errors)    
            
            
        return render(request=request,template_name='upload_video.html')



class VideoListView(View):
    
    
    
    def get(self,request,pk=None):
        
        videos = Video.objects.all().prefetch_related('subtitle_set')
        
        if pk is not None:
            
            print('pk')
            
            
            try:
            
                video = Video.objects.get(id=pk)
            except Video.DoesNotExist :
                
                raise Http404()
                
            subtitles = None    
            
            if video is not None:
                
                subtitles = Subtitle.objects.filter(video_track=video)     
            
            context = {
                
                'video':video,
                'subtitle':subtitles,
            }
                
            return render(request=request,template_name='single_video.html',context=context)
        
        
        context =  {
            'videos':videos
        }  
        
        return render(request,'video_list.html',context=context)


video_list_view = VideoListView.as_view()
video_upload_list_view = VideoUploadListView.as_view()    

    