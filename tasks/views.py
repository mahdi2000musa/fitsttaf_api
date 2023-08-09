from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .serializers import *
from staff.models import Profile
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_406_NOT_ACCEPTABLE, HTTP_404_NOT_FOUND
from .permissions import IsTeamLeader, IsAssigner, IsParticipant, IsParticipantORAssigner, IsOwnerORAdminORReadOnly


class AssigneTask(APIView):

    permission_classes = [IsAuthenticated, IsTeamLeader]
    serializer_class = TaskSerializer
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(

        operation_id='Create a task',
        operation_description='Create a document by providing file and s3_key',
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE,),
            openapi.Parameter('subject', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('status', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('participant_id', openapi.IN_FORM, type=openapi.TYPE_INTEGER),

        ],

    )
    def post(self, request):
        try:
            assigner = Profile.objects.get(user=request.user)
            self.check_object_permissions(request, assigner)
            data = {
                'subject': request.data['subject'],
                "description": request.data['description'],
                'file': request.data['file'],
                'status': request.data['status'],
                'participant_id': request.data['participant_id'],
                'assigner_id': assigner.id,
            }

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        except Profile.DoesNotExist:
            return Response({'message': "No assigner exist with this id!", "data": Task.objects.none()},
                            status=HTTP_404_NOT_FOUND)

# add comment serializer


class TaskAPIVeiw(APIView):

    permission_classes = [IsAuthenticated, IsAssigner]
    parser_classes = [MultiPartParser]

    def get(self, request, pk):

        try:
            task = Task.objects.get(id=pk)
            task_serialized = TaskSerializer(instance=task)
            data = task_serialized.data
            return Response(data, status=HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'message': "No task exist with this id!", "data": Task.objects.none()}, status=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(

        operation_id='update a task',
        operation_description='Create a document by providing file and s3_key',
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, ),
            openapi.Parameter('subject', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('status', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('participant_id', openapi.IN_FORM, type=openapi.TYPE_INTEGER),

        ],

    )
    def put(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
            self.check_object_permissions(request, task)
            updated_task = TaskSerializer(instance=task, data=request.data, partial=True)
            if updated_task.is_valid():
                updated_task.save()
                return Response({'message':"updated succesfully!"}, status=HTTP_200_OK)
            return Response({'message': updated_task.errors}, status=HTTP_406_NOT_ACCEPTABLE)
        except Task.DoesNotExist:
            return Response({"message":"No task exist with this id!", "data":Task.objects.none()} , status=HTTP_404_NOT_FOUND )

    def delete(self, request, pk):

        try:
            task = Task.objects.get(id=pk)
            self.check_object_permissions(request, task)
            task.delete()
            return Response({"message":"task deleted successfully!"}, status=HTTP_200_OK)

        except Task.DoesNotExist:
            return Response({'message':'task not found'}, status=HTTP_404_NOT_FOUND)




class AllTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        tasks = Task.objects.all()
        serialized = TaskSerializer(instance=tasks, many=True)
        data = serialized.data
        return Response(data, status=HTTP_200_OK)


class TaskResponse(APIView):

    permission_classes = [IsAuthenticated, IsParticipant]

    def get(self, request, pk):

        task = get_object_or_404(Task, id=pk)
        self.check_object_permissions(request, task)
        if task.status != "P" and task.status != 'D':
            task.status = "P"
            task.save()
            return Response({
                "message":"change task to Pending status",
            }, status=HTTP_200_OK)

        return Response({
            "message" : "this task cant change to Pending!",
        }, status=HTTP_406_NOT_ACCEPTABLE)


class TaskProblem(APIView):

    permission_classes = [IsAuthenticated, IsParticipant]

    def get(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        self.check_object_permissions(request, task)
        if task.status != 'W' and task.status != 'D':
            task.status = 'W'
            task.save()
            return Response({
                "message": "change task to Wating status",
            }, status=HTTP_200_OK)
        else:
            return Response({"message" : "this task cant change to Wating!"}, status=HTTP_406_NOT_ACCEPTABLE)


class ParticipantTask(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        task = Task.objects.filter(participant=profile)
        serialized_data = TaskSerializer(instance=task, many=True)
        data = serialized_data.data
        return Response(data, status=HTTP_200_OK)


class AssignerTask(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        task = Task.objects.filter(assigner=profile)
        serialized_data = TaskSerializer(instance=task, many=True)
        data = serialized_data.data
        return Response(data, status=HTTP_200_OK)


class TaskComment(APIView):

    permission_classes = [IsAuthenticated, IsParticipantORAssigner]
    serializer_class = CommentSerializer
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(

        operation_id='Create a comment',
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, ),
            openapi.Parameter('text', openapi.IN_FORM, type=openapi.TYPE_STRING),

        ],

    )
    def post(self, request, pk):
        profile = get_object_or_404(Profile, user=request.user)
        task = get_object_or_404(Task, id=pk)
        self.check_object_permissions(request, task)
        data = {
            'profile':profile.id,
            'text': request.data['text'],
            'task': pk,
            'file': request.data['file']
        }
        serialized_data = self.serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response({'message': "comment added successfully!"}, status=HTTP_201_CREATED)

    def get(self, request, pk):

        task = get_object_or_404(Task, id=pk)
        comments = Comment.objects.filter(task=task)
        serialized_data = CommentSerializer(instance=comments, many=True)
        data = serialized_data.data

        return Response(data, status=HTTP_200_OK)


class CommentView(APIView):

    permission_classes = [IsAuthenticated, IsOwnerORAdminORReadOnly]
    serializer_class = CommentSerializer
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(

        operation_id='update the comment',
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, ),
            openapi.Parameter('text', openapi.IN_FORM, type=openapi.TYPE_STRING),

        ],

    )
    def put(self, request, pk):

        try:
            comment = Comment.objects.get(id=pk)
            self.check_object_permissions(request, comment)
            serialized_data = CommentSerializer(instance=comment, data=request.data, partial=True)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()

            return Response(serialized_data.data, status=HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'message' : "comment Not found!"}, status=HTTP_404_NOT_FOUND)


    def get(self,request,pk):
        comment = Comment.objects.get(id=pk)
        serialized_data = CommentSerializer(instance=comment)
        return Response(serialized_data.data,status=HTTP_200_OK)

    def delete(self, request, pk):

        comment = get_object_or_404(Comment, id=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response({'message': f'deleted comment with id {comment.id}'}, status=HTTP_200_OK)






