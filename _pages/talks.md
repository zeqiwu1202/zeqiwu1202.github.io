---
layout: page
permalink: /talks/
title: Talks
description: 
nav: true
nav_order: 5
---

<style>
  /* 容器：使用 Flex 布局 */
  .talk-row {
    display: flex;
    margin-bottom: 30px; /* 每个 Talk 之间的间距 */
    align-items: baseline; /* 保持文字基线对齐 */
  }

  /* 左侧：日期 */
  .talk-date {
    flex: 0 0 120px; /* 固定宽度，防止换行 */
    font-family: 'Open Sans', sans-serif;
    font-size: 0.9rem;
    /* 关键点：不要写死颜色，使用继承颜色的透明度 */
    color: inherit; 
    opacity: 0.6; 
  }

  /* 右侧：内容容器 */
  .talk-content {
    flex: 1;
    font-family: 'Open Sans', sans-serif;
  }

  /* 会议标题 */
  .talk-event {
    font-weight: 600;
    font-size: 1.1rem;
    color: inherit; /* 自动跟随主题色（黑或白） */
    margin-bottom: 4px;
    line-height: 1.4;
  }

  /* 地点信息 */
  .talk-loc {
    font-size: 0.95rem;
    font-style: italic;
    color: inherit;
    opacity: 0.8; /* 稍微比日期深一点，比标题浅一点 */
    margin-bottom: 6px;
  }

  /* 幻灯片按钮 */
  .talk-link a {
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 600;
    text-decoration: none;
    padding: 2px 8px;
    border-radius: 4px;
    transition: all 0.2s ease;
    
    /* 适配黑白主题的核心：使用 currentColor */
    color: inherit; 
    border: 1px solid currentColor; 
    opacity: 0.5; /* 默认半透明 */
  }

  /* 鼠标悬停时的效果 */
  .talk-link a:hover {
    opacity: 1; /* 变实心 */
    background-color: var(--global-theme-color, #007bff); /* 尝试调用主题色，如果没有就用蓝色 */
    border-color: transparent;
    color: #fff !important; /* 悬停时文字强制变白 */
    text-decoration: none;
  }
  
  /* 移动端适配：屏幕变窄时，改为上下排列 */
  @media (max-width: 576px) {
    .talk-row {
      flex-direction: column;
      margin-bottom: 35px;
    }
    .talk-date {
      margin-bottom: 4px;
      font-weight: 600;
      opacity: 0.5;
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
    <div class="talk-event">The 10th Meeting of Young Econometricians (YEAP)</div>
    <div class="talk-loc">Peking University, Beijing, China</div>
  </div>
</div>

<div class="talk-row">
  <div class="talk-date">Jul 2025</div>
  <div class="talk-content">
    <div class="talk-event">Asian Summer School in Econometrics and Statistics</div>
    <div class="talk-loc">Xiamen University, Xiamen, China</div>
  </div>
</div>