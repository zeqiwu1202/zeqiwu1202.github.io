document.addEventListener("DOMContentLoaded", function () {
  const publications = document.querySelector(".publications");
  if (!publications) {
    return;
  }

  const updateSearchState = () => {
    const input = document.getElementById("bibsearch");
    const searchTerm = input ? input.value.trim() : "";
    publications.classList.toggle("is-searching", searchTerm.length > 0);
  };

  publications.querySelectorAll("h2.bibliography").forEach((heading, index) => {
    const list = heading.nextElementSibling;
    if (!list || list.tagName !== "OL" || !list.classList.contains("bibliography")) {
      return;
    }

    if (!list.id) {
      list.id = `publication-year-${index}`;
    }

    const year = heading.textContent.trim();
    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "year-toggle";
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-controls", list.id);
    toggle.setAttribute("aria-label", `Collapse ${year} publications`);
    toggle.innerHTML = '<span class="year-toggle-icon" aria-hidden="true"></span>';

    const toggleYear = () => {
      const isCollapsed = list.classList.toggle("year-collapsed");
      heading.classList.toggle("year-collapsed", isCollapsed);
      toggle.setAttribute("aria-expanded", String(!isCollapsed));
      toggle.setAttribute("aria-label", `${isCollapsed ? "Expand" : "Collapse"} ${year} publications`);
    };

    toggle.addEventListener("click", (event) => {
      event.stopPropagation();
      toggleYear();
    });

    heading.addEventListener("click", toggleYear);

    heading.appendChild(toggle);
  });

  const searchInput = document.getElementById("bibsearch");
  if (searchInput) {
    searchInput.addEventListener("input", updateSearchState);
  }
  window.addEventListener("hashchange", updateSearchState);
  updateSearchState();
});
