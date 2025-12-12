---
layout: page
permalink: /talks/
title: Talks
description: 
nav: true
nav_order: 5
---

<style>

  .talk-row {
    display: flex;
    margin-bottom: 30px; 
    align-items: baseline;
  }


  .talk-date {
    flex: 0 0 120px; 
    font-family: 'Open Sans', sans-serif;
    font-size: 0.9rem;
    
    color: inherit; 
    opacity: 0.6; 
  }


  .talk-content {
    flex: 1;
    font-family: 'Open Sans', sans-serif;
  }

  
  .talk-event {
    font-weight: 600;
    font-size: 1.1rem;
    color: inherit; 
    margin-bottom: 4px;
    line-height: 1.4;
  }

  .talk-loc {
    font-size: 0.95rem;
    font-style: italic;
    color: inherit;
    opacity: 0.8;
    margin-bottom: 6px;
  }


  .talk-link a {
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 600;
    text-decoration: none;
    padding: 2px 8px;
    border-radius: 4px;
    transition: all 0.2s ease;
    
    
    color: inherit; 
    border: 1px solid currentColor; 
    opacity: 0.5; 
  }

  
  .talk-link a:hover {
    opacity: 1; 
    background-color: var(--global-theme-color, #007bff); 
    border-color: transparent;
    color: #fff !important; 
    text-decoration: none;
  }
  

 
  @media (max-width: 576px) {
    
    .talk-row {
      flex-direction: column !important;
      margin-bottom: 20px !important;
      align-items: flex-start !important; 
    }
    
    .talk-date {
      flex: none !important;
      width: 100% !important;
      margin-bottom: 0px !important; 
      padding-bottom: 0px !important;
      line-height: 1.2 !important;
      
      font-size: 0.85rem !important;
      opacity: 0.6;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    .talk-content {
      width: 100% !important;
      flex: none !important;
    }

    .talk-event {
      margin-top: 2px !important; /* 只有 2px 的间距 */
      line-height: 1.3 !important;
    }
  }

</style>

<div class="talk-row">
  <div class="talk-date">Nov 2025</div>
  <div class="talk-content">
    <div class="talk-event">Clubear Online Seminar</div>
    <div class="talk-link">
      <a href="../assets/pdf/FDM_clubear.pdf" target="_blank">PDF Slides</a>
    </div>
  </div>
</div>

<div class="talk-row">
  <div class="talk-date">Oct 2025</div>
  <div class="talk-content">
    <div class="talk-event">The 10th Meeting of Young Econometricians in Asian-Pacific Region (YEAP)</div>
    <div class="talk-loc">Peking University, Beijing, China</div>
  </div>
</div>

<div class="talk-row">
  <div class="talk-date">Jul 2025</div>
  <div class="talk-content">
    <div class="talk-event">2025 Asian Summer School in Econometrics and Statistics</div>
    <div class="talk-loc">Xiamen University, Xiamen, China</div>
  </div>
</div>