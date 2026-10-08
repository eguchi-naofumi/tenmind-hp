#!/usr/bin/env python3
"""トップの index.html（正本）の見た目・ヘッダー・フッターから、下層ページを生成する。
生成するページ: /lab/（実演会の申込）・/lab/thanks/（お礼）・/lab/booking/（面談予約）・/profile/（代表メッセージ）・/privacy/（プライバシーポリシー）・/404.html
使い方: python3 tools/build_lab.py "<Apps Script の Web アプリ URL>"
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAS_URL = sys.argv[1] if len(sys.argv) > 1 else "__GAS_URL__"

src = (ROOT / "index.html").read_text()
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
head_common = re.search(r"<!-- head:common.*?-->\n(.*?)<!-- /head:common -->", src, re.S).group(1)
# トップ内リンク（#lab など）を下層ページ用に /#lab へ。本文へ移動（#main）はページ内なのでそのまま
to_top = lambda html: re.sub(r'href="#(?!main")([\w-]+)"', r'href="/#\1"', html)
header = to_top(re.search(r"<header>.*?</header>", src, re.S).group(0))
footer = to_top(re.search(r"<footer>.*?</footer>", src, re.S).group(0))
portrait = re.search(r"<!-- portrait:start.*?-->\n\s*(.*?)\n\s*<!-- portrait:end -->", src, re.S).group(1)
SITE = "https://tenmindinc.com"

EXTRA_CSS = """
/* 申込ページ */
.nb{display:inline-block}
.ev-head .meta{margin-top:1.2em;font-family:var(--sans);font-size:clamp(14px,.6vw + 11px,16px);letter-spacing:.06em;color:var(--green);font-weight:700}
.flow{counter-reset:f;list-style:none;margin-top:1.4em;max-width:40em}
.flow li{position:relative;padding:.7em 0 .7em 2.6em;border-bottom:1px solid var(--hair)}
.flow li::before{counter-increment:f;content:counter(f);position:absolute;left:0;top:.75em;width:1.8em;height:1.8em;border-radius:50%;background:var(--green);color:#fff;font-family:var(--sans);font-size:13px;display:grid;place-items:center}
.who{list-style:none;margin-top:1.2em}
.who li{padding-left:1.2em;position:relative;margin:.4em 0}
.who li::before{content:"";position:absolute;left:0;top:.85em;width:.45em;height:.45em;border-radius:50%;background:var(--brass)}
.thanks{min-height:60vh;display:flex;align-items:center}
.thanks .box{max-width:36em}

/* 文書ページ（プライバシーポリシー） */
.doc-head{padding:clamp(56px,8vw,96px) 0 clamp(24px,3vw,32px);border-bottom:1px solid var(--hair)}
.doc-head h1{font-weight:600;font-size:clamp(26px,2.6vw + 14px,38px);letter-spacing:.08em;color:var(--green);margin-top:.4em}
.doc-head .date{margin-top:1em;font-family:var(--sans);font-size:13px;letter-spacing:.06em;color:var(--muted)}
.doc{padding-top:clamp(32px,4vw,48px)}
.doc .body{max-width:46em}
.doc h2{font-size:clamp(18px,.8vw + 14px,21px);letter-spacing:.04em;margin-top:2.6em;padding-top:1.2em;border-top:1px solid var(--hair)}
.doc h2:first-child{margin-top:0;padding-top:0;border-top:0}
.doc h3{font-family:var(--sans);font-size:14px;font-weight:700;letter-spacing:.06em;color:var(--green);margin-top:1.8em}
.doc p,.doc ul,.doc dl{margin-top:.9em}
.doc ul{padding-left:1.4em}
.doc li{margin:.3em 0}
.doc a{color:var(--green);word-break:break-all}
.doc .tbl{overflow-x:auto;margin-top:1.2em}
.doc table{margin-top:0;font-size:.92em}
.doc th,.doc td{padding:12px 14px 12px 0}
.doc th{width:11em}
.doc thead th{color:var(--green);border-bottom:2px solid var(--hair);width:auto}
.doc dl{display:grid;grid-template-columns:7em 1fr;gap:6px 16px}
.doc dt{font-family:var(--sans);font-size:13px;font-weight:700;letter-spacing:.06em;color:var(--brass2);padding-top:.25em}
.doc .note{font-family:var(--sans);font-size:13px;color:var(--sub)}

/* 代表メッセージ */
.msg{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,260px);gap:clamp(32px,5vw,72px);align-items:start}
.msg h2{margin-top:0}
.msg .body p{margin-top:1.2em}
.msg .sign{margin-top:2.2em;text-align:right;letter-spacing:.1em}
.msg .sign small{display:block;font-family:var(--sans);font-size:13px;letter-spacing:.08em;color:var(--sub)}
.msg .sign b{font-weight:600;font-size:1.25em;letter-spacing:.2em}
@media(max-width:720px){.msg{grid-template-columns:1fr}.msg .portrait{order:-1;max-width:220px}}
.career{margin-top:clamp(28px,4vw,44px)}
.career th{width:8em}
@media(max-width:560px){.doc dl{grid-template-columns:1fr;gap:0}.doc dd{margin-bottom:10px}.doc thead{display:none}.doc th{width:auto;border-bottom:0;padding-top:16px}.doc td{padding:4px 0 16px}}
"""

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
__META__<style>__STYLE__</style>
</head>
<body>
"""

