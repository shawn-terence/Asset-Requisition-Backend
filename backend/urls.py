from django.contrib import admin
from django.urls import path
from api.views import *

urlpatterns = [
    path("user/register", UserRegistrationView.as_view(), name="register"),
    path("user/all/",AllUsersView.as_view(),name="all"),
    path("user/login", UserLoginView.as_view(), name="login"),
    path("user/logout", UserLogoutView.as_view(), name="logout"),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path("assets/add", AssetAddView.as_view(), name="add_asset"),

    path(
        "user/updatepassword", UserUpdatePasswordView.as_view(), name="update_password"
    ),
    path("user/userdetails", UserDetailView.as_view(), name="user_details"),
    path("user/changerole", ChangeUserRoleView.as_view(), name="change_role"),
    path('user/<int:user_id>/delete', DeleteUserView.as_view(), name='delete_user'),
    path("user/allusers", AllUsersView.as_view(), name="all_users"),
    path("user/alldetails/<int:user_id>/",UserAllDetailsView.as_view(),name="user's_details"),
    path("user/assets", EmployeeAssets.as_view(), name="employee_assets"),
    path("assets/<pk>/update/",UpdateAssetView.as_view(),name="asset_update"),
    path("assets/available/all/", AssetListView.as_view(), name="all_assets"),
    path("assets/all/", AllAssetsView.as_view(), name="all_assets"),
    path(
        "assets/<int:asset_id>/request/",
        AssetUpdateView.as_view(),
        name="request asset",
    ),
    path("assets/<int:asset_id>/delete",AssetDeleteView.as_view(),name="delete_asset"),
    path("requests/", RequestListView.as_view(), name="request_list"),
    path(
        "requests/<int:request_id>", RequestActionView.as_view(), name="request_action"
    ),
    path("requests/user", EmployeeRequestListView.as_view(), name="user_requests"),
    path("requests/<int:request_id>/delete", DeleteRequestView.as_view(), name="delete"),
    path("requests/<int:request_id>/return/", EmployeeReturnAssetView.as_view(), name="employee-return-asset"),
    path("requests/<int:request_id>/handle-return/", AdminHandleReturnView.as_view(), name="admin-handle-return"),
    path("requests/pending-returns/", AdminPendingReturnRequestsView.as_view(), name="admin-pending-returns"),
]
