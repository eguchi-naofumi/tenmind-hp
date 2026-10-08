// 全ページ共通：狭い幅（1120px以下）のメニュー開閉
(() => {
  const btn = document.querySelector(".menu-btn");
  const nav = document.getElementById("gnav");
  if (!btn || !nav) return;
  const isOpen = () => btn.getAttribute("aria-expanded") === "true";
  const set = (open) => {
    btn.setAttribute("aria-expanded", String(open));
    btn.setAttribute("aria-label", open ? "メニューを閉じる" : "メニューを開く");
    document.documentElement.classList.toggle("nav-open", open);
  };
  btn.addEventListener("click", () => {
    set(!isOpen());
    if (isOpen()) nav.querySelector("a").focus();
  });
  nav.addEventListener("click", (e) => { if (e.target.closest("a")) set(false); });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && isOpen()) { set(false); btn.focus(); }
  });
  document.addEventListener("click", (e) => { if (isOpen() && !e.target.closest("header")) set(false); });
  // メニューの最後の項目から Tab で抜けたら閉じる
  nav.addEventListener("focusout", (e) => {
    if (isOpen() && e.relatedTarget && !e.relatedTarget.closest("header")) set(false);
  });
  matchMedia("(min-width: 1121px)").addEventListener("change", (e) => { if (e.matches) set(false); });
})();
