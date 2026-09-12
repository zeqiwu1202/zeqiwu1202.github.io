(function () {
  "use strict";

  document.documentElement.classList.add("js");

  var root = document.documentElement;
  var themeButton = document.querySelector("[data-theme-toggle]");
  var themeColorMeta = document.querySelector("[data-theme-color]");
  var menuButton = document.querySelector("[data-menu-toggle]");
  var navigation = document.querySelector("[data-navigation]");
  var yearNodes = document.querySelectorAll("[data-current-year]");
  var themeTransitionTimer;

  function systemIsDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function themeIsDark() {
    var storedTheme = root.getAttribute("data-theme");
    return storedTheme ? storedTheme === "dark" : systemIsDark();
  }

  function updateThemeLabel() {
    if (!themeButton) return;
    var nextTheme = themeIsDark() ? "light" : "dark";
    themeButton.setAttribute("aria-label", "Switch to " + nextTheme + " theme");
    themeButton.setAttribute("title", "Switch to " + nextTheme + " theme");
  }

  function updateThemeColor() {
    if (!themeColorMeta) return;
    themeColorMeta.setAttribute("content", themeIsDark() ? "#181a1d" : "#fdfdfc");
  }

  function setTheme(theme) {
    window.clearTimeout(themeTransitionTimer);
    root.classList.add("theme-transition");
    root.getBoundingClientRect();
    root.setAttribute("data-theme", theme);
    try {
      window.localStorage.setItem("zeqi-site-theme", theme);
    } catch (error) {
      // The selected theme still works for this page view when storage is unavailable.
    }
    updateThemeLabel();
    updateThemeColor();
    themeTransitionTimer = window.setTimeout(function () {
      root.classList.remove("theme-transition");
    }, 320);
  }

  function closeMenu() {
    if (!menuButton || !navigation) return;
    menuButton.setAttribute("aria-expanded", "false");
    navigation.setAttribute("data-open", "false");
  }

  if (themeButton) {
    updateThemeLabel();
    updateThemeColor();
    themeButton.addEventListener("click", function () {
      setTheme(themeIsDark() ? "light" : "dark");
    });
  }

  if (window.matchMedia) {
    var systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
    var syncSystemTheme = function () {
      if (!root.hasAttribute("data-theme")) {
        updateThemeLabel();
        updateThemeColor();
      }
    };

    if (systemTheme.addEventListener) systemTheme.addEventListener("change", syncSystemTheme);
    else if (systemTheme.addListener) systemTheme.addListener(syncSystemTheme);
  }

  if (menuButton && navigation) {
    menuButton.addEventListener("click", function () {
      var isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      navigation.setAttribute("data-open", String(!isOpen));
    });

    navigation.addEventListener("click", function (event) {
      if (event.target.closest("a")) closeMenu();
    });

    document.addEventListener("click", function (event) {
      var menuIsOpen = menuButton.getAttribute("aria-expanded") === "true";
      var clickedOutsideMenu = !navigation.contains(event.target) && !menuButton.contains(event.target);
      if (menuIsOpen && clickedOutsideMenu) closeMenu();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeMenu();
        menuButton.focus();
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 720) closeMenu();
    });
  }

  yearNodes.forEach(function (node) {
    node.textContent = String(new Date().getFullYear());
  });

  document.querySelectorAll(".abstract-toggle").forEach(function (button) {
    button.addEventListener("click", function () {
      var willOpen = button.getAttribute("aria-expanded") !== "true";

      document.querySelectorAll(".abstract-toggle[aria-expanded=\"true\"]").forEach(function (other) {
        var otherPanel = document.getElementById(other.getAttribute("aria-controls"));
        other.setAttribute("aria-expanded", "false");
        if (otherPanel) otherPanel.hidden = true;
      });

      var panel = document.getElementById(button.getAttribute("aria-controls"));
      button.setAttribute("aria-expanded", String(willOpen));
      if (panel) panel.hidden = !willOpen;
    });
  });
})();
