"""{Kendo} ブランチの画面（index.html / hero.html / _side-bar.html / main.js）を
main のデータ構造で動かすためのつなぎ。

テンプレートと main.js が期待する項目名に合わせて、main のモデルを読み替える。
  Post.content   -> Post.memo
  Comment.author -> Comment.nickname
  Comment.body   -> Comment.comment
AI 分析（AiAnalysis）は main に無いため、常に「未分析」として扱う。
"""
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from .models import Comment, Post


def _post_view(post):
    return {
        "id": post.id,
        "title": post.title,
        "content": post.memo,
        "category": post.category,
        "created_at": post.created_at,
    }


def _comment_view(comment):
    return {
        "id": comment.id,
        "author": comment.nickname,
        "body": comment.comment,
        "created_at": comment.created_at,
    }


def _comments_of(post):
    # {Kendo} の画面は古い順に並べて、新しいコメントを下に追加する
    return post.comments.order_by("created_at")


def _post_dict(post):
    return {
        **_post_view(post),
        "created_at": post.created_at.strftime("%Y/%m/%d"),
    }


def _comment_dict(comment):
    return {
        **_comment_view(comment),
        "created_at": comment.created_at.strftime("%Y/%m/%d %H:%M"),
    }


def home(request):
    posts = Post.objects.order_by("-created_at")
    categories = posts.values_list("category", flat=True).distinct()
    first = posts.first()
    context = {
        "categories": categories,
        "posts": [_post_view(post) for post in posts],
        "selected_post": _post_view(first) if first else None,
        "selected_analysis": None,
        "selected_comments": (
            [_comment_view(c) for c in _comments_of(first)] if first else []
        ),
    }
    return render(request, "kendo/index.html", context)


@require_GET
def posts_json(request):
    category = request.GET.get("category", "")
    qs = Post.objects.order_by("-created_at")
    if category and category != "all":
        qs = qs.filter(category=category)
    return JsonResponse({"posts": [_post_dict(post) for post in qs]})


@require_GET
def post_detail_json(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return JsonResponse(
        {
            "post": _post_dict(post),
            "analysis": None,
            "comments": [_comment_dict(c) for c in _comments_of(post)],
        }
    )


@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    body = (request.POST.get("body") or "").strip()
    author = (request.POST.get("author") or "").strip() or "名無しさん"
    if not body:
        return JsonResponse(
            {"ok": False, "error": "コメントを入力してください。"}, status=400
        )
    comment = Comment.objects.create(post=post, nickname=author, comment=body)
    return JsonResponse({"ok": True, "comment": _comment_dict(comment)})
