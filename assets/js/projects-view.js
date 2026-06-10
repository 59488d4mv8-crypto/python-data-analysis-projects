(function (window, document) {
  "use strict";

  // ===== 项目学习视图：10 个项目列表 + 右侧项目内容 =====
  // 暴露 window.ProjectsView = { init() }

  var PROGRESS_KEY = "pydataedu.projectsProgress";
  var state = {
    data: null,
    currentProjectId: null,
    sidebarEl: null,
    sidebarContentEl: null,
    contentEl: null,
    editors: []
  };

  // ===== 进度存取 =====
  function loadProgress() {
    try {
      var raw = localStorage.getItem(PROGRESS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function saveProgress(p) {
    try {
      localStorage.setItem(PROGRESS_KEY, JSON.stringify(p));
    } catch (e) {}
  }

  function markProjectDone(projectId) {
    var p = loadProgress();
    if (!p[projectId]) p[projectId] = {};
    p[projectId].done = true;
    saveProgress(p);
    if (window.Achievements && typeof window.Achievements.awardChapterComplete === "function") {
      window.Achievements.awardChapterComplete(projectId);
    }
  }

  function isProjectDone(projectId) {
    var p = loadProgress();
    return !!(p[projectId] && p[projectId].done);
  }

  // ===== Hash 路由 =====
  function parseHash() {
    var hash = window.location.hash.replace(/^#\/?/, "");
    if (!hash) return null;
    return hash;
  }

  function goToProject(projectId) {
    window.location.hash = "#/" + projectId;
    state.currentProjectId = projectId;
    renderSidebar();
    renderProject(projectId);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // ===== 查找数据 =====
  function findProject(projectId) {
    if (!state.data || !state.data.projects) return null;
    for (var i = 0; i < state.data.projects.length; i++) {
      if (state.data.projects[i].projectId === projectId) return state.data.projects[i];
    }
    return null;
  }

  // ===== 辅助 =====
  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (typeof text !== "undefined") node.textContent = text;
    return node;
  }

  // ===== 目录树渲染 =====
  function renderSidebar() {
    var sidebar = state.sidebarContentEl;
    if (!sidebar) return;
    sidebar.innerHTML = "";
    if (!state.data) {
      sidebar.innerHTML = '<div style="color: var(--text-soft); padding: 12px;">加载中...</div>';
      return;
    }

    var header = el("div", "sidebar-course-title", "项目实战");
    sidebar.appendChild(header);

    var projects = state.data.projects || [];
    var list = el("ul", "sidebar-chapter-list");
    for (var i = 0; i < projects.length; i++) {
      var project = projects[i];
      var li = el("li", "sidebar-chapter");
      if (state.currentProjectId === project.projectId) li.classList.add("active");
      if (isProjectDone(project.projectId)) li.classList.add("done");

      var link = el("a");
      link.href = "javascript:void(0)";
      var doneIcon = isProjectDone(project.projectId)
        ? '<span class="check">✓</span> '
        : '<span class="dot">·</span> ';
      link.innerHTML = doneIcon + String(i + 1).padStart(2, "0") + ". " + project.title;
      (function (pid) {
        link.addEventListener("click", function (e) {
          e.preventDefault();
          goToProject(pid);
        });
      })(project.projectId);

      li.appendChild(link);
      list.appendChild(li);
    }
    sidebar.appendChild(list);
  }

  // ===== 代码块 =====
  function createCodeSampleBlock(sample) {
    var card = el("div", "code-sample-card");

    var header = el("div", "block-header");
    header.innerHTML = '<span class="block-label">代码</span> <span class="block-title">' + (sample.title || "") + '</span>';
    card.appendChild(header);

    if (sample.description) {
      var expl = el("div", "block-explanation", sample.description);
      card.appendChild(expl);
    }

    var textarea = el("textarea");
    textarea.textContent = sample.code || "";
    card.appendChild(textarea);

    var outputEl = el("div", "code-output");
    card.appendChild(outputEl);

    var plotsEl = el("div", "code-plots");
    card.appendChild(plotsEl);

    var sampleId = sample.id || ("ps_" + Math.random().toString(36).slice(2, 8));

    if (window.Achievements && typeof window.Achievements.recordCodeSampleView === "function") {
      window.Achievements.recordCodeSampleView(sampleId);
    }

    var editor = window.CodeEditor.create(textarea, {
      outputEl: outputEl,
      plotsEl: plotsEl,
      runHandler: function (code) {
        if (!window.PyRunner) {
          outputEl.innerHTML = '<div style="color:#ef4444;">PyRunner 未加载</div>';
          return;
        }
        window.PyRunner.load().then(function () {
          return window.PyRunner.runCode(code, { timeoutMs: 8000, capturePlots: true });
        }).then(function (result) {
          editor.renderResult(result);
          if (result.ok && window.Achievements && typeof window.Achievements.recordCodeRun === "function") {
            window.Achievements.recordCodeRun(sampleId);
          }
        }).catch(function (err) {
          outputEl.innerHTML = '<div style="color:#ef4444;">运行失败: ' + err.message + '</div>';
        });
      }
    });

    state.editors.push(editor);
    return card;
  }

  // ===== 练习块 =====
  function createExerciseBlock(exercise, projectId) {
    var card = el("div", "exercise-card");
    var exId = exercise.exerciseId || ("ex_" + Math.random().toString(36).slice(2, 8));

    var header = el("div", "block-header");
    header.innerHTML = '<span class="block-label exercise-label">练习</span> <span class="block-title">' + (exercise.prompt ? exercise.prompt.slice(0, 80) + (exercise.prompt.length > 80 ? "..." : "") : "练习") + '</span>';
    card.appendChild(header);

    var prompt = el("div", "exercise-prompt", exercise.prompt || "");
    card.appendChild(prompt);

    var textarea = el("textarea");
    textarea.textContent = exercise.starterCode || "";
    card.appendChild(textarea);

    var toolbar = el("div", "exercise-toolbar");
    card.appendChild(toolbar);

    var checkBtn = el("button", "btn btn-primary", "▶ 检查答案");
    toolbar.appendChild(checkBtn);

    var hintBtn = el("button", "btn btn-ghost", "显示提示");
    toolbar.appendChild(hintBtn);

    var answerBtn = el("button", "btn btn-ghost", "参考答案");
    toolbar.appendChild(answerBtn);

    var feedbackEl = el("div", "exercise-feedback");
    card.appendChild(feedbackEl);

    var outputEl = el("div", "code-output");
    card.appendChild(outputEl);

    var editor = window.CodeEditor.create(textarea, {
      outputEl: outputEl,
      plotsEl: null,
      runButton: checkBtn,
      runHandler: function () {}
    });

    state.editors.push(editor);

    checkBtn.addEventListener("click", function () {
      var userCode = textarea.value;
      var combinedCode = userCode + "\n" + (exercise.testCode || "");
      checkBtn.textContent = "运行中...";
      checkBtn.disabled = true;

      window.PyRunner.load().then(function () {
        return window.PyRunner.runCode(combinedCode, { timeoutMs: 8000, capturePlots: false });
      }).then(function (result) {
        checkBtn.textContent = "▶ 检查答案";
        checkBtn.disabled = false;
        editor.renderResult(result);

        if (result.ok) {
          feedbackEl.innerHTML = '<div class="feedback-ok">✓ 正确！所有断言通过。</div>';
          if (window.Achievements && typeof window.Achievements.awardExerciseCorrect === "function") {
            window.Achievements.awardExerciseCorrect(exId, true);
          }
        } else {
          var errMsg = (result.error && (result.error.message || result.error.name)) || "执行失败";
          feedbackEl.innerHTML = '<div class="feedback-err">✗ 未通过：' + escapeHtml(errMsg) + '</div>';
        }
      }).catch(function (err) {
        checkBtn.textContent = "▶ 检查答案";
        checkBtn.disabled = false;
        feedbackEl.innerHTML = '<div class="feedback-err">✗ 运行失败: ' + err.message + '</div>';
      });
    });

    var hintBox = el("div", "hint-box");
    hintBox.style.display = "none";
    if (exercise.hints && exercise.hints.length) {
      var hintHtml = "<strong>提示：</strong><ul>";
      for (var i = 0; i < exercise.hints.length; i++) {
        hintHtml += "<li>" + escapeHtml(exercise.hints[i]) + "</li>";
      }
      hintHtml += "</ul>";
      hintBox.innerHTML = hintHtml;
    } else {
      hintBox.innerHTML = "<em>暂无提示</em>";
    }
    card.appendChild(hintBox);

    hintBtn.addEventListener("click", function () {
      hintBox.style.display = hintBox.style.display === "none" ? "block" : "none";
    });

    var answerBox = el("div", "answer-box");
    answerBox.style.display = "none";
    if (exercise.referenceAnswer) {
      var ansPre = el("pre");
      ansPre.textContent = exercise.referenceAnswer;
      answerBox.appendChild(ansPre);
    } else {
      answerBox.innerHTML = "<em>暂无参考答案</em>";
    }
    card.appendChild(answerBox);

    answerBtn.addEventListener("click", function () {
      answerBox.style.display = answerBox.style.display === "none" ? "block" : "none";
    });

    return card;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // ===== 徽标 =====
  function renderBadge(text, cls) {
    var span = el("span", "project-badge " + (cls || ""), text);
    return span;
  }

  // ===== 项目内容渲染 =====
  function renderProject(projectId) {
    var contentEl = state.contentEl;
    if (!contentEl) return;
    state.editors = [];
    contentEl.innerHTML = "";

    var project = findProject(projectId);
    if (!project) {
      contentEl.innerHTML = "<p>未找到项目：" + projectId + "</p>";
      return;
    }

    // 标题区
    var titleWrap = el("div", "project-title-wrap");
    var h1 = el("h1", "project-title", project.title);
    titleWrap.appendChild(h1);

    if (project.subtitle) {
      var sub = el("div", "project-subtitle", project.subtitle);
      titleWrap.appendChild(sub);
    }

    var badgeRow = el("div", "project-badges");
    badgeRow.appendChild(renderBadge("难度：" + (project.difficulty || "-"), "project-badge-difficulty"));
    badgeRow.appendChild(renderBadge("时长：" + (project.duration || "-"), "project-badge-duration"));
    if (project.tags && project.tags.length) {
      for (var i = 0; i < project.tags.length; i++) {
        badgeRow.appendChild(renderBadge(project.tags[i], "project-badge-tag"));
      }
    }
    titleWrap.appendChild(badgeRow);
    contentEl.appendChild(titleWrap);

    // 业务目标卡片
    if (project.businessGoal) {
      var goalCard = el("div", "info-card goal-card");
      var gh = el("div", "block-header");
      gh.innerHTML = '<span class="block-label">业务目标</span>';
      goalCard.appendChild(gh);
      var gp = el("div", "info-card-content", project.businessGoal);
      goalCard.appendChild(gp);
      contentEl.appendChild(goalCard);
    }

    // 业务背景卡片
    if (project.businessBackground) {
      var bgCard = el("div", "info-card bg-card");
      var bh = el("div", "block-header");
      bh.innerHTML = '<span class="block-label">业务背景</span>';
      bgCard.appendChild(bh);
      var bp = el("div", "info-card-content", project.businessBackground);
      bgCard.appendChild(bp);
      contentEl.appendChild(bgCard);
    }

    // 数据方案卡片
    if (project.dataPlan) {
      var dpCard = el("div", "info-card dp-card");
      var dh = el("div", "block-header");
      dh.innerHTML = '<span class="block-label">数据方案</span>';
      dpCard.appendChild(dh);
      var dpContent = el("div", "info-card-content");
      var lines = String(project.dataPlan).split("\n");
      for (var i = 0; i < lines.length; i++) {
        if (lines[i].trim() === "") continue;
        var line = el("div", "info-card-line", lines[i]);
        dpContent.appendChild(line);
      }
      dpCard.appendChild(dpContent);
      contentEl.appendChild(dpCard);
    }

    // 代码示例
    if (project.codeSamples && project.codeSamples.length) {
      var codeWrap = el("div", "project-section");
      var codeTitle = el("h2", "section-title", "💻 代码示例");
      codeWrap.appendChild(codeTitle);
      for (var ci2 = 0; ci2 < project.codeSamples.length; ci2++) {
        codeWrap.appendChild(createCodeSampleBlock(project.codeSamples[ci2]));
      }
      contentEl.appendChild(codeWrap);
    }

    // 练习
    if (project.exercises && project.exercises.length) {
      var exWrap = el("div", "project-section");
      var exTitle = el("h2", "section-title", "✏️ 动手练习");
      exWrap.appendChild(exTitle);
      for (var ei = 0; ei < project.exercises.length; ei++) {
        exWrap.appendChild(createExerciseBlock(project.exercises[ei], projectId));
      }
      contentEl.appendChild(exWrap);
    }

    // 交付物
    if (project.deliverables && project.deliverables.length) {
      var delWrap = el("div", "project-section");
      var delTitle = el("h2", "section-title", "📦 业务交付物");
      delWrap.appendChild(delTitle);
      var delList = el("ul", "deliverables-list");
      for (var di = 0; di < project.deliverables.length; di++) {
        var li = el("li", "deliverable-item", project.deliverables[di]);
        delList.appendChild(li);
      }
      delWrap.appendChild(delList);
      contentEl.appendChild(delWrap);
    }

    // 底部完成按钮
    var footer = el("div", "project-footer");
    var markBtn = el("button", "btn btn-primary mark-done-btn");
    var doneNow = isProjectDone(projectId);
    markBtn.textContent = doneNow ? "✓ 已完成本项目" : "✓ 标记项目完成";
    markBtn.disabled = doneNow;
    markBtn.addEventListener("click", function () {
      markProjectDone(projectId);
      markBtn.textContent = "✓ 已完成本项目";
      markBtn.disabled = true;
      renderSidebar();
    });
    footer.appendChild(markBtn);
    contentEl.appendChild(footer);
  }

  // ===== 默认定位到第一个项目 =====
  function defaultProject() {
    if (!state.data || !state.data.projects || state.data.projects.length === 0) return null;
    return state.data.projects[0].projectId;
  }

  // ===== 主入口 =====
  function init() {
    state.sidebarEl = document.getElementById("sidebar");
    state.sidebarContentEl = document.getElementById("sidebarContent");
    state.contentEl = document.getElementById("projectContent");

    if (!state.sidebarEl || !state.sidebarContentEl || !state.contentEl) {
      console.warn("ProjectsView.init: 未找到 sidebar / sidebarContent / projectContent 元素");
      return;
    }

    fetch("assets/data/projects.json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        state.data = data;
        var projectId = parseHash();
        if (!projectId) {
          var def = defaultProject();
          if (def) {
            goToProject(def);
          } else {
            state.contentEl.innerHTML = "<p>暂无项目数据</p>";
          }
        } else {
          state.currentProjectId = projectId;
          renderSidebar();
          renderProject(projectId);
        }
      })
      .catch(function (err) {
        if (state.contentEl) {
          state.contentEl.innerHTML = '<p style="color:#ef4444;">加载项目数据失败：' + err.message + '</p>';
        }
      });

    window.addEventListener("hashchange", function () {
      var projectId = parseHash();
      if (projectId) {
        state.currentProjectId = projectId;
        renderSidebar();
        renderProject(projectId);
      }
    });
  }

  window.ProjectsView = {
    init: init
  };

})(window, document);
