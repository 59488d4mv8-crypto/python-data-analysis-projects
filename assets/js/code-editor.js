(function (window, document) {
  "use strict";

  // ===== 轻量代码编辑器：原生 textarea + 行号 + Tab 缩进 + 运行按钮 =====
  // 暴露 window.CodeEditor = { create(textareaEl, opts) }

  function createLineNumbers(textarea) {
    // 左侧行号容器
    var wrapper = document.createElement("div");
    wrapper.className = "code-editor";
    wrapper.style.display = "flex";
    wrapper.style.alignItems = "stretch";
    wrapper.style.background = "var(--code-bg)";
    wrapper.style.border = "1px solid var(--border)";
    wrapper.style.borderRadius = "10px";
    wrapper.style.overflow = "hidden";
    wrapper.style.fontFamily = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
    wrapper.style.fontSize = "0.92rem";

    var gutter = document.createElement("div");
    gutter.className = "code-gutter";
    gutter.style.padding = "12px 10px";
    gutter.style.textAlign = "right";
    gutter.style.userSelect = "none";
    gutter.style.color = "var(--text-soft)";
    gutter.style.opacity = "0.6";
    gutter.style.borderRight = "1px solid var(--border)";
    gutter.style.lineHeight = "1.55";
    gutter.style.whiteSpace = "pre";
    gutter.textContent = "1";

    // 将 textarea 挪进 wrapper
    var parent = textarea.parentNode;
    parent.insertBefore(wrapper, textarea);

    // textarea 样式
    textarea.style.flex = "1";
    textarea.style.width = "100%";
    textarea.style.padding = "12px 14px";
    textarea.style.border = "none";
    textarea.style.outline = "none";
    textarea.style.background = "transparent";
    textarea.style.color = "var(--text)";
    textarea.style.resize = "vertical";
    textarea.style.minHeight = "180px";
    textarea.style.lineHeight = "1.55";
    textarea.style.fontFamily = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
    textarea.style.fontSize = "0.92rem";

    wrapper.appendChild(gutter);
    wrapper.appendChild(textarea);

    function updateLineNumbers() {
      var lines = textarea.value.split("\n").length;
      var nums = [];
      for (var i = 1; i <= lines; i++) nums.push(i);
      gutter.textContent = nums.join("\n");
    }

    textarea.addEventListener("input", updateLineNumbers);
    textarea.addEventListener("keydown", function (e) {
      // Tab 键：插入 4 空格，避免焦点跳走
      if (e.key === "Tab" || e.keyCode === 9) {
        e.preventDefault();
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;
        textarea.value = textarea.value.substring(0, start) + "    " + textarea.value.substring(end);
        textarea.selectionStart = textarea.selectionEnd = start + 4;
        updateLineNumbers();
      }
    });

    // 同步滚动
    textarea.addEventListener("scroll", function () {
      gutter.scrollTop = textarea.scrollTop;
    });

    updateLineNumbers();
    return { wrapper: wrapper, updateLineNumbers: updateLineNumbers };
  }

  function createCopyButton(textarea) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn btn-ghost";
    btn.textContent = "复制代码";
    btn.style.padding = "8px 14px";
    btn.style.fontSize = "0.9rem";
    btn.addEventListener("click", function () {
      var original = btn.textContent;
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(textarea.value).then(function () {
            btn.textContent = "已复制 ✓";
          }, function () {
            fallbackCopy();
          });
        } else {
          fallbackCopy();
        }
      } catch (e) {
        fallbackCopy();
      }
      function fallbackCopy() {
        textarea.select();
        try { document.execCommand("copy"); } catch (ex) {}
        btn.textContent = "已复制 ✓";
      }
      setTimeout(function () { btn.textContent = original; }, 1500);
    });
    return btn;
  }

  function createRunButton(toolbar, opts, runButton) {
    // 若用户没传入 runButton，创建一个
    var btn = runButton || document.createElement("button");
    if (!runButton) {
      btn.type = "button";
      btn.className = "btn btn-primary";
      btn.textContent = "▶ 运行代码";
      btn.style.padding = "8px 14px";
      btn.style.fontSize = "0.9rem";
    }

    btn.addEventListener("click", function () {
      if (typeof opts.runHandler === "function") {
        opts.runHandler(opts.textareaEl.value);
      }
    });
    return btn;
  }

  function renderResult(result, outputEl, plotsEl) {
    if (!outputEl && !plotsEl) return;
    if (outputEl) {
      outputEl.innerHTML = "";
      var title = document.createElement("div");
      title.style.fontSize = "0.85rem";
      title.style.color = "var(--text-soft)";
      title.style.marginBottom = "6px";
      title.textContent = result.ok ? "输出结果 (stdout)：" : "执行出错：";
      outputEl.appendChild(title);

      var pre = document.createElement("pre");
      pre.style.margin = "0";
      pre.style.padding = "12px";
      pre.style.background = "var(--code-bg)";
      pre.style.border = "1px solid var(--border)";
      pre.style.borderRadius = "8px";
      pre.style.whiteSpace = "pre-wrap";
      pre.style.wordBreak = "break-all";
      pre.style.maxHeight = "320px";
      pre.style.overflow = "auto";
      pre.style.fontFamily = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
      pre.style.fontSize = "0.88rem";
      pre.style.color = result.ok ? "var(--text)" : "#ef4444";

      if (result.ok) {
        pre.textContent = result.stdout || "（无 stdout 输出）";
        if (result.stderr) {
          pre.textContent += "\n---- stderr ----\n" + result.stderr;
        }
      } else {
        pre.textContent = "[" + (result.error && result.error.name || "Error") + "] " +
          (result.error && result.error.message || String(result.error));
        if (result.stdout) pre.textContent += "\n\nstdout:\n" + result.stdout;
        if (result.stderr) pre.textContent += "\nstderr:\n" + result.stderr;
      }
      outputEl.appendChild(pre);
    }

    if (plotsEl) {
      plotsEl.innerHTML = "";
      if (result.plots && result.plots.length) {
        var h = document.createElement("div");
        h.style.fontSize = "0.85rem";
        h.style.color = "var(--text-soft)";
        h.style.margin = "12px 0 6px";
        h.textContent = "生成的图表：";
        plotsEl.appendChild(h);
        result.plots.forEach(function (src) {
          var img = document.createElement("img");
          img.src = src;
          img.alt = "plot";
          img.style.maxWidth = "100%";
          img.style.border = "1px solid var(--border)";
          img.style.borderRadius = "8px";
          img.style.marginTop = "6px";
          plotsEl.appendChild(img);
        });
      }
    }
  }

  // ===== 主入口 =====
  function create(textareaEl, opts) {
    opts = opts || {};
    if (!textareaEl) {
      console.warn("CodeEditor.create: 需要提供 textareaEl");
      return null;
    }
    var ln = createLineNumbers(textareaEl);

    // 工具栏
    var toolbar = document.createElement("div");
    toolbar.style.display = "flex";
    toolbar.style.gap = "10px";
    toolbar.style.marginTop = "10px";
    toolbar.style.flexWrap = "wrap";

    // 将 textareaEl 保存到 opts，供 runButton 读取
    opts.textareaEl = textareaEl;

    var runBtn = createRunButton(toolbar, opts, opts.runButton);
    var copyBtn = createCopyButton(textareaEl);

    toolbar.appendChild(runBtn);
    toolbar.appendChild(copyBtn);

    // 输出区与图表区
    var outputEl = opts.outputEl;
    var plotsEl = opts.plotsEl;

    // 把 toolbar 插入到原 textarea 的 wrapper 之后
    ln.wrapper.parentNode.insertBefore(toolbar, ln.wrapper.nextSibling);

    return {
      textarea: textareaEl,
      setCode: function (code) {
        textareaEl.value = code;
        ln.updateLineNumbers();
      },
      getCode: function () { return textareaEl.value; },
      renderResult: function (result) { renderResult(result, outputEl, plotsEl); }
    };
  }

  window.CodeEditor = {
    create: create
  };

})(window, document);
