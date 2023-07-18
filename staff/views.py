import datetime

from pytz import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from staff.models import Profile, Team, Presentation
from staff.pagination import StandardResultsSetPagination
from staff.permissions import IsPresenterOrAdminUserOrReadOnly
from staff.serializers import ProfileSerializers, TeamSerializers, DurationSerializers, PresentationSerializers
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.generics import GenericAPIView, get_object_or_404

from tasks.permissions import IsTeamLeader


class Profile_view(APIView):

    def get(self, request):
        profiles = Profile.objects.all()
        pr_serializer = ProfileSerializers(instance=profiles, many=True)
        pr_json = pr_serializer.data
        return Response(pr_json, status=HTTP_200_OK)


class All_Team_view(APIView):

    def get(self, request):
        teams = Team.objects.all().order_by('name')
        t_serializer = TeamSerializers(instance=teams, many=True)
        team_json = t_serializer.data
        return Response(team_json, status=HTTP_200_OK)


class LogoutView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message':f"Bye {request.user.username}"})


class EndTimeSet(APIView):
    permission_classes = (IsAuthenticated,IsPresenterOrAdminUserOrReadOnly)

    def put(self, request, pk):
        presentation = get_object_or_404(Presentation, id=pk)
        self.check_object_permissions(request, presentation)
        if presentation.is_updated or  presentation.date != datetime.datetime.now().astimezone(timezone('Asia/Tehran')).date():
            return Response({"message":'access denied'}, status=HTTP_403_FORBIDDEN)
        presentation.end_time = datetime.datetime.now().astimezone(timezone('Asia/Tehran')).time()
        presentation.is_updated = True
        serialize_data = PresentationSerializers(instance=presentation)
        data = serialize_data.data
        presentation.save()
        return Response(data, status=HTTP_200_OK)


class PresentationView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            presentation = Presentation.objects.create(profile=profile)
            return Response({"message": 'presentation created successfully'}, status=HTTP_201_CREATED)

        except Profile.DoesNotExist:
            return Response({"message": 'profile not found'}, status=HTTP_404_NOT_FOUND)


class ShowPersonalPresentation(ListAPIView):

    serializer_class = PresentationSerializers
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        profile = Profile.objects.get(user=self.request.user)

        self.queryset = Presentation.objects.filter(profile=profile).order_by('-date')
        return self.queryset



