/* tutor.js: an "Ask the tutor" box for a page of the workshop site.

   Add to a page, before </body>:   <script src="tutor.js" defer></script>
   (from a page in a subfolder:      <script src="../tutor.js" defer></script>)

   It asks the site's own server (api/ask, next to this file), which adds the
   workshop key and calls the model; the key never reaches the browser. On the
   permanent GitHub Pages copy there is no server, so the box says the tutor
   works on the live site while the Codespace runs. site/tutor.txt, if present,
   tells the tutor the topic and the level. Answers are shown as plain text. */
(function () {
  "use strict";
  var here = document.currentScript && document.currentScript.src;
  if (!here) return;
  var STATUS = new URL("api/status", here).href;
  var ASK = new URL("api/ask", here).href;
  var history = [];

  var css = [
    ".tutor-btn{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:99999;",
    "font:600 15px/1.2 system-ui,-apple-system,Segoe UI,sans-serif;padding:12px 16px;border-radius:999px;border:0;cursor:pointer;",
    "background:#0d6a65;color:#fff;box-shadow:0 2px 10px rgba(0,0,0,.25)}",
    ".tutor-btn:focus-visible,.tutor-panel button:focus-visible,.tutor-panel textarea:focus-visible{outline:3px solid #f2b705;outline-offset:2px}",
    ".tutor-panel{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(max(16px,env(safe-area-inset-bottom,0px)) + 56px);z-index:99999;",
    "width:min(380px,calc(100vw - 32px));max-height:min(520px,calc(100vh - 110px));display:flex;flex-direction:column;",
    "background:#fff;color:#15242a;border:1px solid #c9d6d4;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,.2);",
    "font:15px/1.45 system-ui,-apple-system,Segoe UI,sans-serif}",
    ".tutor-panel[hidden]{display:none}",
    ".tutor-head{padding:10px 14px;border-bottom:1px solid #e3ebea;font-weight:700;display:flex;justify-content:space-between;align-items:center}",
    ".tutor-head button{background:none;border:0;font-size:20px;cursor:pointer;color:inherit}",
    ".tutor-log{padding:10px 14px;overflow-y:auto;flex:1;display:flex;flex-direction:column;gap:8px}",
    ".tutor-msg{white-space:pre-wrap;padding:8px 10px;border-radius:8px;max-width:92%}",
    ".tutor-msg.you{align-self:flex-end;background:#dcecea}",
    ".tutor-msg.tutor{align-self:flex-start;background:#f3f5f5}",
    ".tutor-msg.note{align-self:center;background:none;color:#55676e;font-size:13px;text-align:center}",
    ".tutor-form{display:flex;gap:8px;padding:10px 14px;border-top:1px solid #e3ebea}",
    ".tutor-form textarea{flex:1;resize:none;font:inherit;padding:8px;border:1px solid #c9d6d4;border-radius:8px;min-height:40px;color:inherit;background:#fff}",
    ".tutor-form button{font:600 14px system-ui,sans-serif;padding:0 14px;border:0;border-radius:8px;background:#0d6a65;color:#fff;cursor:pointer}",
    ".tutor-form button[disabled]{opacity:.5;cursor:default}",
    "@media (prefers-color-scheme:dark){.tutor-panel{background:#152328;color:#e3ecec;border-color:#27383e}",
    ".tutor-head,.tutor-form{border-color:#27383e}.tutor-msg.you{background:#17353a}.tutor-msg.tutor{background:#1d2e33}",
    ".tutor-form textarea{background:#0f191d;border-color:#27383e}.tutor-msg.note{color:#94a7ac}}"
  ].join("");
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var btn = document.createElement("button");
  btn.className = "tutor-btn";
  btn.type = "button";
  btn.textContent = "Ask the tutor";
  btn.setAttribute("aria-expanded", "false");

  var panel = document.createElement("section");
  panel.className = "tutor-panel";
  panel.hidden = true;
  panel.setAttribute("aria-label", "Ask the tutor");
  var head = document.createElement("div");
  head.className = "tutor-head";
  var title = document.createElement("span");
  title.textContent = "Ask the tutor";
  var close = document.createElement("button");
  close.type = "button";
  close.setAttribute("aria-label", "Close");
  close.textContent = "\u00d7";
  head.appendChild(title);
  head.appendChild(close);
  var log = document.createElement("div");
  log.className = "tutor-log";
  log.setAttribute("aria-live", "polite");
  var form = document.createElement("form");
  form.className = "tutor-form";
  var box = document.createElement("textarea");
  box.id = "tutor-question";
  box.rows = 2;
  box.placeholder = "Your question about this page";
  box.setAttribute("aria-label", "Your question");
  var send = document.createElement("button");
  send.type = "submit";
  send.textContent = "Ask";
  form.appendChild(box);
  form.appendChild(send);
  panel.appendChild(head);
  panel.appendChild(log);
  panel.appendChild(form);

  function say(kind, text) {
    var p = document.createElement("div");
    p.className = "tutor-msg " + kind;
    p.textContent = text;
    log.appendChild(p);
    log.scrollTop = log.scrollHeight;
    return p;
  }
  function setOpen(open) {
    panel.hidden = !open;
    btn.setAttribute("aria-expanded", String(open));
    if (open) box.focus();
  }
  btn.addEventListener("click", function () { setOpen(panel.hidden); });
  close.addEventListener("click", function () { setOpen(false); btn.focus(); });
  box.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
  });

  var live = false;
  function offline(reason) {
    live = false;
    box.disabled = true;
    send.disabled = true;
    say("note", reason);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = box.value.trim();
    if (!q || !live) return;
    box.value = "";
    say("you", q);
    history.push({ role: "user", content: q.slice(0, 2000) });
    history = history.slice(-12);
    send.disabled = true;
    var wait = say("note", "Thinking...");
    var page = (document.querySelector("main") || document.body).innerText || "";
    fetch(ASK, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history, page: page.slice(0, 3000) })
    }).then(function (r) {
      return r.json().catch(function () { return { error: "The tutor gave no answer." }; });
    }).then(function (d) {
      wait.remove();
      if (d && d.answer) {
        say("tutor", d.answer);
        history.push({ role: "assistant", content: d.answer.slice(0, 2000) });
      } else {
        history.pop();
        say("note", (d && d.error) || "The tutor gave no answer.");
      }
    }).catch(function () {
      wait.remove();
      history.pop();
      say("note", "The tutor could not be reached. Try again in a moment.");
    }).then(function () { send.disabled = !live; box.focus(); });
  });

  function mount() {
    document.body.appendChild(panel);
    document.body.appendChild(btn);
    fetch(STATUS, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("no relay");
      return r.json();
    }).then(function (d) {
      if (d && d.available) {
        live = true;
        say("note", "Ask anything about this page. Answers come from an AI model and can be wrong: check them against the page.");
      } else if (d && d.reason === "resting until tomorrow") {
        offline("The tutor has answered all its questions for today.");
      } else {
        offline("The tutor is not connected yet.");
      }
    }).catch(function () {
      offline("The tutor works on the live site while its Codespace is running.");
    });
  }
  if (document.body) mount(); else document.addEventListener("DOMContentLoaded", mount);
})();
