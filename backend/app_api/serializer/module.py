from rest_framework import serializers
from app_api.models import Module



class NodeSerializer(serializers.ModelSerializer):
    """
    模块树节点序列化
    """

    class Meta:
        model = Module
        fields = ['id', 'name', 'parent_id']  # 要显示的字段


class ModuleSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name")  # 反向获取项目的名称
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 日期格式化

    class Meta:
        model = Module
        fields = ['id', 'name', 'describe', 'project_id', "project_name", 'create_time']  # 要显示的字段
        # fields = "__all__"


class ModuleValidator(serializers.Serializer):
    """
    模块的验证器
    """
    name = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于50"})
    project_id = serializers.IntegerField(required=True)
    parent_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        创建
        """
        project = Module.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        """
        更新
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据 - 从request 里面
        """
        instance.name = validated_data.get("name")
        instance.describe = validated_data.get("describe")
        instance.project_id = validated_data.get("project_id")
        instance.parent_id = validated_data.get("parent_id")
        instance.save()
        return instance



















