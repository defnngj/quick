from app_api.models import Module
from app_api.serializer.module import ModuleValidator, ModuleSerializer, NodeSerializer
from app_common.utils.pagination import Pagination
from app_common.utils.base_view import BaseAPIView


class ModuleView(BaseAPIView):

    def get(self, request, *args, **kwargs):
        """
        查询
        """
        mid = kwargs.get("pk")
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        if mid is not None:  # 查询单条数据
            try:
               module = Module.objects.get(pk=mid, is_delete=False)
               ser = ModuleSerializer(instance=module, many=False)
            except Module.DoesNotExist:
                return self.response_success(error=self.MODULE_OBJECT_NULL)
            return self.response_success(data=ser.data)
        else:   # 查询一组数据
            project = Module.objects.filter(is_delete=False).all()
            pg = Pagination()
            page_data = pg.paginate_queryset(queryset=project, request=request, view=self)
            ser = ModuleSerializer(instance=page_data, many=True)
            data = {
                "total": len(project),
                "page": int(page),
                "size": int(size),
                "moduleList": ser.data
            }
            return self.response_success(data=data)

    def post(self, request, *args, **kwargs):
        """
        添加
        /module/abc/
        """
        val = ModuleValidator(data=request.data)
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
                return self.response_success(error=self.MODULE_ID_NULL)
        try:
           module = Module.objects.get(pk=pid, is_delete=False)
        except Module.DoesNotExist:
            return self.response_success(error=self.MODULE_OBJECT_NULL)
        # 更新
        val = ModuleValidator(instance=module, data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response_success()

    def delete(self, request, *args, **kwargs):
        """
        删除
        """
        mid = kwargs.get("pk")
        if mid is not None:  # 查询单条数据

            module = Module.objects.filter(pk=mid, is_delete=False).update(is_delete=True)
            if module == 0:
                return self.response_success(error=self.MODULE_DELETE_ERROR)

        return self.response_success()


class NodeTreeView(BaseAPIView):

    def node_tree(self, nodes, current_node):
        """
        递归：获取节点的子节点
        """
        for node in nodes:
            if node["parent_id"] == current_node["id"]:
                current_node["children"].append(node)
                self.node_tree(nodes, node)

        return current_node
    
    def chileren_node(self, nodes, current_node):
        """
        判断有没有子节点
        """
        for node in nodes:
            if node["parent_id"] == current_node["id"]:
                print("有子节点", current_node["label"])
                return True
        return False

    def get(self, request,  *args, **kwargs):
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
            is_chilerend = self.chileren_node(data_node, n)
            if (n["parent_id"] == 0) and (is_chilerend == False):
                data.append(n)
            elif(n["parent_id"] == 0) and (is_chilerend == True):
                ret = self.node_tree(data_node, n)
                data.append(ret)

        return self.response_success(data=data)














