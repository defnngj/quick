from django.shortcuts import render
from django.http import JsonResponse
# from rest_framework.views import APIView
from app_api.models.project_model import Project
from app_api.models.module_model import Module
from app_api.serializer.project import ProjectValidator, ProjectSerializer
from app_api.serializer.module import NodeSerializer
from app_api.serializer.module import ModuleSerializer
from app_common.utils.pagination import Pagination
from app_common.utils.base_view import BaseAPIView
from app_common.utils.token_auth import TokenAuthentication


class ProjectView(BaseAPIView):
    # authentication_classes = []

    def get(self, request, *args, **kwargs):
        """
        查询
        """
        pid = kwargs.get("pk", None)
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        if pid is not None:  # 查询单条数据
            try:
               project = Project.objects.get(pk=pid, is_delete=False)
               ser = ProjectSerializer(instance=project, many=False)
            except Project.DoesNotExist:
                # return response(error=Error.PROJECT_OBJECT_NULL)

                return self.response_success(error=self.PROJECT_OBJECT_NULL)
            return self.response_success(data=ser.data)
        else:   # 查询all数据
            project = Project.objects.filter(is_delete=False).all()
            pg = Pagination()
            page_data = pg.paginate_queryset(queryset=project, request=request, view=self)
            ser = ProjectSerializer(instance=page_data, many=True)
            data = {
                "total": len(project),
                "page": int(page),
                "size": int(size),
                "projectList": ser.data
            }
            return self.response_success(data=data)

    def post(self, request, *args, **kwargs):
        """
        添加项目
        """
        val = ProjectValidator(data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response_success()

    def put(self, request, *args, **kwargs):
        """
        更新
        """
        pid = kwargs.get("pk")
        if pid is None:
            pid = request.data.get("id", "")
            if pid == "":
                return self.response_success(error=self.PROJECT_ID_NULL)
        try:
           project = Project.objects.get(pk=pid, is_delete=False)
        except Project.DoesNotExist:
            return self.response_success(error=self.PROJECT_OBJECT_NULL)
        # 更新
        val = ProjectValidator(instance=project, data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response_success()

    def delete(self, request, *args, **kwargs):
        """
        删除
        """
        pid = kwargs.get("pk")
        if pid is not None:  # 查询单条数据
            project = Project.objects.filter(pk=pid, is_delete=False).update(is_delete=True)
            if project == 0:
                return self.response_success(error=self.PROJECT_DELETE_ERROR)

        return self.response_success()


class ProjectModuleView(BaseAPIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        """
        查询
        """
        pid = kwargs.get("pk", 1)
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")

        module = Module.objects.filter(project_id=pid, is_delete=False).all()
        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=module, request=request, view=self)
        ser = ModuleSerializer(instance=page_data, many=True)
        data = {
            "total": len(module),
            "page": int(page),
            "size": int(size),
            "moduleList": ser.data
        }
        return self.response_success(data=data)


class ModuleTreeView(BaseAPIView):

    def node_tree(self, nodes, current_node):
        """
        递归：获取节点的子节点
        """
        for node in nodes:
            if node["parent_id"] == current_node["id"]:
                current_node["children"].append(node)
                self.node_tree(nodes, node)

        return current_node

    @staticmethod
    def child_node(nodes, current_node):
        """
        判断有没有子节点
        """
        for node in nodes:
            if node["parent_id"] == current_node["id"]:
                return True
        return False

    def get(self, request, *args, **kwargs):
        """
        获取节点树：父节点->子节点
        """
        pid = kwargs.get("pk", 1)
        module = Module.objects.filter(project_id=pid, is_delete=False).all()
        ser = NodeSerializer(instance=module, many=True)

        nodes = ser.data
        data_node = []
        for n in nodes:
            data_node.append({
                "id": n["id"],
                "parent_id": n["parent_id"],
                "label": n["name"],
                "children": [],
            })

        data = []
        for n in data_node:
            is_child = self.child_node(data_node, n)
            if (n["parent_id"] == 0) and (is_child is False):
                data.append(n)
            elif (n["parent_id"] == 0) and (is_child is True):
                ret = self.node_tree(data_node, n)
                data.append(ret)

        return self.response_success(data=data)