LAB = """<main id="main">
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
        <p class="consent">お申込みいただいたメールアドレスに、本会のご案内と、社長の判断ラボからのお知らせをお送りします。配信はいつでも、メール末尾のリンクから停止できます。お預かりした情報は、株式会社テンマインドが本会の運営とご連絡のためだけに使います。詳しくは<a href="/privacy/">プライバシーポリシー</a>をご覧ください。</p>
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

THANKS = """<main id="main">
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

BOOKING = """<main id="main">
  <section class="hero ev-head">
    <div class="wrap">
      <div class="kicker">Private Session</div>
      <h1>30分で、<br><span class="nb">御社の判断を</span><span class="nb">1枚のカードに。</span></h1>
      <div class="rule"></div>
      <p>個別面談（30分・無料・オンライン）</p>
      <p style="margin-top:1em;max-width:34em">前半15分で、最近迷った判断を一つ伺い、その場で「主張・出典・使い道」の三行にまとめた判断の型カードを1枚作り、面談後にお渡しします。後半は、カードを会社に残していく方法をご説明します。売り込みの場ではありません。</p>
      <p style="margin-top:1em;color:var(--sub)">お申込みは、社長ご本人でも、後継者・幹部の方でも、士業・金融機関の方でも結構です。</p>
    </div>
  </section>
  <section id="book">
    <div class="wrap">
      <div class="kicker">Booking</div>
      <h2>日時を選んでご予約</h2>
      <form class="apply" id="bookForm" novalidate>
        <div><label for="slot">ご希望の日時<span class="req">必須</span></label>
          <select id="slot" name="slot" required><option value="">空いている枠を読み込んでいます…</option></select></div>
        <div><label for="name">お名前<span class="req">必須</span></label><input type="text" id="name" name="name" required autocomplete="name"></div>
        <div><label for="email">メールアドレス<span class="req">必須</span></label><input type="email" id="email" name="email" required autocomplete="email"></div>
        <div><label for="company">会社名・役職<span class="req">必須</span></label><input type="text" id="company" name="company" required autocomplete="organization"></div>
        <div><label for="size">業種・従業員数</label><input type="text" id="size" name="size" placeholder="例：建設業・30名"></div>
        <div><label for="age">社長の年齢層</label>
          <select id="age" name="age"><option value="">選んでください（任意）</option><option>40代以下</option><option>50代</option><option>60代</option><option>70代以上</option></select></div>
        <div><label for="successor">後継者の有無</label>
          <select id="successor" name="successor"><option value="">選んでください（任意）</option><option>決まっている</option><option>候補はいる</option><option>未定</option><option>該当なし</option></select></div>
        <div><label for="topic">面談で扱いたい判断を一言で<span class="req">必須</span></label><input type="text" id="topic" name="topic" required placeholder="例：値上げ、採用、取引先との関係"></div>
        <div><label for="research">研究協力へのご関心</label>
          <select id="research" name="research"><option value="">選んでください（任意）</option><option>ある</option><option>話を聞きたい</option><option>今はない</option></select></div>
        <div class="hp" aria-hidden="true"><label>空欄のまま<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
        <p class="consent">お預かりした情報は、株式会社テンマインドが面談の準備とご連絡のためだけに使います。詳しくは<a href="/privacy/">プライバシーポリシー</a>をご覧ください。</p>
        <p class="err" id="err">未入力の項目があります。日時・お名前・メールアドレス・会社名・扱いたい判断をご確認ください。</p>
        <div><button class="btn" type="submit" id="submitBtn">この日時で予約する</button></div>
      </form>
      <div id="done" style="display:none;margin-top:28px">
        <h3 style="font-weight:600;color:var(--green);font-size:1.2em">ご予約を承りました</h3>
        <p style="margin-top:.8em" id="doneWhen"></p>
        <p style="margin-top:.6em;color:var(--sub)">確認のメールをお送りしました。届かない場合は、迷惑メールのフォルダをご確認いただくか、eguchi@tenmindinc.com までご連絡ください。</p>
      </div>
    </div>
  </section>
</main>
<script>
const ENDPOINT = "__GAS_URL__";
const sel = document.getElementById("slot");
async function loadSlots() {
  try {
    const d = await fetch(ENDPOINT + "?a=slots").then(r => r.json());
    sel.innerHTML = "";
    if (!d.slots || !d.slots.length) { sel.innerHTML = '<option value="">ただいま空いている枠がありません</option>'; return; }
    sel.append(new Option("選んでください", ""));
    d.slots.forEach(s => sel.append(new Option(s.label + "〜（30分）", s.iso)));
  } catch (_) { sel.innerHTML = '<option value="">枠を読み込めませんでした。再読み込みしてください</option>'; }
}
loadSlots();
document.getElementById("bookForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = e.target, err = document.getElementById("err"), btn = document.getElementById("submitBtn");
  const mailOk = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(f.email.value.trim());
  const ok = ["slot", "name", "email", "company", "topic"].every(k => f[k].value.trim()) && mailOk;
  if (!ok) { err.style.display = "block"; return; }
  err.style.display = "none"; btn.disabled = true; btn.textContent = "予約しています…";
  const body = new URLSearchParams(new FormData(f)); body.set("a", "book");
  try {
    const d = await fetch(ENDPOINT, { method: "POST", body }).then(r => r.json());
    if (d.ok) {
      f.style.display = "none"; document.getElementById("done").style.display = "block";
      document.getElementById("doneWhen").textContent = "日時：" + d.when + "（オンライン）";
    } else if (d.error === "taken") {
      err.textContent = "申し訳ありません。その枠は直前に埋まりました。別の日時をお選びください。"; err.style.display = "block";
      btn.disabled = false; btn.textContent = "この日時で予約する"; loadSlots();
    } else { throw new Error(d.error); }
  } catch (_) {
    err.textContent = "送信できませんでした。通信状況をご確認のうえ、もう一度お試しください。"; err.style.display = "block";
    btn.disabled = false; btn.textContent = "この日時で予約する";
  }
});
</script>
"""


