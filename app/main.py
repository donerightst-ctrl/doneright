from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.api.v1.endpoints import auth
from app.core.database import engine, Base
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI(title="ДОНРАЙТ", version="1.0.0")

# ======== НАСТРОЙКИ ПОЧТЫ ========
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "doneright.st@gmail.com"
SMTP_PASSWORD = "tvefqlqhnnokeqqt"
TO_EMAIL = "doneright.st@gmail.com"

def send_email(name: str, phone: str, address: str, message: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = TO_EMAIL
        msg['Subject'] = f"🔧 Новая заявка от {name}"

        body = f"""
        <h2>📩 Новая заявка с сайта ДОНРАЙТ</h2>
        <p><strong>👤 Имя:</strong> {name}</p>
        <p><strong>📞 Телефон:</strong> {phone}</p>
        <p><strong>📍 Адрес:</strong> {address if address else 'Не указан'}</p>
        <p><strong>📝 Задача:</strong> {message if message else 'Без описания'}</p>
        <hr>
        <p>Письмо сгенерировано автоматически.</p>
        """

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Письмо отправлено на {TO_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ДОНРАЙТ — Премиум сервис в Железногорске</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700;14..32,800;14..32,900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: #080808;
            color: #FFFFFF;
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* ===== ФОН С WAVE-ГРАФИКОЙ ===== */
        .bg-wave {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }
        .bg-wave svg {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 40%;
            opacity: 0.05;
        }
        .bg-wave svg:first-child {
            height: 60%;
            opacity: 0.03;
            animation: waveAnim 20s ease-in-out infinite;
        }
        @keyframes waveAnim {
            0%, 100% { transform: translateX(0) scaleY(1); }
            50% { transform: translateX(-5%) scaleY(0.8); }
        }

        .bg-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background-image: 
                linear-gradient(rgba(255, 215, 0, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 215, 0, 0.02) 1px, transparent 1px);
            background-size: 60px 60px;
            pointer-events: none;
        }
        .bg-glow {
            position: fixed;
            top: -20%;
            left: -20%;
            width: 140%;
            height: 140%;
            z-index: 0;
            background: radial-gradient(ellipse at 30% 40%, rgba(255, 215, 0, 0.05) 0%, transparent 60%);
            pointer-events: none;
            animation: pulseGlow 8s ease-in-out infinite;
        }
        @keyframes pulseGlow {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.1); }
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
            position: relative;
            z-index: 1;
        }

        /* ===== АНИМАЦИИ ===== */
        .fade-up {
            opacity: 0;
            transform: translateY(60px);
            transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .fade-up.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .delay-1 { transition-delay: 0.05s; }
        .delay-2 { transition-delay: 0.15s; }
        .delay-3 { transition-delay: 0.25s; }
        .delay-4 { transition-delay: 0.35s; }
        .delay-5 { transition-delay: 0.45s; }
        .delay-6 { transition-delay: 0.55s; }

        /* ===== 3D-НАКЛОН КАРТОЧЕК ===== */
        .tilt-card {
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            transform-style: preserve-3d;
            perspective: 800px;
        }

        /* ===== ЧАСТИЦЫ (интерактивные) ===== */
        .particle-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #FFD700;
            border-radius: 50%;
            opacity: 0.3;
            transition: all 0.1s ease;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-15px) rotate(2deg); }
        }
        @keyframes shimmer {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        @keyframes neonPulse {
            0%, 100% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.1), 0 0 60px rgba(255, 215, 0, 0.05); }
            50% { box-shadow: 0 0 30px rgba(255, 215, 0, 0.2), 0 0 80px rgba(255, 215, 0, 0.1); }
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 28px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.06);
            position: relative;
        }
        .navbar::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent, #FFD700, #FF8C00, #FFD700, transparent);
            background-size: 200% 100%;
            animation: shimmer 4s ease-in-out infinite;
        }
        .logo {
            font-size: 32px;
            font-weight: 900;
            letter-spacing: -1.5px;
            background: linear-gradient(135deg, #FFD700, #FF8C00, #FFD700);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmer 3s ease-in-out infinite;
        }
        .nav a {
            color: #9CA3AF;
            text-decoration: none;
            margin-left: 36px;
            font-size: 14px;
            font-weight: 500;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            position: relative;
        }
        .nav a i { margin-right: 6px; font-size: 12px; }
        .nav a::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 0%;
            height: 2px;
            background: linear-gradient(90deg, #FFD700, #FF8C00);
            transition: width 0.3s ease;
        }
        .nav a:hover { color: #fff; }
        .nav a:hover::after { width: 100%; }

        .btn-gold {
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            color: #0A0A0A;
            padding: 14px 36px;
            border-radius: 60px;
            font-weight: 700;
            font-size: 14px;
            border: none;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            animation: neonPulse 3s ease-in-out infinite;
        }
        .btn-gold::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 60%);
            opacity: 0;
            transition: opacity 0.5s ease;
            transform: scale(0.5);
        }
        .btn-gold:hover::before { opacity: 1; transform: scale(1); }
        .btn-gold:hover { transform: scale(1.05) translateY(-2px); box-shadow: 0 0 60px rgba(255, 215, 0, 0.3); }

        .hero {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 80px;
            align-items: center;
            padding: 80px 0 100px;
        }
        .hero h1 {
            font-size: 68px;
            font-weight: 900;
            line-height: 1.04;
            letter-spacing: -3px;
        }
        .hero h1 .highlight {
            background: linear-gradient(135deg, #FFD700, #FF8C00, #FFD700);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmer 3s ease-in-out infinite;
        }
        .hero .subtitle {
            color: #9CA3AF;
            font-size: 20px;
            margin: 28px 0;
            max-width: 480px;
            font-weight: 400;
            line-height: 1.8;
        }
        .hero .city-tag {
            display: inline-block;
            background: rgba(255, 215, 0, 0.08);
            border: 1px solid rgba(255, 215, 0, 0.12);
            color: #FFD700;
            padding: 6px 20px;
            border-radius: 60px;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 16px;
        }
        .hero .city-tag i { margin-right: 6px; }
        .badge-group {
            display: flex;
            gap: 50px;
            margin-top: 48px;
        }
        .badge-group .stat span {
            font-size: 38px;
            font-weight: 800;
            color: #FFD700;
            display: block;
            letter-spacing: -1px;
        }
        .badge-group .stat p {
            color: #6B7280;
            font-size: 14px;
            font-weight: 500;
            margin: 0;
            letter-spacing: 0.3px;
        }
        .hero-image {
            background: radial-gradient(ellipse at center, rgba(255, 215, 0, 0.04) 0%, transparent 70%);
            border: 1px solid rgba(255, 215, 0, 0.06);
            border-radius: 32px;
            padding: 60px 40px;
            text-align: center;
            backdrop-filter: blur(12px);
            position: relative;
            transition: all 0.5s ease;
        }
        .hero-image:hover { border-color: rgba(255, 215, 0, 0.15); }
        .hero-image .big-icon {
            font-size: 90px;
            display: block;
            margin-bottom: 20px;
            animation: float 4s ease-in-out infinite;
        }
        .hero-image h3 { color: #FFD700; font-size: 24px; font-weight: 700; margin-bottom: 10px; }
        .hero-image p { color: #9CA3AF; font-size: 15px; max-width: 340px; margin: 0 auto; }
        .hero-image .badge-gold {
            display: inline-block;
            background: rgba(255, 215, 0, 0.08);
            border: 1px solid rgba(255, 215, 0, 0.1);
            color: #FFD700;
            padding: 6px 20px;
            border-radius: 60px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 20px;
        }

        .trust-counter {
            text-align: center;
            padding: 50px 0 70px;
            border-bottom: 1px solid rgba(255, 215, 0, 0.05);
        }
        .trust-counter .number {
            font-size: 72px;
            font-weight: 900;
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .trust-counter p { color: #9CA3AF; font-size: 18px; margin-top: 8px; }

        .why-section, .promo-section, .reviews-section, .steps-section, .faq-section, .trust-logos {
            padding: 70px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.05);
        }
        .section-title {
            text-align: center;
            font-size: 40px;
            font-weight: 800;
            margin-bottom: 50px;
            letter-spacing: -1.5px;
        }
        .section-title i { color: #FFD700; margin-right: 12px; }

        .why-grid, .promo-grid, .reviews-carousel, .steps-grid {
            display: grid;
            gap: 28px;
        }
        .why-grid { grid-template-columns: repeat(4, 1fr); }
        .promo-grid { grid-template-columns: repeat(3, 1fr); }
        .reviews-carousel { grid-template-columns: repeat(3, 1fr); }
        .steps-grid { grid-template-columns: repeat(4, 1fr); }

        .why-card, .promo-card, .review-card, .step-card, .guarantee-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 24px;
            padding: 30px 28px;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            text-align: center;
        }
        .why-card:hover, .promo-card:hover, .review-card:hover, .step-card:hover, .guarantee-card:hover {
            transform: translateY(-8px);
            border-color: rgba(255, 215, 0, 0.15);
            box-shadow: 0 30px 50px -20px rgba(0,0,0,0.8);
        }
        .why-card .icon, .step-card .step-number, .guarantee-card .icon {
            font-size: 40px;
            display: block;
            margin-bottom: 14px;
        }
        .why-card h4, .step-card h4, .guarantee-card h3 {
            color: #FFD700;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .why-card p, .step-card p, .guarantee-card p {
            color: #9CA3AF;
            font-size: 14px;
            line-height: 1.7;
        }
        .step-card .step-number {
            width: 48px;
            height: 48px;
            line-height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            color: #0A0A0A;
            font-weight: 900;
            font-size: 18px;
            margin: 0 auto 16px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .promo-card .tag {
            display: inline-block;
            background: #FFD700;
            color: #0A0A0A;
            font-weight: 700;
            font-size: 11px;
            padding: 4px 16px;
            border-radius: 60px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 16px;
        }
        .promo-card h3 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 10px;
            color: #FFD700;
        }
        .promo-card p { color: #9CA3AF; font-size: 15px; }
        .review-card .stars {
            color: #FFD700;
            font-size: 18px;
            letter-spacing: 2px;
            display: block;
            margin-bottom: 12px;
        }
        .review-card .text {
            color: #D1D5DB;
            font-size: 15px;
            line-height: 1.7;
            margin-bottom: 16px;
            font-style: italic;
        }
        .review-card .author {
            color: #6B7280;
            font-size: 14px;
            font-weight: 600;
        }
        .review-card .author span { color: #FFD700; }

        .guarantees {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 28px;
            padding: 70px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.05);
        }
        .guarantee-card {
            position: relative;
            overflow: hidden;
            text-align: left;
        }
        .guarantee-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #FFD700, transparent);
            opacity: 0;
            transition: opacity 0.4s ease;
        }
        .guarantee-card:hover::before { opacity: 1; }

        .faq-grid { max-width: 800px; margin: 0 auto; }
        .faq-item {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 20px;
            padding: 24px 30px;
            margin-bottom: 16px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .faq-item:hover { border-color: rgba(255, 215, 0, 0.12); }
        .faq-item .question {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
            color: #E4E4E4;
            font-size: 17px;
        }
        .faq-item .question .arrow {
            color: #FFD700;
            transition: transform 0.3s ease;
            font-size: 20px;
        }
        .faq-item .answer {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease, padding 0.3s ease;
            color: #9CA3AF;
            font-size: 15px;
            line-height: 1.7;
        }
        .faq-item.active .answer { max-height: 300px; padding-top: 16px; }
        .faq-item.active .question .arrow { transform: rotate(180deg); }

        .logos-grid {
            display: flex;
            justify-content: center;
            gap: 60px;
            flex-wrap: wrap;
        }
        .logos-grid .logo-item {
            color: #3A3A3A;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            transition: 0.3s;
        }
        .logos-grid .logo-item.gold { color: #FFD700; }
        .logos-grid .logo-item:hover { color: #FFD700; }

        .contacts-wrapper {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 24px;
            max-width: 800px;
            margin: 0 auto;
        }
        .contact-link {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #9CA3AF;
            text-decoration: none;
            font-size: 16px;
            transition: all 0.3s ease;
            padding: 14px 28px;
            background: rgba(255, 215, 0, 0.03);
            border-radius: 60px;
            border: 1px solid rgba(255, 215, 0, 0.06);
        }
        .contact-link:hover {
            background: rgba(255, 215, 0, 0.06);
            border-color: rgba(255, 215, 0, 0.15);
            transform: translateY(-2px);
            color: #fff;
        }
        .contact-link i { font-size: 22px; }
        .contact-link .label { color: #fff; }

        .form-section { padding: 90px 0; text-align: center; }
        .form-section h2 { font-size: 44px; font-weight: 800; letter-spacing: -1.5px; margin-bottom: 12px; }
        .form-section .sub { color: #9CA3AF; font-size: 18px; margin-bottom: 44px; }

        .form-box {
            max-width: 560px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 48px 44px;
            border-radius: 32px;
            text-align: left;
        }
        .form-box label {
            font-weight: 600;
            color: #D1D5DB;
            font-size: 14px;
            letter-spacing: 0.3px;
        }
        .form-box input, .form-box textarea {
            width: 100%;
            padding: 14px 18px;
            margin: 8px 0 22px;
            background: #121212;
            border: 1px solid #222;
            border-radius: 16px;
            color: #fff;
            font-size: 16px;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }
        .form-box input:focus, .form-box textarea:focus {
            outline: none;
            border-color: #FFD700;
            box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.06);
            background: #161616;
        }
        .form-box .small-note {
            color: #6B7280;
            font-size: 13px;
            margin-top: 20px;
            text-align: center;
        }

        .scroll-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            color: #0A0A0A;
            width: 52px;
            height: 52px;
            border-radius: 50%;
            border: none;
            font-size: 22px;
            cursor: pointer;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.15);
            transition: all 0.3s ease;
            opacity: 0;
            visibility: hidden;
            z-index: 999;
        }
        .scroll-top.visible { opacity: 1; visibility: visible; }
        .scroll-top:hover { transform: scale(1.1); box-shadow: 0 0 50px rgba(255, 215, 0, 0.3); }

        .popup-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(8px);
            z-index: 9999;
            justify-content: center;
            align-items: center;
        }
        .popup-overlay.active { display: flex; }
        .popup {
            background: #121212;
            border: 1px solid rgba(255, 215, 0, 0.15);
            border-radius: 32px;
            padding: 50px 60px;
            max-width: 480px;
            text-align: center;
            animation: fadeUp 0.5s ease forwards;
        }
        .popup .icon { font-size: 72px; display: block; margin-bottom: 20px; }
        .popup h2 { color: #FFD700; font-size: 28px; font-weight: 800; margin-bottom: 12px; }
        .popup p { color: #9CA3AF; font-size: 16px; margin-bottom: 30px; }

        footer {
            padding: 32px 0;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            color: #6B7280;
            display: flex;
            justify-content: space-between;
            font-size: 14px;
            flex-wrap: wrap;
            gap: 12px;
        }
        footer a { color: #6B7280; text-decoration: none; transition: 0.3s; }
        footer a:hover { color: #FFD700; }

        @media (max-width: 768px) {
            .hero { grid-template-columns: 1fr; gap: 40px; padding: 40px 0 60px; }
            .hero h1 { font-size: 38px; letter-spacing: -1.5px; }
            .why-grid, .promo-grid, .reviews-carousel, .steps-grid, .guarantees {
                grid-template-columns: 1fr;
            }
            .nav a { display: none; }
            .badge-group { flex-wrap: wrap; gap: 24px; }
            .form-box { padding: 28px 20px; }
            .hero-image { padding: 40px 20px; }
            .hero-image .big-icon { font-size: 56px; }
            .form-section h2 { font-size: 30px; }
            footer { flex-direction: column; gap: 12px; text-align: center; }
            .logos-grid { gap: 30px; }
            .trust-counter .number { font-size: 40px; }
            .section-title { font-size: 28px; }
            .popup { padding: 30px 24px; }
            .contacts-wrapper { flex-direction: column; align-items: center; }
            .contact-link { width: 100%; justify-content: center; }
        }
    </style>
</head>
<body>

    <!-- ===== WAVE-ГРАФИКА НА ФОНЕ ===== -->
    <div class="bg-wave">
        <svg viewBox="0 0 1200 200" preserveAspectRatio="none">
            <path d="M0,150 C300,50 600,200 1200,100 L1200,200 L0,200 Z" fill="#FFD700"/>
        </svg>
        <svg viewBox="0 0 1200 200" preserveAspectRatio="none">
            <path d="M0,120 C400,180 800,60 1200,140 L1200,200 L0,200 Z" fill="#FF8C00"/>
        </svg>
    </div>

    <!-- ===== ИНТЕРАКТИВНЫЕ ЧАСТИЦЫ ===== -->
    <div class="particle-container" id="particleContainer"></div>

    <div class="bg-grid"></div>
    <div class="bg-glow"></div>

    <div class="container">
        <!-- ШАПКА -->
        <nav class="navbar fade-up visible">
            <div class="logo">✦ ДОНРАЙТ</div>
            <div class="nav">
                <a href="#why"><i class="fas fa-star"></i>Почему мы</a>
                <a href="#promo"><i class="fas fa-fire"></i>Акции</a>
                <a href="#reviews"><i class="fas fa-comment"></i>Отзывы</a>
                <a href="#guarantees"><i class="fas fa-shield"></i>Гарантии</a>
                <a href="#form" class="btn-gold" style="padding: 10px 28px;"><i class="fas fa-pen"></i> Заявка</a>
            </div>
        </nav>

        <!-- ГЕРОЙ -->
        <section class="hero">
            <div class="fade-up visible delay-1">
                <div class="city-tag"><i class="fas fa-map-pin"></i> Железногорск</div>
                <div style="display: inline-block; background: rgba(255, 215, 0, 0.08); border: 1px solid rgba(255, 215, 0, 0.1); color: #FFD700; padding: 8px 24px; border-radius: 60px; font-weight: 600; font-size: 13px; letter-spacing: 0.5px; margin-bottom: 24px;">
                    <i class="fas fa-lock"></i> Оплата только после вашего одобрения
                </div>
                <h1>Решим вашу задачу.<br><span class="highlight">Без риска и предоплат.</span></h1>
                <p class="subtitle">Сантехника, электрика, сборка мебели. Отвечаем за результат. Если не нравится — переделаем за свой счёт.</p>
                <a href="#form" class="btn-gold" style="padding: 18px 54px; font-size: 17px;"><i class="fas fa-phone"></i> Вызвать мастера</a>
                <div class="badge-group">
                    <div class="stat"><span>4.9</span><p><i class="fas fa-star" style="color: #FFD700; font-size: 12px;"></i> Средний рейтинг</p></div>
                    <div class="stat"><span>0 ₽</span><p><i class="fas fa-wallet" style="color: #FFD700; font-size: 12px;"></i> Плата до результата</p></div>
                    <div class="stat"><span>24 ч</span><p><i class="fas fa-clock" style="color: #FFD700; font-size: 12px;"></i> Гарантийный срок</p></div>
                </div>
            </div>
            <div class="hero-image fade-up visible delay-2">
                <span class="big-icon">🛠️</span>
                <h3>Ваша безопасность — наш приоритет</h3>
                <p>Мастера в чистой обуви. Работаем строго по договору.</p>
                <span class="badge-gold"><i class="fas fa-check-circle"></i> Передача денег мастеру на руки запрещена</span>
            </div>
        </section>

        <!-- СЧЁТЧИК -->
        <section class="trust-counter fade-up visible delay-2">
            <div class="number" id="counter">0</div>
            <p><i class="fas fa-users" style="color: #FFD700; margin-right: 8px;"></i>человек в Железногорске уже доверили нам свои задачи</p>
        </section>

        <!-- ПОЧЕМУ МЫ -->
        <section class="why-section" id="why">
            <h2 class="section-title fade-up"><i class="fas fa-gem"></i>Почему выбирают нас</h2>
            <div class="why-grid">
                <div class="why-card tilt-card fade-up delay-1"><span class="icon">⚡</span><h4>Быстро</h4><p>Приезжаем в течение часа. Работаем без задержек.</p></div>
                <div class="why-card tilt-card fade-up delay-2"><span class="icon">💎</span><h4>Надёжно</h4><p>Даём гарантию на все виды работ — 24 месяца.</p></div>
                <div class="why-card tilt-card fade-up delay-3"><span class="icon">🤝</span><h4>Честно</h4><p>Цена фиксируется до начала работ. Никаких сюрпризов.</p></div>
                <div class="why-card tilt-card fade-up delay-4"><span class="icon">🧹</span><h4>Аккуратно</h4><p>Работаем в чистой обуви. Убираем за собой.</p></div>
            </div>
        </section>

        <!-- АКЦИИ -->
        <section class="promo-section" id="promo">
            <h2 class="section-title fade-up"><i class="fas fa-fire" style="color: #FF8C00;"></i>Наши акции</h2>
            <div class="promo-grid">
                <div class="promo-card tilt-card fade-up delay-1">
                    <span class="tag">Скидка</span>
                    <h3>10%</h3>
                    <p>По промокоду <strong style="color: #FFD700;">DONERIGHT10</strong> на первый заказ</p>
                </div>
                <div class="promo-card tilt-card fade-up delay-2">
                    <span class="tag">Бонус</span>
                    <h3>Приведи друга</h3>
                    <p>Получите скидку 10% на следующий заказ, если порекомендуете нас другу</p>
                </div>
                <div class="promo-card tilt-card fade-up delay-3">
                    <span class="tag">Акция</span>
                    <h3>Пенсионерам</h3>
                    <p>Скидка 10% на все услуги для пенсионеров Железногорска</p>
                </div>
            </div>
        </section>

        <!-- ОТЗЫВЫ -->
        <section class="reviews-section" id="reviews">
            <h2 class="section-title fade-up"><i class="fas fa-comment-dots"></i>Что говорят клиенты в Железногорске</h2>
            <div class="reviews-carousel">
                <div class="review-card tilt-card fade-up delay-1"><span class="stars">★★★★★</span><p class="text">"Сантехника работала отлично. Приехали быстро, сделали качественно. Оплатил только после проверки. Спасибо!"</p><div class="author">— Александр, <span>Железногорск</span></div></div>
                <div class="review-card tilt-card fade-up delay-2"><span class="stars">★★★★★</span><p class="text">"Собрали мебель. Всё чётко, аккуратно. Мастер пришёл со своим инструментом. Рекомендую!"</p><div class="author">— Екатерина, <span>Железногорск</span></div></div>
                <div class="review-card tilt-card fade-up delay-3"><span class="stars">★★★★★</span><p class="text">"Электрику делали. Всё проверили, дали гарантию. Очень удобно, что платить можно после результата."</p><div class="author">— Дмитрий, <span>Железногорск</span></div></div>
            </div>
        </section>

        <!-- КАК МЫ РАБОТАЕМ -->
        <section class="steps-section" id="steps">
            <h2 class="section-title fade-up"><i class="fas fa-route"></i>Как мы работаем</h2>
            <div class="steps-grid">
                <div class="step-card tilt-card fade-up delay-1">
                    <div class="step-number">1</div>
                    <h4>Заявка</h4>
                    <p>Оставляете заявку на сайте или по телефону</p>
                </div>
                <div class="step-card tilt-card fade-up delay-2">
                    <div class="step-number">2</div>
                    <h4>Оценка</h4>
                    <p>Оцениваем объём работ и называем точную цену</p>
                </div>
                <div class="step-card tilt-card fade-up delay-3">
                    <div class="step-number">3</div>
                    <h4>Работа</h4>
                    <p>Выполняем задачу качественно и в срок</p>
                </div>
                <div class="step-card tilt-card fade-up delay-4">
                    <div class="step-number">4</div>
                    <h4>Оплата</h4>
                    <p>Вы проверяете результат и платите только после одобрения</p>
                </div>
            </div>
        </section>

        <!-- ГАРАНТИИ -->
        <section class="guarantees" id="guarantees">
            <div class="guarantee-card tilt-card fade-up delay-1"><span class="icon">💰</span><h3>Платите после</h3><p>Вы принимаете работу лично. Только после этого — оплата на реквизиты компании. Без скрытых комиссий и предоплат.</p></div>
            <div class="guarantee-card tilt-card fade-up delay-2"><span class="icon">🛡️</span><h3>Гарантия качества</h3><p>Сделали криво? Мы исправим за свой счёт или вернём деньги. У вас есть 24 часа на проверку.</p></div>
            <div class="guarantee-card tilt-card fade-up delay-3"><span class="icon">📄</span><h3>Работаем по закону</h3><p>Для заказов от 10 000 ₽ заключаем официальный договор. Мы несём ответственность, а не случайный мастер.</p></div>
        </section>

        <!-- НАС РЕКОМЕНДУЮТ -->
        <section class="trust-logos fade-up delay-3">
            <div style="display: flex; align-items: center; justify-content: center; gap: 16px; margin-bottom: 30px;">
                <span style="display: inline-block; width: 40px; height: 1px; background: linear-gradient(90deg, transparent, #FFD700);"></span>
                <p style="color: #FFD700; font-size: 14px; text-transform: uppercase; letter-spacing: 4px; font-weight: 700; margin: 0;">
                    <i class="fas fa-star" style="margin-right: 10px;"></i>Нас рекомендуют в Железногорске
                </p>
                <span style="display: inline-block; width: 40px; height: 1px; background: linear-gradient(90deg, #FFD700, transparent);"></span>
            </div>
            <div class="logos-grid">
                <span class="logo-item gold"><i class="fas fa-check-circle"></i> Железногорск</span>
                <span class="logo-item"><i class="fas fa-users"></i> Наши клиенты</span>
                <span class="logo-item gold"><i class="fas fa-thumbs-up"></i> Рекомендуют</span>
                <span class="logo-item"><i class="fas fa-home"></i> Соседи</span>
                <span class="logo-item gold"><i class="fas fa-heart"></i> Доверие</span>
            </div>
        </section>

        <!-- КОНТАКТЫ -->
        <section class="trust-logos fade-up delay-2" style="border-bottom: none; padding: 40px 0 60px;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 16px; margin-bottom: 40px;">
                <span style="display: inline-block; width: 30px; height: 1px; background: linear-gradient(90deg, transparent, #FFD700);"></span>
                <p style="color: #FFD700; font-size: 14px; text-transform: uppercase; letter-spacing: 3px; font-weight: 700; margin: 0;">
                    <i class="fas fa-headset" style="margin-right: 10px;"></i>Служба поддержки
                </p>
                <span style="display: inline-block; width: 30px; height: 1px; background: linear-gradient(90deg, #FFD700, transparent);"></span>
            </div>
            <div class="contacts-wrapper">
                <a href="mailto:doneright.st@gmail.com" class="contact-link">
                    <i class="fas fa-envelope" style="color: #FFD700;"></i>
                    <span class="label">doneright.st@gmail.com</span>
                </a>
                <a href="https://vk.ru/doneright" target="_blank" class="contact-link">
                    <i class="fab fa-vk" style="color: #4C75A3;"></i>
                    <span class="label">Сообщество ВК</span>
                </a>
                <a href="https://t.me/DoneRight_bot" target="_blank" class="contact-link">
                    <i class="fab fa-telegram-plane" style="color: #0088cc;"></i>
                    <span class="label">Telegram-бот</span>
                </a>
            </div>
        </section>

        <!-- FAQ -->
        <section class="faq-section" id="faq">
            <h2 class="section-title fade-up"><i class="fas fa-circle-question"></i>Часто задаваемые вопросы</h2>
            <div class="faq-grid">
                <div class="faq-item fade-up delay-1">
                    <div class="question"><span>Какие виды работ вы выполняете?</span><span class="arrow">▼</span></div>
                    <div class="answer">Сантехника, электрика, сборка мебели, мелкий ремонт. Работаем как с частными, так и с коммерческими заказами.</div>
                </div>
                <div class="faq-item fade-up delay-2">
                    <div class="question"><span>Сколько ждать мастера?</span><span class="arrow">▼</span></div>
                    <div class="answer">В среднем мастер приезжает в течение 1 часа после подтверждения заявки.</div>
                </div>
                <div class="faq-item fade-up delay-3">
                    <div class="question"><span>Что если что-то пошло не так?</span><span class="arrow">▼</span></div>
                    <div class="answer">У вас есть 24 часа на проверку. Если работа выполнена некачественно — мы переделаем или вернём деньги.</div>
                </div>
            </div>
        </section>

        <!-- ФОРМА -->
        <section class="form-section" id="form">
            <h2 class="fade-up delay-2"><i class="fas fa-pen-to-square" style="color: #FFD700;"></i> Оставьте заявку</h2>
            <p class="sub fade-up delay-3">Мы перезвоним через 5 минут, уточним детали и назовём точную цену.</p>
            <div class="form-box fade-up delay-4">
                <form id="contactForm" action="/submit-form" method="post">
                    <label><i class="fas fa-user" style="color: #FFD700;"></i> Ваше имя</label>
                    <input type="text" name="name" placeholder="Иван Петров" required>
                    <label><i class="fas fa-phone" style="color: #FFD700;"></i> Телефон</label>
                    <input type="tel" name="phone" placeholder="+7 (999) 123-45-67" required>
                    <label><i class="fas fa-location-dot" style="color: #FFD700;"></i> Адрес в Железногорске</label>
                    <input type="text" name="address" placeholder="Улица, дом, квартира">
                    <label><i class="fas fa-tools" style="color: #FFD700;"></i> Что нужно сделать?</label>
                    <textarea name="message" rows="4" placeholder="Опишите задачу как можно подробнее..."></textarea>
                    <button type="submit" class="btn-gold" style="width: 100%; text-align: center; padding: 16px; font-size: 16px;"><i class="fas fa-paper-plane"></i> Отправить заявку →</button>
                    <div class="small-note">
                        <i class="fas fa-check-circle" style="color: #FFD700;"></i> Никаких скрытых платежей. Цена фиксируется до начала работ.<br>
                        Нажимая «Отправить», вы соглашаетесь с <a href="#" id="openPolicy" style="color: #FFD700; text-decoration: underline;">политикой обработки персональных данных</a>.
                    </div>
                </form>
            </div>
        </section>

        <footer>
            <span>© 2026 ДОНРАЙТ. Работаем честно в Железногорске.</span>
            <span><a href="#" id="openPolicy2" style="color: #6B7280; text-decoration: none; transition: 0.3s;"><i class="fas fa-lock" style="margin-right: 6px;"></i>Политика конфиденциальности</a></span>
        </footer>
    </div>

    <!-- ПОПАП СПАСИБО -->
    <div class="popup-overlay" id="thankYouPopup">
        <div class="popup">
            <span class="icon">🎉</span>
            <h2>Заявка отправлена!</h2>
            <p>Мы перезвоним вам в течение 5 минут. Спасибо за доверие!</p>
            <button class="btn-gold" onclick="closePopup()"><i class="fas fa-check"></i> Отлично!</button>
        </div>
    </div>

    <!-- ПОПАП ПОЛИТИКИ -->
    <div class="popup-overlay" id="policyPopup">
        <div class="popup" style="max-width: 700px; text-align: left; max-height: 80vh; overflow-y: auto;">
            <span class="icon" style="font-size: 48px;">📋</span>
            <h2 style="text-align: center;">Политика обработки персональных данных</h2>
            <div style="color: #D1D5DB; font-size: 14px; line-height: 1.8; margin: 20px 0;">
                <p><strong>1. Общие положения</strong></p>
                <p>Настоящая политика обработки персональных данных составлена в соответствии с требованиями Федерального закона от 27.07.2006 № 152-ФЗ «О персональных данных» и определяет порядок обработки персональных данных и меры по обеспечению безопасности персональных данных, предпринимаемые ООО «ДОНРАЙТ» (далее – Оператор).</p>
                <p><strong>2. Какие данные мы собираем</strong></p>
                <p>При оформлении заявки на сайте мы собираем следующие персональные данные: имя, телефон, адрес объекта и описание задачи.</p>
                <p><strong>3. Цели обработки данных</strong></p>
                <p>Ваши данные используются исключительно для: связи с вами, уточнения деталей заказа, формирования коммерческого предложения и выполнения обязательств по договору.</p>
                <p><strong>4. Правовые основания</strong></p>
                <p>Обработка данных осуществляется на основании вашего согласия, которое вы даёте, заполняя форму заявки на сайте.</p>
                <p><strong>5. Сроки хранения</strong></p>
                <p>Ваши данные хранятся в течение срока, необходимого для выполнения заказа, и в течение 3 лет после завершения работ для юридической защиты сторон.</p>
                <p><strong>6. Передача данных третьим лицам</strong></p>
                <p>Мы не передаём ваши данные третьим лицам, за исключением случаев, предусмотренных законодательством РФ.</p>
                <p><strong>7. Ваши права</strong></p>
                <p>Вы имеете право отозвать своё согласие на обработку данных в любой момент, направив письменное уведомление на адрес: doneright.st@gmail.com.</p>
                <p><strong>8. Контакты</strong></p>
                <p>По всем вопросам, связанным с обработкой ваших данных, вы можете обратиться к нам по email: doneright.st@gmail.com.</p>
            </div>
            <button class="btn-gold" onclick="closePolicyPopup()" style="width: 100%; text-align: center; padding: 14px;"><i class="fas fa-check"></i> Закрыть</button>
        </div>
    </div>

    <!-- КНОПКА НАВЕРХ -->
    <button class="scroll-top" id="scrollTopBtn"><i class="fas fa-arrow-up"></i></button>

    <script>
        // ===== СЧЁТЧИК (34) =====
        const counterEl = document.getElementById('counter');
        let count = 0;
        const target = 34;
        const interval = setInterval(() => {
            if (count < target) {
                count += Math.floor(target / 20) + 1;
                if (count > target) count = target;
                counterEl.textContent = count.toLocaleString();
            } else {
                clearInterval(interval);
            }
        }, 50);

        // ===== АНИМАЦИЯ ПРИ СКРОЛЛЕ (Intersection Observer) =====
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.fade-up').forEach(el => {
            observer.observe(el);
        });

        // ===== 3D-НАКЛОН КАРТОЧЕК =====
        document.querySelectorAll('.tilt-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 20;
                const rotateY = (centerX - x) / 20;
                card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'rotateX(0) rotateY(0) scale(1)';
            });
        });

        // ===== ИНТЕРАКТИВНЫЕ ЧАСТИЦЫ =====
        const container = document.getElementById('particleContainer');
        const particles = [];
        for (let i = 0; i < 40; i++) {
            const p = document.createElement('div');
            p.className = 'particle';
            p.style.left = Math.random() * 100 + '%';
            p.style.top = Math.random() * 100 + '%';
            p.style.width = (Math.random() * 4 + 2) + 'px';
            p.style.height = p.style.width;
            p.style.opacity = Math.random() * 0.3 + 0.1;
            p.style.animation = `float ${Math.random() * 10 + 10}s ease-in-out infinite`;
            container.appendChild(p);
            particles.push(p);
        }

        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth) * 100;
            const y = (e.clientY / window.innerHeight) * 100;
            particles.forEach((p, i) => {
                const offsetX = (x - 50) * 0.02 * (i % 5) / 2;
                const offsetY = (y - 50) * 0.02 * (i % 7) / 2;
                p.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
            });
        });

        // ===== КНОПКА НАВЕРХ =====
        const scrollBtn = document.getElementById('scrollTopBtn');
        window.addEventListener('scroll', () => {
            scrollBtn.classList.toggle('visible', window.scrollY > 300);
        });
        scrollBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // ===== ПЛАВНЫЙ СКРОЛЛ =====
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });

        // ===== FAQ АККОРДЕОН =====
        document.querySelectorAll('.faq-item').forEach(item => {
            item.addEventListener('click', function() {
                this.classList.toggle('active');
            });
        });

        // ===== ФОРМА (ПОЧИНЕНА) =====
        document.getElementById('contactForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/submit-form', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    document.getElementById('thankYouPopup').classList.add('active');
                    this.reset();
                } else {
                    alert('Ошибка при отправке. Попробуйте ещё раз.');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Ошибка сети. Проверьте подключение.');
            });
        });

        function closePopup() {
            document.getElementById('thankYouPopup').classList.remove('active');
        }

        document.getElementById('thankYouPopup').addEventListener('click', function(e) {
            if (e.target === this) {
                closePopup();
            }
        });

        // ===== ПОЛИТИКА =====
        function openPolicyPopup() {
            document.getElementById('policyPopup').classList.add('active');
        }

        function closePolicyPopup() {
            document.getElementById('policyPopup').classList.remove('active');
        }

        document.getElementById('openPolicy').addEventListener('click', function(e) {
            e.preventDefault();
            openPolicyPopup();
        });

        document.getElementById('openPolicy2').addEventListener('click', function(e) {
            e.preventDefault();
            openPolicyPopup();
        });

        document.getElementById('policyPopup').addEventListener('click', function(e) {
            if (e.target === this) {
                closePolicyPopup();
            }
        });
    </script>

</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.post("/submit-form")
async def submit_form(
    name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(""),
    message: str = Form("")
):
    print(f"📩 НОВАЯ ЗАЯВКА!")
    print(f"Имя: {name}")
    print(f"Телефон: {phone}")
    print(f"Адрес: {address}")
    print(f"Задача: {message}")
    print("-" * 30)

    send_email(name, phone, address, message)

    return RedirectResponse(url="/#form", status_code=303)
