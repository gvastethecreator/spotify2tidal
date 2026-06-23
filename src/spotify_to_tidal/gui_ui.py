HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Spotify to Tidal</title>
  <link rel="icon" type="image/png" href="/app-icon.png">
  <script>
    document.documentElement.dataset.theme = localStorage.getItem("s2t-theme") || "dark";
  </script>
  <style>
    :root {
      color-scheme: dark;
      --bg: #050505;
      --surface: #111111;
      --soft: #1a1a1a;
      --line: rgba(255, 255, 255, .10);
      --ink: #ffffff;
      --muted: #999999;
      --faint: #777777;
      --teal: #0099ff;
      --teal-dark: #0077cc;
      --active-ink: #ffffff;
      --green: #1db954;
      --tidal: #080b0c;
      --amber: #ffffff;
      --amber-bg: #232323;
      --red: #ffffff;
      --red-bg: #232323;
      --shadow: 0 18px 45px rgba(0, 0, 0, .32);
      --sidebar-bg: #050505;
      --button-hover-line: rgba(255, 255, 255, .10);
      --nav-color: #ffffff;
      --active-bg: #1a1a1a;
      --active-line: rgba(255, 255, 255, .10);
      --chip-bg: #111111;
      --chip-color: #ffffff;
      --list-bg: #0a0a0a;
      --cover-bg: #232323;
      --badge-line: rgba(255, 255, 255, .10);
      --red-line: rgba(255, 255, 255, .10);
      --warning-text: #ffffff;
      --activity-bg: #111111;
      --focus-ring: rgba(0, 153, 255, .20);
      --primary-shadow: 0 10px 30px rgba(0, 0, 0, .35);
      --primary-bg: #ffffff;
      --primary-ink: #050505;
      --spotlight: radial-gradient(circle at 20% 10%, #ff3da6 0, transparent 35%), radial-gradient(circle at 80% 25%, #6c2cff 0, transparent 42%), linear-gradient(135deg, #2b105f, #6f1dff 45%, #ff7a35);
      --motion-dur: 180ms;
      --motion-ease: cubic-bezier(.22, 1, .36, 1);
      --icon-swap-dur: 200ms;
      --icon-swap-blur: 2px;
      --icon-swap-start-scale: 0.25;
      --icon-swap-ease: ease-in-out;
    }
    :root[data-theme="light"] {
      color-scheme: light;
      --bg: #f7f9f8;
      --surface: #ffffff;
      --soft: #f2f7f5;
      --line: rgba(5, 5, 5, .10);
      --ink: #172121;
      --muted: #667575;
      --faint: #879393;
      --teal: #0b8f86;
      --teal-dark: #07736e;
      --active-ink: #07736e;
      --amber: #7d4a08;
      --amber-bg: #fff5e8;
      --red: #b5473f;
      --red-bg: #fff0ef;
      --shadow: 0 18px 45px rgba(28, 44, 42, .08);
      --sidebar-bg: linear-gradient(180deg, #fbfdfc, #f1f6f4);
      --button-hover-line: rgba(5, 5, 5, .10);
      --nav-color: #334140;
      --active-bg: #e7f4f1;
      --active-line: rgba(5, 5, 5, .10);
      --chip-bg: #f8fbfa;
      --chip-color: #455352;
      --list-bg: #fcfefd;
      --cover-bg: #dce4e1;
      --badge-line: rgba(5, 5, 5, .10);
      --red-line: rgba(5, 5, 5, .10);
      --warning-text: #70450d;
      --activity-bg: #fbfefd;
      --focus-ring: rgba(11, 143, 134, .12);
      --primary-shadow: 0 10px 24px rgba(8, 143, 134, .2);
      --primary-bg: #050505;
      --primary-ink: #ffffff;
      --spotlight: linear-gradient(135deg, #f9e9ff, #e7f0ff 48%, #fff2e6);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      overflow-x: hidden;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.45 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-feature-settings: "cv01", "cv05", "cv09", "cv11", "ss03", "ss07", "dlig", "tnum";
      letter-spacing: 0;
      transition: background-color var(--motion-dur) var(--motion-ease), color var(--motion-dur) var(--motion-ease);
    }
    button, input, select, textarea { font: inherit; letter-spacing: 0; }
    button {
      min-height: 38px;
      border: 2px solid var(--line);
      border-radius: 100px;
      background: var(--surface);
      color: var(--ink);
      padding: 9px 13px;
      font-weight: 720;
      cursor: pointer;
      transition:
        transform var(--motion-dur) var(--motion-ease),
        border-color var(--motion-dur) var(--motion-ease),
        background-color var(--motion-dur) var(--motion-ease),
        box-shadow var(--motion-dur) var(--motion-ease),
        color var(--motion-dur) var(--motion-ease);
    }
    button:hover { border-color: var(--button-hover-line); transform: translateY(-1px); }
    button:active { transform: translateY(0); }
    button:disabled { opacity: .5; cursor: not-allowed; }
    button.primary {
      background: var(--primary-bg);
      border-color: var(--line);
      color: var(--primary-ink);
      box-shadow: var(--primary-shadow);
    }
    button.primary:hover { box-shadow: var(--primary-shadow); }
    button.ghost { background: transparent; }
    input, select, textarea {
      width: 100%;
      border: 2px solid var(--line);
      border-radius: 10px;
      background: var(--surface);
      color: var(--ink);
      padding: 10px 12px;
      outline: none;
      transition:
        border-color var(--motion-dur) var(--motion-ease),
        box-shadow var(--motion-dur) var(--motion-ease),
        background-color var(--motion-dur) var(--motion-ease),
        color var(--motion-dur) var(--motion-ease);
    }
    input:focus, select:focus, textarea:focus {
      border-color: var(--line);
      box-shadow: 0 0 0 3px var(--focus-ring);
    }
    textarea { min-height: 74px; resize: vertical; }
    label { color: var(--muted); display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; }
    .app {
      display: grid;
      grid-template-columns: 230px minmax(0, 1fr);
      min-height: 100vh;
    }
    .sidebar {
      border-right: 2px solid var(--line);
      background: var(--sidebar-bg);
      padding: 22px 16px;
      display: flex;
      flex-direction: column;
      gap: 22px;
      transition: background var(--motion-dur) var(--motion-ease), border-color var(--motion-dur) var(--motion-ease);
    }
    .brand { display: flex; align-items: center; gap: 12px; }
    .mark {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      border: 2px solid var(--line);
      display: block;
      object-fit: cover;
      box-shadow: var(--shadow);
    }
    .brand h1 { font-size: 18px; margin: 0; line-height: 1.15; }
    .brand small { color: var(--muted); display: block; margin-top: 2px; }
    .nav { display: grid; gap: 6px; }
    .nav button {
      text-align: left;
      background: transparent;
      border-color: transparent;
      color: var(--nav-color);
      display: flex;
      align-items: center;
      gap: 9px;
    }
    .nav button.active {
      background: var(--active-bg);
      border-color: var(--active-line);
      color: var(--active-ink);
    }
    .sidebar-foot { margin-top: auto; color: var(--muted); font-size: 12px; display: grid; gap: 8px; }
    .content {
      min-width: 0;
      padding: 20px 24px;
    }
    .topbar {
      display: flex;
      justify-content: space-between;
      gap: 20px;
      align-items: flex-start;
      margin-bottom: 14px;
    }
    .ready {
      display: flex;
      align-items: center;
      gap: 14px;
      min-width: 0;
    }
    .ready-badge {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: linear-gradient(180deg, #16a085, #08736d);
      color: white;
      font-size: 26px;
      font-weight: 900;
    }
    .ready h2 { font-size: 27px; margin: 0; line-height: 1.15; }
    .ready p { margin: 4px 0 0; color: var(--muted); }
    .top-actions { display: flex; gap: 10px; flex-wrap: wrap; justify-content: flex-end; }
    .stepper {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 14px;
    }
    .step {
      border-bottom: 2px solid var(--line);
      padding: 8px 0 12px;
      color: var(--muted);
      font-weight: 760;
    }
    .step span {
      display: inline-grid;
      place-items: center;
      width: 25px;
      height: 25px;
      border-radius: 50%;
      border: 2px solid var(--line);
      margin-right: 8px;
      background: var(--surface);
      color: var(--muted);
    }
    .step.done span, .step.active span { background: var(--teal); border-color: var(--line); color: white; }
    .step.active { border-color: var(--line); color: var(--active-ink); box-shadow: inset 0 -2px 0 var(--teal); }
    .summary {
      background: var(--surface);
      border: 2px solid var(--line);
      border-radius: 20px;
      box-shadow: var(--shadow);
      display: grid;
      grid-template-columns: 1.35fr 1.35fr repeat(4, .9fr);
      margin-bottom: 18px;
      overflow: hidden;
      animation: rise-in 360ms var(--motion-ease) both;
      transition: background-color var(--motion-dur) var(--motion-ease), border-color var(--motion-dur) var(--motion-ease), box-shadow var(--motion-dur) var(--motion-ease);
    }
    .metric {
      padding: 15px 18px;
      border-right: 2px solid var(--line);
      min-width: 0;
    }
    .metric:last-child { border-right: 0; }
    .account-metric { display: flex; align-items: center; gap: 12px; }
    .service-logo {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: white;
      font-weight: 900;
    }
    .spotify-logo { background: var(--green); }
    .tidal-logo { background: var(--tidal); }
    .metric strong { display: block; font-size: 18px; line-height: 1.1; }
    .metric small { color: var(--muted); display: block; margin-top: 4px; }
    .status-dot {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--green);
      margin-left: 4px;
    }
    .icon {
      width: 18px;
      height: 18px;
      flex: 0 0 auto;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    .t-icon-swap {
      position: relative;
      display: inline-grid;
      margin-right: 7px;
    }
    .t-icon-swap .icon { margin: 0; }
    .t-icon-swap .t-icon {
      grid-area: 1 / 1;
      transition:
        opacity   var(--icon-swap-dur) var(--icon-swap-ease),
        filter    var(--icon-swap-dur) var(--icon-swap-ease),
        transform var(--icon-swap-dur) var(--icon-swap-ease);
      will-change: opacity, filter, transform;
    }
    .t-icon-swap[data-state="a"] .t-icon[data-icon="a"],
    .t-icon-swap[data-state="b"] .t-icon[data-icon="b"] {
      opacity: 1;
      filter: blur(0);
      transform: scale(1);
    }
    .t-icon-swap[data-state="a"] .t-icon[data-icon="b"],
    .t-icon-swap[data-state="b"] .t-icon[data-icon="a"] {
      opacity: 0;
      filter: blur(var(--icon-swap-blur));
      transform: scale(var(--icon-swap-start-scale));
    }
    button .icon { margin-right: 7px; }
    button .icon.trailing {
      margin-right: 0;
      margin-left: 7px;
    }
    .nav .icon { color: var(--faint); }
    .nav button.active .icon { color: var(--active-ink); }
    .service-logo .icon {
      width: 25px;
      height: 25px;
      stroke-width: 1.8;
    }
    .panel h3 {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .panel h3 .icon { color: var(--active-ink); }
    .plan-row strong,
    .policy-row summary {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .plan-row strong .icon,
    .policy-row summary .icon { color: var(--active-ink); }
    .locknote {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }
    .locknote .icon { width: 16px; height: 16px; color: var(--faint); }
    .board {
      background: var(--surface);
      border: 2px solid var(--line);
      border-radius: 20px;
      box-shadow: var(--shadow);
      overflow: hidden;
      animation: rise-in 420ms var(--motion-ease) both;
      transition: background-color var(--motion-dur) var(--motion-ease), border-color var(--motion-dur) var(--motion-ease), box-shadow var(--motion-dur) var(--motion-ease);
    }
    .columns {
      display: grid;
      grid-template-columns: minmax(330px, 1fr) minmax(340px, .96fr) minmax(330px, .92fr);
      min-height: 500px;
    }
    .panel {
      min-width: 0;
      padding: 19px 22px;
      border-right: 2px solid var(--line);
    }
    .panel:last-child { border-right: 0; }
    .panel h3 { font-size: 19px; margin: 0; }
    .panel .sub { color: var(--muted); margin: 5px 0 16px; }
    .tools { display: grid; grid-template-columns: 1fr auto; gap: 10px; margin-bottom: 12px; }
    .filters { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
    .chip {
      border: 2px solid var(--line);
      background: var(--chip-bg);
      border-radius: 100px;
      padding: 7px 10px;
      color: var(--chip-color);
      font-weight: 740;
      cursor: pointer;
      transition:
        transform var(--motion-dur) var(--motion-ease),
        background-color var(--motion-dur) var(--motion-ease),
        border-color var(--motion-dur) var(--motion-ease),
        color var(--motion-dur) var(--motion-ease);
    }
    .chip:hover { transform: translateY(-1px); }
    .chip.active { color: var(--active-ink); border-color: var(--active-line); background: var(--active-bg); }
    .playlist-list, .duplicate-list, .plan-list {
      border: 2px solid var(--line);
      border-radius: 15px;
      overflow: auto;
      max-height: 305px;
      background: var(--list-bg);
    }
    .playlist-row {
      display: grid;
      grid-template-columns: 26px 46px minmax(0, 1fr) auto;
      gap: 10px;
      align-items: center;
      padding: 10px 12px;
      border-bottom: 2px solid var(--line);
      transition: background-color var(--motion-dur) var(--motion-ease), transform var(--motion-dur) var(--motion-ease);
    }
    .playlist-row:hover { background: var(--soft); transform: translateX(2px); }
    .playlist-row:last-child { border-bottom: 0; }
    .playlist-row input { width: 17px; height: 17px; accent-color: var(--teal); }
    .cover {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      object-fit: cover;
      background: var(--cover-bg);
    }
    .playlist-title { font-weight: 780; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .meta { color: var(--muted); font-size: 12px; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .badge {
      border: 2px solid var(--badge-line);
      background: var(--amber-bg);
      color: var(--amber);
      border-radius: 100px;
      padding: 4px 7px;
      font-size: 11px;
      font-weight: 800;
    }
    .badge.red { border-color: var(--red-line); background: var(--red-bg); color: var(--red); }
    .selected-count { color: var(--active-ink); font-weight: 820; margin-top: 14px; }
    .dupe-card {
      padding: 12px;
      border-bottom: 2px solid var(--line);
    }
    .dupe-card:last-child { border-bottom: 0; }
    .dupe-head { display: flex; justify-content: space-between; gap: 10px; font-weight: 800; margin-bottom: 8px; }
    .dupe-choice {
      display: grid;
      grid-template-columns: 22px 40px minmax(0, 1fr) auto;
      gap: 9px;
      align-items: center;
      padding: 8px 0;
    }
    .dupe-choice span { min-width: 0; }
    .dupe-choice strong { display: block; }
    .dupe-choice .meta { display: block; }
    .dupe-choice input { width: 16px; height: 16px; accent-color: var(--teal); }
    .policy-row, .plan-row {
      padding: 14px 16px;
      border-bottom: 2px solid var(--line);
    }
    .plan-row:last-child, .policy-row:last-child { border-bottom: 0; }
    .policy-row summary { cursor: pointer; font-weight: 800; }
    .plan-row strong { display: block; }
    .plan-row small { color: var(--muted); }
    .switch-line { display: flex; align-items: center; justify-content: space-between; gap: 14px; }
    .switch-line input { width: 18px; height: 18px; accent-color: var(--teal); }
    .warning {
      margin-top: 12px;
      padding: 12px;
      border-radius: 30px;
      border: 2px solid var(--badge-line);
      background: var(--spotlight);
      color: var(--warning-text);
      box-shadow: inset 0 1px 0 rgba(255,255,255,.12);
    }
    .sync-button { width: 100%; margin-top: 14px; min-height: 50px; font-size: 16px; }
    .locknote { margin: 10px 0 0; color: var(--muted); font-size: 12px; text-align: center; }
    .activity {
      border-top: 2px solid var(--line);
      padding: 15px 22px;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 14px;
      align-items: start;
    }
    .activity h3 { margin: 0 0 10px; }
    .activity-items { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
    .activity-card {
      border: 2px solid var(--line);
      border-radius: 15px;
      padding: 12px;
      background: var(--activity-bg);
      min-width: 0;
      display: grid;
      grid-template-columns: 30px minmax(0, 1fr);
      gap: 10px;
      align-items: start;
      transition:
        transform var(--motion-dur) var(--motion-ease),
        background-color var(--motion-dur) var(--motion-ease),
        border-color var(--motion-dur) var(--motion-ease);
    }
    .activity-card:hover { transform: translateY(-2px); }
    .activity-icon {
      width: 30px;
      height: 30px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: var(--active-ink);
      background: var(--active-bg);
    }
    .activity-icon .icon { width: 17px; height: 17px; }
    .activity-card strong { display: block; }
    .activity-card small { color: var(--muted); }
    .settings-drawer {
      margin-top: 18px;
      border: 2px solid var(--line);
      border-radius: 20px;
      background: var(--activity-bg);
      padding: 12px;
      transition: background-color var(--motion-dur) var(--motion-ease), border-color var(--motion-dur) var(--motion-ease);
    }
    .settings-drawer summary { cursor: pointer; font-weight: 800; }
    .settings-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 12px;
    }
    .checkline { display: flex; align-items: center; gap: 8px; color: var(--ink); font-weight: 700; margin-top: 22px; }
    .checkline input { width: 18px; height: 18px; accent-color: var(--teal); }
    .message { color: var(--muted); min-height: 20px; }
    .message.error { color: var(--red); }
    @keyframes rise-in {
      from { opacity: 0; transform: translateY(8px); filter: blur(2px); }
      to { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
      .t-icon-swap .t-icon { transition: none !important; }
    }
    @media (pointer: coarse) {
      button, input, select, .chip { min-height: 44px; }
    }
    @media (max-width: 1120px) {
      .app { grid-template-columns: 1fr; }
      .sidebar {
        position: static;
        flex-direction: row;
        align-items: center;
        flex-wrap: wrap;
        overflow: visible;
        padding: 16px;
        gap: 12px;
      }
      .sidebar-foot { display: none; }
      .brand { flex: 0 0 auto; }
      .nav {
        display: flex;
        flex: 1 1 420px;
        flex-wrap: wrap;
        min-width: 0;
        gap: 6px;
      }
      .nav button { white-space: nowrap; }
      .content { padding: 18px; }
      .summary { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .columns { grid-template-columns: 1fr; }
      .panel { border-right: 0; border-bottom: 2px solid var(--line); }
      .activity-items { grid-template-columns: 1fr 1fr; }
      .settings-grid { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 640px) {
      .sidebar {
        display: grid;
        grid-template-columns: 1fr;
        align-items: stretch;
      }
      .brand h1 { font-size: 17px; }
      .nav {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        width: 100%;
      }
      .nav button {
        justify-content: center;
        min-width: 0;
        padding: 8px 6px;
        text-align: center;
        white-space: normal;
      }
      .content { padding: 14px; }
      .topbar { flex-direction: column; gap: 14px; }
      .ready { align-items: flex-start; }
      .ready-badge {
        flex: 0 0 auto;
        width: 44px;
        height: 44px;
      }
      .ready h2 { font-size: 25px; }
      .top-actions {
        display: grid;
        grid-template-columns: 1fr 1fr;
        width: 100%;
      }
      .top-actions button {
        min-width: 0;
        padding-left: 8px;
        padding-right: 8px;
      }
      .stepper { grid-template-columns: 1fr 1fr; }
      .step { font-size: 13px; padding-bottom: 10px; }
      .summary { grid-template-columns: 1fr; }
      .metric { border-right: 0; border-bottom: 2px solid var(--line); }
      .metric:last-child { border-bottom: 0; }
      .columns { min-height: 0; }
      .panel { padding: 16px; }
      .panel h3 { font-size: 18px; }
      .playlist-list, .duplicate-list, .plan-list { max-height: 340px; }
      .playlist-row { grid-template-columns: 24px 38px minmax(0, 1fr); }
      .playlist-row .badge { grid-column: 3; width: fit-content; }
      .dupe-choice { grid-template-columns: 22px 38px minmax(0, 1fr); }
      .dupe-choice .badge { grid-column: 3; width: fit-content; max-width: 100%; }
      .activity {
        grid-template-columns: 1fr;
        padding-left: 16px;
        padding-right: 16px;
      }
      .activity > button { justify-self: start; }
      .activity-items, .settings-grid { grid-template-columns: 1fr; }
      .tools { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <svg width="0" height="0" style="position:absolute;display:none" aria-hidden="true" focusable="false">
    <symbol id="i-layout-dashboard" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M5 4h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-6a1 1 0 0 1 1 -1" /><path d="M5 16h4a1 1 0 0 1 1 1v2a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-2a1 1 0 0 1 1 -1" /><path d="M15 12h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-6a1 1 0 0 1 1 -1" /><path d="M15 4h4a1 1 0 0 1 1 1v2a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-2a1 1 0 0 1 1 -1" /></symbol>
    <symbol id="i-playlist" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M11 17a3 3 0 1 0 6 0a3 3 0 1 0 -6 0" /><path d="M17 17v-13h4" /><path d="M13 5h-10" /><path d="M3 9l10 0" /><path d="M9 13h-6" /></symbol>
    <symbol id="i-copy-check" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M7 9.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667l0 -8.666" /><path d="M4.012 16.737a2 2 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1" /><path d="M11 14l2 2l4 -4" /></symbol>
    <symbol id="i-heart" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M19.5 12.572l-7.5 7.428l-7.5 -7.428a5 5 0 1 1 7.5 -6.566a5 5 0 1 1 7.5 6.572" /></symbol>
    <symbol id="i-history" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M12 8l0 4l2 2" /><path d="M3.05 11a9 9 0 1 1 .5 4m-.5 5v-5h5" /></symbol>
    <symbol id="i-settings" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065" /><path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" /></symbol>
    <symbol id="i-logs" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M4 12h.01" /><path d="M4 6h.01" /><path d="M4 18h.01" /><path d="M8 18h2" /><path d="M8 12h2" /><path d="M8 6h2" /><path d="M14 6h6" /><path d="M14 12h6" /><path d="M14 18h6" /></symbol>
    <symbol id="i-sun" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M8 12a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" /><path d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7" /></symbol>
    <symbol id="i-moon" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454l0 .008" /></symbol>
    <symbol id="i-cloud-up" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M12 18.004h-5.343c-2.572 -.004 -4.657 -2.011 -4.657 -4.487c0 -2.475 2.085 -4.482 4.657 -4.482c.393 -1.762 1.794 -3.2 3.675 -3.773c1.88 -.572 3.956 -.193 5.444 1c1.488 1.19 2.162 3.007 1.77 4.769h.99c1.38 0 2.57 .811 3.128 1.986" /><path d="M19 22v-6" /><path d="M22 19l-3 -3l-3 3" /></symbol>
    <symbol id="i-refresh" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4" /><path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4" /></symbol>
    <symbol id="i-brand-spotify" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" /><path d="M8 11.973c2.5 -1.473 5.5 -.973 7.5 .527" /><path d="M9 15c1.5 -1 4 -1 5 .5" /><path d="M7 9c2 -1 6 -2 10 .5" /></symbol>
    <symbol id="i-brand-tidal" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M5.333 6l3.334 3.25l3.333 -3.25l3.333 3.25l3.334 -3.25l3.333 3.25l-3.333 3.25l-3.334 -3.25l-3.333 3.25l3.333 3.25l-3.333 3.25l-3.333 -3.25l3.333 -3.25l-3.333 -3.25l-3.334 3.25l-3.333 -3.25l3.333 -3.25" /></symbol>
    <symbol id="i-list-check" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M3.5 5.5l1.5 1.5l2.5 -2.5" /><path d="M3.5 11.5l1.5 1.5l2.5 -2.5" /><path d="M3.5 17.5l1.5 1.5l2.5 -2.5" /><path d="M11 6l9 0" /><path d="M11 12l9 0" /><path d="M11 18l9 0" /></symbol>
    <symbol id="i-shield-check" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M11.46 20.846a12 12 0 0 1 -7.96 -14.846a12 12 0 0 0 8.5 -3a12 12 0 0 0 8.5 3a12 12 0 0 1 -.09 7.06" /><path d="M15 19l2 2l4 -4" /></symbol>
    <symbol id="i-player-play" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M7 4v16l13 -8l-13 -8" /></symbol>
    <symbol id="i-arrow-right" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M5 12l14 0" /><path d="M13 18l6 -6" /><path d="M13 6l6 6" /></symbol>
    <symbol id="i-plug-connected" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M7 12l5 5l-1.5 1.5a3.536 3.536 0 1 1 -5 -5l1.5 -1.5" /><path d="M17 12l-5 -5l1.5 -1.5a3.536 3.536 0 1 1 5 5l-1.5 1.5" /><path d="M3 21l2.5 -2.5" /><path d="M18.5 5.5l2.5 -2.5" /><path d="M10 11l-2 2" /><path d="M13 14l-2 2" /></symbol>
    <symbol id="i-search" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M3 10a7 7 0 1 0 14 0a7 7 0 1 0 -14 0" /><path d="M21 21l-6 -6" /></symbol>
    <symbol id="i-filter" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M4 4h16v2.172a2 2 0 0 1 -.586 1.414l-4.414 4.414v7l-6 2v-8.5l-4.48 -4.928a2 2 0 0 1 -.52 -1.345v-2.227" /></symbol>
    <symbol id="i-plus" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M12 5l0 14" /><path d="M5 12l14 0" /></symbol>
    <symbol id="i-wand" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M6 21l15 -15l-3 -3l-15 15l3 3" /><path d="M15 6l3 3" /><path d="M9 3a2 2 0 0 0 2 2a2 2 0 0 0 -2 2a2 2 0 0 0 -2 -2a2 2 0 0 0 2 -2" /><path d="M19 13a2 2 0 0 0 2 2a2 2 0 0 0 -2 2a2 2 0 0 0 -2 -2a2 2 0 0 0 2 -2" /></symbol>
    <symbol id="i-music" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M3 17a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" /><path d="M13 17a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" /><path d="M9 17v-13h10v13" /><path d="M9 8h10" /></symbol>
    <symbol id="i-alert-triangle" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M12 9v4" /><path d="M10.363 3.591l-8.106 13.534a1.914 1.914 0 0 0 1.636 2.871h16.214a1.914 1.914 0 0 0 1.636 -2.87l-8.106 -13.536a1.914 1.914 0 0 0 -3.274 0" /><path d="M12 16h.01" /></symbol>
    <symbol id="i-info-circle" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" /><path d="M12 9h.01" /><path d="M11 12h1v4h1" /></symbol>
    <symbol id="i-circle-check" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" /><path d="M9 12l2 2l4 -4" /></symbol>
    <symbol id="i-device-speaker" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M5 5a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2l0 -14" /><path d="M9 14a3 3 0 1 0 6 0a3 3 0 1 0 -6 0" /><path d="M12 7l0 .01" /></symbol>
    <symbol id="i-database" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M4 6a8 3 0 1 0 16 0a8 3 0 1 0 -16 0" /><path d="M4 6v6a8 3 0 0 0 16 0v-6" /><path d="M4 12v6a8 3 0 0 0 16 0v-6" /></symbol>
    <symbol id="i-lock" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M5 13a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-6" /><path d="M11 16a1 1 0 1 0 2 0a1 1 0 0 0 -2 0" /><path d="M8 11v-4a4 4 0 1 1 8 0v4" /></symbol>
    <symbol id="i-activity" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M3 12h4l3 8l4 -16l3 8h4" /></symbol>
    <symbol id="i-checks" viewBox="0 0 24 24"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M7 12l5 5l10 -10" /><path d="M2 12l5 5m5 -5l5 -5" /></symbol>
  </svg>
  <div class="app">
    <aside class="sidebar">
      <div class="brand">
        <img class="mark" src="/app-icon.png" alt="" aria-hidden="true">
        <div><h1>Spotify to Tidal</h1><small>Local sync app</small></div>
      </div>
      <nav class="nav" aria-label="Main navigation">
        <button class="active" type="button"><svg class="icon" aria-hidden="true"><use href="#i-cloud-up"></use></svg>Migrate</button>
        <button type="button"><svg class="icon" aria-hidden="true"><use href="#i-copy-check"></use></svg>Review</button>
        <button type="button"><svg class="icon" aria-hidden="true"><use href="#i-history"></use></svg>History</button>
        <button type="button"><svg class="icon" aria-hidden="true"><use href="#i-settings"></use></svg>Settings</button>
        <button type="button"><svg class="icon" aria-hidden="true"><use href="#i-logs"></use></svg>Logs</button>
      </nav>
      <div class="sidebar-foot">
        <button id="demoBtn" type="button"><svg class="icon" aria-hidden="true"><use href="#i-database"></use></svg>Load public demo</button>
        <span id="configPath">config.yml</span>
      </div>
    </aside>

    <main class="content">
      <div class="topbar">
        <div class="ready">
          <div class="ready-badge" aria-hidden="true">&#10003;</div>
          <div>
            <h2 id="readyTitle">Ready to sync</h2>
            <p id="readySubtitle">Connect accounts, choose playlists, review duplicates, then sync with confidence.</p>
          </div>
        </div>
        <div class="top-actions">
          <button id="spotifyBtn" type="button"><svg class="icon" aria-hidden="true"><use href="#i-brand-spotify"></use></svg>Connect Spotify</button>
          <button id="tidalBtn" type="button"><svg class="icon" aria-hidden="true"><use href="#i-brand-tidal"></use></svg>Connect Tidal</button>
          <button id="logsBtn" type="button"><svg class="icon" aria-hidden="true"><use href="#i-logs"></use></svg>View logs</button>
          <button id="themeBtn" type="button" aria-pressed="true">
            <span class="t-icon-swap" data-state="a" aria-hidden="true">
              <span class="t-icon" data-icon="a"><svg class="icon"><use href="#i-moon"></use></svg></span>
              <span class="t-icon" data-icon="b"><svg class="icon"><use href="#i-sun"></use></svg></span>
            </span>
            <span id="themeLabel">Dark</span>
          </button>
        </div>
      </div>

      <div class="stepper" aria-label="Migration steps">
        <div class="step done"><span>1</span>Connect accounts</div>
        <div class="step active"><span>2</span>Choose playlists</div>
        <div class="step"><span>3</span>Review</div>
        <div class="step"><span>4</span>Sync</div>
      </div>

      <section class="summary" aria-label="Sync readiness summary">
        <div class="metric account-metric">
          <div class="service-logo spotify-logo"><svg class="icon" aria-hidden="true"><use href="#i-brand-spotify"></use></svg></div>
          <div><strong>Spotify</strong><small id="spotifyStatus">Demo ready <span class="status-dot"></span></small></div>
        </div>
        <div class="metric account-metric">
          <div class="service-logo tidal-logo"><svg class="icon" aria-hidden="true"><use href="#i-brand-tidal"></use></svg></div>
          <div><strong>Tidal</strong><small id="tidalStatus">Demo ready <span class="status-dot"></span></small></div>
        </div>
        <div class="metric"><strong id="foundMetric">0</strong><small>Playlists found</small></div>
        <div class="metric"><strong id="selectedMetric">0</strong><small>Playlists selected</small></div>
        <div class="metric"><strong id="duplicateMetric">0</strong><small id="duplicateMetricLabel">Duplicate names</small></div>
        <div class="metric"><strong id="tracksMetric">0</strong><small>Tracks to add</small></div>
      </section>

      <section class="board">
        <div class="columns">
          <section class="panel" aria-label="Choose playlists">
            <h3><svg class="icon" aria-hidden="true"><use href="#i-playlist"></use></svg>Choose playlists</h3>
            <p class="sub">Select the Spotify playlists you want to import.</p>
            <div class="tools">
              <input id="playlistSearch" placeholder="Search playlists">
              <button id="refreshBtn" type="button"><svg class="icon" aria-hidden="true"><use href="#i-refresh"></use></svg>Refresh</button>
            </div>
            <div class="filters">
              <button class="chip active" data-filter="all" type="button">All</button>
              <button class="chip" data-filter="owned" type="button">Owned</button>
              <button class="chip" data-filter="followed" type="button">Followed</button>
              <button class="chip" data-filter="duplicates" type="button">Duplicates</button>
              <button class="chip" data-filter="selected" type="button">Selected</button>
              <button class="chip" data-filter="empty" type="button">Empty</button>
            </div>
            <div class="playlist-list" id="playlistList"></div>
            <div class="selected-count" id="playlistSummary">0 playlists selected</div>
          </section>

          <section class="panel" aria-label="Review duplicates">
            <h3><svg class="icon" aria-hidden="true"><use href="#i-copy-check"></use></svg>Review duplicates <span class="badge" id="duplicateBadge">0 duplicate names</span></h3>
            <p class="sub">Resolve same-name playlists before writing to Tidal.</p>
            <div class="duplicate-list" id="duplicateList"></div>
            <div class="warning" id="reviewHint">No duplicate playlist names in the current selection.</div>
          </section>

          <section class="panel" aria-label="Sync plan">
            <h3><svg class="icon" aria-hidden="true"><use href="#i-list-check"></use></svg>Sync plan</h3>
            <p class="sub">Here is what will happen in Tidal.</p>
            <div class="plan-list">
              <div class="plan-row">
                <strong><svg class="icon" aria-hidden="true"><use href="#i-plus"></use></svg>Create missing playlists</strong>
                <small id="createPlan">Selected playlists will be created if missing.</small>
              </div>
              <label class="plan-row switch-line">
                <span><strong><svg class="icon" aria-hidden="true"><use href="#i-heart"></use></svg>Include favorites</strong><small>Add Spotify liked songs to Tidal favorites.</small></span>
                <input id="includeFavorites" type="checkbox" checked>
              </label>
              <label class="plan-row switch-line">
                <span><strong><svg class="icon" aria-hidden="true"><use href="#i-shield-check"></use></svg>Skip duplicate names</strong><small>Keep the first match when names collide.</small></span>
                <input id="skipDuplicates" type="checkbox">
              </label>
              <div class="policy-row">
                <label for="destinationBehavior">Destination behavior</label>
                <select id="destinationBehavior">
                  <option>Keep existing playlists and add new tracks</option>
                  <option>Create missing playlists only</option>
                </select>
              </div>
            </div>
            <button id="runBtn" class="primary sync-button" type="button">Sync selected <svg class="icon trailing" aria-hidden="true"><use href="#i-arrow-right"></use></svg></button>
            <p class="locknote"><svg class="icon" aria-hidden="true"><use href="#i-lock"></use></svg>Nothing will be deleted. You are in control.</p>
            <p id="message" class="message" role="status" aria-live="polite"></p>
          </section>
        </div>

        <section class="activity" aria-label="Activity" aria-live="polite">
          <div>
            <h3><svg class="icon" aria-hidden="true"><use href="#i-activity"></use></svg>Activity</h3>
            <div class="activity-items" id="activityItems"></div>
          </div>
          <button id="clearActivityBtn" type="button"><svg class="icon" aria-hidden="true"><use href="#i-checks"></use></svg>Clear</button>
        </section>
      </section>

      <details class="settings-drawer">
        <summary><svg class="icon" aria-hidden="true"><use href="#i-settings"></use></svg>Connection settings and advanced options</summary>
        <div class="settings-grid">
          <div><label for="clientId">Spotify Client ID</label><input id="clientId" autocomplete="off"></div>
          <div><label for="clientSecret">Spotify Client secret</label><input id="clientSecret" type="password" autocomplete="off"></div>
          <div><label for="username">Spotify username</label><input id="username" autocomplete="username"></div>
          <div><label for="redirectUri">Redirect URI</label><input id="redirectUri"></div>
          <label class="checkline"><input id="openBrowser" type="checkbox" checked> Open browser for auth</label>
          <div><label for="maxConcurrency">Max concurrency</label><input id="maxConcurrency" type="number" min="1" step="1"></div>
          <div><label for="rateLimit">Rate limit</label><input id="rateLimit" type="number" min="1" step="1"></div>
          <div><label for="playlistUri">Single playlist URI or ID</label><input id="playlistUri" placeholder="37i9dQZF1DXcBWIGoYBM5M"></div>
        </div>
        <div class="settings-grid">
          <div><label for="excludedPlaylists">Excluded playlists</label><textarea id="excludedPlaylists" placeholder="spotify:playlist:..."></textarea></div>
          <div><label for="syncPlaylists">Configured mappings</label><textarea id="syncPlaylists" placeholder="spotify_id -> tidal_id"></textarea></div>
        </div>
        <div class="top-actions" style="justify-content:flex-start;margin-top:12px">
          <button id="saveBtn" type="button"><svg class="icon" aria-hidden="true"><use href="#i-database"></use></svg>Save config</button>
          <button id="stopBtn" class="ghost" disabled type="button"><svg class="icon" aria-hidden="true"><use href="#i-alert-triangle"></use></svg>Stop running sync</button>
        </div>
      </details>
    </main>
  </div>

  <script>
    const $ = (id) => document.getElementById(id);
    const icon = (name) => `<svg class="icon" aria-hidden="true"><use href="#i-${name}"></use></svg>`;
    function setTheme(theme) {
      document.documentElement.dataset.theme = theme;
      localStorage.setItem("s2t-theme", theme);
      const dark = theme === "dark";
      $("themeBtn").setAttribute("aria-pressed", String(dark));
      $("themeLabel").textContent = dark ? "Dark" : "Light";
      $("themeBtn").querySelector(".t-icon-swap").dataset.state = dark ? "a" : "b";
    }
    let spotifyPlaylists = [];
    let selectedPlaylistIds = new Set();
    let spotifyUser = "";
    let activeFilter = "all";
    let poller = null;
    let demoMode = false;
    const activity = [
      ["Ready", "Load demo playlists or connect Spotify"],
      ["Review", "Duplicate names will appear here"],
      ["Plan", "Confirm your sync behavior before running"]
    ];

    function keyName(name) {
      return (name || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
    }

    function selectedPlaylists() {
      return spotifyPlaylists.filter(p => selectedPlaylistIds.has(p.id));
    }

    function plural(count, one, many = `${one}s`) {
      return `${count} ${count === 1 ? one : many}`;
    }

    function duplicateGroups() {
      const groups = new Map();
      for (const playlist of spotifyPlaylists) {
        const key = keyName(playlist.name);
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key).push(playlist);
      }
      return [...groups.values()].filter(group => group.length > 1 && group.some(p => selectedPlaylistIds.has(p.id)));
    }

    function activityIconName(title) {
      const lower = (title || "").toLowerCase();
      if (lower.includes("spotify")) return "brand-spotify";
      if (lower.includes("tidal")) return "brand-tidal";
      if (lower.includes("duplicate") || lower.includes("review")) return "copy-check";
      if (lower.includes("plan") || lower.includes("sync")) return "list-check";
      if (lower.includes("save") || lower.includes("loaded")) return "database";
      if (lower.includes("stop") || lower.includes("fail")) return "alert-triangle";
      return "activity";
    }

    function payload() {
      return {
        spotify: {
          client_id: $("clientId").value,
          client_secret: $("clientSecret").value,
          username: $("username").value,
          redirect_uri: $("redirectUri").value,
          open_browser: $("openBrowser").checked
        },
        sync_favorites_default: $("includeFavorites").checked,
        skip_duplicate_playlist_names: $("skipDuplicates").checked,
        max_concurrency: $("maxConcurrency").value,
        rate_limit: $("rateLimit").value,
        included_playlists: [...selectedPlaylistIds].join("\n"),
        excluded_playlists: $("excludedPlaylists").value,
        sync_playlists: $("syncPlaylists").value
      };
    }

    function fill(data) {
      $("configPath").textContent = data.path;
      $("clientId").value = data.spotify.client_id || "";
      $("clientSecret").value = data.spotify.client_secret || "";
      $("username").value = data.spotify.username || "";
      $("redirectUri").value = data.spotify.redirect_uri || "";
      $("openBrowser").checked = data.spotify.open_browser !== false;
      $("includeFavorites").checked = data.sync_favorites_default !== false;
      $("skipDuplicates").checked = data.skip_duplicate_playlist_names === true;
      $("maxConcurrency").value = data.max_concurrency || 10;
      $("rateLimit").value = data.rate_limit || 10;
      $("excludedPlaylists").value = data.excluded_playlists || "";
      $("syncPlaylists").value = data.sync_playlists || "";
      selectedPlaylistIds = new Set((data.included_playlists || "").split(/\r?\n/).map(x => x.trim()).filter(Boolean));
      render();
    }

    async function api(path, body) {
      const res = await fetch(path, {
        method: body ? "POST" : "GET",
        headers: body ? {"Content-Type": "application/json"} : undefined,
        body: body ? JSON.stringify(body) : undefined
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Request failed");
      return data;
    }

    function visiblePlaylists() {
      const query = $("playlistSearch").value.trim().toLowerCase();
      return spotifyPlaylists.filter(playlist => {
        const duplicate = (playlist.duplicate_name_count || 0) > 1;
        const matchesQuery = !query || playlist.name.toLowerCase().includes(query) || playlist.id.toLowerCase().includes(query);
        const matchesFilter =
          activeFilter === "all" ||
          (activeFilter === "owned" && playlist.owned) ||
          (activeFilter === "followed" && !playlist.owned) ||
          (activeFilter === "duplicates" && duplicate) ||
          (activeFilter === "selected" && selectedPlaylistIds.has(playlist.id)) ||
          (activeFilter === "empty" && !playlist.track_count);
        return matchesQuery && matchesFilter;
      });
    }

    function renderPlaylists() {
      const list = $("playlistList");
      list.innerHTML = "";
      for (const playlist of visiblePlaylists()) {
        const row = document.createElement("label");
        row.className = "playlist-row";
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = selectedPlaylistIds.has(playlist.id);
        checkbox.addEventListener("change", () => {
          checkbox.checked ? selectedPlaylistIds.add(playlist.id) : selectedPlaylistIds.delete(playlist.id);
          render();
        });
        const cover = document.createElement("img");
        cover.className = "cover";
        cover.alt = "";
        cover.src = playlist.image_url || `https://picsum.photos/seed/${encodeURIComponent(playlist.id)}/80/80`;
        const body = document.createElement("div");
        const title = document.createElement("div");
        title.className = "playlist-title";
        title.textContent = playlist.name || "(untitled)";
        const meta = document.createElement("div");
        meta.className = "meta";
        meta.textContent = `${playlist.track_count || 0} tracks - ${playlist.owned ? "owned" : playlist.owner || "followed"} - ${playlist.id}`;
        body.append(title, meta);
        row.append(checkbox, cover, body);
        if ((playlist.duplicate_name_count || 0) > 1) {
          const badge = document.createElement("span");
          badge.className = "badge";
          badge.textContent = "duplicate";
          row.append(badge);
        }
        list.append(row);
      }
    }

    function renderDuplicates() {
      const list = $("duplicateList");
      const groups = duplicateGroups();
      list.innerHTML = "";
      $("duplicateBadge").textContent = plural(groups.length, "duplicate name");
      $("reviewHint").textContent = groups.length
        ? "Review suggested duplicate handling before syncing."
        : "No duplicate playlist names in the current selection.";
      groups.forEach((group, groupIndex) => {
        const card = document.createElement("div");
        card.className = "dupe-card";
        const head = document.createElement("div");
        head.className = "dupe-head";
        const name = document.createElement("span");
        name.textContent = group[0].name || "(untitled)";
        const count = document.createElement("span");
        count.textContent = `${group.length} matches`;
        head.append(name, count);
        card.append(head);
        group.forEach((playlist, index) => {
          const choice = document.createElement("label");
          choice.className = "dupe-choice";
          const radio = document.createElement("input");
          radio.type = "radio";
          radio.name = `dupe-${groupIndex}`;
          radio.checked = index === 0;
          const cover = document.createElement("img");
          cover.className = "cover";
          cover.alt = "";
          cover.src = playlist.image_url || `https://picsum.photos/seed/${encodeURIComponent(playlist.id)}/80/80`;
          const body = document.createElement("span");
          const title = document.createElement("strong");
          title.textContent = playlist.name || "(untitled)";
          const meta = document.createElement("span");
          meta.className = "meta";
          meta.textContent = `${playlist.track_count || 0} tracks - ${playlist.owned ? "by you" : playlist.owner || "followed"}`;
          body.append(title, meta);
          const badge = document.createElement("span");
          badge.className = `badge ${index === 0 ? "" : "red"}`.trim();
          badge.textContent = index === 0 ? "keep first" : "review";
          choice.append(radio, cover, body, badge);
          card.append(choice);
        });
        list.append(card);
      });
    }

    function renderPlan() {
      const selected = selectedPlaylists();
      const totalTracks = selected.reduce((sum, playlist) => sum + (playlist.track_count || 0), 0);
      const duplicateCount = duplicateGroups().length;
      $("foundMetric").textContent = spotifyPlaylists.length;
      $("selectedMetric").textContent = selected.length;
      $("duplicateMetric").textContent = duplicateCount;
      $("duplicateMetricLabel").textContent = duplicateCount === 1 ? "Duplicate name" : "Duplicate names";
      $("tracksMetric").textContent = totalTracks.toLocaleString();
      $("playlistSummary").textContent = plural(selected.length, "playlist") + " selected";
      $("createPlan").textContent = selected.length
        ? `${selected.length} playlists will be created or updated in Tidal.`
        : "Select playlists to build a sync plan.";
      $("runBtn").disabled = selected.length === 0;
      $("readyTitle").textContent = selected.length ? "Ready to sync" : "Choose playlists";
      $("readySubtitle").textContent = selected.length
        ? "Review duplicate handling and start when the plan looks right."
        : "Load demo playlists or connect Spotify to start.";
    }

    function renderActivity() {
      const list = $("activityItems");
      list.innerHTML = "";
      for (const item of activity.slice(-4)) {
        const card = document.createElement("div");
        card.className = "activity-card";
        const badge = document.createElement("div");
        badge.className = "activity-icon";
        badge.innerHTML = icon(activityIconName(item[0]));
        const body = document.createElement("div");
        const title = document.createElement("strong");
        title.textContent = item[0];
        const detail = document.createElement("small");
        detail.textContent = item[1];
        body.append(title, detail);
        card.append(badge, body);
        list.append(card);
      }
    }

    function render() {
      renderPlaylists();
      renderDuplicates();
      renderPlan();
      renderActivity();
    }

    function setMessage(text, isError = false) {
      $("message").textContent = text;
      $("message").classList.toggle("error", isError);
    }

    async function loadDemo() {
      const data = await api("/api/demo-playlists");
      spotifyPlaylists = data.playlists || [];
      spotifyUser = data.user || "Public demo";
      demoMode = true;
      selectedPlaylistIds = new Set(spotifyPlaylists.filter(p => p.selected).map(p => p.id));
      $("spotifyStatus").innerHTML = `Public demo <span class="status-dot"></span>`;
      $("tidalStatus").innerHTML = `Public demo <span class="status-dot"></span>`;
      activity.push(["Loaded public demo", `${spotifyPlaylists.length} Spotify playlists and Tidal-style duplicate review`]);
      render();
      setMessage("Public demo loaded. Nothing was synced.");
    }

    async function connectSpotify() {
      setMessage("Opening Spotify auth if needed...");
      const data = await api("/api/spotify-playlists", { config: payload() });
      spotifyPlaylists = data.playlists || [];
      spotifyUser = data.user || "";
      demoMode = false;
      selectedPlaylistIds = new Set((data.selected || []).map(String));
      $("spotifyStatus").innerHTML = `${spotifyUser || "Connected"} <span class="status-dot"></span>`;
      activity.push(["Connected to Spotify", `${spotifyPlaylists.length} playlists loaded`]);
      render();
      setMessage(`Spotify connected. Loaded ${spotifyPlaylists.length} playlists.`);
    }

    async function connectTidal() {
      setMessage("Opening Tidal device login if needed...");
      const data = await api("/api/tidal-connect", {});
      $("tidalStatus").innerHTML = data.ok ? `Connected <span class="status-dot"></span>` : "Connection failed";
      activity.push([data.ok ? "Connected to Tidal" : "Tidal connection failed", data.ok ? "Device authorization complete" : "Check the login window"]);
      renderActivity();
      setMessage(data.ok ? "Tidal connected." : "Tidal connection failed.", !data.ok);
    }

    async function save() {
      await api("/api/config", payload());
      activity.push(["Saved config", "Your local config.yml was updated"]);
      renderActivity();
      setMessage("Saved");
    }

    async function run() {
      setMessage("");
      if (demoMode) {
        activity.push(["Demo sync simulated", `${selectedPlaylistIds.size} playlists reviewed. Nothing was written to Tidal.`]);
        renderActivity();
        setMessage("Demo sync simulated. Nothing was synced.");
        return;
      }
      await api("/api/run", { config: payload(), mode: "selected", uri: $("playlistUri").value, include_favorites: $("includeFavorites").checked });
      activity.push(["Sync started", `${selectedPlaylistIds.size} playlists queued`]);
      renderActivity();
      startPolling();
    }

    async function stop() {
      await api("/api/stop", {});
      activity.push(["Stopping", "Requested sync stop"]);
      renderActivity();
      startPolling();
    }

    async function poll() {
      const data = await api("/api/status");
      $("stopBtn").disabled = !data.running;
      $("runBtn").disabled = data.running || selectedPlaylistIds.size === 0;
      if (data.logs && data.logs !== "Ready") activity[activity.length - 1] = [data.status, data.logs.split("\n").filter(Boolean).slice(-1)[0] || data.status];
      renderActivity();
      if (!data.running && poller) {
        clearInterval(poller);
        poller = null;
      }
    }

    function startPolling() {
      if (!poller) poller = setInterval(poll, 900);
      poll();
    }

    document.querySelectorAll(".chip").forEach(button => {
      button.addEventListener("click", () => {
        document.querySelectorAll(".chip").forEach(item => item.classList.remove("active"));
        button.classList.add("active");
        activeFilter = button.dataset.filter;
        renderPlaylists();
      });
    });
    $("demoBtn").addEventListener("click", () => loadDemo().catch(err => setMessage(err.message, true)));
    $("refreshBtn").addEventListener("click", () => connectSpotify().catch(err => setMessage(err.message, true)));
    $("spotifyBtn").addEventListener("click", () => connectSpotify().catch(err => setMessage(err.message, true)));
    $("tidalBtn").addEventListener("click", () => connectTidal().catch(err => setMessage(err.message, true)));
    $("saveBtn").addEventListener("click", () => save().catch(err => setMessage(err.message, true)));
    $("runBtn").addEventListener("click", () => run().catch(err => setMessage(err.message, true)));
    $("stopBtn").addEventListener("click", () => stop().catch(err => setMessage(err.message, true)));
    $("clearActivityBtn").addEventListener("click", () => { activity.length = 0; renderActivity(); });
    $("playlistSearch").addEventListener("input", renderPlaylists);
    $("includeFavorites").addEventListener("change", renderPlan);
    $("skipDuplicates").addEventListener("change", renderPlan);
    $("logsBtn").addEventListener("click", () => document.querySelector(".activity").scrollIntoView({behavior:"smooth"}));
    $("themeBtn").addEventListener("click", () => setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark"));
    setTheme(document.documentElement.dataset.theme || "dark");
    api("/api/config")
      .then(fill)
      .then(() => {
        if (new URLSearchParams(window.location.search).has("demo")) return loadDemo();
      })
      .catch(err => setMessage(err.message, true));
  </script>
</body>
</html>
"""
