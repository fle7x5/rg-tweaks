import os
import secrets
from flask import Flask, request, jsonify, session, abort

app = Flask(__name__)

# يقرأ المفتاح الذي أضفته في Render Environment Variables، مع احتياطي للتشغيل المحلي
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-fallback-secret-key")

# كلمة مرور الأدمن (الأفضل وضعها في Environment Variables على Render باسم ADMIN_PASSWORD)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ChangeThisAdminPass123!")

# مخزن مؤقت للتذاكر (يمكن استبداله بملف JSON أو SQLite للاستمرارية بعد السكون)
TICKETS = {}


def get_user_ticket_ids() -> list[str]:
    """إرجاع قائمة معرّفات التذاكر الخاصة بجلسة المستخدم الحالي فقط."""
    ids = session.get("my_ticket_ids", [])
    return ids if isinstance(ids, list) else []


def is_admin() -> bool:
    """التحقق مما إذا كان المستخدم الحالي مسجلاً كأدمن."""
    return bool(session.get("is_admin") is True)


@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")

    if secrets.compare_digest(str(password), ADMIN_PASSWORD):
        session["is_admin"] = True
        return jsonify({"ok": True, "message": "تم تسجيل دخول الأدمن بنجاح"})

    return jsonify({"ok": False, "error": "كلمة المرور غير صحيحة"}), 401


@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("is_admin", None)
    return jsonify({"ok": True, "message": "تم تسجيل الخروج من الأدمن"})


@app.route("/api/tickets", methods=["GET"])
def list_tickets():
    """
    - إذا كان أدمن: يرجع كل التذاكر.
    - إذا كان مستخدماً عادياً: يرجع التذاكر الموجودة في جلسة هذا المستخدم فقط.
    """
    if is_admin():
        return jsonify({
            "role": "admin",
            "tickets": list(TICKETS.values())
        })

    my_ids = set(get_user_ticket_ids())
    user_tickets = [t for tid, t in TICKETS.items() if tid in my_ids]

    return jsonify({
        "role": "user",
        "tickets": user_tickets
    })


@app.route("/api/tickets", methods=["POST"])
def create_ticket():
    """إنشاء تذكرة جديدة وربطها بجلسة المستخدم فقط."""
    data = request.get_json(silent=True) or {}
    customer_name = (data.get("customer_name") or "").strip()
    message = (data.get("message") or "").strip()

    if not customer_name or not message:
        return jsonify({"ok": False, "error": "يرجى إدخال الاسم والرسالة"}), 400

    ticket_id = f"TCK-{secrets.token_hex(4).upper()}"
    ticket = {
        "id": ticket_id,
        "customer_name": customer_name,
        "message": message,
        "price_lyd": 20,
        "status": "pending",       # pending | approved | closed
        "download_unlocked": False,
    }

    TICKETS[ticket_id] = ticket

    # حفظ معرّف التذكرة في جلسة هذا المستخدم فقط
    my_ids = get_user_ticket_ids()
    if ticket_id not in my_ids:
        my_ids.append(ticket_id)
    session["my_ticket_ids"] = my_ids

    return jsonify({"ok": True, "ticket": ticket}), 201


@app.route("/api/tickets/<ticket_id>/message", methods=["POST"])
def add_ticket_message(ticket_id: str):
    """إضافة رد/رسالة (مثل كتابة 'تم') على التذكرة بشرط أن يكون المالك أو الأدمن."""
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        abort(404)

    my_ids = set(get_user_ticket_ids())
    if not is_admin() and ticket_id not in my_ids:
        abort(403)

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"ok": False, "error": "النص فارغ"}), 400

    ticket.setdefault("replies", []).append({
        "by": "admin" if is_admin() else "user",
        "text": text
    })

    # تبقى التذكرة قائمة ولا تُحذف تلقائياً عند كتابة "تم"
    return jsonify({"ok": True, "ticket": ticket})


@app.route("/api/tickets/<ticket_id>/approve", methods=["POST"])
def approve_ticket(ticket_id: str):
    """اعتماد الدفع وفتح التحميل — للأدمن فقط."""
    if not is_admin():
        abort(403)

    ticket = TICKETS.get(ticket_id)
    if not ticket:
        abort(404)

    ticket["status"] = "approved"
    ticket["download_unlocked"] = True
    return jsonify({"ok": True, "ticket": ticket})


@app.route("/api/tickets/<ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id: str):
    """حذف التذكرة — للأدمن فقط."""
    if not is_admin():
        abort(403)

    if ticket_id not in TICKETS:
        abort(404)

    del TICKETS[ticket_id]
    return jsonify({"ok": True, "deleted_id": ticket_id})
