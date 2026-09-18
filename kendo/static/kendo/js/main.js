// Kendo Lab - main.js
document.addEventListener("DOMContentLoaded", () => {
  /* ---------- ヘッダー影 ---------- */
  const header = document.querySelector(".site-header");
  const onScroll = () => {
    header.style.boxShadow =
      window.scrollY > 10 ? "0 6px 20px rgba(43, 38, 34, 0.08)" : "none";
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- ユーティリティ ---------- */
  const escapeHtml = (str) =>
    str.replace(
      /[&<>"']/g,
      (ch) =>
        ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
          ch
        ]
    );

  const $ = (id) => document.getElementById(id);

  const state = {
    currentPostId: Number($("comment-post-id")?.value) || null,
    currentCategory: "all",
  };

  const tabs = document.querySelectorAll(".sb-link");
  const postList = $("post-list");

  const detailCategory = $("detail-category");
  const detailTitle = $("detail-title");
  const detailDate = $("detail-date");
  const detailBody = $("detail-body");
  const commentPostId = $("comment-post-id");
  const commentList = $("comment-list");

  /* ---------- 描画関数 ---------- */
  const renderPostList = (posts) => {
    postList.innerHTML = posts
      .map(
        (post) => `
        <button type="button" class="post-link${
          post.id === state.currentPostId ? " active" : ""
        }"
                data-post-id="${post.id}"
                ${post.id === state.currentPostId ? 'aria-current="true"' : ""}>
          <span class="post-link-title">${escapeHtml(post.title)}</span>
          <span class="post-cat">${escapeHtml(post.category)}</span>
        </button>`
      )
      .join("");

    if (posts.length === 0) {
      postList.innerHTML =
        '<p class="post-empty">このカテゴリには投稿がありません。</p>';
      return;
    }

    postList.querySelectorAll(".post-link").forEach((btn) => {
      btn.addEventListener("click", () => loadDetail(Number(btn.dataset.postId)));
    });
  };

  const highlightPost = (id) => {
    postList.querySelectorAll(".post-link").forEach((btn) => {
      const active = Number(btn.dataset.postId) === id;
      btn.classList.toggle("active", active);
      if (active) btn.setAttribute("aria-current", "true");
      else btn.removeAttribute("aria-current");
    });
  };

  const renderDetail = (post) => {
    detailCategory.textContent = post.category;
    detailTitle.textContent = post.title;
    detailDate.textContent = post.created_at;
    detailBody.textContent = post.content;
    commentPostId.value = post.id;
    state.currentPostId = post.id;
    highlightPost(post.id);
  };

  const renderAnalysis = (analysis) => {
    const scoreBox = $("ai-score-box");
    const score = $("ai-score");
    const summary = $("ai-summary");
    const aiDate = $("ai-date");
    if (!scoreBox || !summary) return;
    if (analysis) {
      scoreBox.hidden = false;
      score.textContent = analysis.score;
      scoreBox.style.setProperty("--score", `${analysis.score}%`);
      summary.textContent = analysis.summary;
      summary.classList.remove("ai-empty");
      aiDate.textContent = `${analysis.created_at} の分析結果`;
      aiDate.hidden = false;
    } else {
      scoreBox.hidden = true;
      aiDate.hidden = true;
      summary.textContent =
        "この投稿はまだ分析されていません。動画・画像をアップロードすると AI が解析します。";
      summary.classList.add("ai-empty");
    }
  };

  const renderComments = (comments) => {
    commentList.querySelectorAll(".comment-item").forEach((el) => el.remove());
    const empty = commentList.querySelector(".comment-empty");
    if (empty) empty.remove();
    if (comments.length === 0) {
      const p = document.createElement("p");
      p.className = "comment-empty";
      p.textContent = "まだコメントはありません。最初のコメントを投稿してみましょう。";
      commentList.appendChild(p);
      return;
    }
    comments.forEach((c) => commentList.appendChild(commentItem(c)));
  };

  const commentItem = (c) => {
    const div = document.createElement("div");
    div.className = "comment-item";
    div.dataset.commentId = c.id;
    const meta = document.createElement("div");
    meta.className = "comment-meta";
    const strong = document.createElement("strong");
    strong.textContent = c.author;
    const time = document.createElement("time");
    time.textContent = c.created_at;
    meta.append(strong, time);
    const p = document.createElement("p");
    p.textContent = c.body;
    div.append(meta, p);
    return div;
  };

  /* ---------- API ---------- */
  const loadDetail = async (id) => {
    if (id === state.currentPostId) return;
    try {
      const res = await fetch(`/posts/${id}/`);
      if (!res.ok) throw new Error("not found");
      const data = await res.json();
      renderDetail(data.post);
      renderAnalysis(data.analysis);
      renderComments(data.comments);
    } catch (err) {
      console.error("投稿詳細の取得に失敗しました:", err);
    }
  };

  const loadPosts = async (category) => {
    try {
      const res = await fetch(`/posts/?category=${encodeURIComponent(category)}`);
      if (!res.ok) throw new Error("bad request");
      const data = await res.json();
      renderPostList(data.posts);
      if (data.posts.length > 0) {
        loadDetail(data.posts[0].id);
      } else {
        state.currentPostId = null;
      }
    } catch (err) {
      console.error("投稿一覧の取得に失敗しました:", err);
    }
  };

  /* ---------- カテゴリタブ ---------- */
  tabs.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabs.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.currentCategory = btn.dataset.category;
      loadPosts(state.currentCategory);
    });
  });

  /* ---------- コメント投稿 ---------- */
  const commentForm = $("comment-form");
  if (commentForm) {
    commentForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = e.currentTarget;
      const body = $("comment-body").value.trim();
      const author = $("comment-author").value.trim();
      const error = $("comment-error");

      if (!body) {
        error.textContent = "コメントを入力してください。";
        error.hidden = false;
        return;
      }

      const token = form.querySelector("input[name=csrfmiddlewaretoken]").value;
      const postId = commentPostId.value;

      try {
        const res = await fetch(`/posts/${postId}/comments/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-CSRFToken": token,
          },
          body: new URLSearchParams({ author, body }).toString(),
        });
        const data = await res.json();
        if (!data.ok) throw new Error(data.error || "投稿に失敗しました");
        error.hidden = true;
        $("comment-body").value = "";
        $("comment-author").value = "";
        const empty = commentList.querySelector(".comment-empty");
        if (empty) empty.remove();
        commentList.appendChild(commentItem(data.comment));
      } catch (err) {
        error.textContent = err.message || "コメントの投稿に失敗しました。";
        error.hidden = false;
      }
    });
  }
});