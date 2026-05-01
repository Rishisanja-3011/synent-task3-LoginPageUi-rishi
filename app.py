from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from config import Config
from extensions import db, mail
from models import User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail.init_app(app)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# ─── Helpers ────────────────────────────────────────────────────────────────

def generate_token(email, salt):
    return serializer.dumps(email, salt=salt)


def verify_token(token, salt, expiry=3600):
    try:
        email = serializer.loads(token, salt=salt, max_age=expiry)
        return email
    except (SignatureExpired, BadSignature):
        return None


def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template)
    mail.send(msg)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        # Server-side validation
        errors = []
        if not name or len(name) < 2:
            errors.append('Name must be at least 2 characters.')
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')
        if User.query.filter_by(email=email).first():
            errors.append('An account with this email already exists.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('register.html', name=name, email=email)

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Send verification email
        token = generate_token(email, salt='email-verify')
        verify_url = url_for('verify_email', token=token, _external=True)
        html = render_template('email/verify.html', name=name, verify_url=verify_url)
        send_email(email, 'Verify Your Email — Synent Auth', html)

        flash('Account created! Please check your email to verify your account.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/verify/<token>')
def verify_email(token):
    email = verify_token(token, salt='email-verify', expiry=app.config['TOKEN_EXPIRY'])
    if not email:
        flash('Verification link is invalid or has expired.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))

    if user.is_verified:
        flash('Your email is already verified. Please log in.', 'info')
    else:
        user.is_verified = True
        db.session.commit()
        flash('Email verified successfully! You can now log in.', 'success')

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'error')
            return render_template('login.html', email=email)

        if not user.is_verified:
            flash('Please verify your email before logging in.', 'warning')
            return render_template('login.html', email=email)

        session['user_id'] = user.id
        session['user_name'] = user.name
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user  = User.query.filter_by(email=email).first()

        # Always show success message (prevents email enumeration)
        if user and user.is_verified:
            token = generate_token(email, salt='password-reset')
            reset_url = url_for('reset_password', token=token, _external=True)
            html = render_template('email/reset.html', name=user.name, reset_url=reset_url)
            send_email(email, 'Reset Your Password — Synent Auth', html)

        flash('If that email exists, a reset link has been sent.', 'info')
        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_token(token, salt='password-reset', expiry=app.config['TOKEN_EXPIRY'])
    if not email:
        flash('Reset link is invalid or has expired.', 'error')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return render_template('reset_password.html', token=token)
        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', token=token)

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('login'))

        user.set_password(password)
        db.session.commit()
        flash('Password reset successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)


@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ─── Init DB & Run ───────────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)