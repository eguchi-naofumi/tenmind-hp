#!/usr/bin/env python3
"""tenmindinc.com/lab/（申込ページ）と /lab/thanks/（お礼ページ）を、トップの index.html の見た目から生成する。
使い方: python3 tools/build_lab.py "<Apps Script の Web アプリ URL>"
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAS_URL = sys.argv[1] if len(sys.argv) > 1 else "__GAS_URL__"

src = (ROOT / "index.html").read_text()
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
header = re.search(r"<header>.*?</header>", src, re.S).group(0)
footer = re.search(r"<footer>.*?</footer>", src, re.S).group(0)
for a in ["top", "tenmind", "lab", "profile", "company", "contact"]:
    header = header.replace(f'href="#{a}"', 'href="/"' if a == "top" else f'href="/#{a}"')

EXTRA_CSS = """
/* 申込ページ */
.ev-head .meta{margin-top:1.2em;font-family:var(--sans);font-size:clamp(14px,.6vw + 11px,16px);letter-spacing:.06em;color:var(--green);font-weight:700}
.flow{counter-reset:f;list-style:none;margin-top:1.4em;max-width:40em}
.flow li{position:relative;padding:.7em 0 .7em 2.6em;border-bottom:1px solid var(--hair)}
.flow li::before{counter-increment:f;content:counter(f);position:absolute;left:0;top:.75em;width:1.8em;height:1.8em;border-radius:50%;background:var(--green);color:#fff;font-family:var(--sans);font-size:13px;display:grid;place-items:center}
.who{list-style:none;margin-top:1.2em}
.who li{padding-left:1.2em;position:relative;margin:.4em 0}
.who li::before{content:"";position:absolute;left:0;top:.85em;width:.45em;height:.45em;border-radius:50%;background:var(--brass)}
form.apply{margin-top:clamp(24px,3vw,36px);display:grid;gap:18px;max-width:640px}
form.apply label{display:block;font-family:var(--sans);font-size:14px;font-weight:700;letter-spacing:.06em;color:var(--green);margin-bottom:6px}
form.apply label .req{color:#a33;font-weight:400;margin-left:.4em;font-size:12px}
form.apply input[type=text],form.apply input[type=email],form.apply select{width:100%;font-family:var(--sans);font-size:16px;padding:12px 14px;border:1px solid var(--hair);border-radius:3px;background:#fffdf8;color:var(--ink)}
form.apply input:focus,form.apply select:focus{outline:2px solid var(--brass);outline-offset:1px}
.consent{font-family:var(--sans);font-size:13px;color:var(--sub);line-height:1.8}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.err{display:none;color:#a33;font-family:var(--sans);font-size:14px}
button.btn{border:0;cursor:pointer;font-family:var(--sans)}
button.btn[disabled]{opacity:.6;cursor:wait}
.thanks{min-height:60vh;display:flex;align-items:center}
.thanks .box{max-width:36em}
"""

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
__ROBOTS__<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600&family=Noto+Sans+JP:wght@400;700&family=Cormorant+Garamond:wght@500&display=swap" rel="stylesheet">
<style>__STYLE__</style>
</head>
<body>
"""

LAB = """<main>
  <section class="hero ev-head">
    <div class="wrap">
      <div class="kicker">Public Demonstration</div>
      <h1>社長の判断を、<br>1枚のカードにする60分</h1>
      <div class="rule"></div>
      <p>社長の判断ラボ 公開実演会 第1回</p>
      <p class="meta">2026年11月18日（水）20:00〜21:00 ／ Zoom ／ 無料</p>
      <a class="btn" href="#apply">申込みはこちら</a>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="kicker">What Happens</div>
      <h2>この会でやること</h2>
      <p style="margin-top:1.2em;max-width:34em">社長が下した一つの判断を、その場で「判断の型カード」1枚にします。カードに書くのは三つだけです。何を基準に判断したか（主張）、その基準はどんな出来事から生まれたか（出典）、どういう場面で使う基準か（使い道）。この三つが揃うと、社長の勘は、後継者が学べる言葉になります。</p>
      <p style="margin-top:1em;max-width:34em">当日は参加者の中からお一人に、最近迷った判断を一つ話していただきます（業種や金額は伏せて構いません）。江口が聞き取り、15分でカードにします。その後、カードを学んだAIが後継者からの問いにどう答えるかを、実際に動かしてお見せします。</p>
      <ol class="flow">
        <li>社長の判断には型がある ― 銀行員29年で見た、残る会社と消える会社の違い（10分）</li>
        <li>公開実演 ― 参加者の判断を1枚のカードにする（20分）</li>
        <li>カードを学んだAIは、後継者にどう答えるか（15分）</li>
        <li>質疑（10分）</li>
        <li>次の一歩の案内（5分）</li>
      </ol>
    </div>
  </section>

  <section class="co">
    <div class="wrap">
      <div class="kicker">For You</div>
      <h2>こんな方へ</h2>
      <ul class="who">
        <li>先代の判断を、自分の言葉で説明できるようになりたい後継者・幹部の方</li>
        <li>「自分がいなくなったら、この会社の判断はどうなるか」を考え始めた社長</li>
        <li>承継を支援する立場で、株や税の先にある「判断の引き継ぎ」に関心のある士業・金融機関の方</li>
      </ul>
      <p style="margin-top:1.6em;max-width:34em;color:var(--sub)">運営：江口尚文（株式会社テンマインド 代表取締役）。地方銀行で29年、営業と融資の両方の現場に立ち、中小企業の社長と向き合ってきました。売り込みの時間はありません。終了後に、希望者向けの個別面談（30分・無料）をご案内します。</p>
    </div>
  </section>

  <section id="apply">
    <div class="wrap">
      <div class="kicker">Apply</div>
      <h2>お申込み</h2>
      <form class="apply" id="applyForm" novalidate>
        <div><label for="name">お名前<span class="req">必須</span></label><input type="text" id="name" name="name" required autocomplete="name"></div>
        <div><label for="email">メールアドレス<span class="req">必須</span></label><input type="email" id="email" name="email" required autocomplete="email"></div>
        <div><label for="company">会社名・役職<span class="req">必須</span></label><input type="text" id="company" name="company" required autocomplete="organization"></div>
        <div><label for="role">立場<span class="req">必須</span></label>
          <select id="role" name="role" required><option value="">選んでください</option><option>社長本人</option><option>後継者・幹部</option><option>士業・金融機関</option><option>その他</option></select></div>
        <div><label for="interest">いちばん近い関心<span class="req">必須</span></label>
          <select id="interest" name="interest" required><option value="">選んでください</option><option>判断を記録したい</option><option>先代の判断を学びたい</option><option>顧客の承継支援に使いたい</option><option>研究に関心</option></select></div>
        <div><label for="demo">実演で、ご自身の判断を取り上げてほしいですか</label>
          <select id="demo" name="demo"><option value="">選んでください（任意）</option><option>取り上げてほしい</option><option>見るだけにしたい</option></select></div>
        <div class="hp" aria-hidden="true"><label>空欄のまま<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
        <p class="consent">お申込みいただいたメールアドレスに、本会のご案内と、社長の判断ラボからのお知らせをお送りします。配信はいつでも停止できます。お預かりした情報は、株式会社テンマインドが本会の運営とご連絡のためだけに使います。</p>
        <p class="err" id="err">未入力の項目があります。お名前・メールアドレス・会社名・立場・関心をご確認ください。</p>
        <div><button class="btn" type="submit" id="submitBtn">申し込む（無料）</button></div>
      </form>
    </div>
  </section>
</main>
<script>
const ENDPOINT = "__GAS_URL__";
document.getElementById("applyForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = e.target, err = document.getElementById("err"), btn = document.getElementById("submitBtn");
  const mailOk = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(f.email.value.trim());
  const ok = ["name", "email", "company", "role", "interest"].every(k => f[k].value.trim()) && mailOk;
  if (!ok) { err.style.display = "block"; return; }
  err.style.display = "none"; btn.disabled = true; btn.textContent = "送信しています…";
  const body = new URLSearchParams(new FormData(f));
  body.set("src", new URLSearchParams(location.search).get("src") || "web");
  try {
    await fetch(ENDPOINT, { method: "POST", mode: "no-cors", body });
    location.href = "/lab/thanks/";
  } catch (_) {
    btn.disabled = false; btn.textContent = "申し込む（無料）";
    err.textContent = "送信できませんでした。通信状況をご確認のうえ、もう一度お試しください。";
    err.style.display = "block";
  }
});
</script>
"""

THANKS = """<main>
  <section class="thanks">
    <div class="wrap box">
      <div class="kicker">Thank You</div>
      <h2>お申込みありがとうございます</h2>
      <p style="margin-top:1.2em">ご登録のメールアドレスに、確認のメールをお送りしました。当日のZoomのURLも記載しています。</p>
      <p style="margin-top:1em;color:var(--sub)">数分たってもメールが届かない場合は、迷惑メールのフォルダをご確認ください。それでも見当たらない場合は、eguchi@tenmindinc.com までご連絡ください。</p>
      <p style="margin-top:1.6em">社長の判断ラボのお知らせは、LINEでもお届けしています。</p>
      <a class="btn" href="https://lin.ee/6UWVMfB">LINEで友だち追加</a>
      <p style="margin-top:2em"><a href="/" style="color:var(--green)">株式会社テンマインド トップへ</a></p>
    </div>
  </section>
</main>
"""


def page(title, desc, body, robots=""):
    h = (HEAD.replace("__TITLE__", title).replace("__DESC__", desc).replace("__ROBOTS__", robots)
         .replace("__STYLE__", style + EXTRA_CSS))
    return h + header + "\n" + body + "\n" + footer + "\n</body>\n</html>\n"


(ROOT / "lab" / "thanks").mkdir(parents=True, exist_ok=True)
(ROOT / "lab" / "index.html").write_text(page(
    "社長の判断ラボ 公開実演会 第1回｜株式会社テンマインド",
    "社長の判断を、1枚のカードにする60分。2026年11月18日（水）20:00〜21:00、Zoom・無料。",
    LAB.replace("__GAS_URL__", GAS_URL)))
(ROOT / "lab" / "thanks" / "index.html").write_text(page(
    "お申込みありがとうございます｜社長の判断ラボ", "お申込みを受け付けました。", THANKS,
    '<meta name="robots" content="noindex">\n'))
print("built lab pages; endpoint =", GAS_URL)
