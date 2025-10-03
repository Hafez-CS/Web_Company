from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from .models import UserProfile
from .serializers import UserSerializer, RegisterSerializer
from groups_module.models import GroupMembership


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({
                "detail": "ایمیل و رمز عبور الزامی است."
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({
                "detail": "ایمیل یا رمز عبور اشتباه است."
            }, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "message": "ورود با موفقیت انجام شد.",
            "data": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }
        }, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            if UserProfile.objects.filter(username=username).exists():
                return Response({
                    "detail": "نام کاربری قبلاً ثبت شده است."
                }, status=status.HTTP_400_BAD_REQUEST)
            if UserProfile.objects.filter(email=email).exists():
                return Response({
                    "detail": "ایمیل قبلاً ثبت شده است."
                }, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            return Response({
                "success": True,
                "message": "ثبت‌نام با موفقیت انجام شد.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({
                "detail": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "detail": f"خطایی رخ داد: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                "success": True,
                "message": "پروفایل با موفقیت بروزرسانی شد",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                "detail": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "detail": f"خطایی رخ داد: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "اکانت شما با موفقیت حذف گردید"}, status=status.HTTP_204_NO_CONTENT)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "رفرش توکن ارسال نشده است."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "خروج با موفقیت انجام شد."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "توکن نامعتبر است یا قبلاً بلاک شده است."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"خطا: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangeTeamAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        new_group_id = request.data.get('group_id')
        
        if not new_group_id:
            return Response({
                'success': False,
                'detail': 'Group ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Deactivate current memberships
        GroupMembership.objects.filter(user=user, is_active=True).update(is_active=False)
        
        # Activate new membership
        try:
            membership = GroupMembership.objects.get(user=user, group_id=new_group_id)
            membership.is_active = True
            membership.save()
            
            return Response({
                'success': True,
                'message': 'Team changed successfully.'
            })
        except GroupMembership.DoesNotExist:
            return Response({
                'success': False,
                'detail': 'You are not a member of this group.'
            }, status=status.HTTP_400_BAD_REQUEST)

class UserSettingsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        current_memberships = GroupMembership.objects.filter(user=user, is_active=True)
        
        groups = [{
            'id': m.group.id,
            'name': m.group.name,
            'role': m.role
        } for m in current_memberships]
        
        return Response({
            'success': True,
            'data': {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_staff': user.is_staff
                },
                'groups': groups
            }
        })
