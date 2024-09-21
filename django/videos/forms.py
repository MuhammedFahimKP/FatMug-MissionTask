import mimetypes
from django import forms

# Add .mkv to the mimetypes if not already present
mimetypes.add_type("video/x-matroska", ".mkv")

class VideoUploadForm(forms.Form):
    video_file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
        'accept': 'video/mp4,video/x-matroska,video/x-msvideo,video/quicktime'
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
