import os, ipaddress, shlex
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.routing import BuildError

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

COURSES = [
    {"slug":"linux", "title":"Linux & Command Line", "department":"ShadowTerminal", "level":"Beginner", "description":"Learn the Linux filesystem, commands, permissions and shell fundamentals.", "lessons":[
        ("Linux fundamentals","Understand distributions, the kernel, shell and terminal."),
        ("Files and directories","Practise pwd, ls, cd, mkdir, touch, cp, mv and rm safely."),
        ("Users and permissions","Learn users, groups, chmod, chown and least privilege."),
        ("Processes and services","Understand processes, signals, system services and resource use."),
        ("Bash scripting","Build scripts with variables, conditions, loops and functions.") ]},
    {"slug":"networking", "title":"Computer Networking", "department":"ShadowNet Simulator", "level":"Beginner", "description":"Build a strong foundation in IP addressing, routing, DNS and network troubleshooting.", "lessons":[
        ("Networking foundations","Learn LAN, WAN, topology, devices and network protocols."),
        ("OSI and TCP/IP","Map common protocols to network layers."),
        ("IPv4 and subnetting","Calculate network addresses, usable hosts and broadcast addresses."),
        ("DNS and DHCP","Understand name resolution and automatic address assignment."),
        ("Routing and switching","Learn routes, switches, VLANs and packet forwarding."),
        ("Network troubleshooting","Use a structured approach to diagnose connectivity issues.") ]},
    {"slug":"cybersecurity", "title":"Cybersecurity Foundations", "department":"ShadowCyber", "level":"Beginner", "description":"Learn defensive security, threat modelling, web security and incident response.", "lessons":[
        ("Security principles","Understand confidentiality, integrity, availability and risk."),
        ("Threat modelling","Identify assets, threats, attack surfaces and mitigations."),
        ("Web application security","Study input validation, access control, sessions and common web risks."),
        ("OWASP Top 10 overview","Learn common web application security weakness categories."),
        ("Incident response","Practise preparation, detection, containment and recovery."),
        ("Security reporting","Write clear findings with impact, evidence and remediation.") ]},
    {"slug":"python", "title":"Python Programming", "department":"ShadowCode", "level":"Beginner", "description":"Learn Python syntax, data structures, functions and practical automation.", "lessons":[
        ("Python basics","Variables, data types, input and output."),
        ("Conditions and loops","Control program flow with if, for and while."),
        ("Functions","Write reusable functions and handle parameters."),
        ("Lists and dictionaries","Work with common Python data structures."),
        ("Files and exceptions","Read files and handle errors safely.") ]},
    {"slug":"web", "title":"Web Development", "department":"ShadowCode", "level":"Beginner", "description":"Build responsive websites with HTML, CSS and JavaScript.", "lessons":[
        ("HTML foundations","Structure accessible web pages."),
        ("CSS styling","Create responsive layouts and reusable design systems."),
        ("JavaScript basics","Add interaction and dynamic behaviour."),
        ("HTTP and APIs","Understand requests, responses, JSON and REST.") ]}
]

CYBER_CHALLENGES = [
    {"id":"headers-01","title":"Read the Security Headers","level":"Beginner","question":"Which HTTP response header helps prevent a page from being embedded in a frame by an untrusted site?","answer":"x-frame-options","hint":"It starts with X-Frame."},
    {"id":"hash-01","title":"Password Storage","level":"Beginner","question":"Should an application store user passwords as plain text or as salted password hashes? Enter the safer choice.","answer":"salted password hashes","hint":"Use a slow, salted password-hashing algorithm."},
    {"id":"access-01","title":"Least Privilege","level":"Beginner","question":"What security principle gives each user only the permissions required for their tasks?","answer":"least privilege","hint":"The answer contains the word privilege."}
]


# ==================== MODELS ====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    lesson_key = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    __table_args__ = (db.UniqueConstraint("user_id","lesson_key"),)

class ChallengeResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    challenge_id = db.Column(db.String(80), nullable=False)
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("user_id","challenge_id"),)


# ==================== HELPERS (MUST BE BEFORE create_app) ====================
def current_user():
    return db.session.get(User, session.get("user_id"))

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Sign in to access your learning dashboard.", "error")
            return redirect(url_for("login"))
        if not current_user():
            session.clear()
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped

