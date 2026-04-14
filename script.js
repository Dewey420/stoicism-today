const DAY_META = {
  Sunday: { sigil: "☉" },
  Monday: { sigil: "☽" },
  Tuesday: { sigil: "♂" },
  Wednesday: { sigil: "☿" },
  Thursday: { sigil: "♃" },
  Friday: { sigil: "♀" },
  Saturday: { sigil: "♄" },
};

async function loadData() {
  const response = await fetch("data/briefing.json", { cache: "no-store" });
  if (!response.ok) throw new Error("Failed to load briefing.json");
  return response.json();
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value || "";
}

function setTarotImage(data) {
  const image = document.getElementById("tarotImage");
  const card = data.tarotCard;
  const imageUrl = card?.image?.url;

  if (!image || !imageUrl) return;

  image.src = imageUrl;
  image.alt = `${card.name} tarot card`;
  image.hidden = false;
}

function render(data) {
  const meta = DAY_META[data.weekday] || DAY_META.Wednesday;
  const cardName = data.tarotCard?.name || "Daily Signal";

  setText("title", "Stoicism Today");
  setText("mode", `${data.weekday || "Today"} // ${data.date || "Daily Briefing"}`);
  setText("tagline", `${data.mode || "The Practice"} — ${data.tagline || ""}`);
  setText("holidays", data.holidays);
  setText("moon", data.moon);
  setText("current", data.current);
  setText("sigilGlyph", data.sigil?.glyph || meta.sigil);
  setText("sigilMeaning", data.sigil?.meaning || "");
  setText("tarot", data.tarot);
  setText("music", data.music);
  setText("directive", data.directive);
  setText("action", data.action);
  setText("persona", data.persona);
  setText("quote", data.quote);
  setText("question", data.question);
  setText("visualCaption", data.tarotCard?.arcana || "Daily Draw");
  setText("visualTitle", cardName);
  setTarotImage(data);
}

loadData().then(render).catch((error) => {
  console.error(error);
  setText("title", "Stoicism Today");
  setText("mode", "Signal Lost");
  setText("tagline", "The data file could not be loaded.");
});
