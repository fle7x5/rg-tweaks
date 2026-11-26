import os
import secrets
from flask import Flask, request, render_template_string, Response, session

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "RG_TWEAKS_SECRET_KEY_2026")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "RG2026")

# تخزين التذاكر حسب معرّف التذكرة (يمكن استبداله بقاعدة بيانات للاستمرارية الدائمة)
TICKETS = {}

# محتوى ملف RG_TWEAKS_PRO.bat المطور مع نقطة استعادة تلقائية في البداية
BAT_SCRIPT_CONTENT = """@echo off\r
title RG TWEAKS PRO MAX - Performance & Bloatware Cleaner\r
color 0A\r
\r
net session >nul 2>&1\r
if %errorLevel% neq 0 (\r
    echo [!] Please run this file as Administrator (Run as administrator).\r
    pause\r
    exit /b 1\r
)\r
\r
echo ==========================================================\r
echo       RG TWEAKS PRO MAX - ACTIVATED SUCCESSFULLY\r
echo ==========================================================\r
echo.\r
echo [0/5] Creating a System Restore Point...\r
powershell -NoProfile -Command "Enable-ComputerRestore -Drive 'C:\\' -ErrorAction SilentlyContinue; Checkpoint-Computer -Description 'RG Tweaks Pro Restore Point' -RestorePointType 'MODIFY_SETTINGS' -ErrorAction SilentlyContinue" >nul 2>&1\r
\r
echo [1/5] Setting High Performance power plan...\r
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c >nul 2>&1\r
powercfg /change monitor-timeout-ac 0 >nul 2>&1\r
powercfg /change standby-timeout-ac 0 >nul 2>&1\r
\r
echo [2/5] Stopping non-essential background services...\r
for %%S in (\r
    "DiagTrack"\r
    "dmwappushservice"\r
    "SysMain"\r
    "WSearch"\r
    "Fax"\r
    "MapsBroker"\r
    "RetailDemo"\r
    "XblAuthManager"\r
    "XblGameSave"\r
    "XboxNetApiSvc"\r
) do (\r
    sc stop %%~S >nul 2>&1\r
    sc config %%~S start= disabled >nul 2>&1\r
)\r
\r
echo [3/5] Removing unused built-in Windows apps (keeping personal apps)...\r
for %%A in (\r
    "Microsoft.549981C3F5F10"\r
    "Microsoft.BingNews"\r
    "Microsoft.BingWeather"\r
    "Microsoft.Clipchamp.Clipchamp"\r
    "Microsoft.GetHelp"\r
    "Microsoft.Getstarted"\r
    "Microsoft.MicrosoftSolitaireCollection"\r
    "Microsoft.People"\r
    "Microsoft.PowerAutomateDesktop"\r
    "Microsoft.Todos"\r
    "Microsoft.YourPhone"\r
    "Microsoft.ZuneMusic"\r
    "Microsoft.ZuneVideo"\r
    "Microsoft.GamingApp"\r
    "Microsoft.Xbox.TCUI"\r
    "Microsoft.XboxGameOverlay"\r
    "Microsoft.XboxGamingOverlay"\r
    "Microsoft.XboxIdentityProvider"\r
    "Microsoft.XboxSpeechToTextOverlay"\r
) do (\r
    powershell -NoProfile -Command "Get-AppxPackage -AllUsers *%%~A* | Remove-AppxPackage -AllUsers -ErrorAction SilentlyContinue; Get-AppXProvisionedPackage -Online | Where-Object {$_.DisplayName -like '*%%~A*'} | Remove-AppXProvisionedPackage -Online -ErrorAction SilentlyContinue" >nul 2>&1\r
)\r
\r
echo [4/5] Attempting to remove Microsoft Edge...\r
winget uninstall --id Microsoft.Edge --silent --accept-source-agreements >nul 2>&1\r
winget uninstall --id Microsoft.EdgeWebView2Runtime --silent --accept-source-agreements >nul 2>&1\r
for /f "delims=" %%I in ('reg query "HKLM\\SOFTWARE\\WOW6432Node\\Microsoft\\EdgeUpdate\\Clients" 2^>nul ^| findstr /i "{"') do (\r
    for /f "tokens=2*" %%V in ('reg query "%%I\\Commands\\uninstall" /v Command 2^>nul ^| findstr /i "Command"') do (\r
        cmd /c "%%W --force-uninstall" >nul 2>&1\r
    )\r
)\r
\r
echo [5/5] Flushing DNS, Winsock and clearing temporary files...\r
ipconfig /flushdns >nul 2>&1\r
netsh winsock reset >nul 2>&1\r
del /q /f /s "%temp%\\*" >nul 2>&1\r
\r
echo.\r
echo [OK] Completed! Restart your PC to apply all changes cleanly.\r
pause\r
"""

