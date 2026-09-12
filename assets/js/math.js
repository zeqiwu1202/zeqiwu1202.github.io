(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var content = document.querySelector("[data-math-content]");
    if (!content || typeof window.renderMathInElement !== "function") return;

    window.renderMathInElement(content, {
      delimiters: [
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true },
      ],
      throwOnError: false,
    });
  });
})();
