

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
    Http404,
)

from django.views import View
from django.contrib.messages import success as success_message , error as error_message



from utils.subtitles import extract_subtitles , get_timeline_by_subtile_phrase 

from .forms import VideoUploadForm
from .models import Video,Subtitle


# Create your views here.





def serve_subtitles(request:HttpRequest,pk:int) -> HttpResponse:
    subtitle = get_object_or_404(Subtitle, id=pk)
    response = HttpResponse(subtitle.subtitle_text, content_type='text/vtt')
    response['Content-Disposition'] = 'inline; filename="subtitles.vtt"'
    return response



class GetPhrasedVideoTimeLine(View):
    
    
    
    def get(self,request:HttpRequest,pk:int) -> JsonResponse:
        
        
        query = request.GET.get('query')
        
        
        if query:
    
            try:
                
                video = Video.objects.get(id=str(pk))
                
                result =  get_timeline_by_subtile_phrase(video=video, query=query)
                
                
                if result is None:    
                    return  JsonResponse({'video':"video does'nt have subtitle  "})
                
                
                return JsonResponse(result,safe=False)
                
            
            except Video.DoesNotExist :
                
                    return JsonResponse({ 'video':'not found' })
            
        return JsonResponse({'query':'please provide query'})     
                
        
        
        
        




class VideoUploadView(View):
    
    #view for handling video upload and listing video 
    
    def get(self,request:HttpRequest)  -> HttpResponse:
        
        form = VideoUploadForm()
        context = {
            'form':form
        }
        
        return render(request=request,template_name='upload_video.html',context=context)
    
    
    def post(self,request:HttpRequest) -> HttpResponse:
        
        form  =  VideoUploadForm(data=request.POST,files=request.FILES) 
        
        
        if form.is_valid():
            
            

            video     = request.FILES['video_file']
            video_obj = Video(track=video)
            video_obj.save()
            
            extract_subtitles(video=video_obj)
            
            success_message(request,'video uploaded')
            
            return redirect('list')
        
        
            
        
            
        for field, errors in form.errors.items():
            
            for error in errors:
             error_message(request, f"{field}: {error}")
             
            
            for error in form.non_field_errors():
                error_message(request, error)
             
        return redirect('video upload')




class VideoListRetriveView(View):
    
    
    def list(self,request:HttpRequest) -> HttpResponse:
        
        videos = Video.objects.all()
        
        context = {
            'videos':videos
        }
        
        return render(request,'video_list.html',context=context)
        
    
    def retrive(self,request:HttpRequest,pk:int) -> HttpResponse:
        
        try:
            
            video = Video.objects.prefetch_related('subtitle_set').get(id=pk)
        except Video.DoesNotExist :
            
            raise Http404()
            
        
        subtitles = video.subtitle_set.all()
        
        
        
        context = {
            
            'video':video,
            'subtitles':subtitles,
            'phrase_url':request.build_absolute_uri('/') + f'phrase/{video.id}/'                
        }
            
        return render(request=request,template_name='single__video.html',context=context)
    
              
    
    
    
    def get(self,request:HttpRequest,pk :int | None = None) -> HttpResponse:
        
        
    
        if pk is not None:
            
            return self.retrive(request=request,pk=pk)
                
        
        return self.list(request=request)







video_list_retrive_view = VideoListRetriveView.as_view()
video_phrase_list_view  = GetPhrasedVideoTimeLine.as_view()
video_upload_view       = VideoUploadView.as_view()    





    