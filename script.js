const DAY_META={
  Sunday:{accent:"#e0b84f"},
  Monday:{accent:"#c7d5f7"},
  Tuesday:{accent:"#d94b4b"},
  Wednesday:{accent:"#59c37a"},
  Thursday:{accent:"#7c6df2"},
  Friday:{accent:"#e78ac3"},
  Saturday:{accent:"#7c7c84"}
};

async function loadData(){
  const res=await fetch("data/briefing.json",{cache:"no-store"});
  if(!res.ok) throw new Error("Failed to load briefing.json");
  return res.json();
}

function setText(id,value){
  const el=document.getElementById(id);
  if(el) el.textContent=value||"";
}

function render(data){
  const meta=DAY_META[data.weekday] || DAY_META.Wednesday;
  document.documentElement.style.setProperty("--accent", meta.accent);
  setText("title", data.title);
  setText("mode", `Mode: ${data.mode}`);
  setText("tagline", data.tagline);
  setText("holidays", data.holidays);
  setText("moon", data.moon);
  setText("current", data.current);
  setText("sigilGlyph", data.sigil?.glyph || "");
  setText("sigilMeaning", data.sigil?.meaning || "");
  setText("tarot", data.tarot);
  setText("music", data.music);
  setText("directive", data.directive);
  setText("action", data.action);
  setText("persona", data.persona);
  setText("quote", data.quote);
  setText("question", data.question);
}

loadData().then(render).catch(err=>{
  console.error(err);
  setText("title","🏛️🌅 STOICISM TODAY // SIGNAL LOST");
  setText("mode","Mode: recovery");
  setText("tagline","The data file could not be loaded.");
});