def simulate_command(raw):
    """Safe educational simulator. It never invokes an operating-system shell."""
    if not raw.strip():
        return "Type 'help' to see available simulated commands."
    try:
        args = shlex.split(raw)
    except ValueError:
        return "Syntax error. Check your quotation marks."
    if not args:
        return ""
    cmd = args[0]
    catalog = {
        "help": "Available commands: help, pwd, whoami, date, uname, ls, clear, ip, ping, echo, history\nThis is a simulated training terminal. Commands do not run on a real server.",
        "pwd": "/home/student",
        "whoami": "student",
        "date": datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y"),
        "uname": "ShadowNet-Lab Linux 6.x x86_64 (simulated)",
        "ls": "Desktop  Documents  Downloads  labs  projects",
        "clear": "",
        "ip": "Usage: ip addr\neth0: 192.0.2.10/24 (documentation-only training address)",
        "ping": "Simulated ping: 4 packets transmitted, 4 received, 0% packet loss. Training output only.",
        "history": "1  help\n2  pwd\n3  whoami"
    }
    if cmd == "echo":
        return " ".join(args[1:])
    if cmd in catalog:
        if cmd == "uname" and len(args) > 1 and args[1] == "-a":
            return catalog[cmd]
        return catalog[cmd]
    return f"{cmd}: command not found in this training simulator. Type 'help'."