# プライバシーポリシー（個人情報保護法 21条・23条・25条・27条・28条・32条〜38条）。
# 事実の正本: tenmind-lab-gas（Code.js・Booking.js）の受付項目と、使っているサービス。仕組みを変えたら、ここも直して改定日を足す。
PRIVACY = """<main id="main">
  <section class="doc-head">
    <div class="wrap">
      <div class="kicker">Privacy Policy</div>
      <h1>プライバシーポリシー</h1>
      <p class="date">2026年10月8日 制定</p>
    </div>
  </section>
  <section class="doc" style="padding-bottom:clamp(64px,9vw,120px)">
    <div class="wrap"><div class="body">
      <p>株式会社テンマインド（以下「当社」）は、このサイトからのご登録・お申込み・ご予約と、メールやLINEでのお問い合わせで取得する個人情報を、個人情報の保護に関する法律（以下「個人情報保護法」）と関係する指針に従って、次のとおり取り扱います。</p>

      <h2>1. 事業者</h2>
      <dl>
        <dt>名称</dt><dd>株式会社テンマインド</dd>
        <dt>代表者</dt><dd>代表取締役　江口 尚文</dd>
        <dt>所在地</dt><dd>〒811-1347　福岡県福岡市南区野多目6-3-4</dd>
        <dt>お問い合わせ</dt><dd><a href="mailto:eguchi@tenmindinc.com">eguchi@tenmindinc.com</a></dd>
      </dl>

      <h2>2. 取得する情報</h2>
      <p>各フォームに入力いただいた情報と、受付の記録を取得します。</p>
      <div class="tbl"><table>
        <thead><tr><th>受付</th><th>取得する情報</th></tr></thead>
        <tr><th>お知らせの登録<br>（トップページ）</th><td>お名前、メールアドレス、どこからお越しになったか（例：本の巻末のリンク）</td></tr>
        <tr><th>公開実演会のお申込み<br>（/lab/）</th><td>お名前、メールアドレス、会社名・役職、立場、いちばん近い関心、実演でご自身の判断を取り上げてほしいか（任意）、どこからお越しになったか</td></tr>
        <tr><th>個別面談のご予約<br>（/lab/booking/）</th><td>ご希望の日時、お名前、メールアドレス、会社名・役職、面談で扱いたい判断、業種・従業員数（任意）、社長の年齢層（任意）、後継者の有無（任意）、研究協力へのご関心（任意）</td></tr>
        <tr><th>受付の記録<br>（上の三つに共通）</th><td>受付日時、メールを送った日時、配信停止や予約取消のリンクに使う識別子、状態（配信中・停止、予約中・取消など）。お知らせの登録と公開実演会のお申込みでは、あわせて、お申込み時に表示した同意の文言の要旨を記録します（個別面談のご予約では記録しません）</td></tr>
        <tr><th>お問い合わせ<br>（メール・LINE）</th><td>お名前、メールアドレスやLINEの表示名、お問い合わせの内容</td></tr>
      </table></div>

      <h2>3. 利用目的</h2>
      <ul>
        <li>『銀行員の目』シリーズの新刊のお知らせと、公開実演会のご案内をメールでお送りするため</li>
        <li>公開実演会のお申込みの受付、参加方法のご連絡、開催前日と翌日のご案内のため</li>
        <li>個別面談のご予約の受付、日程の確保、確認と前日のご案内のため</li>
        <li>お問い合わせにお答えするため</li>
      </ul>
      <p>これ以外の目的には使いません。目的を変えるときは、個人情報保護法に従い、あらかじめご本人の同意をいただくか、変更後の目的をお知らせします。</p>

      <h2>4. 第三者への提供</h2>
      <p>法令に基づく場合を除き、ご本人の同意なく、個人情報を第三者に提供しません。受付の仕組みを動かすために、業務の一部を次の5の事業者に委託しています。</p>

      <h2>5. 業務の委託と、外国での取り扱い</h2>
      <div class="tbl"><table>
        <thead><tr><th>委託先</th><th>委託する業務と、預ける情報</th></tr></thead>
        <tr><th>Google LLC（米国）<br>Google Workspace</th><td>受付の処理（Google Apps Script）、名簿と予約の記録の保管（Google スプレッドシート）、確認・案内メールの送信（Gmail）、面談の予定の登録（Google カレンダー）。預ける情報は、上の2の情報のすべてです。</td></tr>
      </table></div>
      <p>Google LLC は米国の事業者です。当社は、Google との契約（<a href="https://cloud.google.com/terms/data-processing-addendum/">Cloud Data Processing Addendum</a>）で次の事項が定められていることを確認し、個人情報保護法第28条第1項に定める「個人情報取扱事業者が講ずべき措置に相当する措置を継続的に講ずるために必要な体制」を整えた事業者への委託として扱っています。</p>
      <ul>
        <li>当社の指示に従ってのみ、情報を処理すること</li>
        <li>情報の暗号化、アクセスの制限など、技術・組織・物理の各面で安全管理措置を講じること。ISO/IEC 27001 の認証と、SOC 2・SOC 3 の監査を毎年受けること</li>
        <li>再委託先を公開し、追加するときは事前に知らせること</li>
        <li>契約が終わったときは、情報を削除すること</li>
      </ul>
      <h3>移転先の国と、その国の制度</h3>
      <p>米国には、連邦レベルの包括的な個人情報保護法はありません。分野ごとの連邦法（電子通信プライバシー法、医療情報に関する HIPAA など）と、州法（カリフォルニア州消費者プライバシー法など）があります。EU の十分性認定は受けていません。APEC の越境プライバシールール（CBPR）システムには2012年7月から参加しています。事業者に政府の情報収集への協力義務を課す制度で、本人の権利利益に重大な影響を及ぼしうるものは、個人情報保護委員会の調査では挙げられていません。</p>
      <p class="note">出典：個人情報保護委員会「<a href="https://www.ppc.go.jp/enforcement/infoprovision/laws/offshore_report_america/">諸外国・地域の法制度（アメリカ）</a>」（2021年10月時点の情報）</p>
      <h3>情報が保存されるサーバの国</h3>
      <p>特定できません。Google は世界各地のデータセンターで情報を保存・処理しており、当社の契約では保存する国を指定していないためです。データセンターの所在地は、Google の「<a href="https://datacenters.google/locations/">データセンターの所在地</a>」で公開されています。</p>
      <h3>当社が続けて行う確認</h3>
      <p>当社は、年に1回以上、Google の契約条件と安全管理の状況、米国の制度の変化を確認します。相当する措置の実施に支障が生じたときは必要な対応をとり、続けることが難しくなったときは委託をやめます。ご本人から求めがあったときは、個人情報保護法施行規則第18条第3項に定める事項をお知らせします。</p>

      <h2>6. 安全管理のために講じている措置</h2>
      <ul>
        <li>基本方針：このポリシーを定め、個人情報保護法と関係する指針に従って取り扱います。</li>
        <li>取り扱いの決まり：取得・利用・保存・削除の各段階で、誰が、どのように取り扱うかを定めています。</li>
        <li>組織的な措置：個人情報の取り扱いの責任者を代表取締役とします。漏えいなどが起きたとき、またはそのおそれがあるときは、責任者が状況を確かめ、法令に従って個人情報保護委員会への報告とご本人への通知を行います。</li>
        <li>人的な措置：個人情報を取り扱うのは代表取締役に限ります。今後ほかの者に取り扱わせるときは、秘密を守る約束をしたうえで、取り扱いの決まりを教えます。</li>
        <li>物理的な措置：個人情報を扱う端末は、画面ロックをかけ、盗難や紛失に備えます。</li>
        <li>技術的な措置：フォームからの送信は暗号化した通信（HTTPS）で行います。名簿と予約の記録は当社の Google Workspace の中に置き、閲覧・編集できる人を代表取締役に限っています。</li>
        <li>外的環境の把握：外国で取り扱う情報は、上の5のとおり、その国の制度を把握したうえで措置を講じています。</li>
      </ul>

      <h2>7. 保存期間</h2>
      <ul>
        <li>お知らせの登録と公開実演会のお申込み：配信を続けている間、保存します。配信を停止された方の情報は、再び送らないための記録と、特定電子メール法に基づく記録として、停止の日から1年を過ぎた後に消去します。</li>
        <li>個別面談のご予約：面談の後、ご相談が続いている間は保存し、最後のご連絡から3年を過ぎた後に消去します。取り消された予約は、取消の日から1年を過ぎた後に消去します。</li>
        <li>お問い合わせ：対応を終えた日から3年を過ぎた後に消去します。</li>
      </ul>

      <h2>8. 開示・訂正・利用停止などのご請求</h2>
      <p>当社が保有するご本人の情報について、利用目的の通知、開示（電磁的記録での提供を含みます）、内容の訂正・追加・削除、利用の停止・消去、第三者への提供の停止、第三者提供の記録の開示をご請求いただけます。</p>
      <ul>
        <li>ご請求の方法：上の1のお問い合わせ先へ、ご登録のメールアドレスからメールでご連絡ください。</li>
        <li>ご本人の確認：ご登録のメールアドレスからの送信で確認します。必要なときは、追加の確認をお願いします。</li>
        <li>代理人によるご請求：委任状をお送りいただきます。</li>
        <li>手数料：いただきません。</li>
        <li>回答の方法：原則としてメールで、遅滞なくお答えします。</li>
      </ul>

      <h2>9. 配信の停止</h2>
      <p>お知らせと公開実演会のご案内は、毎回のメールの末尾にあるリンクから、いつでも停止できます。上の1のお問い合わせ先へメールでご連絡いただいても停止します。面談のご予約は、確認メールにある取消のリンクから取り消せます。</p>

      <h2>10. このサイトの閲覧と、当社が使うほかのサービス</h2>
      <ul>
        <li>当社は、このサイトでアクセス解析を行っていません。閲覧の追跡のための Cookie も使っていません。</li>
        <li>このサイトは GitHub, Inc.（米国）の GitHub Pages で公開しています。GitHub は、セキュリティのため、閲覧者の IP アドレスを記録します（<a href="https://docs.github.com/ja/pages/getting-started-with-github-pages/what-is-github-pages">GitHub の説明</a>）。</li>
        <li>文字の表示に Google Fonts（Google LLC）を使っています。文字のデータを読み込む際に、閲覧者の IP アドレスなどが Google に送られます（<a href="https://fonts.google.com/faq">Google の説明</a>）。</li>
        <li>公開実演会と個別面談には Zoom（Zoom Communications, Inc.・米国）を使います。当社から申込の情報を Zoom に渡すことはありません。Zoom への参加時に同社が取得する情報は、同社のプライバシーポリシーに従って取り扱われます。</li>
        <li>LINE 公式アカウント（LINEヤフー株式会社のサービス）で友だち追加やご相談をいただいた場合、当社は LINE の表示名とメッセージの内容を、同社のサービスの中で取り扱います。</li>
      </ul>
      <p>これらのサービスが取得する情報は、各社のプライバシーポリシーに従って取り扱われます。</p>

      <h2>11. 改定</h2>
      <p>法令の改正や、受付の仕組みの変更に合わせて、このポリシーを改定します。改定したときは、このページで改定日とともに公表します。</p>

      <h2>12. お問い合わせ・苦情の窓口</h2>
      <p>株式会社テンマインド　個人情報のお問い合わせ窓口<br><a href="mailto:eguchi@tenmindinc.com">eguchi@tenmindinc.com</a></p>
      <p style="margin-top:2.4em" class="note">2026年10月8日 制定</p>
    </div></div>
  </section>
</main>
"""

