(function () {
  "use strict";

  var THEME_KEY = "pydataedu.theme";
  var PROGRESS_KEY = "pydataedu.progress";
  var ROUTES = { home: "index.html", course: "course.html", profile: "profile.html", quiz: "quiz.html" };

  // ---------- Theme ----------
  function applyTheme(theme) {
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
  }

  function getStoredTheme() {
    try {
      return localStorage.getItem(THEME_KEY);
    } catch (e) {
      return null;
    }
  }

  function setStoredTheme(theme) {
    try {
      localStorage.setItem(THEME_KEY, theme);
    } catch (e) {}
  }

  function initTheme() {
    var stored = getStoredTheme();
    var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(stored || (prefersDark ? "dark" : "light"));

    var toggle = document.getElementById("themeToggle");
    if (!toggle) return;
    toggle.addEventListener("click", function () {
      var current = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
      var next = current === "dark" ? "light" : "dark";
      applyTheme(next);
      setStoredTheme(next);
    });
  }

  // ---------- Hash Router ----------
  function parseHash() {
    var hash = location.hash || "#!/home";
    var m = hash.match(/^#!\/([a-z]+)/);
    return m ? m[1] : "home";
  }

  function highlightNav(route) {
    var links = document.querySelectorAll(".nav-links a[data-route]");
    for (var i = 0; i < links.length; i++) {
      if (links[i].getAttribute("data-route") === route) {
        links[i].classList.add("active");
      } else {
        links[i].classList.remove("active");
      }
    }
  }

  function handleRoute(initial) {
    var route = parseHash();
    highlightNav(route);
    if (!initial) {
      var target = ROUTES[route];
      if (target) {
        var current = location.pathname.split("/").pop() || "index.html";
        if (current !== target) {
          location.href = target + location.hash;
        }
      }
    }
  }

  function initRouter() {
    if (!location.hash) {
      location.replace("#!/home");
    }
    handleRoute(true);
    window.addEventListener("hashchange", function () {
      handleRoute(false);
    });
  }

  // ---------- Lesson progress ----------
  function getProgress() {
    try {
      var raw = localStorage.getItem(PROGRESS_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  function setProgress(list) {
    try {
      localStorage.setItem(PROGRESS_KEY, JSON.stringify(list));
    } catch (e) {}
  }

  function markLessonDone(lessonId) {
    var list = getProgress();
    if (list.indexOf(lessonId) === -1) {
      list.push(lessonId);
      setProgress(list);
    }
  }

  function initMarkDone() {
    var buttons = document.querySelectorAll(".mark-done");
    var done = getProgress();
    buttons.forEach(function (btn) {
      var id = btn.getAttribute("data-lesson");
      if (done.indexOf(id) !== -1) {
        btn.classList.add("done");
        btn.textContent = "已完成";
        btn.disabled = true;
      }
      btn.addEventListener("click", function () {
        markLessonDone(id);
        btn.classList.add("done");
        btn.textContent = "已完成";
        btn.disabled = true;
      });
    });
  }

  function renderLessonList() {
    var list = document.getElementById("lessonList");
    if (!list) return;
    var done = getProgress();
    if (done.length === 0) return;
    list.innerHTML = "";
    done.forEach(function (id) {
      var li = document.createElement("li");
      li.textContent = "✔ " + id + " 已完成";
      list.appendChild(li);
    });
  }

  function initResetProgress() {
    var btn = document.getElementById("resetProgress");
    if (!btn) return;
    btn.addEventListener("click", function () {
      setProgress([]);
      var list = document.getElementById("lessonList");
      if (list) {
        list.innerHTML = '<li class="empty">暂无记录,去<a href="#!/course">开始学习</a>吧。</li>';
      }
    });
  }

  // ---------- Quiz ----------
  function initQuiz() {
    var options = document.querySelectorAll(".quiz-opt");
    var feedback = document.getElementById("quizFeedback");
    options.forEach(function (opt) {
      opt.addEventListener("click", function () {
        var correct = opt.getAttribute("data-correct") === "true";
        options.forEach(function (o) {
          o.classList.remove("correct", "wrong");
        });
        opt.classList.add(correct ? "correct" : "wrong");
        if (feedback) {
          feedback.textContent = correct
            ? "正确!read_csv() 是 Pandas 读取 CSV 的标准方法。"
            : "再想想,read_csv() 才是读取 CSV 的标准方法。";
        }
      });
    });
  }

  // ---------- Boot ----------
  document.addEventListener("DOMContentLoaded", function () {
    initTheme();
    initRouter();
    initMarkDone();
    renderLessonList();
    initResetProgress();
    initQuiz();
  });
})();
