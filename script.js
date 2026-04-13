fetch('briefing.json')
  .then(res => res.json())
  .then(data => {

    const app = document.getElementById("app");

    app.innerHTML = `
      <div class="title">${data.title}</div>
      <div class="mode">${data.mode}</div>

      ${createCard("🎉 HOLIDAYS", data.holidays)}
      ${createCard("🌑 LUNAR STATUS", data.moon)}
      ${createCard("🧠 CURRENT", data.current)}
      ${createCard("🔺 SIGIL", data.sigil)}
      ${createCard("🃏 TAROT", data.tarot)}
      ${createCard("🎧 MUSIC OF THE DAY", data.music)}
      ${createCard("⚡ DIRECTIVE", data.directive)}
      ${createCard("⚔️ ACTION", data.action)}
      ${createCard("🏛️ PERSONA", data.persona)}
      ${createCard("💬 STOIC", data.quote)}
      ${createCard("🔮 FINAL QUERY", data.question)}
    `;
  });

function createCard(title, content) {
  return `
    <div class="card">
      <div class="section-title">${title}</div>
      <div class="block">${content}</div>
    </div>
  `;
}
