from flask import Flask, render_template_string, request, jsonify
import urllib.request
import json

app = Flask(__name__)

HTML_TEMPLATE = r"""<!DOCTYPE html>
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

  .top-bar { background: #fff; border-bottom: 1px solid #eee; padding: 14px 20px; display: flex; align-items: center; gap: 12px; }
  .back-btn { background: none; border: none; font-size: 22px; cursor: pointer; color: #555; line-height: 1; padding: 2px; }
  .top-bar-title { font-size: 17px; font-weight: 700; color: #222; flex: 1; }
  .streak { display: flex; align-items: center; gap: 4px; font-size: 14px; font-weight: 700; color: var(--accent); }

  .xp-section { padding: 14px 20px; background: #fff; border-bottom: 1px solid #f0f0f0; }
  .xp-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
  .xp-label { font-size: 12px; color: #999; font-weight: 500; }
  .xp-val { font-size: 12px; color: var(--brand-dark); font-weight: 700; }
  .xp-bar { background: #E8F5E9; border-radius: 8px; height: 8px; overflow: hidden; }
  .xp-fill { background: linear-gradient(90deg, var(--brand), #81C784); height: 100%; border-radius: 8px; transition: width 0.5s ease; }

  .practice-tabs { display: flex; padding: 16px 20px 0; gap: 8px; background: #fff; border-bottom: 1px solid #f0f0f0; overflow-x: auto; }
  .ptab { background: none; border: none; font-family: 'Baloo 2', sans-serif; font-size: 13px; font-weight: 600; color: #999; padding: 8px 14px; border-radius: 20px; cursor: pointer; white-space: nowrap; transition: all 0.15s; }
  .ptab.active { background: var(--brand); color: #fff; }
  .ptab:hover:not(.active) { background: var(--brand-light); color: var(--brand-dark); }

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

  .ai-section { background: #F0F4FF; border-radius: var(--radius); padding: 14px; margin-bottom: 16px; }
  .ai-section h4 { font-size: 13px; font-weight: 700; color: var(--blue); margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
  .ai-response { font-size: 14px; color: #333; line-height: 1.6; }
  .ai-loading { color: #999; font-size: 13px; font-style: italic; }

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
      <span class="owl">🦉</span>
      <h1>DravidaLingo</h1>
      <p>Learn South Indian languages the fun way</p>
    </div>
    <div class="lang-body">
      <h2>Choose your language</h2>
      <div class="lang-grid">
        <div class="lang-card" onclick="selectLang('telugu')" id="card-telugu">
          <span class="lang-flag">🏛️</span>
          <div class="lang-name">Telugu</div>
          <div class="lang-script">తెలుగు</div>
          <div class="lang-speakers">~96M speakers</div>
        </div>
        <div class="lang-card" onclick="selectLang('kannada')" id="card-kannada">
          <span class="lang-flag">🌸</span>
          <div class="lang-name">Kannada</div>
          <div class="lang-script">ಕನ್ನಡ</div>
          <div class="lang-speakers">~58M speakers</div>
        </div>
        <div class="lang-card" onclick="selectLang('tamil')" id="card-tamil">
          <span class="lang-flag">🏺</span>
          <div class="lang-name">Tamil</div>
          <div class="lang-script">தமிழ்</div>
          <div class="lang-speakers">~87M speakers</div>
        </div>
        <div class="lang-card" onclick="selectLang('urdu')" id="card-urdu">
          <span class="lang-flag">☪️</span>
          <div class="lang-name">Urdu</div>
          <div class="lang-script">اردو</div>
          <div class="lang-speakers">~70M speakers</div>
        </div>
        <div class="lang-card" onclick="selectLang('malayalam')" id="card-malayalam" style="grid-column: 1 / -1; max-width: 50%; margin: 0 auto;">
          <span class="lang-flag">🌴</span>
          <div class="lang-name">Malayalam</div>
          <div class="lang-script">മലയാളം</div>
          <div class="lang-speakers">~38M speakers</div>
        </div>
      </div>
    </div>
    <button class="start-btn" id="start-btn" onclick="goToPractice()" disabled>Select a language to begin</button>
  </div>

  <!-- PRACTICE SCREEN -->
  <div class="screen" id="screen-practice">
    <div class="top-bar">
      <button class="back-btn" onclick="goToLangSelect()">←</button>
      <div class="top-bar-title" id="top-lang-title">Learning Telugu</div>
      <div class="streak">🔥 <span id="streak-count">1</span></div>
    </div>
    <div class="xp-section">
      <div class="xp-row">
        <span class="xp-label">Daily XP</span>
        <span class="xp-val" id="xp-display">0 / 50 XP</span>
      </div>
      <div class="xp-bar"><div class="xp-fill" id="xp-fill" style="width:0%"></div></div>
    </div>
    <div class="practice-tabs">
      <button class="ptab active" onclick="switchTab('basics', this)">📝 Basics</button>
      <button class="ptab" onclick="switchTab('greetings', this)">👋 Greetings</button>
      <button class="ptab" onclick="switchTab('numbers', this)">🔢 Numbers</button>
      <button class="ptab" onclick="switchTab('phrases', this)">💬 Phrases</button>
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
      <button class="prog-back" onclick="exitExercise()">✕</button>
      <div class="prog-track"><div class="prog-fill" id="prog-fill" style="width:0%"></div></div>
      <div class="prog-hearts">❤️ <span id="hearts-count">3</span></div>
    </div>
    <div class="exercise-body" id="exercise-body"></div>
  </div>

  <!-- RESULTS SCREEN -->
  <div class="screen" id="screen-results">
    <div class="results-screen">
      <div class="result-emoji" id="result-emoji">🎉</div>
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
const LANG_DATA = {{ lang_data | tojson }};

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
  btn.textContent = 'Start Learning ' + LANG_DATA[lang].name + ' →';
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
  secTitle.textContent = { basics:'📝 Core Skills', greetings:'👋 Greetings', numbers:'🔢 Numbers', phrases:'💬 Phrases' }[currentTab] || 'Lessons';
  list.appendChild(secTitle);

  lessons.forEach((lesson, idx) => {
    const isDone = completedLessons[lesson.id];
    const isLocked = idx > 0 && !completedLessons[lessons[idx-1].id] && !lesson.done;
    const card = document.createElement('div');
    card.className = 'lesson-card' + (isDone ? ' completed' : '') + (isLocked ? ' locked' : '');
    const badge = isDone
      ? '<span class="lesson-badge badge-done">✓ Done</span>'
      : isLocked
        ? '<span class="lesson-badge badge-locked">🔒 Locked</span>'
        : '<span class="lesson-badge badge-new">✦ Start</span>';
    card.innerHTML = `
      <div class="lesson-icon" style="background:${lesson.color}; color:${lesson.iconColor}">${lesson.icon}</div>
      <div class="lesson-info">
        <div class="lesson-title">${lesson.title}</div>
        <div class="lesson-sub">${lesson.sub} · ${lesson.exercises.length} exercises</div>
      </div>
      ${badge}
    `;
    if (!isLocked) card.onclick = () => startLesson(lesson);
    list.appendChild(card);
  });

  if (lessons.length === 0) {
    list.innerHTML += '<div style="text-align:center;padding:40px;color:#bbb;font-size:15px;">More lessons coming soon! 🚀</div>';
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
  html += `<div class="ai-section" id="ai-section" style="display:none"><h4>🤖 AI Explanation</h4><div class="ai-response" id="ai-resp"><span class="ai-loading">Generating explanation...</span></div></div>`;
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
  btn.textContent = currentExIdx < currentExercises.length - 1 ? 'Continue →' : 'Finish!';
  btn.style.background = isCorrect ? '#4CAF50' : '#FF7043';
  btn.disabled = false;
}

function showFeedback(isCorrect, ex) {
  const fb = document.getElementById('fb');
  fb.className = 'feedback-bar show ' + (isCorrect ? 'correct-fb' : 'wrong-fb');
  fb.innerHTML = isCorrect
    ? `<div class="fb-icon">✅</div><div class="fb-text"><h4>Correct!</h4><p>Excellent work! Keep it up!</p></div>`
    : `<div class="fb-icon">❌</div><div class="fb-text"><h4>Incorrect</h4><p>Correct answer: <strong>${ex.answer}</strong></p></div>`;
}

async function fetchAIExplanation(ex, isCorrect) {
  const aiSec = document.getElementById('ai-section');
  const aiResp = document.getElementById('ai-resp');
  aiSec.style.display = 'block';
  aiResp.innerHTML = '<span class="ai-loading">Generating explanation...</span>';

  try {
    const resp = await fetch('/api/explain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lang: LANG_DATA[currentLang].name,
        question: ex.q,
        answer: ex.answer,
        isCorrect
      })
    });
    const data = await resp.json();
    aiResp.textContent = data.explanation || 'Could not load explanation.';
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

  document.getElementById('result-emoji').textContent = acc >= 80 ? '🎉' : acc >= 50 ? '👏' : '💪';
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

LANG_DATA = {
    "telugu": {
        "name": "Telugu", "script": "తెలుగు", "color": "#E65100",
        "lessons": {
            "basics": [
                {"id": "tl-b1", "title": "Vowels (అచ్చులు)", "sub": "a, i, u, e, o", "icon": "📚", "color": "#FFF3E0", "iconColor": "#E65100", "done": True,
                 "exercises": [
                     {"type": "script", "q": "What sound does this make?", "script": "అ", "answer": "a", "options": ["a", "i", "u", "e"], "hint": "First vowel in Telugu"},
                     {"type": "script", "q": "What sound does this make?", "script": "ఇ", "answer": "i", "options": ["a", "i", "u", "o"], "hint": "Second vowel"},
                     {"type": "script", "q": "What sound does this make?", "script": "ఉ", "answer": "u", "options": ["e", "a", "u", "o"], "hint": "Third vowel"},
                     {"type": "translate", "q": "How do you write \"a\" in Telugu?", "answer": "అ", "options": ["అ", "ఇ", "ఉ", "ఏ"], "hint": "The first letter"},
                     {"type": "translate", "q": "How do you write \"ka\" in Telugu?", "answer": "క", "options": ["ట", "క", "గ", "చ"], "hint": "Starts like \"k\""},
                 ]},
                {"id": "tl-b2", "title": "Consonants", "sub": "k, g, ch, j, t", "icon": "🔤", "color": "#E3F2FD", "iconColor": "#1565C0", "done": False,
                 "exercises": [
                     {"type": "script", "q": "What is this consonant?", "script": "క", "answer": "ka", "options": ["ka", "ga", "cha", "ta"], "hint": "Sounds like K"},
                     {"type": "script", "q": "What is this consonant?", "script": "గ", "answer": "ga", "options": ["ka", "ga", "cha", "ja"], "hint": "Soft G sound"},
                     {"type": "translate", "q": "Translate: \"ka\" in Telugu", "answer": "క", "options": ["క", "గ", "చ", "జ"], "hint": ""},
                     {"type": "build", "q": "Arrange to spell \"కమల\" (Kamala)", "words": ["క", "మ", "ల", "డ"], "answer": "కమల", "hint": "A lotus flower"},
                 ]},
                {"id": "tl-b3", "title": "Numbers 1–5", "sub": "ఒకటి to అయిదు", "icon": "🔢", "color": "#E8F5E9", "iconColor": "#2E7D32", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "What is \"ఒకటి\" in English?", "answer": "One", "options": ["One", "Two", "Three", "Four"], "hint": "The first number"},
                     {"type": "translate", "q": "How do you say \"Three\" in Telugu?", "answer": "మూడు", "options": ["ఒకటి", "రెండు", "మూడు", "నాలుగు"], "hint": ""},
                     {"type": "script", "q": "What number is this?", "script": "రెండు", "answer": "Two", "options": ["One", "Two", "Three", "Five"], "hint": ""},
                 ]},
            ],
            "greetings": [
                {"id": "tl-g1", "title": "Hello & Goodbye", "sub": "నమస్కారం", "icon": "👋", "color": "#F3E5F5", "iconColor": "#6A1B9A", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you say \"Hello\" in Telugu?", "answer": "నమస్కారం", "options": ["నమస్కారం", "ధన్యవాదాలు", "క్షమించండి", "శుభోదయం"], "hint": "The classic greeting"},
                     {"type": "translate", "q": "What does \"ధన్యవాదాలు\" mean?", "answer": "Thank you", "options": ["Hello", "Goodbye", "Thank you", "Sorry"], "hint": ""},
                     {"type": "translate", "q": "How do you say \"Good morning\"?", "answer": "శుభోదయం", "options": ["శుభోదయం", "నమస్కారం", "వీడ్కోలు", "శుభ రాత్రి"], "hint": "Subho + dayam"},
                 ]},
            ],
            "numbers": [
                {"id": "tl-n1", "title": "Numbers 1–10", "sub": "ఒకటి నుండి పది", "icon": "🔢", "color": "#E0F2F1", "iconColor": "#00695C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "What is \"అయిదు\" in English?", "answer": "Five", "options": ["Four", "Five", "Six", "Seven"], "hint": ""},
                     {"type": "translate", "q": "Say \"Ten\" in Telugu", "answer": "పది", "options": ["తొమ్మిది", "పది", "ఎనిమిది", "ఏడు"], "hint": ""},
                 ]},
            ],
            "phrases": [
                {"id": "tl-p1", "title": "Basic Phrases", "sub": "Daily expressions", "icon": "💬", "color": "#FBE9E7", "iconColor": "#BF360C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you say \"What is your name?\" in Telugu?", "answer": "మీ పేరేమిటి?", "options": ["మీరు ఎక్కడ ఉన్నారు?", "మీ పేరేమిటి?", "మీకు నచ్చిందా?", "మీరు బాగున్నారా?"], "hint": ""},
                     {"type": "translate", "q": "What does \"నాకు అర్థం కాలేదు\" mean?", "answer": "I don't understand", "options": ["I am fine", "What is this?", "I don't understand", "Where are you?"], "hint": ""},
                 ]},
            ]
        }
    },
    "kannada": {
        "name": "Kannada", "script": "ಕನ್ನಡ", "color": "#6A1B9A",
        "lessons": {
            "basics": [
                {"id": "kn-b1", "title": "Vowels (ಸ್ವರಗಳು)", "sub": "a, i, u, e, o", "icon": "📚", "color": "#F3E5F5", "iconColor": "#6A1B9A", "done": True,
                 "exercises": [
                     {"type": "script", "q": "What sound does this make?", "script": "ಅ", "answer": "a", "options": ["a", "i", "u", "e"], "hint": "First Kannada vowel"},
                     {"type": "script", "q": "What sound does this make?", "script": "ಇ", "answer": "i", "options": ["a", "i", "o", "u"], "hint": ""},
                     {"type": "translate", "q": "Write \"ka\" in Kannada", "answer": "ಕ", "options": ["ಕ", "ಗ", "ಚ", "ಟ"], "hint": ""},
                 ]},
                {"id": "kn-b2", "title": "Consonants", "sub": "k, g, t, d, n", "icon": "🔤", "color": "#E3F2FD", "iconColor": "#1565C0", "done": False,
                 "exercises": [
                     {"type": "script", "q": "What is this letter?", "script": "ಗ", "answer": "ga", "options": ["ka", "ga", "ja", "ta"], "hint": "Soft G"},
                     {"type": "translate", "q": "How do you say \"One\" in Kannada?", "answer": "ಒಂದು", "options": ["ಒಂದು", "ಎರಡು", "ಮೂರು", "ನಾಲ್ಕು"], "hint": ""},
                 ]},
            ],
            "greetings": [
                {"id": "kn-g1", "title": "Greetings", "sub": "ನಮಸ್ಕಾರ", "icon": "👋", "color": "#E8EAF6", "iconColor": "#283593", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you say \"Hello\" in Kannada?", "answer": "ನಮಸ್ಕಾರ", "options": ["ನಮಸ್ಕಾರ", "ಧನ್ಯವಾದ", "ಬರ್ತೀನಿ", "ಶುಭೋದಯ"], "hint": "Classic greeting"},
                     {"type": "translate", "q": "What is \"Thank you\" in Kannada?", "answer": "ಧನ್ಯವಾದ", "options": ["ನಮಸ್ಕಾರ", "ಧನ್ಯವಾದ", "ಕ್ಷಮಿಸಿ", "ಹೇಗಿದ್ದೀರಿ"], "hint": ""},
                 ]},
            ],
            "numbers": [
                {"id": "kn-n1", "title": "Numbers 1–5", "sub": "ಒಂದು to ಐದು", "icon": "🔢", "color": "#E0F2F1", "iconColor": "#00695C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "What is \"ಮೂರು\" in English?", "answer": "Three", "options": ["Two", "Three", "Four", "Five"], "hint": ""},
                     {"type": "translate", "q": "Say \"Five\" in Kannada", "answer": "ಐದು", "options": ["ಮೂರು", "ನಾಲ್ಕು", "ಐದು", "ಆರು"], "hint": ""},
                 ]},
            ],
            "phrases": [
                {"id": "kn-p1", "title": "Daily Phrases", "sub": "Everyday Kannada", "icon": "💬", "color": "#FBE9E7", "iconColor": "#BF360C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you ask \"How are you?\" in Kannada?", "answer": "ಹೇಗಿದ್ದೀರಿ?", "options": ["ಹೆಸರೇನು?", "ಹೇಗಿದ್ದೀರಿ?", "ಎಷ್ಟು ಆಯ್ತು?", "ಎಲ್ಲಿ ಇದ್ದೀರಿ?"], "hint": ""},
                 ]},
            ]
        }
    },
    "tamil": {
        "name": "Tamil", "script": "தமிழ்", "color": "#B71C1C",
        "lessons": {
            "basics": [
                {"id": "ta-b1", "title": "Vowels (உயிரெழுத்து)", "sub": "a, i, u, e, o", "icon": "📚", "color": "#FFEBEE", "iconColor": "#B71C1C", "done": True,
                 "exercises": [
                     {"type": "script", "q": "What sound does this make?", "script": "அ", "answer": "a", "options": ["a", "i", "u", "e"], "hint": "First Tamil vowel"},
                     {"type": "script", "q": "What sound does this make?", "script": "இ", "answer": "i", "options": ["a", "i", "o", "u"], "hint": ""},
                     {"type": "translate", "q": "Write \"ka\" in Tamil", "answer": "க", "options": ["க", "ட", "ச", "ந"], "hint": ""},
                     {"type": "build", "q": "Arrange to spell \"கமல்\" (Kamal)", "words": ["க", "ம", "ல்", "ட"], "answer": "கமல்", "hint": "A lotus"},
                 ]},
                {"id": "ta-b2", "title": "Consonants", "sub": "க, ச, ட, த, ப", "icon": "🔤", "color": "#E3F2FD", "iconColor": "#1565C0", "done": False,
                 "exercises": [
                     {"type": "script", "q": "What consonant is this?", "script": "ச", "answer": "sa/cha", "options": ["ka", "sa/cha", "ta", "na"], "hint": ""},
                     {"type": "translate", "q": "How do you say \"One\" in Tamil?", "answer": "ஒன்று", "options": ["ஒன்று", "இரண்டு", "மூன்று", "நான்கு"], "hint": ""},
                 ]},
            ],
            "greetings": [
                {"id": "ta-g1", "title": "Greetings", "sub": "வணக்கம்", "icon": "👋", "color": "#FCE4EC", "iconColor": "#880E4F", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you say \"Hello\" in Tamil?", "answer": "வணக்கம்", "options": ["வணக்கம்", "நன்றி", "மன்னிக்கவும்", "காலை வணக்கம்"], "hint": "The universal Tamil greeting"},
                     {"type": "translate", "q": "What does \"நன்றி\" mean?", "answer": "Thank you", "options": ["Hello", "Goodbye", "Thank you", "Sorry"], "hint": ""},
                 ]},
            ],
            "numbers": [
                {"id": "ta-n1", "title": "Numbers 1–5", "sub": "ஒன்று to ஐந்து", "icon": "🔢", "color": "#E0F2F1", "iconColor": "#00695C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "What is \"மூன்று\" in English?", "answer": "Three", "options": ["Two", "Three", "Four", "Five"], "hint": ""},
                     {"type": "translate", "q": "Say \"Five\" in Tamil", "answer": "ஐந்து", "options": ["மூன்று", "நான்கு", "ஐந்து", "ஆறு"], "hint": ""},
                 ]},
            ],
            "phrases": [
                {"id": "ta-p1", "title": "Daily Phrases", "sub": "Everyday Tamil", "icon": "💬", "color": "#FBE9E7", "iconColor": "#BF360C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you ask \"What is your name?\" in Tamil?", "answer": "உங்கள் பெயர் என்ன?", "options": ["நீங்கள் எங்கே இருக்கிறீர்கள்?", "உங்கள் பெயர் என்ன?", "நீங்கள் எப்படி இருக்கிறீர்கள்?", "உங்களுக்கு புரிகிறதா?"], "hint": ""},
                 ]},
            ]
        }
    },
    "urdu": {
        "name": "Urdu", "script": "اردو", "color": "#1A237E",
        "lessons": {
            "basics": [
                {"id": "ur-b1", "title": "Alphabet (حروفِ تہجی)", "sub": "alef, ba, ta, sa", "icon": "📚", "color": "#E8EAF6", "iconColor": "#1A237E", "done": True,
                 "exercises": [
                     {"type": "script", "q": "What letter is this?", "script": "ا", "answer": "Alef (a)", "options": ["Alef (a)", "Ba (b)", "Ta (t)", "Jim (j)"], "hint": "First letter of Arabic-Urdu alphabet"},
                     {"type": "script", "q": "What letter is this?", "script": "ب", "answer": "Ba (b)", "options": ["Alef (a)", "Ba (b)", "Pa (p)", "Ta (t)"], "hint": ""},
                     {"type": "translate", "q": "How do you write \"one\" in Urdu?", "answer": "ایک", "options": ["ایک", "دو", "تین", "چار"], "hint": "Ek"},
                 ]},
                {"id": "ur-b2", "title": "Common Letters", "sub": "Jim, dal, ra, sin", "icon": "🔤", "color": "#E3F2FD", "iconColor": "#1565C0", "done": False,
                 "exercises": [
                     {"type": "script", "q": "What letter is this?", "script": "س", "answer": "Sin (s)", "options": ["Sin (s)", "Shin (sh)", "Sad (s)", "Zal (z)"], "hint": ""},
                     {"type": "translate", "q": "How do you say \"Two\" in Urdu?", "answer": "دو", "options": ["ایک", "دو", "تین", "پانچ"], "hint": "Do"},
                 ]},
            ],
            "greetings": [
                {"id": "ur-g1", "title": "Greetings", "sub": "سلام", "icon": "👋", "color": "#E8EAF6", "iconColor": "#283593", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you say \"Hello/Peace\" in Urdu?", "answer": "السلام علیکم", "options": ["السلام علیکم", "شکریہ", "معاف کریں", "خداحافظ"], "hint": "The Islamic greeting"},
                     {"type": "translate", "q": "What does \"شکریہ\" mean?", "answer": "Thank you", "options": ["Hello", "Goodbye", "Thank you", "Sorry"], "hint": "Shukriya"},
                 ]},
            ],
            "numbers": [
                {"id": "ur-n1", "title": "Numbers 1–5", "sub": "ایک سے پانچ", "icon": "🔢", "color": "#E0F2F1", "iconColor": "#00695C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "What is \"تین\" in English?", "answer": "Three", "options": ["Two", "Three", "Four", "Five"], "hint": "Teen"},
                     {"type": "translate", "q": "Say \"Five\" in Urdu", "answer": "پانچ", "options": ["تین", "چار", "پانچ", "چھ"], "hint": "Paanch"},
                 ]},
            ],
            "phrases": [
                {"id": "ur-p1", "title": "Daily Phrases", "sub": "Everyday Urdu", "icon": "💬", "color": "#FBE9E7", "iconColor": "#BF360C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you ask \"How are you?\" in Urdu?", "answer": "آپ کیسے ہیں؟", "options": ["آپ کا نام کیا ہے؟", "آپ کیسے ہیں؟", "آپ کہاں ہیں؟", "کیا آپ سمجھے؟"], "hint": "Aap kaise hain?"},
                 ]},
            ]
        }
    },
    "malayalam": {
        "name": "Malayalam", "script": "മലയാളം", "color": "#004D40",
        "lessons": {
            "basics": [
                {"id": "ml-b1", "title": "Vowels (സ്വരങ്ങൾ)", "sub": "a, i, u, e, o", "icon": "📚", "color": "#E0F2F1", "iconColor": "#004D40", "done": True,
                 "exercises": [
                     {"type": "script", "q": "What sound does this make?", "script": "അ", "answer": "a", "options": ["a", "i", "u", "e"], "hint": "First Malayalam vowel"},
                     {"type": "script", "q": "What sound does this make?", "script": "ഇ", "answer": "i", "options": ["a", "i", "o", "u"], "hint": ""},
                     {"type": "translate", "q": "Write \"ka\" in Malayalam", "answer": "ക", "options": ["ക", "ഗ", "ച", "ട"], "hint": ""},
                 ]},
                {"id": "ml-b2", "title": "Consonants", "sub": "ക, ഗ, ച, ട, ത", "icon": "🔤", "color": "#E3F2FD", "iconColor": "#1565C0", "done": False,
                 "exercises": [
                     {"type": "script", "q": "What consonant is this?", "script": "ഗ", "answer": "ga", "options": ["ka", "ga", "cha", "ta"], "hint": "Soft G"},
                     {"type": "translate", "q": "How do you say \"One\" in Malayalam?", "answer": "ഒന്ന്", "options": ["ഒന്ന്", "രണ്ട്", "മൂന്ന്", "നാല്"], "hint": "Onnu"},
                 ]},
            ],
            "greetings": [
                {"id": "ml-g1", "title": "Greetings", "sub": "നമസ്കാരം", "icon": "👋", "color": "#F3E5F5", "iconColor": "#4A148C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you say \"Hello\" in Malayalam?", "answer": "നമസ്കാരം", "options": ["നമസ്കാരം", "നന്ദി", "ക്ഷമിക്കണം", "സുപ്രഭാതം"], "hint": ""},
                     {"type": "translate", "q": "What does \"നന്ദി\" mean?", "answer": "Thank you", "options": ["Hello", "Goodbye", "Thank you", "Sorry"], "hint": "Nandi"},
                 ]},
            ],
            "numbers": [
                {"id": "ml-n1", "title": "Numbers 1–5", "sub": "ഒന്ന് to അഞ്ച്", "icon": "🔢", "color": "#E0F2F1", "iconColor": "#00695C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "What is \"മൂന്ന്\" in English?", "answer": "Three", "options": ["Two", "Three", "Four", "Five"], "hint": "Moonn"},
                     {"type": "translate", "q": "Say \"Five\" in Malayalam", "answer": "അഞ്ച്", "options": ["മൂന്ന്", "നാല്", "അഞ്ച്", "ആറ്"], "hint": "Anchu"},
                 ]},
            ],
            "phrases": [
                {"id": "ml-p1", "title": "Daily Phrases", "sub": "Everyday Malayalam", "icon": "💬", "color": "#FBE9E7", "iconColor": "#BF360C", "done": False,
                 "exercises": [
                     {"type": "translate", "q": "How do you ask \"How are you?\" in Malayalam?", "answer": "സുഖമാണോ?", "options": ["പേര് എന്ത്?", "സുഖമാണോ?", "എവിടെ ആണ്?", "മനസ്സിലായോ?"], "hint": "Sukhamaano?"},
                 ]},
            ]
        }
    }
}


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, lang_data=LANG_DATA)


@app.route("/api/explain", methods=["POST"])
def explain():
    data = request.get_json()
    lang_name = data.get("lang", "")
    question = data.get("question", "")
    answer = data.get("answer", "")

    prompt = (
        f'You are a {lang_name} language tutor. In 2-3 short sentences, explain this language fact: '
        f'"{question}" — the answer is "{answer}". '
        f'Give an interesting memory tip or cultural context. Be friendly and encouraging. Keep it very brief.'
    )

    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = "".join(c.get("text", "") for c in result.get("content", []))
            return jsonify({"explanation": text})
    except Exception as e:
        return jsonify({"explanation": "AI explanation unavailable. Keep practicing!"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
