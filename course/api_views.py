from rest_framework.views import APIView
from rest_framework import generics, viewsets, status
from .models import Subject, Course, Comment
from .serializers import SubjectSerializer, CourseSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import CombinedCustomPermission
from rest_framework.response import Response


# SUBJECT CRUD
class SubjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer



class SubjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# COURSE CRUD
class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer




class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer




class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CombinedCustomPermission]
    # permission_classes = [IsSuperUserOnly, IsEvenYearPermission, AllowPutPatchOnly]




class CoursePutOnlyView(APIView):
    permission_classes = [CombinedCustomPermission]

    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
