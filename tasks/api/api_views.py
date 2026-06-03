from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .Serializers import TaskSellizer
from rest_framework import status
from tasks.models import Task
from rest_framework.decorators import api_view, permission_classes,action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status,viewsets, filters
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission
 
from drf_spectacular.utils import extend_schema
@extend_schema(tags=['auth'])
class RegisterApiView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        if not username or  not password:
          return Response({'error': 'username and password required'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'},status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.create_user(username=username,password=password)
        token=Token.objects.create(user=user)
        return Response({'token':token.key},status=status.HTTP_201_CREATED)

# ---------------------------function base-----------------
@api_view(['GET','POST'])

@permission_classes([IsAuthenticated])
def tasks_api(request):

    tasks = Task.objects.filter(owner=request.user)
    
    if request.method =='GET':
      serializer =TaskSellizer(tasks, many=True)
      return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskSellizer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT','DELETE','GET','PATCH'])
@permission_classes([IsAuthenticated])
def tasks_details(request,pk):
    # task = Task.objects.filter(pk=pk, owner=request.user).first()
    # task=get_object_or_404(Task,pk=pk,owner=request.user)
    # tasks = Task.objects.get(pk,owner=request.user)
    try:
      task = Task.objects.get( pk=pk,owner=request.user)
    except Task.DoesNotExist:
            return Response({'error': 'Task not found'},status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer =TaskSellizer(task)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer=TaskSellizer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH':

        serializer = TaskSellizer(task,data=request.data,partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#-----------------------------------class base ----------------------------------

@extend_schema(tags=['tasts'])
class TaskApiView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        task=Task.objects.filter(owner=request.user)
        serializer=TaskSellizer(task,many=True).data
        return Response(serializer,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=TaskSellizer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
@extend_schema(tags=['tasts'])
class TaskApiDetails(APIView):
     permission_classes=[IsAuthenticated,IsOwner]
     def get_object(self, pk):
         return Task.objects.filter(pk=pk).first()
     def get(self,request,pk):
        task=self.get_object(pk)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, task)
        return Response(TaskSerializer(task).data)
     def put(self, request, pk):
        task = self.get_object(pk)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)
            self.check_object_permissions(request, task)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     def delete(self, request, pk):
        task = self.get_object(pk)
        if not task:
           return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


        #update one field in object and not return error 
     def patch(self, request, pk):
        task = self.get_object(pk)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, task)

        serializer = TaskSellizer(task,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#---------------------------------------viewset-----------------------------
class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSellizer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description','status']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']
    def get_queryset(self):
        qs = Task.objects.filter(owner=self.request.user)
        return qs
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    @action(detail=False, methods=['get'])
    def summary(self, request):
            qs=self.get_queryset()
            data = {
            'total': qs.count(),
            'pending': qs.filter(status='pending').count(),
            'in_progress': qs.filter(status='in_progress').count(),
            'done': qs.filter(status='done').count(),
            }
            return Response(data)
    @action(detail=True, methods=['post'])
    def mark_done(self, request, pk=None):
        task = self.get_object()
        task.status = 'done'
        task.save()
        return Response({"message": "Task marked as done"},status=status.HTTP_200_OK)




 



    
