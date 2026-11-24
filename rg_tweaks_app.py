from flask import Flask, request, render_template_string, Response, session
import random
import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "RG_TWEAKS_SECRET_KEY_2026")

TICKET = None
ADMIN_PASSWORD = "RG2026"
ACTIVE_DOWNLOAD_TOKEN = None
TICKET_DELETED_MSG = False

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>RG TWEAKS PRO — باقة المحترفين (20 دينار ليبي)</title>
  <style>
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: Tahoma, Arial, sans-serif;
      background-color: #070812;
      background-image:
        radial-gradient(circle at 50% 18%, rgba(124, 58, 237, 0.24), transparent 52%),
        radial-gradient(circle at 80% 45%, rgba(56, 189, 248, 0.12), transparent 45%),
        linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 44px 44px, 44px 44px;
      color: #f8fafc;
      line-height: 1.7;
    }
    a { color: inherit; text-decoration: none; }

    .navbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 36px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
      background: rgba(7, 8, 18, 0.78);
      backdrop-filter: blur(10px);
      position: sticky;
      top: 0;
      z-index: 20;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      text-align: right;
    }
    .brand-icon {
      width: 34px;
      height: 34px;
      border-radius: 9px;
      background: linear-gradient(135deg, #7c3aed, #38bdf8);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 17px;
      color: #fff;
    }
    .brand-title { font-weight: bold; font-size: 16px; letter-spacing: 0.5px; }
    .brand-sub { font-size: 11px; color: #94a3b8; }
    .nav-links { display: flex; gap: 22px; font-size: 14px; color: #cbd5e1; }
    .nav-links a:hover { color: #fff; }
    .nav-cta {
      background: linear-gradient(90deg, #8b5cf6, #7c3aed);
      color: #fff;
      padding: 9px 18px;
      border-radius: 9px;
      font-size: 13px;
      font-weight: bold;
      box-shadow: 0 0 20px rgba(139, 92, 246, 0.35);
    }

    .hero {
      max-width: 980px;
      margin: 46px auto 24px;
      padding: 0 20px;
      text-align: center;
    }
    .badge {
      display: inline-block;
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 12px;
      color: #ddd6fe;
      background: rgba(124, 58, 237, 0.16);
      border: 1px solid rgba(167, 139, 250, 0.35);
      margin-bottom: 18px;
    }
    .hero h1 {
      margin: 0 auto 14px;
      font-size: 44px;
      line-height: 1.25;
      font-weight: 800;
    }
    .hero h1 span {
      display: block;
      background: linear-gradient(90deg, #c084fc, #60a5fa, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-size: 48px;
      margin-top: 4px;
    }
    .hero p {
      max-width: 690px;
      margin: 0 auto 28px;
      color: #94a3b8;
      font-size: 15px;
    }
    .hero-actions {
      display: flex;
      justify-content: center;
      gap: 14px;
      flex-wrap: wrap;
      margin-bottom: 38px;
    }
    .btn-primary {
      background: linear-gradient(90deg, #8b5cf6, #6366f1);
      color: #fff;
      padding: 12px 24px;
      border-radius: 10px;
      font-weight: bold;
      font-size: 14px;
      border: none;
      cursor: pointer;
      box-shadow: 0 0 24px rgba(139, 92, 246, 0.4);
    }
    .btn-secondary {
      background: rgba(15, 23, 42, 0.85);
      color: #e2e8f0;
      padding: 12px 22px;
      border-radius: 10px;
      font-weight: bold;
      font-size: 14px;
      border: 1px solid rgba(255, 255, 255, 0.14);
      cursor: pointer;
    }

    .stats {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-bottom: 34px;
    }
    .stat-card {
      background: rgba(15, 18, 34, 0.82);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 16px 14px;
      text-align: center;
    }
    .stat-val { font-size: 22px; font-weight: 800; color: #a78bfa; }
    .stat-val.cyan { color: #38bdf8; }
    .stat-lbl { font-size: 12px; color: #94a3b8; margin-top: 4px; }

    .container {
      max-width: 860px;
      margin: 0 auto 48px;
      padding: 0 16px;
    }
    .box {
      background: rgba(15, 18, 34, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 14px;
      padding: 22px;
      margin-bottom: 20px;
    }
    .box h2, .box h3 { margin-top: 0; }
    .features-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-top: 12px;
    }
    .feat-item {
      background: rgba(7, 8, 18, 0.72);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 14px;
      color: #e2e8f0;
    }
    label { display: block; font-size: 14px; color: #cbd5e1; margin-top: 8px; }
    input, textarea {
      width: 100%;
      padding: 10px 12px;
      margin: 6px 0 12px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.14);
      background: #080a16;
      color: #fff;
      font-family: inherit;
    }
    button.action-btn {
      padding: 10px 18px;
      border: none;
      border-radius: 8px;
      background: linear-gradient(90deg, #8b5cf6, #6366f1);
      color: #fff;
      font-weight: bold;
      cursor: pointer;
    }
    button.approve-btn {
      padding: 10px 18px;
      border: none;
      border-radius: 8px;
      background: #16a34a;
      color: #fff;
      font-weight: bold;
      cursor: pointer;
    }
    button.logout-btn {
      padding: 8px 14px;
      border: 1px solid rgba(255,255,255,0.18);
      border-radius: 8px;
      background: transparent;
      color: #e2e8f0;
      font-weight: bold;
      cursor: pointer;
      margin-right: 8px;
    }
    .notice-ok {
      background: rgba(34, 197, 94, 0.14);
      border: 1px solid #22c55e;
      color: #bbf7d0;
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 12px;
      font-size: 14px;
    }
    .notice-err {
      background: rgba(239, 68, 68, 0.14);
      border: 1px solid #ef4444;
      color: #fecaca;
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 12px;
      font-size: 14px;
    }
    .msg {
      background: #080a16;
      border-right: 3px solid #8b5cf6;
      padding: 9px 13px;
      margin-bottom: 8px;
      border-radius: 8px;
      font-size: 14px;
    }
    .dl {
      background: rgba(22, 163, 74, 0.12);
      border: 1px solid #22c55e;
      padding: 16px;
      border-radius: 10px;
      margin-top: 14px;
    }
    a.dl-btn {
      display: inline-block;
      background: #22c55e;
      color: #052e16;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: bold;
      margin-top: 8px;
      margin-left: 8px;
    }
    @media (max-width: 720px) {
      .stats { grid-template-columns: repeat(2, 1fr); }
      .features-grid { grid-template-columns: 1fr; }
      .nav-links { display: none; }
      .hero h1, .hero h1 span { font-size: 32px; }
    }
  </style>
</head>
<body>
  <nav class="navbar">
    <div class="brand">
      <div class="brand-icon">⚡</div>
      <div>
        <div class="brand-title">RG TWEAKS</div>
        <div class="brand-sub">باقة المحترفين • 20 دينار ليبي</div>
      </div>
    </div>
    <div class="nav-links">
      <a href="#features">المميزات</a>
      <a href="#package">باقة المحترفين (20 د.ل)</a>
      <a href="#ticket">فتح تذكرة</a>
      <a href="#admin">الإدارة</a>
    </div>
    <a class="nav-cta" href="#ticket">اطلب باقة 20 د.ل</a>
  </nav>

  <section class="hero">
    <div class="badge">الإصدار الكامل RG TWEAKS PRO v4.2 • سعر موحد 20 دينار ليبي مدى الحياة</div>
    <h1>
      ارفع أداء جهازك لأقصى حد مع
      <span>RG TWEAKS PRO</span>
    </h1>
    <p>
      تخلص من التقطيع (Stuttering)، ارفع الفريمات (FPS) إلى أقصى حد ممكن، وقلل البينق وصفر تأخير الاستجابة (Zero Input Delay) بضغطة زر واحدة عبر برنامج التويك الخاص بباقة المحترفين.
    </p>
    <div class="hero-actions">
      <a class="btn-primary" href="#ticket">⚡ باقة المحترفين • 20 د.ل</a>
      <a class="btn-secondary" href="#ticket">🎫 افتح تذكرة شراء</a>
    </div>

    <div class="stats">
      <div class="stat-card">
        <div class="stat-val cyan">45%+</div>
        <div class="stat-lbl">زيادة في استقرار الفريمات</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">0.1ms</div>
        <div class="stat-lbl">تقليل تأخير الماوس والكيبورد</div>
      </div>
      <div class="stat-card">
        <div class="stat-val cyan">Restore</div>
        <div class="stat-lbl">نقطة استعادة تلقائية آمنة</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">20 د.ل</div>
        <div class="stat-lbl">باقة واحدة شاملة مدى الحياة</div>
      </div>
    </div>
  </section>

  <div class="container">
    <div class="box" id="features">
      <h2>مميزات باقة المحترفين — Pro Gaming Tweak (20 دينار ليبي)</h2>
      <div class="features-grid">
        <div class="feat-item">• تنظيف الملفات المؤقتة وملفات الكراش للألعاب والنظام.</div>
        <div class="feat-item">• زيادة استقرار الفريمات وتفعيل خطة الطاقة القصوى.</div>
        <div class="feat-item">• تقليل تأخير الكيبورد والماوس وتحسين البينغ.</div>
        <div class="feat-item">• إنشاء نقطة استعادة تلقائية آمنة قبل تطبيق التعديلات.</div>
      </div>
    </div>

    <div class="box" id="ticket">
      <h2>فتح تذكرة شراء</h2>

      {% if ticket_deleted_msg %}
        <div class="notice-ok">تم حذف التذكرة بنجاح.</div>
      {% endif %}

      <form method="post" action="/create_ticket">
        <label>حساب الديسكورد:</label>
        <input type="text" name="discord" required placeholder="مثال: flex_rg" />
        <label>ملاحظة:</label>
        <textarea name="note" rows="2" placeholder="أي ملاحظة إضافية..."></textarea>
        <button class="action-btn" type="submit">فتح التذكرة</button>
      </form>

      {% if ticket %}
        <hr style="margin: 18px 0; border-color: rgba(255,255,255,0.1);" />
        <h3>تذكرة رقم: {{ ticket.id }} — {{ ticket.discord }}</h3>
        <p>الحالة: {{ "مفعّل (يمكن التحميل من الأسفل)" if ticket.approved else "بانتظار تأكيد الدفع من الإدارة" }}</p>

        {% for m in ticket.messages %}
          <div class="msg"><strong>{{ m.sender }}:</strong> {{ m.text }}</div>
        {% endfor %}

        <form method="post" action="/send_message">
          <input type="text" name="text" placeholder="اكتب رسالة داخل التذكرة (اكتب: تم لحذف التذكرة)..." required />
          <button class="action-btn" type="submit">إرسال رسالة</button>
        </form>

        {% if ticket.approved and download_url %}
          <div class="dl">
            <h3>تم تفعيل التذكرة — برنامج التويك جاهز</h3>
            <p>حمّل ملف <strong>RG_TWEAKS_PRO.bat</strong> وشغّله كمسؤول (Run as administrator) مباشرة بدون إدخال أي رمز.</p>
            <a class="dl-btn" href="{{ download_url }}">تحميل برنامج التويك (RG_TWEAKS_PRO.bat)</a>
          </div>
        {% endif %}
      {% endif %}
    </div>

    <div class="box" id="admin">
      <h2>دخول الإدارة</h2>

      {% if admin_error %}
        <div class="notice-err">كلمة المرور غير صحيحة.</div>
      {% endif %}

      {% if admin_logged_in %}
        <div class="notice-ok">تم تسجيل الدخول كإدارة بنجاح.</div>

        {% if ticket %}
          <form method="post" action="/approve_ticket" style="display: inline-block;">
            <button class="approve-btn" type="submit">تفعيل زر تحميل العميل</button>
          </form>
        {% endif %}

        {% if download_url %}
          <a class="dl-btn" href="{{ download_url }}">تنزيل للعميل (RG_TWEAKS_PRO.bat)</a>
        {% endif %}

        <form method="post" action="/logout_admin" style="display: inline-block;">
          <button class="logout-btn" type="submit">تسجيل خروج الإدارة</button>
        </form>
      {% else %}
        <form method="post" action="/login_admin">
          <input type="password" name="password" placeholder="أدخل كلمة المرور" required />
          <button class="action-btn" type="submit">دخول الإدارة</button>
        </form>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

def _get_current_download_url():
    if not TICKET or not TICKET.get("approved") or not ACTIVE_DOWNLOAD_TOKEN:
        return None
    if session.get("client_download_token") == ACTIVE_DOWNLOAD_TOKEN or session.get("admin_logged_in"):
        return f"/download_tweak?token={ACTIVE_DOWNLOAD_TOKEN}"
    return None

@app.route("/")
def home():
    global TICKET_DELETED_MSG
    admin_error = session.pop("admin_error", False)
    deleted_notice = TICKET_DELETED_MSG
    TICKET_DELETED_MSG = False
    return render_template_string(
        HTML_PAGE,
        ticket=TICKET,
        admin_logged_in=bool(session.get("admin_logged_in")),
        admin_error=admin_error,
        download_url=_get_current_download_url(),
        ticket_deleted_msg=deleted_notice
    )

@app.route("/create_ticket", methods=["POST"])
def create_ticket():
    global TICKET, ACTIVE_DOWNLOAD_TOKEN, TICKET_DELETED_MSG
    TICKET_DELETED_MSG = False
    ACTIVE_DOWNLOAD_TOKEN = None
    session.pop("client_download_token", None)

    discord = request.form.get("discord", "").strip()
    note = request.form.get("note", "").strip()
    if discord:
        TICKET = {
            "id": f"RG-{random.randint(1000, 9999)}",
            "discord": discord,
            "approved": False,
            "messages": [
                {"sender": f"العميل ({discord})", "text": f"أريد شراء باقة المحترفين (20 دينار ليبي). {note}".strip()},
                {"sender": "النظام", "text": "تم فتح التذكرة. بانتظار تأكيد الدفع من الإدارة."}
            ]
        }
    return render_template_string(
        HTML_PAGE,
        ticket=TICKET,
        admin_logged_in=bool(session.get("admin_logged_in")),
        admin_error=False,
        download_url=_get_current_download_url(),
        ticket_deleted_msg=False
    )

@app.route("/send_message", methods=["POST"])
def send_message():
    global TICKET, ACTIVE_DOWNLOAD_TOKEN, TICKET_DELETED_MSG
    text = request.form.get("text", "").strip()
    is_admin = bool(session.get("admin_logged_in"))

    if TICKET and text:
        if text == "تم":
            TICKET = None
            ACTIVE_DOWNLOAD_TOKEN = None
            session.pop("client_download_token", None)
            TICKET_DELETED_MSG = True
            return render_template_string(
                HTML_PAGE,
                ticket=None,
                admin_logged_in=is_admin,
                admin_error=False,
                download_url=None,
                ticket_deleted_msg=True
            )

        sender = "الإدارة (RG TWEAKS)" if is_admin else f"العميل ({TICKET['discord']})"
        TICKET["messages"].append({"sender": sender, "text": text})

    return render_template_string(
        HTML_PAGE,
        ticket=TICKET,
        admin_logged_in=is_admin,
        admin_error=False,
        download_url=_get_current_download_url(),
        ticket_deleted_msg=False
    )

@app.route("/login_admin", methods=["POST"])
def login_admin():
    pwd = request.form.get("password", "").strip()
    if pwd == ADMIN_PASSWORD:
        session["admin_logged_in"] = True
        session["admin_error"] = False
    else:
        session["admin_logged_in"] = False
        session["admin_error"] = True
    return render_template_string(
        HTML_PAGE,
        ticket=TICKET,
        admin_logged_in=bool(session.get("admin_logged_in")),
        admin_error=session.pop("admin_error", False),
        download_url=_get_current_download_url(),
        ticket_deleted_msg=False
    )

@app.route("/logout_admin", methods=["POST"])
def logout_admin():
    session["admin_logged_in"] = False
    return render_template_string(
        HTML_PAGE,
        ticket=TICKET,
        admin_logged_in=False,
        admin_error=False,
        download_url=_get_current_download_url(),
        ticket_deleted_msg=False
    )

@app.route("/approve_ticket", methods=["POST"])
def approve_ticket():
    global ACTIVE_DOWNLOAD_TOKEN
    if not session.get("admin_logged_in"):
        return "غير مصرح لك بتنفيذ هذا الإجراء.", 403
    if TICKET:
        ACTIVE_DOWNLOAD_TOKEN = secrets.token_urlsafe(16)
        session["client_download_token"] = ACTIVE_DOWNLOAD_TOKEN
        TICKET["approved"] = True
        TICKET["messages"].append({
            "sender": "الإدارة (RG TWEAKS)",
            "text": "تم تأكيد الدفع وتفعيل تحميل برنامج التويك في أسفل التذكرة."
        })
    return render_template_string(
        HTML_PAGE,
        ticket=TICKET,
        admin_logged_in=True,
        admin_error=False,
        download_url=_get_current_download_url(),
        ticket_deleted_msg=False
    )

@app.route("/download_tweak")
def download_tweak():
    token = request.args.get("token", "").strip()
    is_admin = bool(session.get("admin_logged_in"))
    client_token = session.get("client_download_token")

    if not TICKET or not TICKET.get("approved") or not ACTIVE_DOWNLOAD_TOKEN:
        return "التحميل غير مفعّل أو تم حذف التذكرة.", 403

    if not token or token != ACTIVE_DOWNLOAD_TOKEN:
        return "رمز التحميل غير صالح أو منتهي.", 403

    if not is_admin and client_token != ACTIVE_DOWNLOAD_TOKEN:
        return "هذا الرابط مقيّد بالجلسة المفعّلة للعميل ولا يمكن استخدامه من جلسة أخرى.", 403

    ticket_code = TICKET["id"]
    bat_lines = [
        "@echo off",
        "title RG TWEAKS - Pro Gaming Tweak (20 LYD)",
        "color 0B",
        "cls",
        "echo ================================================",
        "echo        RG TWEAKS - PRO GAMING TWEAK",
        f"echo        Ticket: {ticket_code}",
        "echo ================================================",
        "echo.",
        "echo [1/6] Creating System Restore Point before applying tweaks...",
        "powershell -Command \"Enable-ComputerRestore -Drive 'C:\\' -ErrorAction SilentlyContinue; Checkpoint-Computer -Description 'RG_TWEAKS_Restore' -RestorePointType 'MODIFY_SETTINGS'\" >nul 2>&1",
        "echo [2/6] Cleaning Temp and Crash Dump files (System and Games)...",
        "del /s /f /q \"%temp%\\*.*\" >nul 2>&1",
        "del /s /f /q \"C:\\Windows\\Temp\\*.*\" >nul 2>&1",
        "del /s /f /q \"C:\\Windows\\Minidump\\*.*\" >nul 2>&1",
        "del /f /q \"C:\\Windows\\MEMORY.DMP\" >nul 2>&1",
        "del /s /f /q \"C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportArchive\\*.*\" >nul 2>&1",
        "del /s /f /q \"C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportQueue\\*.*\" >nul 2>&1",
        "for /d %%D in (\"%localappdata%\\*Crash*\" \"%localappdata%\\*Dump*\" \"%localappdata%\\CrashReportClient*\") do (",
        "  if exist \"%%D\" rmdir /s /q \"%%D\" >nul 2>&1",
        ")",
        "echo [3/6] Boosting frame stability (High Performance and Game Mode)...",
        "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c >nul 2>&1",
        "reg add \"HKCU\\Software\\Microsoft\\GameBar\" /v AllowAutoGameMode /t REG_DWORD /d 1 /f >nul 2>&1",
        "reg add \"HKCU\\Software\\Microsoft\\GameBar\" /v AutoGameModeEnabled /t REG_DWORD /d 1 /f >nul 2>&1",
        "echo [4/6] Reducing keyboard and mouse latency...",
        "reg add \"HKCU\\Control Panel\\Mouse\" /v MouseHoverTime /t REG_SZ /d \"10\" /f >nul 2>&1",
        "reg add \"HKCU\\Control Panel\\Keyboard\" /v KeyboardDelay /t REG_SZ /d \"0\" /f >nul 2>&1",
        "reg add \"HKCU\\Control Panel\\Keyboard\" /v KeyboardSpeed /t REG_SZ /d \"31\" /f >nul 2>&1",
        "echo [5/6] Improving ping and network stack...",
        "netsh int tcp set global autotuninglevel=normal >nul 2>&1",
        "netsh int tcp set global ecncapability=disabled >nul 2>&1",
        "ipconfig /flushdns >nul 2>&1",
        "echo [6/6] Finalizing...",
        "echo.",
        "echo Done! Please restart your PC for best results.",
        "pause"
    ]
    bat_script = "\r\n".join(bat_lines)
    return Response(
        bat_script,
        mimetype="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=RG_TWEAKS_PRO.bat"}
    )

if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    app.run(host=host, port=port, debug=False)