---
layout: page
permalink: /talks/
title: Talks
description: 
nav: true
nav_order: 5
---

<style>
  /* ============ Desktop Base Styles ============ */
  .talk-row {
    display: flex;
    margin-bottom: 30px; /* Consistent vertical spacing between items */
    align-items: baseline; 
  }

  /* Left column: Date */
  .talk-date {
    flex: 0 0 120px; /* Fixed width */
    font-family: 'Open Sans', sans-serif;
    font-size: 0.9rem;
    /* Use inherited color with opacity for dark mode compatibility */
    color: inherit; 
    opacity: 0.6; 
  }

  /* Right column: Content container */
  .talk-content {
    flex: 1;
    font-family: 'Open Sans', sans-serif;
  }

  /* Event Title */
  .talk-event {
    font-weight: 600;
    font-size: 1.1rem;
    color: inherit; /* Automatically adapts to theme color */
    margin-bottom: 4px;
    line-height: 1.4;
  }

  /* Location Info */
  .talk-loc {
    font-size: 0.95rem;
    font-style: italic;
    color: inherit;
    opacity: 0.8;
    margin-bottom: 6px; /* Bottom margin for spacing consistency */
  }

  /* --- FIX: Button Container --- */
  .talk-link {
    /* Add 6px margin to match .talk-loc spacing, ensuring equal gaps between items */
    margin-bottom: 6px; 
    display: block; 
  }

  /* Slides Button Style */
  .talk-link a {
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 600;
    text-decoration: none;
    padding: 2px 8px;
    border-radius: 4px;
    transition: all 0.2s ease;
    
    /* Dark mode core: use currentColor to adapt to text color */
    color: inherit; 
    border: 1px solid currentColor; 
    opacity: 0.5; /* Semi-transparent by default */
  }

  /* Button Hover Effect */
  .talk-link a:hover {
    opacity: 1;
    background-color: var(--global-theme-color, #007bff); /* Use theme color if available */
    border-color: transparent;
    color: #fff !important; /* Force white text on hover */
  }
  
  /* ============ Mobile Responsiveness (Force Override) ============ */
  @media (max-width: 576px) {
    .talk-row {
      flex-direction: column !important; /* Stack vertically */
      margin-bottom: 25px !important;    /* Adjusted spacing for mobile */
      align-items: flex-start !important;
    }
    
    .talk-date {
      flex: none !important;
      width: 100% !important;
      margin-bottom: 0px !important; /* Remove bottom margin to stack tightly */
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
      margin-top: 2px !important; /* Minimal gap between date and title */
      line-height: 1.3 !important;
    }
  }
</style>

<div class="talk-row">
  <div class="talk-date">Nov 2025</div>
  <div class="talk-content">
    <div class="talk-event">Clubear Online Seminar</div>
    <div class="talk-link">
      <a href="../assets/pdf/FDM_clubear.pdf" target="_blank">Click for Slides</a>
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