# ==================== APP FACTORY ====================
def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-development-only-change-me")
    db_url = os.environ.get("DATABASE_URL", "sqlite:///shadownet.db")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.environ.get("COOKIE_SECURE", "0") == "1"
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    @app.context_processor
    def inject_globals():
        return {
            "site_name": "ShadowNet",
            "site_version": "9.0",
            "current_year": datetime.now().year,
            "csrf_token": generate_csrf,
        }

    # -------- BuildError handler (prints the real culprit) --------
    @app.errorhandler(BuildError)
    def handle_build_error(e):
        import traceback
        traceback.print_exc()
        return f"URL build error: {e}", 500

    # ---------------- ROUTES ----------------
    @app.route("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("dashboard"))
        return render_template("index.html", courses=COURSES)

    @app.route("/register", methods=["GET","POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username","").strip()
            email = request.form.get("email","").strip().lower()
            password = request.form.get("password","")
            if len(username) < 3 or len(password) < 10 or "@" not in email:
                flash("Use a username of at least 3 characters, a valid email and a password of at least 10 characters.", "error")
            elif User.query.filter((User.username == username) | (User.email == email)).first():
                flash("That username or email is already registered.", "error")
            else:
                user = User(username=username, email=email, password_hash=generate_password_hash(password))
                db.session.add(user); db.session.commit()
                session.clear(); session["user_id"] = user.id
                flash("Your ShadowNet account is ready.", "success")
                return redirect(url_for("dashboard"))
        return render_template("auth.html", mode="register")

    @app.route("/login", methods=["GET","POST"])
    def login():
        if request.method == "POST":
            identity = request.form.get("identity","").strip().lower()
            password = request.form.get("password","")
            user = User.query.filter(db.or_(db.func.lower(User.username) == identity, User.email == identity)).first()
            if user and check_password_hash(user.password_hash, password):
                session.clear(); session["user_id"] = user.id
                user.last_login = datetime.now(timezone.utc); db.session.commit()
                return redirect(url_for("dashboard"))
            flash("Invalid username/email or password.", "error")
        return render_template("auth.html", mode="login")

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        session.clear()
        return redirect(url_for("index"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        user = current_user()
        completed = Progress.query.filter_by(user_id=user.id, completed=True).count()
        return render_template("dashboard.html", user=user, courses=COURSES, completed=completed)

    @app.route("/academy")
    @login_required
    def academy():
        return render_template("academy.html", courses=COURSES)

    @app.route("/course/<slug>")
    @login_required
    def course(slug):
        item = next((c for c in COURSES if c["slug"] == slug), None)
        if not item:
            return render_template("404.html"), 404
        progress = {p.lesson_key for p in Progress.query.filter_by(user_id=session["user_id"], completed=True).all()}
        return render_template("course.html", course=item, progress=progress)

    @app.route("/lesson/<slug>/<int:number>", methods=["GET","POST"])
    @login_required
    def lesson(slug, number):
        item = next((c for c in COURSES if c["slug"] == slug), None)
        if not item or number < 0 or number >= len(item["lessons"]):
            return render_template("404.html"), 404
        title, body = item["lessons"][number]
        key = f"{slug}:{number}"
        if request.method == "POST":
            progress = Progress.query.filter_by(user_id=session["user_id"], lesson_key=key).first()
            if not progress:
                db.session.add(Progress(user_id=session["user_id"], lesson_key=key, completed=True))
                db.session.commit()
            flash("Lesson marked as complete.", "success")
            return redirect(url_for("course", slug=slug))
        return render_template("lesson.html", course=item, number=number, title=title, body=body)

    @app.route("/terminal")
    @login_required
    def terminal():
        return render_template("terminal.html")

    @app.route("/api/terminal/execute", methods=["POST"])
    @login_required
    def terminal_execute():
        command = request.json.get("command","") if request.is_json else request.form.get("command","")
        output = simulate_command(command)
        return jsonify({"output": output})

    @app.route("/networking")
    @login_required
    def networking():
        return render_template("networking.html")

    @app.route("/api/network/subnet", methods=["POST"])
    @login_required
    def subnet():
        data = request.get_json(silent=True) or {}
        cidr = (data.get("cidr") or "").strip()
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            if network.version != 4:
                raise ValueError("Enter an IPv4 network in CIDR format.")
            hosts = list(network.hosts()) if network.num_addresses <= 65536 else None
            return jsonify({
                "ok": True,
                "network": str(network.network_address),
                "broadcast": str(network.broadcast_address),
                "mask": str(network.netmask),
                "prefix": network.prefixlen,
                "total_addresses": network.num_addresses,
                "usable_hosts": max(network.num_addresses - 2, 0) if network.prefixlen <= 30 else (1 if network.prefixlen == 31 else 1),
                "first_host": str(hosts[0]) if hosts else (str(network.network_address + 1) if network.prefixlen <= 30 else str(network.network_address)),
                "last_host": str(hosts[-1]) if hosts else (str(network.broadcast_address - 1) if network.prefixlen <= 30 else str(network.broadcast_address)),
            })
        except ValueError as exc:
            return jsonify({"ok": False, "error": str(exc) or "Invalid network."}), 400

    @app.route("/cybersecurity")
    @login_required
    def cybersecurity():
        return render_template("cybersecurity.html", challenges=CYBER_CHALLENGES)

    @app.route("/api/cyber/submit", methods=["POST"])
    @login_required
    def cyber_submit():
        data = request.get_json(silent=True) or {}
        challenge_id = data.get("challenge_id")
        answer = (data.get("answer") or "").strip().lower()
        challenge = next((c for c in CYBER_CHALLENGES if c["id"] == challenge_id), None)
        if not challenge:
            return jsonify({"ok": False, "message": "Challenge not found."}), 404
        correct = answer == challenge["answer"]
        if correct:
            existing = ChallengeResult.query.filter_by(user_id=session["user_id"], challenge_id=challenge_id).first()
            if not existing:
                db.session.add(ChallengeResult(user_id=session["user_id"], challenge_id=challenge_id))
                db.session.commit()
        return jsonify({"ok": correct, "message": "Correct. Challenge completed." if correct else "Not quite. Review the hint and try again."})

    @app.route("/profile")
    @login_required
    def profile():
        user = current_user()
        return render_template("profile.html", user=user)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/privacy")
    def privacy():
        return render_template("legal.html", title="Privacy Policy", content="ShadowNet stores account details, course progress and challenge results to operate the learning platform. Use a unique password. Do not submit secrets or sensitive personal information into practice labs. Administrators should publish a complete privacy notice that matches their actual hosting, logging and retention practices before public launch.")

    @app.route("/terms")
    def terms():
        return render_template("legal.html", title="Terms and Conditions", content="Use ShadowNet lawfully. Cybersecurity exercises must remain within the platform's authorized training environments or systems for which you have explicit permission. Do not attack, scan or disrupt third-party systems. Lab access may be limited to protect platform availability.")

    @app.errorhandler(404)
    def not_found(_):
        return render_template("404.html"), 404

    with app.app_context():
        db.create_all()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
