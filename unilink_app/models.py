from django.db import models
from .utils import create_shortened_url
from .link_process import extract_info
from django.utils import timezone
from django.contrib.auth.hashers import make_password
date_generated = models.DateTimeField(default=timezone.now)


class UniCollection(models.Model):
    '''
    Creates a collection base on which all others links will be added
    ''' 
    created = models.DateTimeField(auto_now_add=True)
    collection_name = models.CharField(max_length=300, blank=True, null = True)
    description = models.CharField(max_length = 600, null= True, blank = True)
    short_url = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=600, null=True, blank=True)
    public = models.CharField(max_length=15, default=0)

    class Meta:
        db_table = "unicollection"
        ordering = ["-created"]

    def __str__(self):
        return self.short_url

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = create_shortened_url(self)
        if self.password != None:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Link(models.Model):
    """
    Model for links to be added
    """

    created = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey(UniCollection, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length = 500, null = True, blank=True)
    image_url = models.URLField(blank=True, null =True)
    favicon_url = models.URLField(null = True, blank = True)
    description = models.CharField(max_length = 1000, null = True, blank=True)
    host_name = models.CharField(max_length = 500, null = True, )
    url = models.URLField()
    
    class Meta:
        db_table = "links"
        ordering = ["-created"]
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        title,image_url, desc, favicon, host_name = extract_info(self.url)
        self.title = title
        self.image_url = image_url
        self.description = desc
        self.favicon_url = favicon
        self.host_name = host_name
        super().save(*args, **kwargs)