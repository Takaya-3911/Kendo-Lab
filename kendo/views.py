from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Post, PostImage
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        video_list = data.pop('video', None)
        video = video_list[0] if isinstance(video_list, list) else video_list

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        if video:
            post.video.save(video.name, video, save=True)

        for image in request.FILES.getlist('images'):
            PostImage.objects.create(post=post, image=image)

        return Response(self.get_serializer(post).data, status=status.HTTP_201_CREATED)