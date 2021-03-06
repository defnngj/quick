from django.db import models
from app_api.models import Project


class Module(models.Model):
    """
    模块表
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, null=False, default="")
    describe = models.TextField("描述", null=True, blank=True, default="")
    parent_id = models.IntegerField("父级ID", default=0)
    is_delete = models.BooleanField("删除", default=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
