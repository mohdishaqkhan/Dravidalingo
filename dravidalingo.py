#!/usr/bin/env python3
"""
DravidaLingo - Learn South Indian Languages
Python launcher: embeds the full app HTML and serves it locally.
Requires Python 3.6+. No third-party dependencies needed.

Run:  python3 dravidalingo.py
"""

import os
import sys
import threading
import webbrowser
import http.server
import socketserver
import time

# ── Embedded HTML (the full app) ──────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>DravidaLingo</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Noto+Sans+Telugu&family=Noto+Sans+Kannada&family=Noto+Sans+Tamil&family=Noto+Nastaliq+Urdu&family=Noto+Sans+Malayalam&display=swap" rel="stylesheet" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --brand: #4CAF50;
    --brand-light: #E8F5E9;
    --brand-dark: #2E7D32;
    --accent: #FF7043;
    --accent-light: #FBE9E7;
    --yellow: #FFC107;
    --yellow-light: #FFF8E1;
    --blue: #1976D2;
    --blue-light: #E3F2FD;
    --purple: #7B1FA2;
    --purple-light: #F3E5F5;
    --radius: 16px;
    --radius-sm: 10px;
  }

  body { font-family: 'Baloo 2', sans-serif; background: #F5F7FA; min-height: 100vh; }

  .app { max-width: 480px; margin: 0 auto; background: #fff; min-height: 100vh; display: flex; flex-direction: column; position: relative; }

  .screen { display: none; flex-direction: column; flex: 1; }
  .screen.active { display: flex; }

  /* Language Select Screen */
  .lang-header { background: linear-gradient(135deg, #1B5E20 0%, #388E3C 60%, #66BB6A 100%); padding: 40px 24px 32px; text-align: center; }
  .lang-header h1 { font-size: 32px; font-weight: 800; color: #fff; letter-spacing: -0.5px; }
  .lang-header p { color: rgba(255,255,255,0.85); font-size: 15px; margin-top: 6px; }
  .owl { font-size: 64px; margin-bottom: 12px; display: block; }

  .lang-body { padding: 24px; flex: 1; background: #F5F7FA; }
  .lang-body h2 { font-size: 16px; font-weight: 600; color: #555; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.5px; }

  .lang-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .lang-card { background: #fff; border-radius: var(--radius); padding: 20px 16px; text-align: center; cursor: pointer; border: 2.5px solid transparent; transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  .lang-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
  .lang-card.selected { border-color: var(--brand); background: var(--brand-light); }
  .lang-flag { font-size: 40px; margin-bottom: 8px; display: block; }
  .lang-name { font-size: 16px; font-weight: 700; color: #222; }
  .lang-script { font-size: 18px; color: #666; margin-top: 4px; }
  .lang-speakers { font-size: 11px; color: #999; margin-top: 2px; }

  .start-btn { background: var(--brand); color: #fff; border: none; border-radius: var(--radius); padding: 18px; font-size: 17px; font-weight: 700; font-family: 'Baloo 2', sans-serif; cursor: pointer; margin: 20px 24px 24px; width: calc(100% - 48px); transition: all 0.2s; letter-spacing: 0.3px; }
  .start-btn:hover { background: var(--brand-dark); transform: translateY(-1px); }
  .start-btn:disabled { background: #ccc; cursor: not-allowed; transform: none; }

  /* Top Bar */
  .top-bar { background: #fff; border-bottom: 1px solid #eee; padding: 14px 20px; display: flex; align-items: center; gap: 12px; }
  .back-btn { background: none; border: none; font-size: 22px; cursor: pointer; color: #555; line-height: 1; padding: 2px; }
  .top-bar-title { font-size: 17px; font-weight: 700; color: #222; flex: 1; }
  .streak { display: flex; align-items: center; gap: 4px; font-size: 14px; font-weight: 700; color: var(--accent); }

  /* XP Bar */
  .xp-section { padding: 14px 20px; background: #fff; border-bottom: 1px solid #f0f0f0; }
  .xp-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
  .xp-label { font-size: 12px; color: #999; font-weight: 500; }
  .xp-val { font-size: 12px; color: var(--brand-dark); font-weight: 700; }
  .xp-bar { background: #E8F5E9; border-radius: 8px; height: 8px; overflow: hidden; }
  .xp-fill { background: linear-gradient(90deg, var(--brand), #81C784); height: 100%; border-radius: 8px; transition: width 0.5s ease; }

  /* Practice Tabs */
  .practice-tabs { display: flex; padding: 16px 20px 0; gap: 8px; background: #fff; border-bottom: 1px solid #f0f0f0; overflow-x: auto; }
  .ptab { background: none; border: none; font-family: 'Baloo 2', sans-serif; font-size: 13px; font-weight: 600; color: #999; padding: 8px 14px; border-radius: 20px; cursor: pointer; white-space: nowrap; transition: all 0.15s; }
  .ptab.active { background: var(--brand); color: #fff; }
  .ptab:hover:not(.active) { background: var(--brand-light); color: var(--brand-dark); }

  /* Lesson List */
  .lesson-list { padding: 16px 20px; flex: 1; overflow-y: auto; background: #F5F7FA; }
  .section-title { font-size: 13px; font-weight: 700; color: #999; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 12px; margin-top: 8px; }
  .section-title:first-child { margin-top: 0; }

  .lesson-card { background: #fff; border-radius: var(--radius); padding: 16px; margin-bottom: 10px; cursor: pointer; border: 2px solid transparent; transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.05); display: flex; align-items: center; gap: 14px; }
  .lesson-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,0.1); border-color: var(--brand); }
  .lesson-card.locked { opacity: 0.5; cursor: not-allowed; }
  .lesson-card.locked:hover { transform: none; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-color: transparent; }
  .lesson-card.completed { border-color: var(--brand); background: var(--brand-light); }

  .lesson-icon { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 26px; flex-shrink: 0; }
  .lesson-info { flex: 1; }
  .lesson-title { font-size: 15px; font-weight: 700; color: #222; }
  .lesson-sub { font-size: 12px; color: #999; margin-top: 2px; }
  .lesson-badge { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; }
  .badge-done { background: var(--brand-light); color: var(--brand-dark); }
  .badge-new { background: var(--yellow-light); color: #795548; }
  .badge-locked { background: #f0f0f0; color: #bbb; }

  /* Exercise Screen */
  .exercise-screen { flex-direction: column; background: #fff; }
  .progress-bar { padding: 16px 20px 8px; display: flex; align-items: center; gap: 12px; }
  .prog-back { background: none; border: none; font-size: 22px; cursor: pointer; color: #777; }
  .prog-track { flex: 1; background: #f0f0f0; height: 10px; border-radius: 5px; overflow: hidden; }
  .prog-fill { background: linear-gradient(90deg, var(--brand), #81C784); height: 100%; border-radius: 5px; transition: width 0.4s ease; }
  .prog-hearts { font-size: 15px; color: var(--accent); font-weight: 700; }

  .exercise-body { flex: 1; padding: 24px 20px; display: flex; flex-direction: column; overflow-y: auto; }
  .ex-type-badge { font-size: 12px; font-weight: 700; color: var(--blue); background: var(--blue-light); padding: 4px 12px; border-radius: 20px; display: inline-block; margin-bottom: 16px; }
  .ex-question { font-size: 22px; font-weight: 800; color: #111; line-height: 1.3; margin-bottom: 8px; }
  .ex-hint { font-size: 14px; color: #999; margin-bottom: 24px; }

  .script-display { font-size: 56px; text-align: center; padding: 24px; background: var(--brand-light); border-radius: var(--radius); margin-bottom: 24px; border: 2px dashed var(--brand); line-height: 1.2; }

  .options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
  .option-btn { background: #fff; border: 2px solid #e0e0e0; border-radius: var(--radius-sm); padding: 14px 12px; font-family: 'Baloo 2', sans-serif; font-size: 15px; font-weight: 600; color: #333; cursor: pointer; transition: all 0.15s; text-align: center; }
  .option-btn:hover:not(:disabled) { border-color: var(--blue); background: var(--blue-light); color: var(--blue); }
  .option-btn.correct { border-color: var(--brand) !important; background: var(--brand-light) !important; color: var(--brand-dark) !important; }
  .option-btn.wrong { border-color: var(--accent) !important; background: var(--accent-light) !important; color: #BF360C !important; }
  .option-btn:disabled { cursor: not-allowed; }

  .word-tiles { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
  .word-tile { background: #fff; border: 2px solid #ddd; border-radius: 10px; padding: 10px 16px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.15s; user-select: none; }
  .word-tile:hover { border-color: var(--blue); background: var(--blue-light); }
  .word-tile.used { opacity: 0.35; cursor: not-allowed; }

  .answer-zone { min-height: 52px; border: 2px dashed #ccc; border-radius: 10px; padding: 8px 12px; display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 16px; }
  .answer-zone:empty::before { content: 'Tap words to build the answer'; color: #bbb; font-size: 14px; }
  .answer-tile { background: var(--purple); color: #fff; border-radius: 8px; padding: 8px 14px; font-size: 14px; font-weight: 600; cursor: pointer; }

  .feedback-bar { border-radius: var(--radius); padding: 16px; margin-bottom: 16px; display: none; }
  .feedback-bar.show { display: flex; align-items: flex-start; gap: 12px; }
  .feedback-bar.correct-fb { background: var(--brand-light); }
  .feedback-bar.wrong-fb { background: var(--accent-light); }
  .fb-icon { font-size: 24px; }
  .fb-text h4 { font-size: 15px; font-weight: 700; margin-bottom: 2px; }
  .fb-text p { font-size: 13px; color: #666; }
  .correct-fb h4 { color: var(--brand-dark); }
  .wrong-fb h4 { color: #BF360C; }

  .check-btn { background: var(--brand); color: #fff; border: none; border-radius: var(--radius-sm); padding: 16px; font-size: 17px; font-weight: 700; font-family: 'Baloo 2', sans-serif; cursor: pointer; width: 100%; transition: all 0.2s; margin-top: auto; }
  .check-btn:hover { background: var(--brand-dark); }
  .check-btn:disabled { background: #ccc; cursor: not-allowed; }

  /* AI Explanation */
  .ai-section { background: #F0F4FF; border-radius: var(--radius); padding: 14px; margin-bottom: 16px; }
  .ai-section h4 { font-size: 13px; font-weight: 700; color: var(--blue); margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
  .ai-response { font-size: 14px; color: #333; line-height: 1.6; }
  .ai-loading { color: #999; font-size: 13px; font-style: italic; }

  /* Results Screen */
  .results-screen { flex-direction: column; align-items: center; background: #fff; padding: 40px 24px; text-align: center; }
  .result-emoji { font-size: 80px; margin-bottom: 16px; }
  .result-title { font-size: 28px; font-weight: 800; color: #222; }
  .result-sub { font-size: 16px; color: #777; margin: 8px 0 28px; }
  .result-stats { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; width: 100%; margin-bottom: 28px; }
  .rstat { background: #F5F7FA; border-radius: var(--radius-sm); padding: 16px 8px; }
  .rstat-val { font-size: 24px; font-weight: 800; color: #222; }
  .rstat-label { font-size: 11px; color: #999; font-weight: 600; margin-top: 4px; }
  .rstat.highlight .rstat-val { color: var(--brand-dark); }

  .continue-btn { background: var(--brand); color: #fff; border: none; border-radius: var(--radius-sm); padding: 16px 40px; font-size: 17px; font-weight: 700; font-family: 'Baloo 2', sans-serif; cursor: pointer; transition: all 0.2s; }
  .continue-btn:hover { background: var(--brand-dark); }

  /* Bottom Nav */
  .nav-bottom { display: flex; border-top: 1px solid #eee; background: #fff; }
  .nav-item { flex: 1; padding: 12px 4px; display: flex; flex-direction: column; align-items: center; gap: 3px; cursor: pointer; color: #bbb; font-size: 10px; font-weight: 600; transition: color 0.15s; }
  .nav-item.active { color: var(--brand); }
  .nav-item i { font-size: 24px; }
</style>
</head>
<body>

<div class="app">

  <!-- LANGUAGE SELECT SCREEN -->
  <div class="screen active" id="screen-lang">
    <div class="lang-header">
      <span class="owl">&#129417;</span>
      <h1>DravidaLingo</h1>
      <p>Learn South Indian languages the fun way</p>
    </div>
    <div class="lang-body">
      <h2>Choose your language</h2>
      <div class="lang-grid">
        <div class="lang-card" onclick="selectLang('telugu')" id="card-telugu">
          <span class="lang-flag">&#127963;</span>
          <div class="lang-name">Telugu</div>
          <div class="lang-script">&#3108;&#3142;&#3122;&#3137;&#3095;&#3137;</div>
          <div class="lang-speakers">~96M speakers</div>
        </div>
        <div class="lang-card" onclick="selectLang('kannada')" id="card-kannada">
          <span class="lang-flag">&#127800;</span>
          <div class="lang-name">Kannada</div>
          <div class="lang-script">&#3221;&#3240;&#3277;&#3240;&#3233;</div>
          <div class="lang-speakers">~58M speakers</div>
        </div>
        <div class="lang-card" onclick="selectLang('tamil')" id="card-tamil">
          <span class="lang-flag">&#127994;</span>
          <div class="lang-name">Tamil</div>
          <div class="lang-script">&#2980;&#2990;&#3007;&#2996;&#3021;</div>
          <div class="lang-speakers">~87M speakers</div>
        </div>
        <div class="lang-card" onclick="selectLang('urdu')" id="card-urdu">
          <span class="lang-flag">&#9765;&#65039;</span>
          <div class="lang-name">Urdu</div>
          <div class="lang-script">&#1575;&#1585;&#1583;&#1608;</div>
          <div class="lang-speakers">~70M speakers</div>
        </div>
        <div class="lang-card" onclick="selectLang('malayalam')" id="card-malayalam" style="grid-column: 1 / -1; max-width: 50%; margin: 0 auto;">
          <span class="lang-flag">&#127796;</span>
          <div class="lang-name">Malayalam</div>
          <div class="lang-script">&#3374;&#3378;&#3375;&#3390;&#3379;&#3330;</div>
          <div class="lang-speakers">~38M speakers</div>
        </div>
      </div>
    </div>
    <button class="start-btn" id="start-btn" onclick="goToPractice()" disabled>Select a language to begin</button>
  </div>

  <!-- PRACTICE SCREEN -->
  <div class="screen" id="screen-practice">
    <div class="top-bar">
      <button class="back-btn" onclick="goToLangSelect()">&#8592;</button>
      <div class="top-bar-title" id="top-lang-title">Learning Telugu</div>
      <div class="streak">&#128293; <span id="streak-count">1</span></div>
    </div>
    <div class="xp-section">
      <div class="xp-row">
        <span class="xp-label">Daily XP</span>
        <span class="xp-val" id="xp-display">0 / 50 XP</span>
      </div>
      <div class="xp-bar"><div class="xp-fill" id="xp-fill" style="width:0%"></div></div>
    </div>
    <div class="practice-tabs">
      <button class="ptab active" onclick="switchTab('basics', this)">&#128221; Basics</button>
      <button class="ptab" onclick="switchTab('greetings', this)">&#128075; Greetings</button>
      <button class="ptab" onclick="switchTab('numbers', this)">&#128290; Numbers</button>
      <button class="ptab" onclick="switchTab('phrases', this)">&#128172; Phrases</button>
    </div>
    <div class="lesson-list" id="lesson-list"></div>
    <div class="nav-bottom">
      <div class="nav-item active"><i class="ti ti-brand-speedtest"></i>Practice</div>
      <div class="nav-item"><i class="ti ti-trophy"></i>Leaderboard</div>
      <div class="nav-item"><i class="ti ti-user"></i>Profile</div>
    </div>
  </div>

  <!-- EXERCISE SCREEN -->
  <div class="screen" id="screen-exercise">
    <div class="progress-bar">
      <button class="prog-back" onclick="exitExercise()">&#10005;</button>
      <div class="prog-track"><div class="prog-fill" id="prog-fill" style="width:0%"></div></div>
      <div class="prog-hearts">&#10084;&#65039; <span id="hearts-count">3</span></div>
    </div>
    <div class="exercise-body" id="exercise-body"></div>
  </div>

  <!-- RESULTS SCREEN -->
  <div class="screen" id="screen-results">
    <div class="results-screen">
      <div class="result-emoji" id="result-emoji">&#127881;</div>
      <div class="result-title" id="result-title">Lesson Complete!</div>
      <div class="result-sub" id="result-sub">Great work! Keep the streak going.</div>
      <div class="result-stats">
        <div class="rstat highlight">
          <div class="rstat-val" id="res-xp">+15</div>
          <div class="rstat-label">XP Earned</div>
        </div>
        <div class="rstat">
          <div class="rstat-val" id="res-acc">100%</div>
          <div class="rstat-label">Accuracy</div>
        </div>
        <div class="rstat">
          <div class="rstat-val" id="res-time">0s</div>
          <div class="rstat-label">Time</div>
        </div>
      </div>
      <button class="continue-btn" onclick="goToPractice()">Continue</button>
    </div>
  </div>

</div>

<script>
const LANG_DATA = {
  telugu: {
    name: 'Telugu', script: '\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41', color: '#E65100',
    lessons: {
      basics: [
        { id:'tl-b1', title:'Vowels (\u0c05\u0c1a\u0c4d\u0c1a\u0c41\u0c32\u0c41)', sub:'a, i, u, e, o', icon:'\ud83d\udcda', color:'#FFF3E0', iconColor:'#E65100', done:true,
          exercises:[
            {type:'script', q:'What sound does this make?', script:'\u0c05', answer:'a', options:['a','i','u','e'], hint:'First vowel in Telugu'},
            {type:'script', q:'What sound does this make?', script:'\u0c07', answer:'i', options:['a','i','u','o'], hint:'Second vowel'},
            {type:'script', q:'What sound does this make?', script:'\u0c09', answer:'u', options:['e','a','u','o'], hint:'Third vowel'},
            {type:'translate', q:'How do you write "a" in Telugu?', answer:'\u0c05', options:['\u0c05','\u0c07','\u0c09','\u0c0f'], hint:'The first letter'},
            {type:'translate', q:'How do you write "ka" in Telugu?', answer:'\u0c15', options:['\u0c1f','\u0c15','\u0c17','\u0c1a'], hint:'Starts like "k"'},
          ]
        },
        { id:'tl-b2', title:'Consonants', sub:'k, g, ch, j, t', icon:'\ud83d\udd24', color:'#E3F2FD', iconColor:'#1565C0', done:false,
          exercises:[
            {type:'script', q:'What is this consonant?', script:'\u0c15', answer:'ka', options:['ka','ga','cha','ta'], hint:'Sounds like K'},
            {type:'script', q:'What is this consonant?', script:'\u0c17', answer:'ga', options:['ka','ga','cha','ja'], hint:'Soft G sound'},
            {type:'translate', q:'Translate: "ka" in Telugu', answer:'\u0c15', options:['\u0c15','\u0c17','\u0c1a','\u0c1c'], hint:''},
            {type:'build', q:'Arrange to spell "\u0c15\u0c2e\u0c32" (Kamala)', words:['\u0c15','\u0c2e','\u0c32','\u0c21'], answer:'\u0c15\u0c2e\u0c32', hint:'A lotus flower'},
          ]
        },
        { id:'tl-b3', title:'Numbers 1\u20135', sub:'\u0c12\u0c15\u0c1f\u0c3f to \u0c05\u0c2f\u0c3f\u0c26\u0c41', icon:'\ud83d\udd22', color:'#E8F5E9', iconColor:'#2E7D32', done:false,
          exercises:[
            {type:'translate', q:'What is "\u0c12\u0c15\u0c1f\u0c3f" in English?', answer:'One', options:['One','Two','Three','Four'], hint:'The first number'},
            {type:'translate', q:'How do you say "Three" in Telugu?', answer:'\u0c2e\u0c42\u0c21\u0c41', options:['\u0c12\u0c15\u0c1f\u0c3f','\u0c30\u0c46\u0c02\u0c21\u0c41','\u0c2e\u0c42\u0c21\u0c41','\u0c28\u0c3e\u0c32\u0c41\u0c17\u0c41'], hint:''},
            {type:'script', q:'What number is this?', script:'\u0c30\u0c46\u0c02\u0c21\u0c41', answer:'Two', options:['One','Two','Three','Five'], hint:''},
          ]
        },
      ],
      greetings: [
        { id:'tl-g1', title:'Hello & Goodbye', sub:'\u0c28\u0c2e\u0c38\u0c4d\u0c15\u0c3e\u0c30\u0c02', icon:'\ud83d\udc4b', color:'#F3E5F5', iconColor:'#6A1B9A', done:false,
          exercises:[
            {type:'translate', q:'How do you say "Hello" in Telugu?', answer:'\u0c28\u0c2e\u0c38\u0c4d\u0c15\u0c3e\u0c30\u0c02', options:['\u0c28\u0c2e\u0c38\u0c4d\u0c15\u0c3e\u0c30\u0c02','\u0c27\u0c28\u0c4d\u0c2f\u0c35\u0c3e\u0c26\u0c3e\u0c32\u0c41','\u0c15\u0c4d\u0c37\u0c2e\u0c3f\u0c02\u0c1a\u0c02\u0c21\u0c3f','\u0c36\u0c41\u0c2d\u0c4b\u0c26\u0c2f\u0c02'], hint:'The classic greeting'},
            {type:'translate', q:'What does "\u0c27\u0c28\u0c4d\u0c2f\u0c35\u0c3e\u0c26\u0c3e\u0c32\u0c41" mean?', answer:'Thank you', options:['Hello','Goodbye','Thank you','Sorry'], hint:''},
            {type:'translate', q:'How do you say "Good morning"?', answer:'\u0c36\u0c41\u0c2d\u0c4b\u0c26\u0c2f\u0c02', options:['\u0c36\u0c41\u0c2d\u0c4b\u0c26\u0c2f\u0c02','\u0c28\u0c2e\u0c38\u0c4d\u0c15\u0c3e\u0c30\u0c02','\u0c35\u0c40\u0c21\u0c4d\u0c15\u0c4b\u0c32\u0c41','\u0c36\u0c41\u0c2d \u0c30\u0c3e\u0c24\u0c4d\u0c30\u0c3f'], hint:'Subho + dayam'},
          ]
        },
      ],
      numbers: [
        { id:'tl-n1', title:'Numbers 1\u201310', sub:'\u0c12\u0c15\u0c1f\u0c3f \u0c28\u0c41\u0c02\u0c21\u0c3f \u0c2a\u0c26\u0c3f', icon:'\ud83d\udd22', color:'#E0F2F1', iconColor:'#00695C', done:false,
          exercises:[
            {type:'translate', q:'What is "\u0c05\u0c2f\u0c3f\u0c26\u0c41" in English?', answer:'Five', options:['Four','Five','Six','Seven'], hint:''},
            {type:'translate', q:'Say "Ten" in Telugu', answer:'\u0c2a\u0c26\u0c3f', options:['\u0c24\u0c4a\u0c2e\u0c4d\u0c2e\u0c3f\u0c26\u0c3f','\u0c2a\u0c26\u0c3f','\u0c0e\u0c28\u0c3f\u0c2e\u0c3f\u0c26\u0c3f','\u0c0f\u0c21\u0c41'], hint:''},
          ]
        },
      ],
      phrases: [
        { id:'tl-p1', title:'Basic Phrases', sub:'Daily expressions', icon:'\ud83d\udcac', color:'#FBE9E7', iconColor:'#BF360C', done:false,
          exercises:[
            {type:'translate', q:'How do you say "What is your name?" in Telugu?', answer:'\u0c2e\u0c40 \u0c2a\u0c47\u0c30\u0c47\u0c2e\u0c3f\u0c1f\u0c3f?', options:['\u0c2e\u0c40\u0c30\u0c41 \u0c0e\u0c15\u0c4d\u0c15\u0c21 \u0c09\u0c28\u0c4d\u0c28\u0c3e\u0c30\u0c41?','\u0c2e\u0c40 \u0c2a\u0c47\u0c30\u0c47\u0c2e\u0c3f\u0c1f\u0c3f?','\u0c2e\u0c40\u0c15\u0c41 \u0c28\u0c1a\u0c4d\u0c1a\u0c3f\u0c02\u0c26\u0c3e?','\u0c2e\u0c40\u0c30\u0c41 \u0c2c\u0c3e\u0c17\u0c41\u0c28\u0c4d\u0c28\u0c3e\u0c30\u0c3e?'], hint:''},
            {type:'translate', q:'What does "\u0c28\u0c3e\u0c15\u0c41 \u0c05\u0c30\u0c4d\u0c27\u0c02 \u0c15\u0c3e\u0c32\u0c47\u0c26\u0c41" mean?', answer:"I don't understand", options:['I am fine','What is this?',"I don't understand",'Where are you?'], hint:''},
          ]
        },
      ]
    }
  },
  kannada: {
    name: 'Kannada', script: '\u0c95\u0ca8\u0ccd\u0ca8\u0ca1', color: '#6A1B9A',
    lessons: {
      basics: [
        { id:'kn-b1', title:'Vowels (\u0cb8\u0ccd\u0cb5\u0cb0\u0c97\u0cb3\u0cc1)', sub:'a, i, u, e, o', icon:'\ud83d\udcda', color:'#F3E5F5', iconColor:'#6A1B9A', done:true,
          exercises:[
            {type:'script', q:'What sound does this make?', script:'\u0c85', answer:'a', options:['a','i','u','e'], hint:'First Kannada vowel'},
            {type:'script', q:'What sound does this make?', script:'\u0c87', answer:'i', options:['a','i','o','u'], hint:''},
            {type:'translate', q:'Write "ka" in Kannada', answer:'\u0c95', options:['\u0c95','\u0c97','\u0c9a','\u0c9f'], hint:''},
          ]
        },
        { id:'kn-b2', title:'Consonants', sub:'k, g, t, d, n', icon:'\ud83d\udd24', color:'#E3F2FD', iconColor:'#1565C0', done:false,
          exercises:[
            {type:'script', q:'What is this letter?', script:'\u0c97', answer:'ga', options:['ka','ga','ja','ta'], hint:'Soft G'},
            {type:'translate', q:'How do you say "One" in Kannada?', answer:'\u0c92\u0c82\u0ca6\u0cc1', options:['\u0c92\u0c82\u0ca6\u0cc1','\u0c8e\u0cb0\u0ca1\u0cc1','\u0cae\u0cc2\u0cb0\u0cc1','\u0ca8\u0cbe\u0cb2\u0ccd\u0c95\u0cc1'], hint:''},
          ]
        },
      ],
      greetings: [
        { id:'kn-g1', title:'Greetings', sub:'\u0ca8\u0cae\u0cb8\u0ccd\u0c95\u0cbe\u0cb0', icon:'\ud83d\udc4b', color:'#E8EAF6', iconColor:'#283593', done:false,
          exercises:[
            {type:'translate', q:'How do you say "Hello" in Kannada?', answer:'\u0ca8\u0cae\u0cb8\u0ccd\u0c95\u0cbe\u0cb0', options:['\u0ca8\u0cae\u0cb8\u0ccd\u0c95\u0cbe\u0cb0','\u0ca7\u0ca8\u0ccd\u0caf\u0cb5\u0cbe\u0ca6','\u0cac\u0cb0\u0ccd\u0ca4\u0cc0\u0ca8\u0cbf','\u0cb6\u0cc1\u0cad\u0ccb\u0ca6\u0caf'], hint:'Classic greeting'},
            {type:'translate', q:'What is "Thank you" in Kannada?', answer:'\u0ca7\u0ca8\u0ccd\u0caf\u0cb5\u0cbe\u0ca6', options:['\u0ca8\u0cae\u0cb8\u0ccd\u0c95\u0cbe\u0cb0','\u0ca7\u0ca8\u0ccd\u0caf\u0cb5\u0cbe\u0ca6','\u0c95\u0ccd\u0cb7\u0cae\u0cbf\u0cb8\u0cbf','\u0cb9\u0cc7\u0c97\u0cbf\u0ca6\u0ccd\u0ca6\u0cc0\u0cb0\u0cbf'], hint:''},
          ]
        },
      ],
      numbers: [
        { id:'kn-n1', title:'Numbers 1\u20135', sub:'\u0c92\u0c82\u0ca6\u0cc1 to \u0c90\u0ca6\u0cc1', icon:'\ud83d\udd22', color:'#E0F2F1', iconColor:'#00695C', done:false,
          exercises:[
            {type:'translate', q:'What is "\u0cae\u0cc2\u0cb0\u0cc1" in English?', answer:'Three', options:['Two','Three','Four','Five'], hint:''},
            {type:'translate', q:'Say "Five" in Kannada', answer:'\u0c90\u0ca6\u0cc1', options:['\u0cae\u0cc2\u0cb0\u0cc1','\u0ca8\u0cbe\u0cb2\u0ccd\u0c95\u0cc1','\u0c90\u0ca6\u0cc1','\u0c86\u0cb0\u0cc1'], hint:''},
          ]
        },
      ],
      phrases: [
        { id:'kn-p1', title:'Daily Phrases', sub:'Everyday Kannada', icon:'\ud83d\udcac', color:'#FBE9E7', iconColor:'#BF360C', done:false,
          exercises:[
            {type:'translate', q:'How do you ask "How are you?" in Kannada?', answer:'\u0cb9\u0cc7\u0c97\u0cbf\u0ca6\u0ccd\u0ca6\u0cc0\u0cb0\u0cbf?', options:['\u0cb9\u0cc6\u0cb8\u0cb0\u0cc7\u0ca8\u0cc1?','\u0cb9\u0cc7\u0c97\u0cbf\u0ca6\u0ccd\u0ca6\u0cc0\u0cb0\u0cbf?','\u0c8e\u0cb7\u0ccd\u0c9f\u0cc1 \u0c86\u0caf\u0ccd\u0ca4\u0cc1?','\u0c8e\u0cb2\u0ccd\u0cb2\u0cbf \u0c87\u0ca6\u0ccd\u0ca6\u0cc0\u0cb0\u0cbf?'], hint:''},
          ]
        },
      ]
    }
  },
  tamil: {
    name: 'Tamil', script: '\u0ba4\u0bae\u0bbf\u0bb4\u0bcd', color: '#B71C1C',
    lessons: {
      basics: [
        { id:'ta-b1', title:'Vowels (\u0b89\u0baf\u0bbf\u0bb0\u0bc6\u0bb4\u0bc1\u0ba4\u0bcd\u0ba4\u0bc1)', sub:'a, i, u, e, o', icon:'\ud83d\udcda', color:'#FFEBEE', iconColor:'#B71C1C', done:true,
          exercises:[
            {type:'script', q:'What sound does this make?', script:'\u0b85', answer:'a', options:['a','i','u','e'], hint:'First Tamil vowel'},
            {type:'script', q:'What sound does this make?', script:'\u0b87', answer:'i', options:['a','i','o','u'], hint:''},
            {type:'translate', q:'Write "ka" in Tamil', answer:'\u0b95', options:['\u0b95','\u0b9f','\u0b9a','\u0ba8'], hint:''},
            {type:'build', q:'Arrange to spell "\u0b95\u0bae\u0bb2\u0bcd" (Kamal)', words:['\u0b95','\u0bae','\u0bb2\u0bcd','\u0b9f'], answer:'\u0b95\u0bae\u0bb2\u0bcd', hint:'A lotus'},
          ]
        },
        { id:'ta-b2', title:'Consonants', sub:'\u0b95, \u0b9a, \u0b9f, \u0ba4, \u0baa', icon:'\ud83d\udd24', color:'#E3F2FD', iconColor:'#1565C0', done:false,
          exercises:[
            {type:'script', q:'What consonant is this?', script:'\u0b9a', answer:'sa/cha', options:['ka','sa/cha','ta','na'], hint:''},
            {type:'translate', q:'How do you say "One" in Tamil?', answer:'\u0b92\u0ba9\u0bcd\u0bb1\u0bc1', options:['\u0b92\u0ba9\u0bcd\u0bb1\u0bc1','\u0b87\u0bb0\u0ba3\u0bcd\u0b9f\u0bc1','\u0bae\u0bc2\u0ba9\u0bcd\u0bb1\u0bc1','\u0ba8\u0bbe\u0ba9\u0bcd\u0b95\u0bc1'], hint:''},
          ]
        },
      ],
      greetings: [
        { id:'ta-g1', title:'Greetings', sub:'\u0bb5\u0ba3\u0b95\u0bcd\u0b95\u0bae\u0bcd', icon:'\ud83d\udc4b', color:'#FCE4EC', iconColor:'#880E4F', done:false,
          exercises:[
            {type:'translate', q:'How do you say "Hello" in Tamil?', answer:'\u0bb5\u0ba3\u0b95\u0bcd\u0b95\u0bae\u0bcd', options:['\u0bb5\u0ba3\u0b95\u0bcd\u0b95\u0bae\u0bcd','\u0ba8\u0ba9\u0bcd\u0bb1\u0bbf','\u0bae\u0ba9\u0bcd\u0ba9\u0bbf\u0b95\u0bcd\u0b95\u0bb5\u0bc1\u0bae\u0bcd','\u0b95\u0bbe\u0bb2\u0bc8 \u0bb5\u0ba3\u0b95\u0bcd\u0b95\u0bae\u0bcd'], hint:'The universal Tamil greeting'},
            {type:'translate', q:'What does "\u0ba8\u0ba9\u0bcd\u0bb1\u0bbf" mean?', answer:'Thank you', options:['Hello','Goodbye','Thank you','Sorry'], hint:''},
          ]
        },
      ],
      numbers: [
        { id:'ta-n1', title:'Numbers 1\u20135', sub:'\u0b92\u0ba9\u0bcd\u0bb1\u0bc1 to \u0b90\u0ba8\u0bcd\u0ba4\u0bc1', icon:'\ud83d\udd22', color:'#E0F2F1', iconColor:'#00695C', done:false,
          exercises:[
            {type:'translate', q:'What is "\u0bae\u0bc2\u0ba9\u0bcd\u0bb1\u0bc1" in English?', answer:'Three', options:['Two','Three','Four','Five'], hint:''},
            {type:'translate', q:'Say "Five" in Tamil', answer:'\u0b90\u0ba8\u0bcd\u0ba4\u0bc1', options:['\u0bae\u0bc2\u0ba9\u0bcd\u0bb1\u0bc1','\u0ba8\u0bbe\u0ba9\u0bcd\u0b95\u0bc1','\u0b90\u0ba8\u0bcd\u0ba4\u0bc1','\u0b86\u0bb1\u0bc1'], hint:''},
          ]
        },
      ],
      phrases: [
        { id:'ta-p1', title:'Daily Phrases', sub:'Everyday Tamil', icon:'\ud83d\udcac', color:'#FBE9E7', iconColor:'#BF360C', done:false,
          exercises:[
            {type:'translate', q:'How do you ask "What is your name?" in Tamil?', answer:'\u0b89\u0b99\u0bcd\u0b95\u0bb3\u0bcd \u0baa\u0bc6\u0baf\u0bb0\u0bcd \u0b8e\u0ba9\u0bcd\u0ba9?', options:['\u0ba8\u0bc0\u0b99\u0bcd\u0b95\u0bb3\u0bcd \u0b8e\u0b99\u0bcd\u0b95\u0bc7 \u0b87\u0bb0\u0bc1\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bc0\u0bb0\u0bcd\u0b95\u0bb3\u0bcd?','\u0b89\u0b99\u0bcd\u0b95\u0bb3\u0bcd \u0baa\u0bc6\u0baf\u0bb0\u0bcd \u0b8e\u0ba9\u0bcd\u0ba9?','\u0ba8\u0bc0\u0b99\u0bcd\u0b95\u0bb3\u0bcd \u0b8e\u0baa\u0bcd\u0baa\u0b9f\u0bbf \u0b87\u0bb0\u0bc1\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bc0\u0bb0\u0bcd\u0b95\u0bb3\u0bcd?','\u0b89\u0b99\u0bcd\u0b95\u0bb3\u0bc1\u0b95\u0bcd\u0b95\u0bc1 \u0baa\u0bc1\u0bb0\u0bbf\u0b95\u0bbf\u0bb1\u0ba4\u0bbe?'], hint:''},
          ]
        },
      ]
    }
  },
  urdu: {
    name: 'Urdu', script: '\u0627\u0631\u062f\u0648', color: '#1A237E',
    lessons: {
      basics: [
        { id:'ur-b1', title:'Alphabet (\u062d\u0631\u0648\u0641\u0650 \u062a\u06c1\u062c\u06cc)', sub:'alef, ba, ta, sa', icon:'\ud83d\udcda', color:'#E8EAF6', iconColor:'#1A237E', done:true,
          exercises:[
            {type:'script', q:'What letter is this?', script:'\u0627', answer:'Alef (a)', options:['Alef (a)','Ba (b)','Ta (t)','Jim (j)'], hint:'First letter of Arabic-Urdu alphabet'},
            {type:'script', q:'What letter is this?', script:'\u0628', answer:'Ba (b)', options:['Alef (a)','Ba (b)','Pa (p)','Ta (t)'], hint:''},
            {type:'translate', q:'How do you write "one" in Urdu?', answer:'\u0627\u06cc\u06a9', options:['\u0627\u06cc\u06a9','\u062f\u0648','\u062a\u06cc\u0646','\u0686\u0627\u0631'], hint:'Ek'},
          ]
        },
        { id:'ur-b2', title:'Common Letters', sub:'Jim, dal, ra, sin', icon:'\ud83d\udd24', color:'#E3F2FD', iconColor:'#1565C0', done:false,
          exercises:[
            {type:'script', q:'What letter is this?', script:'\u0633', answer:'Sin (s)', options:['Sin (s)','Shin (sh)','Sad (s)','Zal (z)'], hint:''},
            {type:'translate', q:'How do you say "Two" in Urdu?', answer:'\u062f\u0648', options:['\u0627\u06cc\u06a9','\u062f\u0648','\u062a\u06cc\u0646','\u067e\u0627\u0646\u0686'], hint:'Do'},
          ]
        },
      ],
      greetings: [
        { id:'ur-g1', title:'Greetings', sub:'\u0633\u0644\u0627\u0645', icon:'\ud83d\udc4b', color:'#E8EAF6', iconColor:'#283593', done:false,
          exercises:[
            {type:'translate', q:'How do you say "Hello/Peace" in Urdu?', answer:'\u0627\u0644\u0633\u0644\u0627\u0645 \u0639\u0644\u06cc\u06a9\u0645', options:['\u0627\u0644\u0633\u0644\u0627\u0645 \u0639\u0644\u06cc\u06a9\u0645','\u0634\u06a9\u0631\u06cc\u06c1','\u0645\u0639\u0627\u0641 \u06a9\u0631\u06cc\u06ba','\u062e\u062f\u0627\u062d\u0627\u0641\u0638'], hint:'The Islamic greeting'},
            {type:'translate', q:'What does "\u0634\u06a9\u0631\u06cc\u06c1" mean?', answer:'Thank you', options:['Hello','Goodbye','Thank you','Sorry'], hint:'Shukriya'},
          ]
        },
      ],
      numbers: [
        { id:'ur-n1', title:'Numbers 1\u20135', sub:'\u0627\u06cc\u06a9 \u0633\u06d2 \u067e\u0627\u0646\u0686', icon:'\ud83d\udd22', color:'#E0F2F1', iconColor:'#00695C', done:false,
          exercises:[
            {type:'translate', q:'What is "\u062a\u06cc\u0646" in English?', answer:'Three', options:['Two','Three','Four','Five'], hint:'Teen'},
            {type:'translate', q:'Say "Five" in Urdu', answer:'\u067e\u0627\u0646\u0686', options:['\u062a\u06cc\u0646','\u0686\u0627\u0631','\u067e\u0627\u0646\u0686','\u0686\u06be'], hint:'Paanch'},
          ]
        },
      ],
      phrases: [
        { id:'ur-p1', title:'Daily Phrases', sub:'Everyday Urdu', icon:'\ud83d\udcac', color:'#FBE9E7', iconColor:'#BF360C', done:false,
          exercises:[
            {type:'translate', q:'How do you ask "How are you?" in Urdu?', answer:'\u0622\u067e \u06a9\u06cc\u0633\u06d2 \u06c1\u06cc\u06ba?', options:['\u0622\u067e \u06a9\u0627 \u0646\u0627\u0645 \u06a9\u06cc\u0627 \u06c1\u06d2?','\u0622\u067e \u06a9\u06cc\u0633\u06d2 \u06c1\u06cc\u06ba?','\u0622\u067e \u06a9\u06c1\u0627\u06ba \u06c1\u06cc\u06ba?','\u06a9\u06cc\u0627 \u0622\u067e \u0633\u0645\u062c\u06be\u06d2?'], hint:'Aap kaise hain?'},
          ]
        },
      ]
    }
  },
  malayalam: {
    name: 'Malayalam', script: '\u0d2e\u0d32\u0d2f\u0d3e\u0d33\u0d02', color: '#004D40',
    lessons: {
      basics: [
        { id:'ml-b1', title:'Vowels (\u0d38\u0d4d\u0d35\u0d30\u0d19\u0d4d\u0d19\u0d33\u0d4d\u200d)', sub:'a, i, u, e, o', icon:'\ud83d\udcda', color:'#E0F2F1', iconColor:'#004D40', done:true,
          exercises:[
            {type:'script', q:'What sound does this make?', script:'\u0d05', answer:'a', options:['a','i','u','e'], hint:'First Malayalam vowel'},
            {type:'script', q:'What sound does this make?', script:'\u0d07', answer:'i', options:['a','i','o','u'], hint:''},
            {type:'translate', q:'Write "ka" in Malayalam', answer:'\u0d15', options:['\u0d15','\u0d17','\u0d1a','\u0d1f'], hint:''},
          ]
        },
        { id:'ml-b2', title:'Consonants', sub:'\u0d15, \u0d17, \u0d1a, \u0d1f, \u0d24', icon:'\ud83d\udd24', color:'#E3F2FD', iconColor:'#1565C0', done:false,
          exercises:[
            {type:'script', q:'What consonant is this?', script:'\u0d17', answer:'ga', options:['ka','ga','cha','ta'], hint:'Soft G'},
            {type:'translate', q:'How do you say "One" in Malayalam?', answer:'\u0d12\u0d28\u0d4d\u0d28\u0d4d', options:['\u0d12\u0d28\u0d4d\u0d28\u0d4d','\u0d30\u0d23\u0d4d\u0d1f\u0d4d','\u0d2e\u0d42\u0d28\u0d4d\u0d28\u0d4d','\u0d28\u0d3e\u0d32\u0d4d'], hint:'Onnu'},
          ]
        },
      ],
      greetings: [
        { id:'ml-g1', title:'Greetings', sub:'\u0d28\u0d2e\u0d38\u0d4d\u0d15\u0d3e\u0d30\u0d02', icon:'\ud83d\udc4b', color:'#F3E5F5', iconColor:'#4A148C', done:false,
          exercises:[
            {type:'translate', q:'How do you say "Hello" in Malayalam?', answer:'\u0d28\u0d2e\u0d38\u0d4d\u0d15\u0d3e\u0d30\u0d02', options:['\u0d28\u0d2e\u0d38\u0d4d\u0d15\u0d3e\u0d30\u0d02','\u0d28\u0d28\u0d4d\u0d26\u0d3f','\u0d15\u0d4d\u0d37\u0d2e\u0d3f\u0d15\u0d4d\u0d15\u0d23\u0d02','\u0d38\u0d41\u0d2a\u0d4d\u0d30\u0d2d\u0d3e\u0d24\u0d02'], hint:''},
            {type:'translate', q:'What does "\u0d28\u0d28\u0d4d\u0d26\u0d3f" mean?', answer:'Thank you', options:['Hello','Goodbye','Thank you','Sorry'], hint:'Nandi'},
          ]
        },
      ],
      numbers: [
        { id:'ml-n1', title:'Numbers 1\u20135', sub:'\u0d12\u0d28\u0d4d\u0d28\u0d4d to \u0d05\u0d1e\u0d4d\u0d1a\u0d4d', icon:'\ud83d\udd22', color:'#E0F2F1', iconColor:'#00695C', done:false,
          exercises:[
            {type:'translate', q:'What is "\u0d2e\u0d42\u0d28\u0d4d\u0d28\u0d4d" in English?', answer:'Three', options:['Two','Three','Four','Five'], hint:'Moonn'},
            {type:'translate', q:'Say "Five" in Malayalam', answer:'\u0d05\u0d1e\u0d4d\u0d1a\u0d4d', options:['\u0d2e\u0d42\u0d28\u0d4d\u0d28\u0d4d','\u0d28\u0d3e\u0d32\u0d4d','\u0d05\u0d1e\u0d4d\u0d1a\u0d4d','\u0d06\u0d31\u0d4d'], hint:'Anchu'},
          ]
        },
      ],
      phrases: [
        { id:'ml-p1', title:'Daily Phrases', sub:'Everyday Malayalam', icon:'\ud83d\udcac', color:'#FBE9E7', iconColor:'#BF360C', done:false,
          exercises:[
            {type:'translate', q:'How do you ask "How are you?" in Malayalam?', answer:'\u0d38\u0d41\u0d16\u0d2e\u0d3e\u0d23\u0d4b?', options:['\u0d2a\u0d47\u0d30\u0d4d \u0d0e\u0d28\u0d4d\u0d24\u0d4d?','\u0d38\u0d41\u0d16\u0d2e\u0d3e\u0d23\u0d4b?','\u0d0e\u0d35\u0d3f\u0d1f\u0d46 \u0d06\u0d23\u0d4d?','\u0d2e\u0d28\u0d38\u0d4d\u0d38\u0d3f\u0d32\u0d3e\u0d2f\u0d4b?'], hint:'Sukhamaano?'},
          ]
        },
      ]
    }
  }
};

let currentLang = null;
let currentTab = 'basics';
let currentLesson = null;
let currentExercises = [];
let currentExIdx = 0;
let hearts = 3;
let correct = 0;
let xp = 0;
let startTime = 0;
let selectedOption = null;
let answered = false;
let buildAnswer = [];
let completedLessons = {};

function selectLang(lang) {
  currentLang = lang;
  document.querySelectorAll('.lang-card').forEach(c => c.classList.remove('selected'));
  document.getElementById('card-' + lang).classList.add('selected');
  const btn = document.getElementById('start-btn');
  btn.disabled = false;
  btn.textContent = 'Start Learning ' + LANG_DATA[lang].name + ' \u2192';
}

function goToLangSelect() {
  showScreen('lang');
}

function goToPractice() {
  if (!currentLang) return;
  document.getElementById('top-lang-title').textContent = 'Learning ' + LANG_DATA[currentLang].name;
  renderLessons();
  showScreen('practice');
}

function switchTab(tab, el) {
  currentTab = tab;
  document.querySelectorAll('.ptab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  renderLessons();
}

function renderLessons() {
  const data = LANG_DATA[currentLang];
  const lessons = data.lessons[currentTab] || [];
  const list = document.getElementById('lesson-list');
  list.innerHTML = '';

  const secTitle = document.createElement('div');
  secTitle.className = 'section-title';
  secTitle.textContent = { basics:'\ud83d\udcdd Core Skills', greetings:'\ud83d\udc4b Greetings', numbers:'\ud83d\udd22 Numbers', phrases:'\ud83d\udcac Phrases' }[currentTab] || 'Lessons';
  list.appendChild(secTitle);

  lessons.forEach((lesson, idx) => {
    const isDone = completedLessons[lesson.id];
    const isLocked = idx > 0 && !completedLessons[lessons[idx-1].id] && !lesson.done;
    const card = document.createElement('div');
    card.className = 'lesson-card' + (isDone ? ' completed' : '') + (isLocked ? ' locked' : '');
    const badge = isDone
      ? '<span class="lesson-badge badge-done">\u2713 Done</span>'
      : isLocked
        ? '<span class="lesson-badge badge-locked">\ud83d\udd12 Locked</span>'
        : '<span class="lesson-badge badge-new">\u2726 Start</span>';
    card.innerHTML = `
      <div class="lesson-icon" style="background:${lesson.color}; color:${lesson.iconColor}">${lesson.icon}</div>
      <div class="lesson-info">
        <div class="lesson-title">${lesson.title}</div>
        <div class="lesson-sub">${lesson.sub} \u00b7 ${lesson.exercises.length} exercises</div>
      </div>
      ${badge}
    `;
    if (!isLocked) card.onclick = () => startLesson(lesson);
    list.appendChild(card);
  });

  if (lessons.length === 0) {
    list.innerHTML += '<div style="text-align:center;padding:40px;color:#bbb;font-size:15px;">More lessons coming soon! \ud83d\ude80</div>';
  }
  updateXP();
}

function updateXP() {
  const pct = Math.min((xp / 50) * 100, 100);
  document.getElementById('xp-fill').style.width = pct + '%';
  document.getElementById('xp-display').textContent = xp + ' / 50 XP';
}

function startLesson(lesson) {
  currentLesson = lesson;
  currentExercises = [...lesson.exercises];
  currentExIdx = 0;
  hearts = 3;
  correct = 0;
  answered = false;
  startTime = Date.now();
  showScreen('exercise');
  renderExercise();
}

function getFontFamily() {
  return {
    telugu: 'Noto Sans Telugu',
    kannada: 'Noto Sans Kannada',
    tamil: 'Noto Sans Tamil',
    urdu: 'Noto Nastaliq Urdu',
    malayalam: 'Noto Sans Malayalam'
  }[currentLang] || 'sans-serif';
}

function renderExercise() {
  const ex = currentExercises[currentExIdx];
  const prog = (currentExIdx / currentExercises.length) * 100;
  document.getElementById('prog-fill').style.width = prog + '%';
  document.getElementById('hearts-count').textContent = hearts;
  selectedOption = null;
  answered = false;
  buildAnswer = [];

  const body = document.getElementById('exercise-body');
  const typeLabel = { script:'Identify the Script', translate:'Translate', build:'Build the Word' }[ex.type] || 'Exercise';
  const fontFamily = getFontFamily();

  let html = `<div class="ex-type-badge">${typeLabel}</div>`;
  html += `<div class="ex-question">${ex.q}</div>`;
  if (ex.hint) html += `<div class="ex-hint">Hint: ${ex.hint}</div>`;

  if (ex.type === 'script' || ex.type === 'translate') {
    if (ex.script) {
      html += `<div class="script-display" style="font-family:'${fontFamily}',sans-serif">${ex.script}</div>`;
    }
    html += `<div class="options-grid" id="opts">`;
    ex.options.forEach((opt) => {
      const fontStyle = !ex.script ? `font-family:'${fontFamily}',sans-serif;font-size:18px;` : '';
      const safeOpt = opt.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
      const safeAns = ex.answer.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
      html += `<button class="option-btn" style="${fontStyle}" onclick="selectOpt(this,'${safeOpt}','${safeAns}')">${opt}</button>`;
    });
    html += `</div>`;
  } else if (ex.type === 'build') {
    html += `<div class="answer-zone" id="answer-zone"></div>`;
    html += `<div class="word-tiles" id="word-tiles">`;
    ex.words.forEach((w, i) => {
      html += `<div class="word-tile" id="tile-${i}" onclick="addTile(this,'${w}',${i})">${w}</div>`;
    });
    html += `</div>`;
  }

  html += `<div class="feedback-bar" id="fb"></div>`;
  html += `<div class="ai-section" id="ai-section" style="display:none"><h4>\ud83e\udd16 AI Explanation</h4><div class="ai-response" id="ai-resp"><span class="ai-loading">Generating explanation...</span></div></div>`;
  html += `<button class="check-btn" id="check-btn" onclick="checkAnswer()" disabled>Check</button>`;

  body.innerHTML = html;
}

function addTile(el, word, idx) {
  if (el.classList.contains('used')) {
    buildAnswer = buildAnswer.filter(b => b.idx !== idx);
    el.classList.remove('used');
  } else {
    buildAnswer.push({ word, idx });
    el.classList.add('used');
  }
  const zone = document.getElementById('answer-zone');
  zone.innerHTML = buildAnswer.map(b => `<div class="answer-tile" onclick="removeTile(${b.idx})">${b.word}</div>`).join('');
  document.getElementById('check-btn').disabled = buildAnswer.length === 0;
}

function removeTile(idx) {
  buildAnswer = buildAnswer.filter(b => b.idx !== idx);
  const el = document.getElementById('tile-' + idx);
  if (el) el.classList.remove('used');
  const zone = document.getElementById('answer-zone');
  zone.innerHTML = buildAnswer.map(b => `<div class="answer-tile" onclick="removeTile(${b.idx})">${b.word}</div>`).join('');
  document.getElementById('check-btn').disabled = buildAnswer.length === 0;
}

function selectOpt(el, opt, answer) {
  if (answered) return;
  selectedOption = opt;
  document.querySelectorAll('.option-btn').forEach(b => {
    b.style.borderColor = '';
    b.style.background = '';
  });
  el.style.borderColor = '#1976D2';
  el.style.background = '#E3F2FD';
  document.getElementById('check-btn').disabled = false;
}

function checkAnswer() {
  if (answered) { nextExercise(); return; }
  answered = true;
  const ex = currentExercises[currentExIdx];
  let isCorrect = false;

  if (ex.type === 'build') {
    const built = buildAnswer.map(b => b.word).join('');
    isCorrect = built === ex.answer;
    document.querySelectorAll('.word-tile').forEach(t => t.onclick = null);
  } else {
    isCorrect = selectedOption === ex.answer;
    document.querySelectorAll('.option-btn').forEach(btn => {
      btn.disabled = true;
      btn.style.borderColor = '';
      btn.style.background = '';
      if (btn.textContent.trim() === ex.answer) btn.classList.add('correct');
      else if (btn.textContent.trim() === selectedOption && !isCorrect) btn.classList.add('wrong');
    });
  }

  if (isCorrect) { correct++; } else { hearts = Math.max(0, hearts - 1); }
  document.getElementById('hearts-count').textContent = hearts;

  showFeedback(isCorrect, ex);
  fetchAIExplanation(ex, isCorrect);

  const btn = document.getElementById('check-btn');
  btn.textContent = currentExIdx < currentExercises.length - 1 ? 'Continue \u2192' : 'Finish!';
  btn.style.background = isCorrect ? '#4CAF50' : '#FF7043';
  btn.disabled = false;
}

function showFeedback(isCorrect, ex) {
  const fb = document.getElementById('fb');
  fb.className = 'feedback-bar show ' + (isCorrect ? 'correct-fb' : 'wrong-fb');
  fb.innerHTML = isCorrect
    ? `<div class="fb-icon">\u2705</div><div class="fb-text"><h4>Correct!</h4><p>Excellent work! Keep it up!</p></div>`
    : `<div class="fb-icon">\u274c</div><div class="fb-text"><h4>Incorrect</h4><p>Correct answer: <strong>${ex.answer}</strong></p></div>`;
}

async function fetchAIExplanation(ex, isCorrect) {
  const aiSec = document.getElementById('ai-section');
  const aiResp = document.getElementById('ai-resp');
  aiSec.style.display = 'block';
  aiResp.innerHTML = '<span class="ai-loading">Generating explanation...</span>';

  const langName = LANG_DATA[currentLang].name;
  const prompt = `You are a ${langName} language tutor. In 2-3 short sentences, explain this language fact: "${ex.q}" — the answer is "${ex.answer}". Give an interesting memory tip or cultural context. Be friendly and encouraging. Keep it very brief.`;

  try {
    const resp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 1000,
        messages: [{ role: 'user', content: prompt }]
      })
    });
    const data = await resp.json();
    const text = data.content?.map(c => c.text || '').join('') || 'Could not load explanation.';
    aiResp.textContent = text;
  } catch(e) {
    aiResp.textContent = 'AI explanation unavailable. Keep practicing!';
  }
}

function nextExercise() {
  currentExIdx++;
  if (hearts <= 0 || currentExIdx >= currentExercises.length) {
    finishLesson();
  } else {
    renderExercise();
  }
}

function finishLesson() {
  const earned = Math.round((correct / currentExercises.length) * 15) + 5;
  xp = Math.min(xp + earned, 50);
  completedLessons[currentLesson.id] = true;
  const elapsed = Math.round((Date.now() - startTime) / 1000);
  const acc = Math.round((correct / currentExercises.length) * 100);

  document.getElementById('result-emoji').textContent = acc >= 80 ? '\ud83c\udf89' : acc >= 50 ? '\ud83d\udc4f' : '\ud83d\udcaa';
  document.getElementById('result-title').textContent = acc >= 80 ? 'Excellent!' : acc >= 50 ? 'Good job!' : 'Keep Practicing!';
  document.getElementById('result-sub').textContent = `You got ${correct}/${currentExercises.length} correct in ${currentLesson.title}`;
  document.getElementById('res-xp').textContent = '+' + earned;
  document.getElementById('res-acc').textContent = acc + '%';
  document.getElementById('res-time').textContent = elapsed + 's';
  showScreen('results');
  updateXP();
}

function exitExercise() {
  showScreen('practice');
}

function showScreen(name) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById('screen-' + name).classList.add('active');
}
</script>
</body>
</html>"""


# ── HTTP Server ───────────────────────────────────────────────────────────────

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(HTML.encode("utf-8"))))
        # Allow the Anthropic API call from our local origin
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def log_message(self, fmt, *args):
        pass  # suppress request logs


def find_free_port(start=8765):
    import socket
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start


def run():
    port = find_free_port()
    url  = f"http://127.0.0.1:{port}"

    # Start server in daemon thread so it dies when the script exits
    server = socketserver.TCPServer(("127.0.0.1", port), Handler)
    server.allow_reuse_address = True
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    print(f"\n  🦉  DravidaLingo is running!")
    print(f"  ➜  Opening: {url}\n")
    print("  Press Ctrl+C to stop.\n")

    # Brief delay so the server is ready, then open browser
    time.sleep(0.3)
    webbrowser.open(url)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Shutting down. Goodbye!")
        server.shutdown()


if __name__ == "__main__":
    run()
