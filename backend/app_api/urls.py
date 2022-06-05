from django.urls import path
from rest_framework import routers
from app_api.views.user_views import LoginView
from app_api.views.register_views import RegisterView
from app_api.views.project_view_v2 import ProjectViewV2
from app_api.views.project_view import ProjectView, ProjectModuleView, ModuleTreeView
from app_api.views.module_view import ModuleView
from app_api.views.module_view import NodeCaseView
from app_api.views.case_view import CaseViewSet
from app_api.views.task_view import TaskViewSet
from app_api.views.result_view import ResultViewSet


url_path = [
    path('v1/login/', LoginView.as_view()),
    path('v1/register/', RegisterView.as_view()),
    path('v1/project/', ProjectView.as_view()),
    path('v1/project/<int:pk>/', ProjectView.as_view()),
    path("v1/project/<int:pk>/module/", ProjectModuleView.as_view()),
    path("v1/project/<int:pk>/moduleTree/", ModuleTreeView.as_view()),

    path('v1/module/', ModuleView.as_view()),
    path('v1/module/<int:pk>/', ModuleView.as_view()),
    path("v1/module/<int:pk>/cases/", NodeCaseView.as_view()),
]

router = routers.SimpleRouter()
router.register(r'v2/project', ProjectViewV2)  # 项目管理
router.register(r'v1/case', CaseViewSet)  # 用例管理
router.register(r'v1/task', TaskViewSet)  # 任务管理
router.register(r'v1/result', ResultViewSet)  # 结果管理

urlpatterns = url_path + router.urls
