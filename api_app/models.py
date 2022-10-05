from django.db import models

# Create your models here.
class RequestLog(models.Model):
    ViewName = models.CharField(max_length = 64, default = "root_app:index")
    Method = models.CharField(max_length = 10, default = "GET")
    Path = models.CharField(max_length = 500, default = "/")
    Username = models.CharField(max_length = 128, default = "@Anonymous")
    Device = models.CharField(max_length = 1000, default = "")
    Date = models.DateTimeField(auto_now_add = True)

    def as_dict(self):
        return {
            "view_name": self.ViewName,
            "path": self.Path,
            "username": self.Username,
            "device": self.Device,
            "date": self.Date,
        }