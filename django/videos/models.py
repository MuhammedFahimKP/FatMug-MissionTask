from typing import Any
from django.db import models

# Create your models here.



class BaseModel(models.Model):
    
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    is_deleted  = models.BooleanField(default=False)
    
    
    class Meta:
        
        abstract = True
    
       
class Video(BaseModel):
    
    track = models.FileField(upload_to='videos/')  
    
    

    
class Subtitle(BaseModel):
    
    video_track     = models.ForeignKey(Video,on_delete=models.CASCADE)
    language        = models.CharField()
    track_path      = models.CharField()  
    
    
    
        
    
     
        
    
            
    
    

