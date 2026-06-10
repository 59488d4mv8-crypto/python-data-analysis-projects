(function (window, document) {
  "use strict";

  var state = {
    data: null,
    currentQuizId: null,
    sidebarEl: null,
    sidebarContentEl: null,
    contentEl: null,
    answers: {},
    submitted: false,
    score: 0,
    editors: []
  };

  function isQuizDone(quizId) {
    if (!window.Achievements || typeof window.Achievements.getQuizResult !== "function") return null;
    return window.Achievements.getQuizResult(quizId);
  }

  function parseHash() {
    var hash = window.location.hash.replace(/^#\/?/, "");
    if (!hash) return null;
    var parts = hash.split("/").filter(function (x) { return x.length > 0; });
    if (parts.length >= 1 && parts[0].indexOf("q") === 0) {
      return { quizId: parts[0] };
    }
    return null;
  }

  function renderSidebar() {
    var sidebar = state.sidebarContentEl;
    if (!sidebar) return;
    sidebar.innerHTML = "";
    if (!state.data || !state.data.quizzes) {
      sidebar.innerHTML = '<div style="color: var(--text-soft); padding: 12px;">加载中...</div>';
      return;
    }

    var header = document.createElement("div");
    header.className = "sidebar-course-title";
    header.textContent = "测评列表";
    sidebar.appendChild(header);

    for (var i = 0; i < state.data.quizzes.length; i++) {
      var q = state.data.quizzes[i];
      var li = document.createElement("div");
      li.className = "sidebar-chapter";
      if (state.currentQuizId === q.quizId) li.classList.add("active");

      var doneInfo = isQuizDone(q.quizId);
      var doneMark = doneInfo ? '<span class="check">✓</span> ' : '<span class="dot">·</span> ';

      var link = document.createElement("a");
      link.href = "javascript:void(0)";
      link.innerHTML = doneMark + q.title;
      if (doneInfo && typeof doneInfo.score === "number") {
        var scoreBadge = document.createElement("span");
        scoreBadge.className = "quiz-score-badge";
        scoreBadge.textContent = doneInfo.score + "分";
        link.appendChild(scoreBadge);
      }
      (function (quizId) {
        link.addEventListener("click", function (e) {
          e.preventDefault();
          goToQuiz(quizId);
        });
      })(q.quizId);
      li.appendChild(link);
      sidebar.appendChild(li);
    }
  }

  function goToQuiz(quizId) {
    window.location.hash = "#/" + quizId;
    state.currentQuizId = quizId;
    state.answers = {};
    state.submitted = false;
    state.score = 0;
    state.editors = [];
    renderSidebar();
    renderQuiz(quizId);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function renderQuiz(quizId) {
    var contentEl = state.contentEl;
    if (!contentEl) return;
    contentEl.innerHTML = "";

    var quiz = null;
    if (state.data && state.data.quizzes) {
      for (var i = 0; i < state.data.quizzes.length; i++) {
        if (state.data.quizzes[i].quizId === quizId) {
          quiz = state.data.quizzes[i];
          break;
        }
      }
    }
    if (!quiz) {
      contentEl.innerHTML = "<p>未找到测评：" + quizId + "</p>";
      return;
    }

    var title = document.createElement("h1");
    title.className = "chapter-title";
    title.textContent = quiz.title;
    contentEl.appendChild(title);

    var desc = document.createElement("p");
    desc.className = "chapter-content-text";
    desc.textContent = "本测评包含 " + quiz.questions.length + " 道题目（选择题 + 编程题），完成后点击提交查看成绩与薄弱知识点。";
    contentEl.appendChild(desc);

    var doneInfo = isQuizDone(quizId);
    if (doneInfo && typeof doneInfo.score === "number") {
      var reattempt = document.createElement("div");
      reattempt.className = "chapter-section";
      reattempt.innerHTML = '<div style="padding: 12px 16px; background: rgba(37,99,235,0.08); border-radius: 8px; color: var(--text);">你之前已提交过该测评，历史得分为 <strong>' + doneInfo.score + ' 分</strong>。可以重新作答并提交（最新成绩将覆盖历史记录）。</div>';
      contentEl.appendChild(reattempt);
    }

    for (var qi = 0; qi < quiz.questions.length; qi++) {
      var q = quiz.questions[qi];
      if (q.type === "choice") {
        contentEl.appendChild(renderChoiceQuestion(q, qi));
      } else if (q.type === "coding") {
        contentEl.appendChild(renderCodingQuestion(q, qi));
      }
    }

    var footer = document.createElement("div");
    footer.className = "chapter-footer";

    var submitBtn = document.createElement("button");
    submitBtn.className = "btn btn-primary";
    submitBtn.textContent = "✓ 提交测评";
    submitBtn.addEventListener("click", function () {
      submitQuiz(quiz);
    });
    footer.appendChild(submitBtn);

    var resultBox = document.createElement("div");
    resultBox.id = "quizResultBox";
    resultBox.style.cssText = "margin-top: 16px; padding: 16px; border-radius: 8px; display: none; background: rgba(16,185,129,0.08); color: var(--text);";
    footer.appendChild(resultBox);

    contentEl.appendChild(footer);
  }

  function renderChoiceQuestion(q, idx) {
    var card = document.createElement("div");
    card.className = "quiz-question-card";

    var header = document.createElement("div");
    header.className = "block-header";
    header.innerHTML = '<span class="block-label exercise-label">选择题 ' + (idx + 1) + '</span> <span class="block-title">' + escapeHtml(q.prompt) + '</span>';
    card.appendChild(header);

    var opts = document.createElement("div");
    opts.className = "quiz-options";
    opts.style.marginTop = "12px";
    for (var i = 0; i < q.options.length; i++) {
      var btn = document.createElement("button");
      btn.className = "btn btn-ghost quiz-opt";
      btn.textContent = String.fromCharCode(65 + i) + ". " + q.options[i];
      btn.setAttribute("data-option-index", String(i));
      (function (qObj, question, optionIdx, button) {
        button.addEventListener("click", function () {
          var sibling = button.parentNode.querySelectorAll(".quiz-opt");
          for (var s = 0; s < sibling.length; s++) sibling[s].classList.remove("chosen");
          button.classList.add("chosen");
          state.answers[qObj.qid] = { type: "choice", chosen: optionIdx, correct: question.correctIndex };
        });
      })(q, q, i, btn);
      opts.appendChild(btn);
    }
    card.appendChild(opts);

    var expl = document.createElement("div");
    expl.className = "question-explanation";
    expl.textContent = "解析：" + (q.explanation || "");
    expl.style.display = "none";
    expl.style.marginTop = "10px";
    expl.style.color = "var(--text-soft)";
    card.appendChild(expl);

    card._explanation = expl;

    return card;
  }

  function renderCodingQuestion(q, idx) {
    var card = document.createElement("div");
    card.className = "quiz-question-card";

    var header = document.createElement("div");
    header.className = "block-header";
    header.innerHTML = '<span class="block-label exercise-label">编程题 ' + (idx + 1) + '</span> <span class="block-title">' + escapeHtml(q.prompt) + '</span>';
    card.appendChild(header);

    var textarea = document.createElement("textarea");
    textarea.textContent = q.starterCode || "";
    card.appendChild(textarea);

    var toolbar = document.createElement("div");
    toolbar.className = "exercise-toolbar";
    card.appendChild(toolbar);

    var checkBtn = document.createElement("button");
    checkBtn.className = "btn btn-primary";
    checkBtn.textContent = "▶ 运行自测";
    toolbar.appendChild(checkBtn);

    var hintBtn = document.createElement("button");
    hintBtn.className = "btn btn-ghost";
    hintBtn.textContent = "显示提示";
    toolbar.appendChild(hintBtn);

    var outputEl = document.createElement("div");
    outputEl.className = "code-output";
    card.appendChild(outputEl);

    var feedbackEl = document.createElement("div");
    feedbackEl.className = "exercise-feedback";
    feedbackEl.style.marginTop = "8px";
    card.appendChild(feedbackEl);

    var editor = window.CodeEditor.create(textarea, {
      outputEl: outputEl,
      plotsEl: null,
      runButton: checkBtn,
      runHandler: function () {}
    });
    state.editors.push(editor);

    checkBtn.addEventListener("click", function () {
      var userCode = textarea.value;
      var combinedCode = userCode + "\n" + (q.testCode || "");
      checkBtn.textContent = "运行中...";
      checkBtn.disabled = true;
      window.PyRunner.load().then(function () {
        return window.PyRunner.runCode(combinedCode, { timeoutMs: 8000, capturePlots: false });
      }).then(function (result) {
        checkBtn.textContent = "▶ 运行自测";
        checkBtn.disabled = false;
        editor.renderResult(result);
        if (result.ok) {
          feedbackEl.innerHTML = '<div class="feedback-ok">✓ 自测通过。提交后可计入总成绩。</div>';
          state.answers[q.qid] = { type: "coding", code: userCode, passed: true };
        } else {
          var errMsg = (result.error && (result.error.message || result.error.name)) || "执行失败";
          feedbackEl.innerHTML = '<div class="feedback-err">✗ 未通过：' + escapeHtml(errMsg) + '</div>';
          state.answers[q.qid] = { type: "coding", code: userCode, passed: false };
        }
      }).catch(function (err) {
        checkBtn.textContent = "▶ 运行自测";
        checkBtn.disabled = false;
        feedbackEl.innerHTML = '<div class="feedback-err">✗ 运行失败：' + err.message + '</div>';
      });
    });

    var hintBox = document.createElement("div");
    hintBox.className = "hint-box";
    hintBox.style.display = "none";
    if (q.hints && q.hints.length) {
      var hHtml = "<strong>提示：</strong><ul>";
      for (var hi = 0; hi < q.hints.length; hi++) hHtml += "<li>" + escapeHtml(q.hints[hi]) + "</li>";
      hHtml += "</ul>";
      hintBox.innerHTML = hHtml;
    } else {
      hintBox.innerHTML = "<em>暂无提示</em>";
    }
    card.appendChild(hintBox);

    hintBtn.addEventListener("click", function () {
      hintBox.style.display = hintBox.style.display === "none" ? "block" : "none";
    });

    return card;
  }

  function submitQuiz(quiz) {
    // 未作答的题目视作错误；统计；计算总分
    var choiceTotal = 0;
    var codingTotal = 0;
    var choiceCorrect = 0;
    var codingPassed = 0;
    var weakTags = [];

    for (var i = 0; i < quiz.questions.length; i++) {
      var q = quiz.questions[i];
      if (q.type === "choice") {
        choiceTotal++;
        var a = state.answers[q.qid];
        if (a && a.chosen === q.correctIndex) {
          choiceCorrect++;
        } else {
          weakTags.push("知识点：" + (q.prompt || "").slice(0, 30));
        }
      } else if (q.type === "coding") {
        codingTotal++;
        var ca = state.answers[q.qid];
        if (ca && ca.passed) {
          codingPassed++;
        } else {
          // 显示未通过信息
        }
      }
    }

    var totalQuestions = choiceTotal + codingTotal;
    var perChoice = choiceTotal > 0 ? Math.round(100 / totalQuestions) : 0;
    var perCoding = codingTotal > 0 ? Math.round(100 / totalQuestions) : 0;
    // 简单均分：每题 100 / totalQuestions 分
    var perQ = totalQuestions > 0 ? 100 / totalQuestions : 0;
    var score = Math.round((choiceCorrect + codingPassed) * perQ);
    state.score = score;
    state.submitted = true;

    var box = document.getElementById("quizResultBox");
    if (box) {
      box.style.display = "block";
      box.style.background = "rgba(16,185,129,0.10)";
      var weakHtml = "";
      if (weakTags.length > 0) {
        weakHtml = '<div style="margin-top: 10px; color: var(--text-soft); font-size: 0.92rem;">薄弱知识点：' + weakTags.slice(0, 4).map(function (t) { return "• " + t; }).join(" ") + "</div>";
      }
      box.innerHTML =
        '<div style="font-size: 1.2rem; font-weight: 700;">你的成绩：' + score + ' 分 / 100</div>' +
        '<div style="margin-top: 8px; color: var(--text-soft);">选择题：' + choiceCorrect + ' / ' + choiceTotal + '；编程题：' + codingPassed + ' / ' + codingTotal + '</div>' +
        weakHtml;
    }

    // 积分 & 徽章
    if (window.Achievements && typeof window.Achievements.awardQuizPass === "function") {
      window.Achievements.awardQuizPass(quiz.quizId, score);
    }

    renderSidebar();
  }

  function init() {
    state.sidebarEl = document.getElementById("sidebar");
    state.sidebarContentEl = document.getElementById("sidebarContent");
    state.contentEl = document.getElementById("quizContent");

    if (!state.sidebarEl || !state.contentEl) return;

    fetch("assets/data/quizzes.json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        state.data = data;
        var route = parseHash();
        if (route && route.quizId) {
          goToQuiz(route.quizId);
        } else if (data.quizzes && data.quizzes.length > 0) {
          goToQuiz(data.quizzes[0].quizId);
        }
      })
      .catch(function (err) {
        if (state.contentEl) {
          state.contentEl.innerHTML = '<div class="card"><p style="color:#ef4444;">加载测评数据失败：' + err.message + '</p></div>';
        }
      });

    window.addEventListener("hashchange", function () {
      var route = parseHash();
      if (route && route.quizId && route.quizId !== state.currentQuizId) {
        goToQuiz(route.quizId);
      }
    });
  }

  window.QuizView = { init: init };
})(window, document);
