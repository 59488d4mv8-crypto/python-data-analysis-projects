(function (window, document) {
  "use strict";

  // ===== 课程视图：目录树 + 章节内容 + 进度 =====
  // 暴露 window.CourseView = { init(), renderSidebar(), renderChapter(), goToChapter() }

  var PROGRESS_KEY = "pydataedu.courseProgress";
  var state = {
    data: null,
    currentCourseId: null,
    currentUnitId: null,
    currentChapterId: null,
    sidebarEl: null,
    sidebarContentEl: null,
    contentEl: null,
    editors: []
  };

  // ============== 进度存取 ==============
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

  function markChapterDone(chapterId) {
    var p = loadProgress();
    if (!p[chapterId]) p[chapterId] = {};
    p[chapterId].done = true;
    saveProgress(p);
    if (window.Achievements && typeof window.Achievements.awardChapterComplete === "function") {
      window.Achievements.awardChapterComplete(chapterId);
    }
  }

  function isChapterDone(chapterId) {
    var p = loadProgress();
    return !!(p[chapterId] && p[chapterId].done);
  }

  function markExerciseDone(chapterId, exerciseId) {
    var p = loadProgress();
    if (!p[chapterId]) p[chapterId] = { done: false, exercisesDone: [] };
    if (!p[chapterId].exercisesDone) p[chapterId].exercisesDone = [];
    if (p[chapterId].exercisesDone.indexOf(exerciseId) === -1) {
      p[chapterId].exercisesDone.push(exerciseId);
    }
    saveProgress(p);
  }

  // ============== Hash 路由 ==============
  function parseHash() {
    // 期望: course.html#/c01/u01/ch0101
    var hash = window.location.hash.replace(/^#\/?/, "");
    if (!hash) return null;
    var parts = hash.split("/").filter(function (x) { return x.length > 0; });
    if (parts.length >= 3) {
      return { courseId: parts[0], unitId: parts[1], chapterId: parts[2] };
    }
    return null;
  }

  function buildHash(courseId, unitId, chapterId) {
    return "#/" + courseId + "/" + unitId + "/" + chapterId;
  }

  function goToChapter(courseId, unitId, chapterId) {
    var h = buildHash(courseId, unitId, chapterId);
    window.location.hash = h;
    state.currentCourseId = courseId;
    state.currentUnitId = unitId;
    state.currentChapterId = chapterId;
    renderSidebar();
    renderChapter(courseId, unitId, chapterId);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // ============== 查找数据 ==============
  function findCourse(courseId) {
    if (!state.data || !state.data.courses) return null;
    for (var i = 0; i < state.data.courses.length; i++) {
      if (state.data.courses[i].courseId === courseId) return state.data.courses[i];
    }
    return null;
  }

  function findUnit(course, unitId) {
    if (!course || !course.units) return null;
    for (var i = 0; i < course.units.length; i++) {
      if (course.units[i].unitId === unitId) return course.units[i];
    }
    return null;
  }

  function findChapter(unit, chapterId) {
    if (!unit || !unit.chapters) return null;
    for (var i = 0; i < unit.chapters.length; i++) {
      // courses.json 中字段是 chapter_id
      var cid = unit.chapters[i].chapterId || unit.chapters[i].chapter_id;
      if (cid === chapterId) return unit.chapters[i];
    }
    return null;
  }

  function getChapterId(chapter) {
    return chapter.chapterId || chapter.chapter_id;
  }

  // ============== 目录树渲染 ==============
  function renderSidebar() {
    var sidebar = state.sidebarContentEl;
    if (!sidebar) return;
    sidebar.innerHTML = "";
    if (!state.data) {
      sidebar.innerHTML = '<div style="color: var(--text-soft); padding: 12px;">加载中...</div>';
      return;
    }

    var courses = state.data.courses || [];
    for (var ci = 0; ci < courses.length; ci++) {
      var course = courses[ci];
      var courseBlock = document.createElement("div");
      courseBlock.className = "sidebar-course";

      var courseTitle = document.createElement("div");
      courseTitle.className = "sidebar-course-title";
      courseTitle.textContent = course.title;
      courseBlock.appendChild(courseTitle);

      var units = course.units || [];
      for (var ui = 0; ui < units.length; ui++) {
        var unit = units[ui];
        var unitBlock = document.createElement("div");
        unitBlock.className = "sidebar-unit";

        var unitTitle = document.createElement("div");
        unitTitle.className = "sidebar-unit-title";
        unitTitle.textContent = unit.title;
        unitBlock.appendChild(unitTitle);

        var chapterList = document.createElement("ul");
        chapterList.className = "sidebar-chapter-list";

        var chapters = unit.chapters || [];
        for (var chi = 0; chi < chapters.length; chi++) {
          var chapter = chapters[chi];
          var cid = getChapterId(chapter);
          var li = document.createElement("li");
          li.className = "sidebar-chapter";

          var isActive = (
            state.currentCourseId === course.courseId &&
            state.currentUnitId === unit.unitId &&
            state.currentChapterId === cid
          );
          if (isActive) li.classList.add("active");
          if (isChapterDone(cid)) li.classList.add("done");

          var link = document.createElement("a");
          link.href = "javascript:void(0)";
          link.innerHTML = (isChapterDone(cid) ? '<span class="check">✓</span> ' : '<span class="dot">·</span> ') + chapter.title;
          (function (cid2, unitId2, courseId2) {
            link.addEventListener("click", function (e) {
              e.preventDefault();
              goToChapter(courseId2, unitId2, cid2);
            });
          })(cid, unit.unitId, course.courseId);

          li.appendChild(link);
          chapterList.appendChild(li);
        }

        unitBlock.appendChild(chapterList);
        courseBlock.appendChild(unitBlock);
      }

      sidebar.appendChild(courseBlock);
    }
  }

  // ============== 代码编辑器块 ==============
  function createCodeSampleBlock(sample) {
    var card = document.createElement("div");
    card.className = "code-sample-card";

    var header = document.createElement("div");
    header.className = "block-header";
    header.innerHTML = '<span class="block-label">代码示例</span> <span class="block-title">' + (sample.title || "示例代码") + '</span>';
    card.appendChild(header);

    if (sample.explanation) {
      var expl = document.createElement("div");
      expl.className = "block-explanation";
      expl.textContent = sample.explanation;
      card.appendChild(expl);
    }

    var textarea = document.createElement("textarea");
    textarea.textContent = sample.code || "";
    card.appendChild(textarea);

    var outputEl = document.createElement("div");
    outputEl.className = "code-output";
    card.appendChild(outputEl);

    var plotsEl = document.createElement("div");
    plotsEl.className = "code-plots";
    card.appendChild(plotsEl);

    var sampleId = sample.id || ("cs_" + Math.random().toString(36).slice(2, 8));

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

  // ============== 练习块 ==============
  function createExerciseBlock(exercise, chapterId) {
    var card = document.createElement("div");
    card.className = "exercise-card";
    var exId = exercise.exerciseId || ("ex_" + Math.random().toString(36).slice(2, 8));

    var header = document.createElement("div");
    header.className = "block-header";
    header.innerHTML = '<span class="block-label exercise-label">练习</span> <span class="block-title">' + (exercise.prompt ? exercise.prompt.slice(0, 80) + (exercise.prompt.length > 80 ? "..." : "") : "练习") + '</span>';
    card.appendChild(header);

    var prompt = document.createElement("div");
    prompt.className = "exercise-prompt";
    prompt.textContent = exercise.prompt || "";
    card.appendChild(prompt);

    var textarea = document.createElement("textarea");
    textarea.textContent = exercise.starterCode || "";
    card.appendChild(textarea);

    var toolbar = document.createElement("div");
    toolbar.className = "exercise-toolbar";
    card.appendChild(toolbar);

    var checkBtn = document.createElement("button");
    checkBtn.className = "btn btn-primary";
    checkBtn.textContent = "▶ 检查答案";
    toolbar.appendChild(checkBtn);

    var hintBtn = document.createElement("button");
    hintBtn.className = "btn btn-ghost";
    hintBtn.textContent = "显示提示";
    toolbar.appendChild(hintBtn);

    var answerBtn = document.createElement("button");
    answerBtn.className = "btn btn-ghost";
    answerBtn.textContent = "参考答案";
    toolbar.appendChild(answerBtn);

    var feedbackEl = document.createElement("div");
    feedbackEl.className = "exercise-feedback";
    card.appendChild(feedbackEl);

    var outputEl = document.createElement("div");
    outputEl.className = "code-output";
    card.appendChild(outputEl);

    var editor = window.CodeEditor.create(textarea, {
      outputEl: outputEl,
      plotsEl: null,
      runButton: checkBtn,
      runHandler: function () {}
    });

    state.editors.push(editor);

    // 检查按钮逻辑
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
          markExerciseDone(chapterId, exId);
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

    // 提示按钮
    var hintBox = document.createElement("div");
    hintBox.className = "hint-box";
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

    // 参考答案按钮
    var answerBox = document.createElement("div");
    answerBox.className = "answer-box";
    answerBox.style.display = "none";
    if (exercise.referenceAnswer) {
      var ansPre = document.createElement("pre");
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

  // ============== 上下一章导航 ==============
  function findAdjacentChapters(courseId, unitId, chapterId) {
    var course = findCourse(courseId);
    if (!course) return { prev: null, next: null };

    var flat = [];
    var units = course.units || [];
    for (var ui = 0; ui < units.length; ui++) {
      var chapters = units[ui].chapters || [];
      for (var ci = 0; ci < chapters.length; ci++) {
        flat.push({ unitId: units[ui].unitId, chapterId: getChapterId(chapters[ci]), title: chapters[ci].title });
      }
    }

    var idx = -1;
    for (var i = 0; i < flat.length; i++) {
      if (flat[i].unitId === unitId && flat[i].chapterId === chapterId) {
        idx = i;
        break;
      }
    }
    return {
      prev: idx > 0 ? { courseId: courseId, unitId: flat[idx - 1].unitId, chapterId: flat[idx - 1].chapterId, title: flat[idx - 1].title } : null,
      next: (idx >= 0 && idx < flat.length - 1) ? { courseId: courseId, unitId: flat[idx + 1].unitId, chapterId: flat[idx + 1].chapterId, title: flat[idx + 1].title } : null
    };
  }

  // ============== 章节内容渲染 ==============
  function renderChapter(courseId, unitId, chapterId) {
    var contentEl = state.contentEl;
    if (!contentEl) return;
    state.editors = [];
    contentEl.innerHTML = "";

    var course = findCourse(courseId);
    if (!course) {
      contentEl.innerHTML = "<p>未找到课程：" + courseId + "</p>";
      return;
    }
    var unit = findUnit(course, unitId);
    if (!unit) {
      contentEl.innerHTML = "<p>未找到单元：" + unitId + "</p>";
      return;
    }
    var chapter = findChapter(unit, chapterId);
    if (!chapter) {
      contentEl.innerHTML = "<p>未找到章节：" + chapterId + "</p>";
      return;
    }

    // 面包屑
    var breadcrumb = document.createElement("div");
    breadcrumb.className = "breadcrumb";
    breadcrumb.innerHTML = '<span class="crumb">' + course.title + '</span> <span class="sep">›</span> <span class="crumb">' + unit.title + '</span>';
    contentEl.appendChild(breadcrumb);

    // 章节标题
    var h1 = document.createElement("h1");
    h1.className = "chapter-title";
    h1.textContent = chapter.title;
    contentEl.appendChild(h1);

    // 学习目标
    if (chapter.objectives && chapter.objectives.length) {
      var objWrap = document.createElement("div");
      objWrap.className = "chapter-section";
      var objTitle = document.createElement("h2");
      objTitle.className = "section-title";
      objTitle.textContent = "🎯 学习目标";
      objWrap.appendChild(objTitle);
      var ul = document.createElement("ul");
      ul.className = "objectives-list";
      for (var i = 0; i < chapter.objectives.length; i++) {
        var li = document.createElement("li");
        li.textContent = chapter.objectives[i];
        ul.appendChild(li);
      }
      objWrap.appendChild(ul);
      contentEl.appendChild(objWrap);
    }

    // 讲解内容
    if (chapter.content) {
      var contentWrap = document.createElement("div");
      contentWrap.className = "chapter-section";
      var contentTitle = document.createElement("h2");
      contentTitle.className = "section-title";
      contentTitle.textContent = "📖 章节讲解";
      contentWrap.appendChild(contentTitle);
      var p = document.createElement("div");
      p.className = "chapter-content-text";
      p.textContent = chapter.content;
      contentWrap.appendChild(p);
      contentEl.appendChild(contentWrap);
    }

    // 代码示例
    if (chapter.code_samples && chapter.code_samples.length) {
      var codeWrap = document.createElement("div");
      codeWrap.className = "chapter-section";
      var codeTitle = document.createElement("h2");
      codeTitle.className = "section-title";
      codeTitle.textContent = "💻 代码示例";
      codeWrap.appendChild(codeTitle);
      for (var ci2 = 0; ci2 < chapter.code_samples.length; ci2++) {
        codeWrap.appendChild(createCodeSampleBlock(chapter.code_samples[ci2]));
      }
      contentEl.appendChild(codeWrap);
    }

    // 练习
    if (chapter.exercises && chapter.exercises.length) {
      var exWrap = document.createElement("div");
      exWrap.className = "chapter-section";
      var exTitle = document.createElement("h2");
      exTitle.className = "section-title";
      exTitle.textContent = "✏️ 动手练习";
      exWrap.appendChild(exTitle);
      for (var ei = 0; ei < chapter.exercises.length; ei++) {
        exWrap.appendChild(createExerciseBlock(chapter.exercises[ei], chapterId));
      }
      contentEl.appendChild(exWrap);
    }

    // 小结
    if (chapter.summary) {
      var summaryWrap = document.createElement("div");
      summaryWrap.className = "chapter-section summary-section";
      var sumTitle = document.createElement("h2");
      sumTitle.className = "section-title";
      sumTitle.textContent = "🧠 本章小结";
      summaryWrap.appendChild(sumTitle);
      var sp = document.createElement("p");
      sp.className = "chapter-content-text";
      sp.textContent = chapter.summary;
      summaryWrap.appendChild(sp);
      contentEl.appendChild(summaryWrap);
    }

    // 底部工具栏：标记完成 + 上下章
    var footer = document.createElement("div");
    footer.className = "chapter-footer";

    var markBtn = document.createElement("button");
    markBtn.className = "btn btn-primary mark-done-btn";
    var doneNow = isChapterDone(chapterId);
    markBtn.textContent = doneNow ? "✓ 已完成本章" : "✓ 标记本章完成";
    markBtn.disabled = doneNow;
    markBtn.addEventListener("click", function () {
      markChapterDone(chapterId);
      markBtn.textContent = "✓ 已完成本章";
      markBtn.disabled = true;
      renderSidebar();
    });
    footer.appendChild(markBtn);

    var nav = document.createElement("div");
    nav.className = "chapter-nav";
    var adj = findAdjacentChapters(courseId, unitId, chapterId);
    if (adj.prev) {
      var prevBtn = document.createElement("a");
      prevBtn.href = "javascript:void(0)";
      prevBtn.className = "btn btn-ghost";
      prevBtn.textContent = "← " + adj.prev.title;
      (function (p) {
        prevBtn.addEventListener("click", function (e) {
          e.preventDefault();
          goToChapter(p.courseId, p.unitId, p.chapterId);
        });
      })(adj.prev);
      nav.appendChild(prevBtn);
    }
    if (adj.next) {
      var nextBtn = document.createElement("a");
      nextBtn.href = "javascript:void(0)";
      nextBtn.className = "btn btn-primary";
      nextBtn.textContent = adj.next.title + " →";
      (function (n) {
        nextBtn.addEventListener("click", function (e) {
          e.preventDefault();
          goToChapter(n.courseId, n.unitId, n.chapterId);
        });
      })(adj.next);
      nav.appendChild(nextBtn);
    }
    footer.appendChild(nav);

    contentEl.appendChild(footer);
  }

  // ============== 默认定位到第一章 ==============
  function defaultChapter() {
    if (!state.data || !state.data.courses || state.data.courses.length === 0) return null;
    var course = state.data.courses[0];
    if (!course.units || course.units.length === 0) return null;
    var unit = course.units[0];
    if (!unit.chapters || unit.chapters.length === 0) return null;
    var chapter = unit.chapters[0];
    return { courseId: course.courseId, unitId: unit.unitId, chapterId: getChapterId(chapter) };
  }

  // ============== 主入口 ==============
  function init() {
    state.sidebarEl = document.getElementById("sidebar");
    state.sidebarContentEl = document.getElementById("sidebarContent");
    state.contentEl = document.getElementById("chapterContent");

    if (!state.sidebarEl || !state.sidebarContentEl || !state.contentEl) {
      console.warn("CourseView.init: 未找到 sidebar / sidebarContent / chapterContent 元素");
      return;
    }

    fetch("assets/data/courses.json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        state.data = data;
        var route = parseHash();
        if (!route) {
          var def = defaultChapter();
          if (def) {
            goToChapter(def.courseId, def.unitId, def.chapterId);
          } else {
            state.contentEl.innerHTML = "<p>暂无课程数据</p>";
          }
        } else {
          state.currentCourseId = route.courseId;
          state.currentUnitId = route.unitId;
          state.currentChapterId = route.chapterId;
          renderSidebar();
          renderChapter(route.courseId, route.unitId, route.chapterId);
        }
      })
      .catch(function (err) {
        if (state.contentEl) {
          state.contentEl.innerHTML = '<p style="color:#ef4444;">加载课程数据失败：' + err.message + '</p>';
        }
      });

    window.addEventListener("hashchange", function () {
      var route = parseHash();
      if (route) {
        state.currentCourseId = route.courseId;
        state.currentUnitId = route.unitId;
        state.currentChapterId = route.chapterId;
        renderSidebar();
        renderChapter(route.courseId, route.unitId, route.chapterId);
      }
    });
  }

  window.CourseView = {
    init: init,
    renderSidebar: renderSidebar,
    renderChapter: renderChapter,
    goToChapter: goToChapter
  };

})(window, document);
