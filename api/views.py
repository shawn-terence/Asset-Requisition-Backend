from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveUpdateAPIView
import logging
User = get_user_model()
# Create your views here.
"""                                     USER VIEWS                                                                      """
logger = logging.getLogger(__name__)

# user registration

#url(user/register)
class UserRegistrationView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User log in view
# url(user/login)
class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        print(email)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)
            user_details=request.user
            serializer=UserSerializer(user_details)
            message= {"message": "User logged in successfully"}
            response_data = {
                "message":message,
                "user":serializer.data,
                "token":token.key
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid email and/or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class UserLogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        token=Token.objects.get(user=request.user)
        print(request.user)
        token.delete()
        return Response({'message':'logged out successfully'},status=status.HTTP_200_OK)

# url(user/userdetails)
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# User list
# url(user/all)
class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# User update password
# url(user/updatepassword)
class UserUpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        password = request.data.get("password")
        if len(password) < 8:
            return Response(
                {"error": "New password must be at least 8 characters long"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(password)
        user.save()

        return Response(
            {"message": "Password updated successfully"}, status=status.HTTP_200_OK
        )

class UserAllDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        print(user)
        # Fetch related assets and requests
        assets = Asset.objects.filter(owner=user)
        requests = Request.objects.filter(employee=user)

        # Serialize data
        user_data = UserSerializer(user).data
        assets_data = AssetSerializer(assets, many=True).data
        requests_data = RequestSerializer(requests, many=True).data

        return Response(
            {
                "user": user_data,
                "assets": assets_data,
                "requests": requests_data,
            },
            status=status.HTTP_200_OK,
        )
# Admin change employee role
# url(user/changerole)
class ChangeUserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role not in ["admin", "superadmin"]:
            return Response(
                {"error": "You are not authorized to change user roles."},
                status=status.HTTP_403_FORBIDDEN,
            )

        email = request.data.get("email")
        new_role = request.data.get("new_role")

        if not email or not new_role:
            return Response(
                {"error": "Email and new role are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_role not in ["admin", "employee", "superadmin"]:
            return Response(
                {"error": "Invalid role specified."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        user.role = new_role
        user.save()

        return Response(
            {"success": f"User role updated to {new_role}."}, status=status.HTTP_200_OK
        )

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Handle profile picture deletion
        
        self.perform_update(serializer)
        
            
        return Response(serializer.data, status=status.HTTP_200_OK)
# delete a user from the database
# url(user/id/delete)
class DeleteUserView(APIView):
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        # Check if the current user has the admin or superadmin role
        if request.user.role != "superadmin":
            return Response(
                {"error": "You are not authorized to delete users."},
                status=status.HTTP_403_FORBIDDEN,
            )


        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        user.delete()


        return Response(
            {"success": "User deleted successfully."}, status=status.HTTP_200_OK
        )

    """                                     ASSET VIEWS                                                                     """
    # Add asset

#url(asset/add/)
class AssetAddView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Allow handling file uploads

    def post(self, request):
        user = request.user

        if user.role == "employee":
            return Response(
                {"error": "You are not authorized to add assets"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = AssetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#get all Available Assets
class AssetListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        assets = Asset.objects.filter(status=True)
        serializer=AssetSerializer(assets,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AllAssetsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        assets = Asset.objects.all()
        serializer=AssetSerializer(assets,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

# request for asset
#url(assets/<id>/request/)
class AssetUpdateView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, asset_id):
        user = request.user
        asset = get_object_or_404(Asset, id=asset_id)

        if not asset.status:
            return Response(
                {"error": "Asset is already requested "},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Change the asset status to False (requested)
        asset.status = False
        asset.save()

        # Log the request in the Request table
        request_log = Request.objects.create(
            asset=asset, employee=user, status="pending"
        )

        return Response(
            {"success": "Asset requested successfully and logged."},
            status=status.HTTP_200_OK,
        )
#Delete an asset
#url(assets/id/delete)
class AssetDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, asset_id):
        if request.user.role == "employee":
            return Response(
                {"error": "You are not authorized to remove assets."},
                status=status.HTTP_403_FORBIDDEN,
            )
        asset = get_object_or_404(Asset, id=asset_id)
        asset.delete()
        return Response({"success": "Asset deleted successfully."}, status=status.HTTP_200_OK)
class UpdateAssetView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        asset = get_object_or_404(Asset, pk=pk)

        serializer = AssetSerializer(asset, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": error_details}, status=status.HTTP_400_BAD_REQUEST)
class EmployeeAssets(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        employee_id = user.id

        user_requests = Request.objects.filter(employee__id=employee_id)


        if not user_requests.exists():
            return Response({"error": "No assets have been allocated yet."}, status=status.HTTP_400_BAD_REQUEST)


        serializer = RequestSerializer(user_requests, many=True)


        approved_assets = []
        for request_data in serializer.data:
            if request_data.get('status') == 'approved':
                asset_data = request_data.get('asset')
                if asset_data:
                    approved_assets.append(asset_data)


        if approved_assets:
            return Response(approved_assets, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No approved assets found."}, status=status.HTTP_400_BAD_REQUEST)


# request list
class RequestListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class RequestActionView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, request_id):
        user = request.user
        if user.role not in ["admin", "superadmin"]:
            return Response(
                {"error": "Only admins or superadmins can approve or reject requests."},
                status=status.HTTP_403_FORBIDDEN,
            )

        request_instance = get_object_or_404(Request, id=request_id)
        action = request.data.get("action")  # 'approve' or 'reject'

        # Prevent admins from approving or rejecting their own requests
        if request_instance.employee == user:
            return Response(
                {"error": "You cannot approve or reject your own requests."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if action == "approve":
            request_instance.status = "approved"
            request_instance.return_status = None
            request_instance.save()

            # Set asset status to False upon approval
            request_instance.asset.status = False
            request_instance.asset.owner = request_instance.employee  # Set the owner of the asset
            request_instance.asset.save()

            return Response(
                {"success": "Request approved successfully."}, status=status.HTTP_200_OK
            )

        elif action == "reject":
            request_instance.status = "rejected"
            request_instance.save()

            request_instance.asset.status = True
            request_instance.asset.save()

            return Response(
                {"success": "Request rejected successfully."}, status=status.HTTP_200_OK
            )

        return Response(
            {"error": 'Invalid action. Use "approve" or "reject".'},
            status=status.HTTP_400_BAD_REQUEST,
        )

# employee request list
class EmployeeRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        employee_id = user.id

        user_requests = Request.objects.filter(employee=employee_id)


        serializer = RequestSerializer(user_requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

#Employee deletes non approved requests
class DeleteRequestView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request,request_id):
        user = request.user
        employee_id=user.id
        request_instance = get_object_or_404(Request, id=request_id)
        if request_instance.status == "approved":
            return Response(
                {"error": "Cannot delete an approved request."},
                status=status.HTTP_400_BAD_REQUEST,)
        asset = request_instance.asset
        asset.status = True
        asset.save()

        request_instance.delete()
        return Response({"success": "Request deleted successfully."}, status=status.HTTP_200_OK)


class EmployeeReturnAssetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        user = request.user
        if user.role != "employee":
            return Response(
                {"error": "Only employees can return assets."},
                status=status.HTTP_403_FORBIDDEN,
            )

        request_instance = get_object_or_404(Request, id=request_id)

        # Ensure the request belongs to the employee
        if request_instance.employee != user:
            return Response(
                {"error": "You can only return assets you requested."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Ensure the asset is currently assigned to the employee
        if request_instance.status != "approved" or request_instance.asset.status != False:
            return Response(
                {"error": "This asset is not currently assigned to you."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set return_status to "pending"
        request_instance.return_status = "pending"
        request_instance.save()

        return Response(
            {"success": "Asset return request submitted successfully."},
            status=status.HTTP_200_OK,
        )

class AdminHandleReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, request_id):
        user = request.user
        if user.role not in ["admin", "superadmin"]:
            return Response(
                {"error": "Only admins or superadmins can handle return requests."},
                status=status.HTTP_403_FORBIDDEN,
            )

        request_instance = get_object_or_404(Request, id=request_id)
        action = request.data.get("action")

        # Ensure the request is a return request
        if request_instance.return_status != "pending":
            return Response(
                {"error": "This is not a pending return request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if action == "approve":
            # Approve the return request
            request_instance.return_status = "approved"
            request_instance.asset.status = True  # Mark asset as available
            request_instance.asset.save()
            request_instance.save()

            return Response(
                {"success": "Asset return request approved successfully."},
                status=status.HTTP_200_OK,
            )

        elif action == "reject":
            # Reject the return request
            request_instance.return_status = "rejected"
            request_instance.save()

            return Response(
                {"success": "Asset return request rejected successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": 'Invalid action. Use "approve" or "reject".'},
            status=status.HTTP_400_BAD_REQUEST,
        )
class AdminPendingReturnRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role not in ["admin", "superadmin"]:
            return Response(
                {"error": "Only admins or superadmins can view pending return requests."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Filter requests with return_status = "pending"
        pending_return_requests = Request.objects.filter(return_status="pending")
        serializer = RequestSerializer(pending_return_requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)