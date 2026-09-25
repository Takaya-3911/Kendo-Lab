from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from kendo.models import Comment, Post, PostImage


class Command(BaseCommand):
    help = "デモ用の投稿・コメントデータを作成します"

    def handle(self, *args, **options):
        # 既存のデモデータがあれば削除してから作り直す
        Comment.objects.all().delete()
        PostImage.objects.all().delete()
        Post.objects.all().delete()

        demo_video = "videos/demo.mp4"
        demo_image = "images/kendou01_16.png"

        now = timezone.now()

        demo_posts = [
            {
                "post_type": "video",
                "category": "正面素振り",
                "experience_period": "1年",
                "title": "【動画】正面素振り50本！息が上がると竹刀がブレてしまいます",
                "nickname": "はやて",
                "memo": "息が上がると竹刀がブレます。左手の力加減も教えてください。",
                "video": demo_video,
                "offset_hours": 0,
            },
            {
                "post_type": "image",
                "category": "中段の構え",
                "experience_period": "1ヶ月",
                "title": "【写真】中段の構え（正面）のチェックをお願いします",
                "nickname": "さくら剣士",
                "memo": "初心者です。構えの姿勢で気をつける点を教えてください。",
                "video": None,
                "offset_hours": 1,
            },
            {
                "post_type": "video",
                "category": "跳躍素振り（早素振り）",
                "experience_period": "2ヶ月",
                "title": "【初心者】跳躍素振り100本チャレンジ！刃筋を見てください",
                "nickname": "剣道はじめたて太郎",
                "memo": "100本続けると足がつらくなります。リズムの取り方のコツはありますか？",
                "video": demo_video,
                "offset_hours": 2,
            },
        ]

        posts = []
        for item in demo_posts:
            created_at = now - timedelta(hours=item["offset_hours"])
            post = Post.objects.create(
                post_type=item["post_type"],
                category=item["category"],
                experience_period=item["experience_period"],
                title=item["title"],
                nickname=item["nickname"],
                memo=item["memo"],
            )
            Post.objects.filter(pk=post.pk).update(created_at=created_at)
            if item["video"]:
                post.video.name = item["video"]
                post.save(update_fields=["video"])
            posts.append((post, item["video"]))
            self.stdout.write(self.style.SUCCESS(f"投稿を作成: {post.title}"))

        # 画像投稿には画像ファイルを1枚付ける
        image_post = Post.objects.filter(post_type="image").first()
        if image_post:
            image = PostImage(post=image_post)
            image.image.name = demo_image
            image.save()

        demo_comments = [
            {
                "nickname": "指導員の先生",
                "level": Comment.KendoLevel.INSTRUCTOR,
                "video_time_seconds": 12,
                "text": "手元が少し下がっています。竹刀は水平を意識しましょう。",
                "offset_hours": 0.05,
            },
            {
                "nickname": "三段",
                "level": Comment.KendoLevel.SANDAN,
                "video_time_seconds": 30,
                "text": "打ち込み後の残心が良いですね！",
                "offset_hours": 1.05,
            },
            {
                "nickname": "初段",
                "level": Comment.KendoLevel.SHODAN,
                "video_time_seconds": None,
                "text": "中段の構え、足の位置が良いと思います。肩に力が入らないように。",
                "offset_hours": 2.05,
            },
            {
                "nickname": "剣道歴1年",
                "level": Comment.KendoLevel.ONE_YEAR,
                "video_time_seconds": None,
                "text": "参考になります。ありがとうございます！",
                "offset_hours": 3.05,
            },
        ]

        for post, video in posts:
            for cmt in demo_comments:
                created_at = now - timedelta(hours=cmt["offset_hours"])
                comment = Comment.objects.create(
                    post=post,
                    nickname=cmt["nickname"],
                    level=cmt["level"],
                    video_time_seconds=cmt["video_time_seconds"],
                    comment=cmt["text"],
                )
                Comment.objects.filter(pk=comment.pk).update(created_at=created_at)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"コメントを作成: {post.title} -> {cmt['nickname']}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("デモデータの作成が完了しました"))