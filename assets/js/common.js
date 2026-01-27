$(document).ready(function () {
  const root = document.documentElement;
  const markLoaded = function (key, cls) {
    try {
      sessionStorage.setItem(key, "1");
    } catch (e) {}
    root.classList.add(cls);
  };

  const maybeRestore = function (key, cls) {
    try {
      if (sessionStorage.getItem(key) === "1") {
        root.classList.add(cls);
        return true;
      }
    } catch (e) {}
    return false;
  };

  if (document.fonts && document.fonts.load) {
    if (!maybeRestore("fa-loaded", "fa-loaded")) {
      document.fonts.load('1em "Font Awesome 6 Free"').then(function () {
        markLoaded("fa-loaded", "fa-loaded");
      });
      document.fonts.load('1em "Font Awesome 6 Brands"').then(function () {
        markLoaded("fa-loaded", "fa-loaded");
      });
    }

    if (!maybeRestore("ai-loaded", "ai-loaded")) {
      document.fonts.load('1em "Academicons"').then(function () {
        markLoaded("ai-loaded", "ai-loaded");
      });
    }
  } else {
    root.classList.add("fa-loaded", "ai-loaded");
  }

  // add toggle functionality to abstract, award and bibtex buttons
  $("a.abstract").click(function () {
    $(this).parent().parent().find(".abstract.hidden").toggleClass("open");
    $(this).parent().parent().find(".award.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden.open").toggleClass("open");
  });
  $("a.award").click(function () {
    $(this).parent().parent().find(".abstract.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".award.hidden").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden.open").toggleClass("open");
  });
  $("a.bibtex").click(function () {
    $(this).parent().parent().find(".abstract.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".award.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden").toggleClass("open");
  });
  $("a").removeClass("waves-effect waves-light");

  // bootstrap-toc
  if ($("#toc-sidebar").length) {
    // remove related publications years from the TOC
    $(".publications h2").each(function () {
      $(this).attr("data-toc-skip", "");
    });
    var navSelector = "#toc-sidebar";
    var $myNav = $(navSelector);
    Toc.init($myNav);
    $("body").scrollspy({
      target: navSelector,
      offset: 100,
    });
  }

  // add css to jupyter notebooks
  const cssLink = document.createElement("link");
  cssLink.href = "../css/jupyter.css";
  cssLink.rel = "stylesheet";
  cssLink.type = "text/css";

  let jupyterTheme = determineComputedTheme();

  $(".jupyter-notebook-iframe-container iframe").each(function () {
    $(this).contents().find("head").append(cssLink);

    if (jupyterTheme == "dark") {
      $(this).bind("load", function () {
        $(this).contents().find("body").attr({
          "data-jp-theme-light": "false",
          "data-jp-theme-name": "JupyterLab Dark",
        });
      });
    }
  });

  // trigger popovers
  $('[data-toggle="popover"]').popover({
    trigger: "hover",
  });
});
