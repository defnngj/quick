import json
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from app_common.utils.response import Error


class BaseView:

    def response_fail(self, error=""):
        """
        返回失败, 主要用于参数验证失败
        """
        error_msg = {
            "30010": str(error)
        }
        return self.response_success(success=False, error=error_msg, data=[])

    @staticmethod
    def response_success(success: bool = True, message: str = "", error: dict = None, data: any = None) -> Response:
        """
        自定义接口返回格式
        """
        if error is None:
            error_code = ""
            error_msg = ""
        else:
            success = False
            error_code = list(error.keys())[0]
            error_msg = list(error.values())[0]

        if data is None:
            data = []

        resp = {
            "success": success,
            "message": message,
            "error": {
                "code": error_code,
                "message": error_msg
            },
            "data": data
        }
        return Response(resp)

    @staticmethod
    def json_to_dict(json_str):
        """
        json to dict
        """
        if json_str == "":
            ret = dict()
            return ret

        try:
            ret = json.loads(json_str)
            if isinstance(ret, dict) is False:
                return None
        except json.decoder.JSONDecodeError as e:
            print("error", e)
            return None
        return ret

    def check_header_type(self, data: dict) -> bool:
        """
        check header type, Value must be a string
        """
        ret = True
        for d in data:
            print("h", data[d])
            if isinstance(data[d], str) is False:
                ret = False
                break
        return ret


class BaseAPIView(APIView, BaseView, Error):
    """
    继承APIView，
    Response：自定义返回格式
    Error: 自定义错误信息
    """
    pass


class BaseViewSet(ViewSet, BaseView, Error):
    """
    继承ViewSet，
    Response：自定义返回格式
    Error: 自定义错误信息
    """
    pass


