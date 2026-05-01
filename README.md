# synent-task3-loginpage-sanja

**Synent Technologies Internship — Task 3: Login Page UI**  
Candidate: Sanja Rishi Bharatbhai | ID: SYN/H2/IP1807

---

## 🚀 Features

- **User Registration** with full server + client-side validation
- **Email Verification** via tokenized link (expires in 1 hour)
- **Secure Login** with session management
- **Forgot Password** flow with Gmail SMTP reset email
- **Password Reset** with secure itsdangerous tokens
- **Password Strength Indicator** (real-time, 4-level)
- **Show/Hide Password** toggle on all password fields
- **Flash Messages** with categorized styling
- **Protected Dashboard** with login-required decorator
- **Anti-enumeration** on forgot password endpoint
- **Responsive Design** — works on mobile and desktop

---

## 🛠️ Tech Stack

| Layer    | Technology                    |
|----------|-------------------------------|
| Backend  | Python 3.10+ / Flask 3.0      |
| Database | MySQL + Flask-SQLAlchemy      |
| Email    | Gmail SMTP + Flask-Mail       |
| Tokens   | itsdangerous (URLSafeTimedSerializer) |
| Auth     | Werkzeug password hashing + Flask sessions |
| Frontend | HTML5, CSS3, Vanilla JavaScript |

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/synent-task3-loginpage-sanja.git
cd synent-task3-loginpage-sanja
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` with your values:
```
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/synent_auth
MAIL_USERNAME=yourgmail@gmail.com
MAIL_PASSWORD=your-gmail-app-password
```

> **Gmail App Password:** Go to Google Account → Security → 2-Step Verification → App Passwords → Generate one for "Mail".

### 5. Create the MySQL database
```sql
CREATE DATABASE synent_auth CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Run the app
```bash
python app.py
```
Visit `http://localhost:5000`

---

## 📁 Project Structure

```
synent-task3-loginpage-sanja/
├── app.py                    # Main Flask application & routes
├── config.py                 # Configuration (DB, mail, tokens)
├── extensions.py             # SQLAlchemy & Mail instances
├── models.py                 # User database model
├── requirements.txt
├── .env.example
├── templates/
│   ├── base.html             # Shared layout
│   ├── login.html
│   ├── register.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── dashboard.html
│   └── email/
│       ├── verify.html       # Verification email
│       └── reset.html        # Password reset email
└── static/
    ├── css/style.css         # Full design system
    └── js/validation.js      # Client-side validation
```

---

## 🔐 Security Notes

- Passwords hashed with Werkzeug (PBKDF2-SHA256)
- Tokens signed & time-limited via itsdangerous
- Forgot password endpoint never reveals if email exists
- Sessions cleared on logout

---

*Built for Synent Technologies Web Development Internship Program*