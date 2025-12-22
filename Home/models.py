from django.conf import settings
from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # moderation fields
    is_flagged = models.BooleanField(default=False)
    labels = models.JSONField(default=dict, blank=True)    
    scores = models.JSONField(default=dict, blank=True)     
    top_label = models.CharField(max_length=50, blank=True) 
