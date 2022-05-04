import json
from rest_framework import serializers
from app_api.models import TestCase, TestTask, TaskCaseRelevance
from app_api.serializer.config import CaseDataList
from app_common.utils.base_serializer import check_json


class TaskSerializer(serializers.ModelSerializer):
    """
    测试任务序列化
    """
    cases = serializers.SerializerMethodField()  # 反向获取模块的名称
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 日期格式化

    class Meta:
        model = TestTask
        fields = ['id', 'project_id', 'name', 'describe', 'status', 'cases', 'create_time']  # 要显示的字段

    def get_cases(self, testtask_obj):
        """查询task关联的case id list"""
        tcr = TaskCaseRelevance.objects.filter(task=testtask_obj)
        case_list = []
        for i in tcr:
            case_list.append({
                "moduleId": i.module_id,
                "casesId": json.loads(i.cases)
            })
        return case_list


class TaskValidator(serializers.Serializer):
    """
    任务的验证器
    """
    project_id = serializers.IntegerField(required=True, error_messages={"required": "project_id不能为空"})
    name = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于50"})
    describe = serializers.CharField(required=False)
    cases = serializers.ListField(required=False,
                                  error_messages={"required": "case不能为空"},
                                  write_only=True)

    def validate_cases(self, value):
        """ 验证cases是否为list格式 """
        if len(value) == 0:
            raise serializers.ValidationError("cases不能为空list")
        return value

    def create(self, validated_data):
        """
        创建任务
        """
        project_id = validated_data.get('project_id')
        name = validated_data.get('name')
        describe = validated_data.get('describe')
        status = validated_data.get('status', 0)
        # 创建关联数据
        task = TestTask.objects.create(project_id=project_id, name=name, describe=describe, status=status)
        for case in validated_data.get('cases', []):
            module_id = case["moduleId"]
            cases = json.dumps(case["casesId"])
            TaskCaseRelevance.objects.create(task_id=task.id, module_id=module_id, cases=cases)
        return task

    def update(self, instance, validated_data):
        """
        更新任务
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据 - 从request 里面
        """
        instance.name = validated_data.get('name')
        instance.describe = validated_data.get('describe')
        instance.status = validated_data.get('status', True)
        # 删除任务关联数据，重新创建
        TaskCaseRelevance.objects.filter(task_id=instance.id).delete()
        for case in validated_data.get('cases', []):
            module_id = case["moduleId"]
            cases = json.dumps(case["casesId"])
            TaskCaseRelevance.objects.create(task_id=instance.id, module_id=module_id, cases=cases)
        instance.save()
        return instance
