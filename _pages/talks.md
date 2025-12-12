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
  

  @media (max-width: 576px) {
    .talk-row {
      flex-direction: column; /* 上下排列 */
      margin-bottom: 30px;    /* 每一项之间的距离 */
    }
    
    .talk-date {
      width: 100%;            /* 占满整行 */
      margin-bottom: 0px;     /* 核心：去除日期的下边距 */
      padding-bottom: 0px;    /* 核心：去除内边距 */
      line-height: 1.2;       /* 核心：收紧行高，防止文字上下有留白 */
      
      font-weight: 600;
      font-size: 0.85rem;     /* 稍微调小一点，显得精致 */
      opacity: 0.6;
      letter-spacing: 0.5px;  /* 稍微加点字间距，增加可读性 */
      text-transform: uppercase; /* 变大写（可选），看起来像分类标签 */
    }

    .talk-content {
      width: 100%;
    }

    .talk-event {
      margin-top: 2px;       /* 核心：标题距离上方日期的距离，极小 */
      line-height: 1.3;      /* 防止标题自己太高 */
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