PROFILE = """<main id="main">
  <section class="doc-head">
    <div class="wrap">
      <div class="kicker">Message</div>
      <h1>代表メッセージ</h1>
    </div>
  </section>

  <section>
    <div class="wrap msg">
      <div class="body">
        <h2>決算書の奥にあるものを、<br>会社に残す。</h2>
        <p>地方銀行に29年勤め、営業と融資の両方の現場で、中小企業の社長と向き合ってきました。融資のご相談を受けるとき、私が最後に見ていたのは、決算書の数字の奥にある社長の判断でした。何を大事にし、どんな出来事から学び、どの場面でどう決めてきたのか。それが、その会社の本当の力でした。</p>
        <p>銀行を離れたあと、事業会社にて常務取締役・代表取締役を歴任しました。今度は、自分が決める側です。経営の判断の多くは、どこにも書かれていません。社長の頭の中にだけあり、社長が現場を離れれば、その判断も会社から消えていきます。決める側に立って、そのことを身をもって知りました。</p>
        <p>2023年に、株式会社テンマインドを設立しました。社長の判断を聞き取って言葉にし、社員や後継者が学べる形で、会社に残す。社長の判断が届く範囲を、10倍に広げる。社名の「テン」には、その志を込めています。</p>
        <p>私にとって、AIは大切なパートナーです。私自身もAIエンジニアとしてAIを組み、日々ともに仕事をしています。社長と向き合い、判断を引き出すのは人。その判断を整理して蓄え、社長が不在のときも、代替わりしたあとも、社員や後継者がいつでも尋ねて答えを得られるようにするのはAI。人とAIが手を携えることで、判断は会社の資産になります。銀行員、経営者、そしてAIエンジニア。並べると脈絡のない経歴に見えますが、私の中では「社長をどう支えるか」という一本の線でつながっています。</p>
        <p class="sign"><small>株式会社テンマインド　代表取締役</small><b>江口 尚文</b></p>
      </div>
      __PORTRAIT__
    </div>
  </section>

  <section class="co">
    <div class="wrap">
      <div class="kicker">Career</div>
      <h2>略歴</h2>
      <table class="career">
        <tr><th>学歴</th><td>佐賀大学 経済学部 卒業</td></tr>
        <tr><th>銀行</th><td>地方銀行に29年勤務。営業と融資の両方の現場で、中小企業の社長と向き合う</td></tr>
        <tr><th>経営</th><td>事業会社にて常務取締役・代表取締役を歴任</td></tr>
        <tr><th>2023年10月</th><td>株式会社テンマインドを設立し、代表取締役に就任</td></tr>
        <tr><th>現在</th><td>社長の判断ラボを主宰</td></tr>
        <tr><th>資格・所属</th><td>2級FP技能士／宅地建物取引士／人工知能学会 正会員</td></tr>
      </table>
      <div class="actions">
        <a class="btn" href="/lab/">公開実演会に申し込む（無料）</a>
        <a class="btn btn-ghost" href="/#news">新刊・実演会のお知らせを受け取る</a>
      </div>
    </div>
  </section>
</main>
"""

