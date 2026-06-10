(function (window) {
  "use strict";

  // ===== Pyodide Runner: 浏览器端 Python 执行模块 =====
  // 懒加载 Pyodide, 暴露 window.PyRunner API

  var PYODIDE_CDN = "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js";
  var DEFAULT_PACKAGES = ["numpy", "pandas", "matplotlib"];

  // 内部状态
  var state = {
    pyodide: null,
    loadingPromise: null,
    ready: false,
    listeners: {}  // event -> [cb, ...]
  };

  // ===== 事件机制 =====
  function emit(event, payload) {
    var cbs = state.listeners[event] || [];
    for (var i = 0; i < cbs.length; i++) {
      try { cbs[i](payload); } catch (e) { /* swallow listener errors */ }
    }
  }

  function on(event, cb) {
    if (!state.listeners[event]) state.listeners[event] = [];
    state.listeners[event].push(cb);
  }

  function off(event, cb) {
    var cbs = state.listeners[event];
    if (!cbs) return;
    var idx = cbs.indexOf(cb);
    if (idx !== -1) cbs.splice(idx, 1);
  }

  // ===== 动态加载 Pyodide script =====
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      if (typeof window.loadPyodide === "function") {
        return resolve();
      }
      var s = document.createElement("script");
      s.src = src;
      s.async = true;
      s.onload = function () { resolve(); };
      s.onerror = function () {
        reject(new Error("加载 Pyodide 失败: " + src));
      };
      document.head.appendChild(s);
    });
  }

  // ===== Python 侧初始化代码：每次 runCode 前注入 =====
  // - 重置 stdout/stderr 为 StringIO
  // - matplotlib 使用 Agg 后端
  // - 提供 _capture_plots() 收集所有 figure 为 base64 PNG
  var PY_INIT_CODE = [
    "import sys, io",
    "sys.stdout = io.StringIO()",
    "sys.stderr = io.StringIO()",
    "import matplotlib",
    "matplotlib.use('Agg')",
    "import matplotlib.pyplot as plt",
    "plt._plots = []",
    "def _capture_plots():",
    "    import base64, io as _io",
    "    _out = []",
    "    for _f in plt.get_fignums():",
    "        _buf = _io.BytesIO()",
    "        plt.figure(_f).savefig(_buf, format='png')",
    "        _out.append('data:image/png;base64,' + base64.b64encode(_buf.getvalue()).decode())",
    "        plt.close(_f)",
    "    return _out"
  ].join("\n");

  // ===== 主 API: load() =====
  function load() {
    if (state.ready && state.pyodide) {
      return Promise.resolve(state.pyodide);
    }
    if (state.loadingPromise) {
      return state.loadingPromise;
    }

    emit("loadstart", { message: "开始加载 Pyodide..." });

    state.loadingPromise = loadScript(PYODIDE_CDN)
      .then(function () {
        emit("loadprogress", { message: "初始化 Pyodide 运行时..." });
        if (typeof window.loadPyodide !== "function") {
          throw new Error("loadPyodide 未找到");
        }
        return window.loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/"
        });
      })
      .then(function (py) {
        state.pyodide = py;
        emit("loadprogress", { message: "加载常用包 (numpy/pandas/matplotlib)..." });
        return py.loadPackage(DEFAULT_PACKAGES).then(function () { return py; });
      })
      .then(function (py) {
        state.ready = true;
        emit("ready", { packages: DEFAULT_PACKAGES });
        return py;
      })
      .catch(function (err) {
        state.loadingPromise = null;  // 允许下次重试
        emit("error", { name: err.name, message: err.message });
        throw err;
      });

    return state.loadingPromise;
  }

  // ===== 主 API: runCode(code, opts) =====
  function runCode(code, opts) {
    opts = opts || {};
    var timeoutMs = typeof opts.timeoutMs === "number" ? opts.timeoutMs : 5000;
    var capturePlots = opts.capturePlots !== false;

    emit("runstart", { code: code });

    if (!state.ready || !state.pyodide) {
      var notReadyErr = {
        ok: false,
        stdout: "",
        stderr: "",
        plots: [],
        error: { name: "NotReadyError", message: "Pyodide 尚未加载完成,请先调用 load()" }
      };
      emit("runend", notReadyErr);
      emit("error", notReadyErr.error);
      return Promise.resolve(notReadyErr);
    }

    var py = state.pyodide;

    // 执行主 Promise: 初始化 -> 用户代码 -> 收集
    var runPromise = Promise.resolve()
      .then(function () {
        return py.runPythonAsync(PY_INIT_CODE);
      })
      .then(function () {
        return py.runPythonAsync(code);
      })
      .then(function () {
        // 收集 stdout/stderr
        var stdout = py.runPython("sys.stdout.getvalue()") || "";
        var stderr = py.runPython("sys.stderr.getvalue()") || "";
        var plots = [];
        if (capturePlots) {
          try {
            var plotsJs = py.runPython("_capture_plots()");
            if (plotsJs && plotsJs.toJs) {
              plots = plotsJs.toJs();
            } else if (Array.isArray(plotsJs)) {
              plots = plotsJs;
            }
          } catch (e) { /* 忽略抓图失败 */ }
        }
        return {
          ok: true,
          stdout: String(stdout),
          stderr: String(stderr),
          plots: plots,
          error: null
        };
      })
      .catch(function (err) {
        // 尝试获取执行到目前为止的 stdout/stderr
        var stdout = "", stderr = "";
        try {
          stdout = String(py.runPython("sys.stdout.getvalue()") || "");
          stderr = String(py.runPython("sys.stderr.getvalue()") || "");
        } catch (e) { /* ignore */ }

        var errName = err && err.name ? err.name : "Error";
        var errMsg = err && err.message ? err.message : String(err);
        // Pyodide 异常通常包含更详细的 message, 直接用它
        return {
          ok: false,
          stdout: stdout,
          stderr: stderr,
          plots: [],
          error: { name: errName, message: errMsg }
        };
      });

    // 超时控制
    var timeoutPromise = new Promise(function (_, reject) {
      setTimeout(function () {
        reject(new Error("执行超时（超过 " + (timeoutMs / 1000) + " 秒）。代码似乎陷入死循环或太慢，请优化后再试。"));
      }, timeoutMs);
    });

    return Promise.race([runPromise, timeoutPromise])
      .then(function (result) {
        emit("runend", result);
        if (!result.ok) emit("error", result.error);
        return result;
      })
      .catch(function (err) {
        var result = {
          ok: false,
          stdout: "",
          stderr: "",
          plots: [],
          error: { name: err && err.name ? err.name : "TimeoutError", message: err && err.message ? err.message : String(err) }
        };
        emit("runend", result);
        emit("error", result.error);
        return result;
      });
  }

  function isReady() {
    return state.ready && !!state.pyodide;
  }

  // ===== 暴露 =====
  window.PyRunner = {
    load: load,
    runCode: runCode,
    isReady: isReady,
    on: on,
    off: off
  };

})(window);