HTML_PAGE = """<!DOCTYPE html>
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
      color: #f3f4f6;
      line-height: 1.6;
    }
    .container {
      max-width: 960px;
      margin: 0 auto;
      padding: 24px 16px 60px;
    }
    .hero {
      background: linear-gradient(135deg, #11152b, #1b1235);
      border: 1px solid #2b2f55;
      border-radius: 16px;
      padding: 28px 22px;
      text-align: center;
      margin-bottom: 24px;
    }
    .badge {
      display: inline-block;
      background: #2563eb;
      color: #fff;
      padding: 4px 12px;
      border-radius: 999px;
      font-size: 13px;
      margin-bottom: 10px;
    }
    h1 { margin: 6px 0 10px; font-size: 28px; }
    .price { font-size: 22px; color: #38bdf8; font-weight: bold; margin-bottom: 16px; }
    .btn {
      display: inline-block;
      background: #2563eb;
      color: #fff;
      border: none;
      padding: 11px 18px;
      border-radius: 10px;
      font-size: 14px;
      font-weight: bold;
      cursor: pointer;
      text-decoration: none;
      margin: 4px;
    }
    .btn:hover { background: #1d4ed8; }
    .btn-green { background: #16a34a; }
    .btn-green:hover { background: #15803d; }
    .btn-red { background: #dc2626; }
    .btn-red:hover { background: #b91c1c; }
    .btn-gray { background: #374151; }
    .btn-gray:hover { background: #4b5563; }
    .card {
      background: #0e1120;
      border: 1px solid #1f2544;
      border-radius: 14px;
      padding: 20px;
      margin-bottom: 20px;
    }
    h2 { margin-top: 0; font-size: 20px; color: #e2e8f0; }
    input, textarea {
      width: 100%;
      padding: 11px 12px;
      margin: 8px 0 14px;
      border-radius: 10px;
      border: 1px solid #2a3158;
      background: #070812;
      color: #fff;
      font-family: inherit;
      font-size: 14px;
    }
    .ticket-box {
      background: #13182e;
      border: 1px solid #2a325c;
      border-radius: 12px;
      padding: 16px;
      margin-top: 12px;
    }
    .status-pending { color: #facc15; font-weight: bold; }
    .status-approved { color: #4ade80; font-weight: bold; }
    .msg-item {
      background: #0a0d1a;
      border-right: 3px solid #38bdf8;
      padding: 8px 12px;
      margin: 6px 0;
      border-radius: 6px;
      font-size: 14px;
    }
    .alert {
      padding: 12px 14px;
      border-radius: 10px;
      margin-bottom: 16px;
      font-size: 14px;
    }
    .alert-info { background: #172554; border: 1px solid #2563eb; color: #dbeafe; }
    .alert-success { background: #052e16; border: 1px solid #16a34a; color: #dcfce7; }
    .alert-danger { background: #450a0a; border: 1px solid #dc2626; color: #fee2e2; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
    .muted { color: #94a3b8; font-size: 13px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <div class="badge">RG TWEAKS PRO</div>
      <h1>باقة المحترفين — تحسين الأداء والاستقرار</h1>
      <div class="price">السعر: 20 دينار ليبي (20 LYD)</div>
      <p class="muted">افتح تذكرة شراء، أتمّ الدفع، اكتب «تم»، وبعد مراجعة الأدمن يظهر لك زر تحميل ملف RG_TWEAKS_PRO.bat</p>
      <a href="#ticket-section" class="btn">فتح تذكرة جديدة</a>
      <a href="#admin-section" class="btn btn-gray">دخول الأدمن</a>
    </div>

    {% if notice %}
      <div class="alert alert-{{ notice_type or 'info' }}">{{ notice }}</div>
    {% endif %}

    <div class="grid-2">
      <!-- قسم فتح تذكرة للعميل -->
      <div class="card" id="ticket-section">
        <h2>1. فتح تذكرة شراء جديدة</h2>
        <form method="POST" action="/create_ticket">
          <label>اسم العميل أو حسابه:</label>
          <input type="text" name="customer_name" placeholder="مثال: Flex RG" required />

          <label>ملاحظة أو طريقة الدفع:</label>
          <textarea name="note" rows="3" placeholder="مثال: أريد شراء باقة المحترفين 20 د.ل" required></textarea>

          <button type="submit" class="btn">إرسال التذكرة</button>
        </form>
      </div>

      <!-- قسم دخول الأدمن -->
      <div class="card" id="admin-section">
        <h2>2. لوحة إدارة الأدمن</h2>
        {% if is_admin %}
          <div class="alert alert-success">أنت مسجل دخول كأدمن الآن. يمكنك مشاهدة جميع التذاكر واعتمادها أو حذفها.</div>
          <form method="POST" action="/admin_logout" style="display:inline;">
            <button type="submit" class="btn btn-gray">تسجيل خروج الأدمن</button>
          </form>
        {% else %}
          <p class="muted">أدخل كلمة مرور الأدمن لعرض جميع التذاكر وإدارتها.</p>
          <form method="POST" action="/admin_login">
            <label>كلمة مرور الأدمن:</label>
            <input type="password" name="password" placeholder="أدخل كلمة المرور" required />
            <button type="submit" class="btn btn-gray">دخول الأدمن</button>
          </form>
        {% endif %}
      </div>
    </div>

    <!-- عرض التذاكر: للمستخدم يرى تذكرته فقط، وللأدمن يرى الكل -->
    <div class="card">
      {% if is_admin %}
        <h2>جميع التذاكر (عرض الأدمن فقط)</h2>
      {% else %}
        <h2>تذكرتك الخاصة فقط</h2>
      {% endif %}

      {% if tickets %}
        {% for t in tickets %}
          <div class="ticket-box">
            <div><strong>رقم التذكرة:</strong> {{ t.id }} | <strong>العميل:</strong> {{ t.customer_name }}</div>
            <div><strong>السعر:</strong> {{ t.price_lyd }} دينار ليبي</div>
            <div>
              <strong>الحالة:</strong>
              {% if t.status == 'approved' %}
                <span class="status-approved">معتمدة — التحميل مفتوح</span>
              {% else %}
                <span class="status-pending">قيد المراجعة</span>
              {% endif %}
            </div>
            <p><strong>الطلب:</strong> {{ t.note }}</p>

            <div>
              <strong>الرسائل:</strong>
              {% for m in t.messages %}
                <div class="msg-item"><strong>{{ m.sender }}:</strong> {{ m.text }}</div>
              {% endfor %}
            </div>

            <!-- إرسال رسالة من العميل أو الأدمن (مثل كتابة "تم") ولا تحذف التذكرة تلقائياً -->
            <form method="POST" action="/ticket/{{ t.id }}/message" style="margin-top:10px;">
              <input type="text" name="text" placeholder="اكتب (تم) بعد إتمام التحويل أو اكتب رسالة..." required />
              <button type="submit" class="btn">إرسال الرسالة</button>
            </form>

            <!-- زر التحميل يظهر فقط إذا اعتمد الأدمن التذكرة -->
            {% if t.download_unlocked %}
              <div style="margin-top:10px;">
                <a href="/download/{{ t.id }}/{{ t.token }}" class="btn btn-green">تحميل RG_TWEAKS_PRO.bat</a>
              </div>
            {% endif %}

            <!-- أزرار الأدمن فقط: اعتماد التذكرة أو حذفها -->
            {% if is_admin %}
              <div style="margin-top:12px; padding-top:10px; border-top:1px solid #27305c;">
                {% if not t.download_unlocked %}
                  <form method="POST" action="/ticket/{{ t.id }}/approve" style="display:inline;">
                    <button type="submit" class="btn btn-green">اعتماد وفتح التحميل</button>
                  </form>
                {% endif %}
                <form method="POST" action="/ticket/{{ t.id }}/delete" style="display:inline;">
                  <button type="submit" class="btn btn-red">حذف التذكرة</button>
                </form>
              </div>
            {% endif %}
          </div>
        {% endfor %}
      {% else %}
        <p class="muted">
          {% if is_admin %}
            لا توجد أي تذاكر حالياً في النظام.
          {% else %}
            لا توجد لديك تذكرة مفتوحة في هذه الجلسة حالياً. افتح تذكرة جديدة من الأعلى.
          {% endif %}
        </p>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""


def get_session_ticket_ids() -> list[str]:
    ids = session.get("my_ticket_ids", [])
    return ids if isinstance(ids, list) else []


def is_admin_logged_in() -> bool:
    return bool(session.get("is_admin") is True)


def render_main(notice: str | None = None, notice_type: str = "info"):
    admin_mode = is_admin_logged_in()
    if admin_mode:
        visible_tickets = list(TICKETS.values())
    else:
        allowed_ids = set(get_session_ticket_ids())
        visible_tickets = [t for tid, t in TICKETS.items() if tid in allowed_ids]

    return render_template_string(
        HTML_PAGE,
        tickets=visible_tickets,
        is_admin=admin_mode,
        notice=notice,
        notice_type=notice_type,
    )


@app.route("/", methods=["GET"])
def home():
    return render_main()


@app.route("/create_ticket", methods=["POST"])
def create_ticket():
    customer_name = (request.form.get("customer_name") or "").strip()
    note = (request.form.get("note") or "").strip()

    if not customer_name or not note:
        return render_main("يرجى تعبئة الاسم وملاحظة الطلب.", "danger")

    ticket_id = f"RG-{secrets.token_hex(3).upper()}"
    download_token = secrets.token_urlsafe(12)

    TICKETS[ticket_id] = {
        "id": ticket_id,
        "customer_name": customer_name,
        "note": note,
        "price_lyd": 20,
        "status": "pending",
        "download_unlocked": False,
        "token": download_token,
        "messages": [
            {"sender": "النظام", "text": "تم فتح التذكرة بنجاح. يرجى إتمام الدفع ثم كتابة (تم)."}
        ],
    }

    my_ids = get_session_ticket_ids()
    if ticket_id not in my_ids:
        my_ids.append(ticket_id)
    session["my_ticket_ids"] = my_ids

    return render_main(f"تم إنشاء تذكرتك برقم {ticket_id}. هذه التذكرة خاصة بك فقط.", "success")


@app.route("/ticket/<ticket_id>/message", methods=["POST"])
def ticket_message(ticket_id: str):
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        return render_main("التذكرة غير موجودة.", "danger")

    allowed_ids = set(get_session_ticket_ids())
    if not is_admin_logged_in() and ticket_id not in allowed_ids:
        return render_main("غير مسموح لك بالتعديل على تذكرة ليست خاصة بك.", "danger")

    text = (request.form.get("text") or "").strip()
    if not text:
        return render_main("لا يمكن إرسال رسالة فارغة.", "danger")

    sender_label = "الأدمن" if is_admin_logged_in() else ticket["customer_name"]
    ticket["messages"].append({"sender": sender_label, "text": text})

    return render_main("تم إرسال رسالتك وحفظها داخل التذكرة.", "success")


@app.route("/admin_login", methods=["POST"])
def admin_login():
    password = request.form.get("password") or ""
    if secrets.compare_digest(password, ADMIN_PASSWORD):
        session["is_admin"] = True
        return render_main("تم تسجيل دخول الأدمن بنجاح.", "success")
    return render_main("كلمة مرور الأدمن غير صحيحة.", "danger")


@app.route("/admin_logout", methods=["POST"])
def admin_logout():
    session.pop("is_admin", None)
    return render_main("تم تسجيل الخروج من حساب الأدمن.", "info")


@app.route("/ticket/<ticket_id>/approve", methods=["POST"])
def approve_ticket(ticket_id: str):
    if not is_admin_logged_in():
        return render_main("هذا الإجراء متاح للأدمن فقط.", "danger")

    ticket = TICKETS.get(ticket_id)
    if not ticket:
        return render_main("التذكرة غير موجودة.", "danger")

    ticket["status"] = "approved"
    ticket["download_unlocked"] = True
    ticket["messages"].append({"sender": "الأدمن", "text": "تم اعتماد التذكرة وفتح رابط التحميل."})
    return render_main(f"تم اعتماد التذكرة {ticket_id} وفتح التحميل.", "success")


@app.route("/ticket/<ticket_id>/delete", methods=["POST"])
def delete_ticket(ticket_id: str):
    if not is_admin_logged_in():
        return render_main("حذف التذاكر متاح للأدمن فقط.", "danger")

    if ticket_id not in TICKETS:
        return render_main("التذكرة غير موجودة أو تم حذفها مسبقاً.", "danger")

    del TICKETS[ticket_id]
    return render_main(f"تم حذف التذكرة {ticket_id} بنجاح.", "success")


@app.route("/download/<ticket_id>/<token>", methods=["GET"])
def download_bat(ticket_id: str, token: str):
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        return render_main("التذكرة غير موجودة.", "danger")

    allowed_ids = set(get_session_ticket_ids())
    if not is_admin_logged_in() and ticket_id not in allowed_ids:
        return render_main("غير مصرح لك بتحميل هذا الملف.", "danger")

    if not ticket.get("download_unlocked") or not secrets.compare_digest(ticket.get("token", ""), token):
        return render_main("لم يتم اعتماد التذكرة بعد أو الرمز غير صالح.", "danger")

    return Response(
        BAT_SCRIPT_CONTENT,
        mimetype="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=RG_TWEAKS_PRO.bat"},
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