NOT_FOUND = """<main id="main">
  <section class="thanks">
    <div class="wrap box">
      <div class="kicker">404 Not Found</div>
      <h2>お探しのページが<br>見つかりませんでした</h2>
      <p style="margin-top:1.2em">ページが移動したか、URLが違っている可能性があります。</p>
      <div class="actions">
        <a class="btn" href="/">トップページへ</a>
        <a class="btn btn-ghost" href="/#news">新刊・実演会のお知らせを受け取る</a>
      </div>
      <p style="margin-top:2em;font-family:var(--sans);font-size:14px">公開実演会のお申込みは<a href="/lab/" style="color:var(--green)">こちら</a>です。</p>
    </div>
  </section>
</main>
"""


def page(title, desc, body, path, index=True):
    """path=公開URLのパス（例 /lab/）。index=False で検索に載せない（noindex・canonical なし）"""
    meta = (f'<link rel="canonical" href="{SITE}{path}">\n' if index else '<meta name="robots" content="noindex">\n') + (
        '<meta property="og:type" content="website">\n<meta property="og:site_name" content="株式会社テンマインド">\n'
        f'<meta property="og:locale" content="ja_JP">\n<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{SITE}{path}">\n') + head_common
    h = (HEAD.replace("__TITLE__", title).replace("__DESC__", desc).replace("__META__", meta)
         .replace("__STYLE__", style + EXTRA_CSS))
    return h + header + "\n" + body + "\n" + footer + "\n</body>\n</html>\n"


