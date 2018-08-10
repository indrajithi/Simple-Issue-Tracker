from rest_framework import generics, permissions
from .permissions import IsOwner
from rest_framework import generics
from .serializers import IssueSerializer
from .models import Issue


class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
       
        serializer.save(created_by=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)

