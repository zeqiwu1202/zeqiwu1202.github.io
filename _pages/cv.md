---
layout: cv
permalink: /cv/
title: CV
nav: true
nav_order: 6
cv_pdf: Zeqi_CV.pdf
description:
toc:
  sidebar: left
---

<div class="cv">

  <div class="card mt-3 p-3">
    <h3 class="card-title font-weight-medium">Education</h3>
    <ul class="card-text font-weight-light list-group list-group-flush">
      {% for edu in site.data.cv.education %}
      <li class="list-group-item">
        <div class="row">
          <div class="col-xs-2 cl-sm-2 col-md-auto text-left" style="min-width: 75px;">
            <span class="badge font-weight-bold danger-color-dark text-uppercase align-middle" style="min-width: 75px;">
              {% if edu.endDate == "Present" or edu.endDate == "present" %}
                {{ edu.startDate | date: "%Y" }} - Now
              {% else %}
                {{ edu.startDate | date: "%Y" }} - {{ edu.endDate | date: "%Y" }}
              {% endif %}
            </span>
          </div>
          <div class="col-xs-10 cl-sm-10 col-md mt-2 mt-md-0">
            <h6 class="title font-weight-bold ml-1 ml-md-4">
              <a href="{{ edu.url }}" target="_blank">{{ edu.institution }}</a>
            </h6>
            <h6 class="ml-1 ml-md-4" style="font-size: 0.95rem;">
              {{ edu.studyType }} in {{ edu.area }}
            </h6>
            <h6 class="ml-1 ml-md-4" style="font-size: 0.95rem; font-style: italic;">
              {{ edu.location }}
            </h6>
          </div>
        </div>
      </li>
      {% endfor %}
    </ul>
  </div>

  <div class="card mt-4 p-3">
    <h3 class="card-title font-weight-medium">Languages</h3>
    <div class="ml-1 ml-md-4">
      <ul class="list-unstyled">
        {% for lang in site.data.cv.languages %}
        <li class="mb-2">
          <strong>{{ lang.language }}:</strong> {{ lang.fluency }}
        </li>
        {% endfor %}
      </ul>
    </div>
  </div>

</div>