from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from .models import Comment, Post


def _post_dict(post):
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "category": post.category,
        "created_at": post.created_at.strftime("%Y/%m/%d"),
    }


def home(request):
    categories = Post.objects.values_list("category", flat=True).distinct()
    first = Post.objects.first()
    context = {
        "categories": categories,
        "posts": Post.objects.all(),
        "selected_post": first,
        "selected_analysis": first.analyses.first() if first else None,
        "selected_comments": first.comments.all() if first else Comment.objects.none(),
    }
    return render(request, "kendo/index.html", context)


def _detail_dict(post):
    analysis = post.analyses.first()
    return {
        "post": _post_dict(post),
        "analysis": {
            "score": analysis.score,
            "summary": analysis.summary,
            "created_at": analysis.created_at.strftime("%Y/%m/%d"),
        }
        if analysis
        else None,
        "comments": [
            {
                "id": c.id,
                "author": c.author,
                "body": c.body,
                "created_at": c.created_at.strftime("%Y/%m/%d %H:%M"),
            }
            for c in post.comments.all()
        ],
    }


@require_GET
def posts_json(request):
    category = request.GET.get("category", "")
    qs = Post.objects.all()
    if category and category != "all":
        qs = qs.filter(category=category)
    return JsonResponse({"posts": [_post_dict(post) for post in qs]})


@require_GET
def post_detail_json(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return JsonResponse(_detail_dict(post))


@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    body = (request.POST.get("body") or "").strip()
    author = (request.POST.get("author") or "").strip() or "名無しさん"
    if not body:
        return JsonResponse(
            {"ok": False, "error": "コメントを入力してください。"}, status=400
        )
    comment = Comment.objects.create(post=post, author=author, body=body)
    return JsonResponse(
        {
            "ok": True,
            "comment": {
                "id": comment.id,
                "author": comment.author,
                "body": comment.body,
                "created_at": comment.created_at.strftime("%Y/%m/%d %H:%M"),
            },
        }
    )