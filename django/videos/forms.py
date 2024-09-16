from django import forms
from .models import Video
import mimetypes

class VideoUploadForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter video title'
    }))
    video_file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
        'accept': 'video/*'
    }))

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file', False)
        if video:
            mime_type, encoding = mimetypes.guess_type(video.name)
            if mime_type is None or not mime_type.startswith('video'):
                raise forms.ValidationError("Uploaded file is not a valid video.")

            return video
        else:
            raise forms.ValidationError("Couldn't read uploaded video.")