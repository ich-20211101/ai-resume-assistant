async function handleSubmit() {
  const jd          = document.getElementById("jd").value.trim();
  const resume      = document.getElementById("resume").value.trim();
  const instruction = document.getElementById("instruction").value.trim();
  const errorEl     = document.getElementById("error-msg");
  const outputEl    = document.getElementById("output");

  // Reset
  errorEl.classList.add("hidden");
  outputEl.classList.add("hidden");

  if (!jd)     return showError("Please paste a job description.");
  if (!resume) return showError("Please paste your resume.");

  setLoading(true);

  try {
    const res = await fetch("/api/tailor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_description: jd, resume, instruction }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Something went wrong.");
    }

    const data = await res.json();
    renderOutput(data);
    outputEl.classList.remove("hidden");
    outputEl.scrollIntoView({ behavior: "smooth", block: "start" });

  } catch (err) {
    showError(err.message);
  } finally {
    setLoading(false);
  }
}

// ── Render ─────────────────────────────────────────────────────────────────
function renderOutput(data) {
  // Keywords
  renderTags("keywords-matched", data.keywords.matched, "matched");
  renderTags("keywords-missing", data.keywords.missing, "missing");

  // Summary
  document.getElementById("summary-text").textContent = data.summary;

  // Skills
  renderTags("skills-list", data.skills, "skill");

  // Experience
  const expContainer = document.getElementById("experience-list");
  expContainer.innerHTML = "";

  data.experience.forEach((job) => {
    const item = document.createElement("div");
    item.className = "exp-item";

    const bulletsHTML = job.bullets
      .map((b) => `<li>${escapeHtml(b)}</li>`)
      .join("");

    item.innerHTML = `
      <div class="exp-header">
        <div class="exp-title">${escapeHtml(job.title)}</div>
        <div class="exp-company">${escapeHtml(job.company)}</div>
      </div>
      <ul class="exp-bullets">${bulletsHTML}</ul>
      <button class="copy-btn exp-copy-btn" onclick="copyBullets(this)">Copy Bullets</button>
    `;

    expContainer.appendChild(item);
  });
}

function renderTags(containerId, items, type) {
  const el = document.getElementById(containerId);
  el.innerHTML = "";
  if (!items || items.length === 0) {
    el.innerHTML = `<span style="color:#b0b0ae;font-size:13px;">None</span>`;
    return;
  }
  items.forEach((item) => {
    const tag = document.createElement("span");
    tag.className = `tag ${type}`;
    tag.textContent = item;
    el.appendChild(tag);
  });
}

// ── Copy Helpers ───────────────────────────────────────────────────────────
function copyText(elementId) {
  const text = document.getElementById(elementId).textContent;
  navigator.clipboard.writeText(text).then(() => flashCopied(event.target));
}

function copySkills() {
  const tags = document.querySelectorAll("#skills-list .tag");
  const text = Array.from(tags).map((t) => t.textContent).join(", ");
  navigator.clipboard.writeText(text).then(() => flashCopied(event.target));
}

function copyBullets(btn) {
  const ul = btn.previousElementSibling;
  const text = Array.from(ul.querySelectorAll("li"))
    .map((li) => "- " + li.textContent)
    .join("\n");
  navigator.clipboard.writeText(text).then(() => flashCopied(btn));
}

function flashCopied(btn) {
  const original = btn.textContent;
  btn.textContent = "Copied!";
  setTimeout(() => (btn.textContent = original), 1500);
}

// ── Utils ──────────────────────────────────────────────────────────────────
function setLoading(isLoading) {
  const btn    = document.getElementById("submit-btn");
  const text   = document.getElementById("btn-text");
  const loader = document.getElementById("btn-loader");
  btn.disabled = isLoading;
  text.classList.toggle("hidden", isLoading);
  loader.classList.toggle("hidden", !isLoading);
}

function showError(msg) {
  const el = document.getElementById("error-msg");
  el.textContent = msg;
  el.classList.remove("hidden");
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
