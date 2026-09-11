---
layout: page
permalink: /publications/
title: Research
description: 
nav: true
nav_order: 2
compact_scale: true
---

<!-- _pages/publications.md -->

<div class="publications research-list">
  <section class="publication-section" aria-labelledby="peer-reviewed-publications">
    <h2 id="peer-reviewed-publications" class="publication-section-title">Peer-reviewed Publications</h2>
    {% bibliography --group_by none --query @*[status=published] %}
  </section>

  <section class="publication-section" aria-labelledby="working-papers">
    <h2 id="working-papers" class="publication-section-title">Working Papers</h2>
    {% bibliography --group_by none --query @*[status=working] %}
  </section>
</div>
