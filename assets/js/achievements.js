(function () {
  "use strict";

  var STORAGE_KEY = "pydataedu.state";
  var STATE_VERSION = 1;

  var LEVEL_THRESHOLDS = [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5000];

  var BADGE_DEFINITIONS = {
    first_chapter: {
      title: "初出茅庐",
      icon: "📘",
      description: "完成首章学习，开启数据分析之旅。"
    },
    first_perfect_exercise: {
      title: "完美练习",
      icon: "✏️",
      description: "首次完成练习并全部答对。"
    },
    streak_7_days: {
      title: "坚持一周",
      icon: "🔥",
      description: "连续 7 天有学习活动记录。"
    },
    hours_10: {
      title: "十小时达人",
      icon: "⏱️",
      description: "累计学习时长达到 600 分钟。"
    },
    all_units_done: {
      title: "单元通关",
      icon: "🏆",
      description: "所有单元的章节全部完成。"
    },
    explorer: {
      title: "代码探险家",
      icon: "🧪",
      description: "阅读过至少 5 个代码示例并成功运行过代码。"
    }
  };

  function defaultState() {
    return {
      version: STATE_VERSION,
      points: 0,
      level: 1,
      badges: {},
      chaptersDone: {},
      exercisesDone: {},
      quizzesDone: {},
      stats: {
        totalMinutes: 0,
        dailyActivity: {},
        firstVisit: null,
        lastVisit: null,
        codeRuns: 0,
        codeSamplesViewed: {}
      }
    };
  }

  var state = loadState();
  var listeners = {};
  var studyTimer = null;
  var pendingBadgeChecks = Object.keys(BADGE_DEFINITIONS);

  function emit(event, payload) {
    var list = listeners[event] || [];
    for (var i = 0; i < list.length; i++) {
      try {
        list[i](payload);
      } catch (e) {
        // swallow listener errors
      }
    }
  }

  function todayISO() {
    var d = new Date();
    var y = d.getFullYear();
    var m = String(d.getMonth() + 1).padStart(2, "0");
    var day = String(d.getDate()).padStart(2, "0");
    return y + "-" + m + "-" + day;
  }

  function recordVisit() {
    var now = todayISO();
    if (!state.stats.firstVisit) state.stats.firstVisit = now;
    state.stats.lastVisit = now;
    if (!state.stats.dailyActivity[now]) {
      state.stats.dailyActivity[now] = 0;
    }
  }

  function computeLevel(points) {
    var level = 1;
    for (var i = 0; i < LEVEL_THRESHOLDS.length; i++) {
      if (points >= LEVEL_THRESHOLDS[i]) level = i + 1;
    }
    return Math.min(level, LEVEL_THRESHOLDS.length);
  }

  function addPoints(n) {
    if (typeof n !== "number" || n <= 0) return;
    var oldLevel = state.level;
    state.points = state.points + n;
    state.level = computeLevel(state.points);
    emit("pointsChanged", { points: state.points, level: state.level, delta: n });
    if (state.level > oldLevel) {
      emit("levelUp", { level: state.level, points: state.points });
    }
  }

  function unlockBadge(badgeId) {
    if (state.badges[badgeId]) return false;
    var def = BADGE_DEFINITIONS[badgeId];
    if (!def) return false;
    state.badges[badgeId] = {
      unlockedAt: new Date().toISOString(),
      title: def.title,
      icon: def.icon,
      description: def.description
    };
    emit("badgeUnlocked", {
      badgeId: badgeId,
      title: def.title,
      icon: def.icon,
      description: def.description
    });
    return true;
  }

  function checkBadges() {
    var checks = pendingBadgeChecks.slice();
    pendingBadgeChecks = [];
    for (var i = 0; i < checks.length; i++) {
      checkBadge(checks[i]);
    }
  }

  function checkBadge(badgeId) {
    if (state.badges[badgeId]) return;
    var def = BADGE_DEFINITIONS[badgeId];
    if (!def) return;
    var unlocked = false;
    switch (badgeId) {
      case "first_chapter":
        unlocked = Object.keys(state.chaptersDone).length >= 1;
        break;
      case "first_perfect_exercise":
        var exIds = Object.keys(state.exercisesDone);
        for (var i = 0; i < exIds.length; i++) {
          if (state.exercisesDone[exIds[i]] && state.exercisesDone[exIds[i]].correct) {
            unlocked = true;
            break;
          }
        }
        break;
      case "streak_7_days":
        unlocked = hasConsecutiveDays(7);
        break;
      case "hours_10":
        unlocked = state.stats.totalMinutes >= 600;
        break;
      case "all_units_done":
        unlocked = isAllUnitsDone();
        break;
      case "explorer":
        var viewed = Object.keys(state.stats.codeSamplesViewed || {}).length;
        unlocked = viewed >= 5 && state.stats.codeRuns >= 1;
        break;
    }
    if (unlocked) unlockBadge(badgeId);
  }

  function hasConsecutiveDays(n) {
    var dates = [];
    for (var d in state.stats.dailyActivity) {
      if (state.stats.dailyActivity[d] > 0) dates.push(d);
    }
    if (dates.length < n) return false;
    dates.sort();
    var count = 1;
    for (var i = 1; i < dates.length; i++) {
      var prev = new Date(dates[i - 1]);
      var curr = new Date(dates[i]);
      var diff = Math.round((curr - prev) / 86400000);
      if (diff === 1) {
        count++;
        if (count >= n) return true;
      } else {
        count = 1;
      }
    }
    return count >= n;
  }

  function isAllUnitsDone() {
    try {
      var raw = localStorage.getItem("pydataedu.course");
      if (!raw) return false;
      var course = JSON.parse(raw);
      if (!course || !Array.isArray(course.units)) return false;
      var allChapters = [];
      for (var u = 0; u < course.units.length; u++) {
        var unit = course.units[u];
        if (!unit || !Array.isArray(unit.chapters)) continue;
        for (var c = 0; c < unit.chapters.length; c++) {
          var ch = unit.chapters[c];
          if (ch && ch.chapter_id) allChapters.push(ch.chapter_id);
        }
      }
      if (allChapters.length === 0) return false;
      for (var k = 0; k < allChapters.length; k++) {
        if (!state.chaptersDone[allChapters[k]]) return false;
      }
      return true;
    } catch (e) {
      return false;
    }
  }

  function scheduleBadgeCheck(badgeId) {
    if (pendingBadgeChecks.indexOf(badgeId) === -1) {
      pendingBadgeChecks.push(badgeId);
    }
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      // private mode or quota full
    }
  }

  function loadState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return defaultState();
      var parsed = JSON.parse(raw);
      if (!parsed || typeof parsed !== "object") return defaultState();
      var base = defaultState();
      for (var k in base) {
        if (parsed[k] === undefined) parsed[k] = base[k];
      }
      if (!parsed.stats) parsed.stats = base.stats;
      if (!parsed.stats.dailyActivity) parsed.stats.dailyActivity = {};
      if (!parsed.stats.codeSamplesViewed) parsed.stats.codeSamplesViewed = {};
      if (typeof parsed.stats.codeRuns !== "number") parsed.stats.codeRuns = 0;
      if (typeof parsed.level !== "number" || parsed.level < 1) {
        parsed.level = computeLevel(parsed.points || 0);
      }
      return parsed;
    } catch (e) {
      return defaultState();
    }
  }

  // ===== Public API =====
  var Achievements = {
    awardChapterComplete: function (chapterId) {
      if (!chapterId) return;
      if (!state.chaptersDone[chapterId]) {
        state.chaptersDone[chapterId] = {
          done: true,
          doneAt: new Date().toISOString()
        };
        addPoints(10);
        recordVisit();
        scheduleBadgeCheck("first_chapter");
        scheduleBadgeCheck("all_units_done");
        checkBadges();
        saveState();
      }
      return state.chaptersDone[chapterId];
    },

    awardExerciseCorrect: function (exerciseId, isPerfect) {
      if (!exerciseId) return;
      var existing = state.exercisesDone[exerciseId] || {
        correct: false,
        attemptCount: 0
      };
      existing.attemptCount = (existing.attemptCount || 0) + 1;
      if (isPerfect && !existing.correct) {
        existing.correct = true;
        addPoints(20);
        scheduleBadgeCheck("first_perfect_exercise");
      }
      state.exercisesDone[exerciseId] = existing;
      recordVisit();
      checkBadges();
      saveState();
      return existing;
    },

    awardQuizPass: function (quizId, score) {
      if (!quizId) return;
      var existing = state.quizzesDone[quizId];
      var isPass = score >= 80;
      if (!existing || score > existing.score) {
        state.quizzesDone[quizId] = {
          score: score,
          submittedAt: new Date().toISOString()
        };
        if (isPass) addPoints(50);
      }
      recordVisit();
      saveState();
      return state.quizzesDone[quizId];
    },

    recordCodeRun: function (sampleId) {
      state.stats.codeRuns = (state.stats.codeRuns || 0) + 1;
      if (sampleId) {
        if (!state.stats.codeSamplesViewed) state.stats.codeSamplesViewed = {};
        state.stats.codeSamplesViewed[sampleId] = true;
      }
      recordVisit();
      scheduleBadgeCheck("explorer");
      checkBadges();
      saveState();
    },

    recordCodeSampleView: function (sampleId) {
      if (!sampleId) return;
      if (!state.stats.codeSamplesViewed) state.stats.codeSamplesViewed = {};
      state.stats.codeSamplesViewed[sampleId] = true;
      scheduleBadgeCheck("explorer");
      checkBadges();
      saveState();
    },

    recordStudyMinute: function () {
      recordVisit();
      var key = todayISO();
      state.stats.totalMinutes = (state.stats.totalMinutes || 0) + 1;
      state.stats.dailyActivity[key] = (state.stats.dailyActivity[key] || 0) + 1;
      scheduleBadgeCheck("hours_10");
      scheduleBadgeCheck("streak_7_days");
      checkBadges();
      saveState();
    },

    startStudyTimer: function () {
      if (studyTimer) return;
      if (typeof document !== "undefined" && document.addEventListener) {
        document.addEventListener("visibilitychange", function () {
          if (document.hidden) {
            if (studyTimer) {
              clearInterval(studyTimer);
              studyTimer = null;
            }
          } else {
            if (!studyTimer) {
              studyTimer = setInterval(function () {
                Achievements.recordStudyMinute();
              }, 60000);
            }
          }
        });
      }
      studyTimer = setInterval(function () {
        Achievements.recordStudyMinute();
      }, 60000);
      recordVisit();
      saveState();
    },

    getLevelInfo: function () {
      var currentLevel = state.level;
      var prevThreshold = LEVEL_THRESHOLDS[currentLevel - 1] || 0;
      var nextThreshold = LEVEL_THRESHOLDS[currentLevel] || null;
      return {
        level: currentLevel,
        points: state.points,
        previousThreshold: prevThreshold,
        nextThreshold: nextThreshold,
        progressToNext: nextThreshold
          ? Math.min(1, (state.points - prevThreshold) / (nextThreshold - prevThreshold))
          : 1
      };
    },

    getProgressForLevel: function () {
      var info = this.getLevelInfo();
      if (!info.nextThreshold) return 1;
      return info.progressToNext;
    },

    getStats: function () {
      var uniqueDays = Object.keys(state.stats.dailyActivity || {}).filter(function (d) {
        return state.stats.dailyActivity[d] > 0;
      }).length;
      var totalChapters = Object.keys(state.chaptersDone).length;
      var totalExercises = Object.keys(state.exercisesDone).length;
      var perfectExercises = Object.keys(state.exercisesDone).filter(function (e) {
        return state.exercisesDone[e] && state.exercisesDone[e].correct;
      }).length;
      var quizScores = Object.keys(state.quizzesDone).map(function (q) {
        return state.quizzesDone[q].score;
      });
      var avgQuiz = quizScores.length
        ? Math.round(
            quizScores.reduce(function (a, b) {
              return a + b;
            }, 0) / quizScores.length
          )
        : 0;
      return {
        totalMinutes: state.stats.totalMinutes || 0,
        studyDays: uniqueDays,
        firstVisit: state.stats.firstVisit,
        lastVisit: state.stats.lastVisit,
        chaptersCompleted: totalChapters,
        exercisesCompleted: totalExercises,
        exercisesPerfect: perfectExercises,
        averageQuizScore: avgQuiz,
        totalBadges: Object.keys(state.badges).length,
        codeRuns: state.stats.codeRuns || 0
      };
    },

    getBadges: function () {
      var result = [];
      for (var id in BADGE_DEFINITIONS) {
        var def = BADGE_DEFINITIONS[id];
        var unlocked = state.badges[id];
        result.push({
          badgeId: id,
          title: def.title,
          icon: def.icon,
          description: def.description,
          unlocked: !!unlocked,
          unlockedAt: unlocked ? unlocked.unlockedAt : null
        });
      }
      return result;
    },

    getBadgeDefinitions: function () {
      return BADGE_DEFINITIONS;
    },

    getPoints: function () {
      return state.points;
    },

    getLevel: function () {
      return state.level;
    },

    getNextThreshold: function () {
      var info = this.getLevelInfo();
      return info.nextThreshold;
    },

    getQuizResult: function (quizId) {
      if (state.quizzesDone[quizId]) {
        return state.quizzesDone[quizId];
      }
      return null;
    },

    getState: function () {
      return JSON.parse(JSON.stringify(state));
    },

    on: function (event, cb) {
      if (typeof cb !== "function") return;
      if (!listeners[event]) listeners[event] = [];
      listeners[event].push(cb);
    },

    off: function (event, cb) {
      if (!listeners[event]) return;
      var idx = listeners[event].indexOf(cb);
      if (idx >= 0) listeners[event].splice(idx, 1);
    },

    exportData: function () {
      return JSON.parse(JSON.stringify(state));
    },

    importData: function (data, mode) {
      if (!data || typeof data !== "object") return false;
      var actualMode = mode === "overwrite" ? "overwrite" : "merge";
      recordVisit();
      if (actualMode === "overwrite") {
        var fresh = defaultState();
        for (var k in data) {
          fresh[k] = data[k];
        }
        if (typeof fresh.points !== "number") fresh.points = 0;
        if (typeof fresh.level !== "number" || fresh.level < 1) {
          fresh.level = computeLevel(fresh.points);
        }
        state = fresh;
      } else {
        // merge: take higher values for numerics, union for collections
        state.points = Math.max(state.points || 0, data.points || 0);
        state.level = Math.max(state.level || 1, data.level || 1);
        if (state.level < computeLevel(state.points)) {
          state.level = computeLevel(state.points);
        }
        if (data.badges && typeof data.badges === "object") {
          for (var b in data.badges) {
            if (!state.badges[b]) state.badges[b] = data.badges[b];
          }
        }
        if (data.chaptersDone && typeof data.chaptersDone === "object") {
          for (var ch in data.chaptersDone) {
            if (!state.chaptersDone[ch]) state.chaptersDone[ch] = data.chaptersDone[ch];
          }
        }
        if (data.exercisesDone && typeof data.exercisesDone === "object") {
          for (var ex in data.exercisesDone) {
            var cur = state.exercisesDone[ex] || { correct: false, attemptCount: 0 };
            var inc = data.exercisesDone[ex] || { correct: false, attemptCount: 0 };
            state.exercisesDone[ex] = {
              correct: cur.correct || inc.correct,
              attemptCount: Math.max(cur.attemptCount || 0, inc.attemptCount || 0)
            };
          }
        }
        if (data.quizzesDone && typeof data.quizzesDone === "object") {
          for (var q in data.quizzesDone) {
            var curQ = state.quizzesDone[q];
            var incQ = data.quizzesDone[q];
            if (!curQ || (incQ && incQ.score > curQ.score)) {
              state.quizzesDone[q] = incQ;
            }
          }
        }
        if (data.stats && typeof data.stats === "object") {
          state.stats.totalMinutes = Math.max(
            state.stats.totalMinutes || 0,
            data.stats.totalMinutes || 0
          );
          if (data.stats.dailyActivity && typeof data.stats.dailyActivity === "object") {
            for (var d in data.stats.dailyActivity) {
              state.stats.dailyActivity[d] = Math.max(
                state.stats.dailyActivity[d] || 0,
                data.stats.dailyActivity[d] || 0
              );
            }
          }
          state.stats.codeRuns = Math.max(
            state.stats.codeRuns || 0,
            data.stats.codeRuns || 0
          );
          if (data.stats.codeSamplesViewed && typeof data.stats.codeSamplesViewed === "object") {
            if (!state.stats.codeSamplesViewed) state.stats.codeSamplesViewed = {};
            for (var s in data.stats.codeSamplesViewed) {
              state.stats.codeSamplesViewed[s] = true;
            }
          }
        }
      }
      checkBadges();
      saveState();
      emit("imported", { mode: actualMode, points: state.points, level: state.level });
      emit("pointsChanged", { points: state.points, level: state.level, delta: 0 });
      return true;
    },

    reset: function () {
      state = defaultState();
      recordVisit();
      saveState();
      emit("pointsChanged", { points: 0, level: 1, delta: 0 });
    },

    _getLevelThresholds: function () {
      return LEVEL_THRESHOLDS.slice();
    },

    _computeLevel: computeLevel
  };

  // Initialize on load
  if (typeof window !== "undefined") {
    window.Achievements = Achievements;
    recordVisit();
    saveState();
  }
})();
