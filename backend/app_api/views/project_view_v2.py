import os
import hashlib
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from backend.settings import PROJECT_IMAGE_DIR
from app_common.utils.base_view import BaseViewSet
from app_api.models.project_model import Project
from app_api.models.module_model import Module
from app_api.serializer.project import ProjectValidator, ProjectSerializer
from app_api.serializer.module import NodeSerializer
from app_api.serializer.module import ModuleSerializer
from app_common.utils.pagination import Pagination
from app_common.utils.token_auth import TokenAuthentication


class ProjectViewV2(BaseViewSet):

    queryset = Project.objects.all()
    # authentication_classes = []

    @action(methods=["get"], detail=True, url_path="info")
    def get_project_info(self, request, *args, **kwargs):
        """
        获取一条项目信息
        api/v2/project/<project_id>/info
        """
        pid = kwargs.get("pk")
        project = get_object_or_404(Project, id=pid, is_delete=False)
        ser = ProjectSerializer(instance=project, many=False)
        return self.response_success(data=ser.data)

    @action(methods=["get"], detail=False, url_path="list")
    def get_project_list(self, request, *args, **kwargs):
        """
        分页查询项目信息
        api/v2/project/list/
        """
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
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

    @action(methods=["post"], detail=False, url_path="create")
    def create_project(self, request, *args, **kwargs):
        """
        创建项目
        api/v2/project/create/
        """
        val = ProjectValidator(data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response_success()

    @action(methods=["put"], detail=True, url_path="update")
    def update_project(self, request, *args, **kwargs):
        """
        更新项目
        api/v2/project/<project_id>/update/
        """
        pid = kwargs.get("pk", None)
        project = get_object_or_404(Project, id=pid, is_delete=False)
        # 更新
        val = ProjectValidator(instance=project, data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response_success()

    @action(methods=["delete"], detail=True, url_path="delete")
    def delete_project(self, request, *args, **kwargs):
        """
        删除项目
        api/v2/project/<project_id>/delete/
        """
        pid = kwargs.get("pk")
        project = get_object_or_404(Project, id=pid, is_delete=False)
        project.update(is_delete=True)
        return self.response_success()

    @action(methods=["post"], detail=False, url_path="upload")
    def upload_project_image(self, request, *args, **kwargs):
        """
        上传项目图片
        api/v2/project/upload/
        """
        file = self.request.FILES['file']

        suffix = file.name.split(".")[-1]
        if suffix not in ["png", "jpg", "jpeg", "gif"]:
            return self.response_success(error=self.PROJECT_IMAGE_TYPE_ERROR)

        # 判断文件大小 1024 * 1024 * 2 = 2MB
        if file.size > 2097152:
            return self.response_success(error=self.PROJECT_IMAGE_SIZE_ERROR)

        # 文件名生成md5
        file_md5 = hashlib.md5(bytes(file.name, encoding="utf8")).hexdigest()
        file_name = file_md5 + "." + suffix

        # 保存到本地
        upload_file = os.path.join(PROJECT_IMAGE_DIR, file_name)
        with open(upload_file, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return self.response_success(data={"name": file_name})

    @action(methods=["get"], detail=True, url_path="moduleTree")
    def get_module_tree(self, request, *args, **kwargs):
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
        mtu = ModuleTreeUtils()

        for n in data_node:
            is_child = mtu.child_node(data_node, n)
            if (n["parent_id"] == 0) and (is_child is False):
                data.append(n)
            elif (n["parent_id"] == 0) and (is_child is True):
                ret = mtu.node_tree(data_node, n)
                data.append(ret)

        return self.response_success(data=data)


class ModuleTreeUtils:
    """
    模块树模块方法
    """

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

