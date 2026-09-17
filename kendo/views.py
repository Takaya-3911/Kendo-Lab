from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Post, PostImage
from .serializers import PostSerializer


def main_view(request):
    # 1. DBに存在するカテゴリ一覧を動的に取得（重複を除外）
    db_categories = list(
        Post.objects.values_list("category", flat=True).distinct()
    )
    # 空文字やNoneを除外
    db_categories = [c for c in db_categories if c]
    filters = ["すべて"] + db_categories

    # 2. URLパラメータから選択されたカテゴリを取得
    selected_category = request.GET.get("category", "すべて")

    # 3. 最新順で投稿を取得
    posts_queryset = Post.objects.all().order_by("-created_at")

    # 4. カテゴリで絞り込み
    if selected_category != "すべて":
        posts_queryset = posts_queryset.filter(category=selected_category)

    # 5. サイドバー用に最大5件取得
    sidebar_posts = posts_queryset[:5]

    # 6. メイン画面（左側）で大きく表示する1件を選択
    selected_id = request.GET.get("selected_id")
    selected_post = None

    if selected_id:
        selected_post = Post.objects.filter(id=selected_id).first()

    if not selected_post and sidebar_posts:
        selected_post = sidebar_posts[0]

    context = {
        "posts": sidebar_posts,
        "selected_post": selected_post,
        "selected_category": selected_category,
        "filters": filters,  # 動的に生成したカテゴリフィルター
    }

    return render(request, "kendo/main.html", context)


def video_sidebar_view(request):
    # 稽古種目フィルターのリスト
    filters = ['すべて', '正面素振り', '中段の構え', '跳躍素振り（早素振り）', '左右素振り', '胴打ち・その他']

    # 他の剣士の稽古動画・画像データ（仮のデータ）
    dummy_videos = [
        {
            'id': 1,
            'title': '【動画】跳躍素振り50本！息が上がると竹刀がブレてしまいます',
            'user_name': 'はやて',
            'user_role': '初心者 (半年)',
            'score': 78,
            'type': '動画',
        },
        {
            'id': 2,
            'title': '【写真3枚】中段の構え（正面・側面・足元）のチェックをお願いします',
            'user_name': 'さくら剣士',
            'user_role': '初心者 (1ヶ月)',
            'score': 89,
            'type': '3枚',
        },
        {
            'id': 3,
            'title': '【初心者】正面素振り100本チャレンジ！刃筋と左手の位置を見てください',
            'user_name': '剣道はじめたて太郎',
            'user_role': '初心者 (2ヶ月)',
            'score': 84,
            'type': '動画',
        },
    ]

    context = {
        'filters': filters,
        'dummy_videos': dummy_videos,
        'selected_filter': 'すべて',
    }

    return render(request, 'kendo/video_sidebar.html', context)


def registration_view(request):
    return render(request, 'kendo/register.html')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        # 大きな動画ファイルは一時ファイルになるため、
        # request.data.copy() だと「コピーできない」エラーになる。
        # ファイルは request.FILES から直接取り出し、
        # テキストデータのみを dict で組み立てる。
        video = request.FILES.get('video')

        data = {
            'post_type': request.data.get('post_type'),
            'category': request.data.get('category'),
            'experience_period': request.data.get('experience_period'),
            'title': request.data.get('title'),
            'nickname': request.data.get('nickname'),
            'memo': request.data.get('memo'),
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        if video:
            post.video.save(video.name, video, save=True)

        for image in request.FILES.getlist('images'):
            PostImage.objects.create(post=post, image=image)

        return Response(self.get_serializer(post).data, status=status.HTTP_201_CREATED)