for d in ["lab/thanks", "lab/booking", "profile", "privacy"]:
    (ROOT / d).mkdir(parents=True, exist_ok=True)
(ROOT / "lab" / "index.html").write_text(page(
    "社長の判断ラボ 公開実演会 第1回｜株式会社テンマインド",
    "社長の判断を、1枚のカードにする60分。2026年11月18日（水）20:00〜21:00、Zoom・無料。",
    LAB.replace("__GAS_URL__", GAS_URL), "/lab/"))
(ROOT / "lab" / "thanks" / "index.html").write_text(page(
    "お申込みありがとうございます｜社長の判断ラボ", "お申込みを受け付けました。", THANKS, "/lab/thanks/", index=False))
(ROOT / "lab" / "booking" / "index.html").write_text(page(
    "個別面談のご予約｜社長の判断ラボ", "30分で、御社の判断を1枚のカードに。個別面談（無料・オンライン）のご予約。",
    BOOKING.replace("__GAS_URL__", GAS_URL), "/lab/booking/", index=False))
(ROOT / "profile" / "index.html").write_text(page(
    "代表メッセージ｜株式会社テンマインド",
    "株式会社テンマインド 代表取締役 江口尚文のメッセージと略歴。地方銀行で29年、営業と融資の現場で中小企業の社長と向き合い、事業会社にて常務取締役・代表取締役を歴任。",
    PROFILE.replace("__PORTRAIT__", portrait.replace('loading="lazy"', 'loading="eager" fetchpriority="high"')), "/profile/"))
(ROOT / "privacy" / "index.html").write_text(page(
    "プライバシーポリシー｜株式会社テンマインド",
    "株式会社テンマインドが、このサイトのお申込み・ご登録・お問い合わせで取得する個人情報の取り扱いを定めます。",
    PRIVACY, "/privacy/"))
(ROOT / "404.html").write_text(page(
    "ページが見つかりません｜株式会社テンマインド", "お探しのページは見つかりませんでした。", NOT_FOUND, "/404.html", index=False))
print("built lab / profile / privacy / 404 pages; endpoint =", GAS_URL)
