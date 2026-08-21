from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.api.v1.endpoints import auth
from app.core.database import engine, Base
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI(title="ДОНРАЙТ", version="1.0.0")

# ======== НАСТРОЙКИ ПОЧТЫ (ЯНДЕКС) ========
SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 587
SMTP_USER = "DoneRight.st@yandex.ru"
SMTP_PASSWORD = "bvyusmrcodhuvsub"
TO_EMAIL = "DoneRight.st@yandex.ru"

def send_email(name: str, phone: str, address: str, message: str, career: bool = False):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = TO_EMAIL
        if career:
            msg['Subject'] = f"🔧 Новая заявка от мастера: {name}"
        else:
            msg['Subject'] = f"🔧 Новая заявка от {name}"

        body = f"""
        <h2>📩 {'Заявка от мастера' if career else 'Новая заявка с сайта'}</h2>
        <p><strong>👤 Имя:</strong> {name}</p>
        <p><strong>📞 Телефон:</strong> {phone}</p>
        """
        if career:
            body += f"""
            <p><strong>🛠️ Специализация:</strong> {address if address else 'Не указана'}</p>
            <p><strong>📝 Опыт работы:</strong> {message if message else 'Без описания'}</p>
            """
        else:
            body += f"""
            <p><strong>📍 Адрес:</strong> {address if address else 'Не указан'}</p>
            <p><strong>📝 Задача:</strong> {message if message else 'Без описания'}</p>
            """
        body += """
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

# ============================================================
# ГЛАВНАЯ СТРАНИЦА
# ============================================================
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
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #080808;
            color: #FFFFFF;
            line-height: 1.6;
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
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            position: relative;
            z-index: 1;
        }
        .fade-up {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease;
        }
        .fade-up.visible {
            opacity: 1;
            transform: translateY(0);
        }
        .delay-1 { transition-delay: 0.05s; }
        .delay-2 { transition-delay: 0.1s; }
        .delay-3 { transition-delay: 0.15s; }
        .delay-4 { transition-delay: 0.2s; }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.06);
        }
        .logo {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .nav a {
            color: #9CA3AF;
            text-decoration: none;
            margin-left: 24px;
            font-size: 14px;
            font-weight: 500;
            transition: 0.3s;
        }
        .nav a:hover { color: #fff; }
        .btn-gold {
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            color: #0A0A0A;
            padding: 12px 30px;
            border-radius: 60px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .btn-gold:hover { transform: scale(1.04); box-shadow: 0 0 30px rgba(255, 215, 0, 0.2); }
        .hero {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
            padding: 60px 0 80px;
        }
        .hero h1 {
            font-size: 52px;
            font-weight: 800;
            line-height: 1.08;
            letter-spacing: -2px;
        }
        .hero h1 .highlight {
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero .subtitle {
            color: #9CA3AF;
            font-size: 18px;
            margin: 20px 0;
            max-width: 460px;
        }
        .hero .city-tag {
            display: inline-block;
            background: rgba(255, 215, 0, 0.08);
            border: 1px solid rgba(255, 215, 0, 0.1);
            color: #FFD700;
            padding: 4px 16px;
            border-radius: 60px;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 16px;
        }
        .badge-group {
            display: flex;
            gap: 40px;
            margin-top: 32px;
        }
        .badge-group .stat span {
            font-size: 32px;
            font-weight: 700;
            color: #FFD700;
            display: block;
        }
        .badge-group .stat p {
            color: #6B7280;
            font-size: 14px;
        }
        .hero-image {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 24px;
            padding: 40px 30px;
            text-align: center;
        }
        .hero-image .big-icon {
            font-size: 72px;
            display: block;
            margin-bottom: 16px;
        }
        .hero-image h3 { color: #FFD700; font-size: 20px; font-weight: 700; }
        .hero-image p { color: #9CA3AF; font-size: 14px; max-width: 300px; margin: 0 auto; }
        .hero-image .badge-gold {
            display: inline-block;
            background: rgba(255, 215, 0, 0.08);
            border: 1px solid rgba(255, 215, 0, 0.1);
            color: #FFD700;
            padding: 4px 16px;
            border-radius: 60px;
            font-size: 12px;
            margin-top: 16px;
        }
        .trust-counter {
            text-align: center;
            padding: 40px 0 60px;
            border-bottom: 1px solid rgba(255, 215, 0, 0.05);
        }
        .trust-counter .number {
            font-size: 56px;
            font-weight: 800;
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .trust-counter p { color: #9CA3AF; font-size: 16px; margin-top: 4px; }
        .section-block {
            padding: 50px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.05);
        }
        .section-title {
            text-align: center;
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 40px;
        }
        .section-title i { color: #FFD700; margin-right: 10px; }
        .grid-4, .grid-3, .grid-2 {
            display: grid;
            gap: 24px;
        }
        .grid-4 { grid-template-columns: repeat(4, 1fr); }
        .grid-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-2 { grid-template-columns: repeat(2, 1fr); }
        .card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 20px;
            padding: 28px 24px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .card:hover {
            transform: translateY(-4px);
            border-color: rgba(255, 215, 0, 0.1);
        }
        .card .icon { font-size: 36px; display: block; margin-bottom: 12px; }
        .card h4 { color: #FFD700; font-size: 18px; font-weight: 600; margin-bottom: 6px; }
        .card p { color: #9CA3AF; font-size: 14px; line-height: 1.6; }
        .card .tag {
            display: inline-block;
            background: #FFD700;
            color: #0A0A0A;
            font-weight: 600;
            font-size: 10px;
            padding: 2px 12px;
            border-radius: 60px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }
        .card .stars {
            color: #FFD700;
            font-size: 16px;
            letter-spacing: 2px;
            display: block;
            margin-bottom: 8px;
        }
        .card .text {
            color: #D1D5DB;
            font-size: 14px;
            line-height: 1.6;
            font-style: italic;
        }
        .card .author { color: #6B7280; font-size: 13px; margin-top: 8px; }
        .card .author span { color: #FFD700; }
        .step-number {
            display: inline-block;
            width: 44px;
            height: 44px;
            line-height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            color: #0A0A0A;
            font-weight: 700;
            font-size: 16px;
            margin: 0 auto 12px;
        }
        .guarantees .card { text-align: left; }
        .form-section { padding: 60px 0; text-align: center; }
        .form-section h2 { font-size: 36px; font-weight: 700; }
        .form-section .sub { color: #9CA3AF; font-size: 16px; margin-bottom: 32px; }
        .form-box {
            max-width: 520px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            padding: 36px 32px;
            border-radius: 24px;
            text-align: left;
        }
        .form-box label {
            font-weight: 500;
            color: #D1D5DB;
            font-size: 14px;
        }
        .form-box input, .form-box textarea, .form-box select {
            width: 100%;
            padding: 12px 16px;
            margin: 6px 0 18px;
            background: #121212;
            border: 1px solid #222;
            border-radius: 14px;
            color: #fff;
            font-size: 15px;
            transition: 0.3s;
        }
        .form-box input:focus, .form-box textarea:focus, .form-box select:focus {
            outline: none;
            border-color: #FFD700;
            box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.05);
        }
        .form-box select option { background: #121212; }
        .form-box .small-note {
            color: #6B7280;
            font-size: 12px;
            margin-top: 12px;
            text-align: center;
        }
        .btn-gold-full {
            width: 100%;
            text-align: center;
            padding: 14px;
            font-size: 15px;
        }
        footer {
            padding: 24px 0;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            color: #6B7280;
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            flex-wrap: wrap;
            gap: 10px;
        }
        footer a { color: #6B7280; text-decoration: none; transition: 0.3s; }
        footer a:hover { color: #FFD700; }
        .footer-link { cursor: pointer; }
        .popup-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.75);
            backdrop-filter: blur(4px);
            z-index: 9999;
            justify-content: center;
            align-items: center;
        }
        .popup-overlay.active { display: flex; }
        .popup {
            background: #121212;
            border: 1px solid rgba(255, 215, 0, 0.1);
            border-radius: 24px;
            padding: 40px 44px;
            max-width: 480px;
            text-align: center;
        }
        .popup .icon { font-size: 56px; display: block; margin-bottom: 16px; }
        .popup h2 { color: #FFD700; font-size: 24px; font-weight: 700; margin-bottom: 8px; }
        .popup p { color: #9CA3AF; font-size: 15px; margin-bottom: 24px; }
        .popup .popup-text {
            color: #D1D5DB;
            font-size: 14px;
            line-height: 1.7;
            text-align: left;
            margin: 16px 0 24px;
            max-height: 50vh;
            overflow-y: auto;
        }
        .checkbox-group {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin: 12px 0 20px;
        }
        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-top: 2px;
            flex-shrink: 0;
            accent-color: #FFD700;
        }
        .checkbox-group label {
            font-weight: 400;
            color: #9CA3AF;
            font-size: 14px;
            line-height: 1.5;
            cursor: pointer;
        }
        .checkbox-group label a { color: #FFD700; text-decoration: underline; }
        @media (max-width: 768px) {
            .hero { grid-template-columns: 1fr; gap: 30px; padding: 40px 0 60px; }
            .hero h1 { font-size: 34px; }
            .grid-4, .grid-3 { grid-template-columns: 1fr; }
            .grid-2 { grid-template-columns: 1fr; }
            .nav a { display: none; }
            .badge-group { flex-wrap: wrap; gap: 16px; }
            .form-box { padding: 24px 16px; }
            footer { flex-direction: column; text-align: center; }
            .popup { padding: 28px 20px; }
        }
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="container">
        <nav class="navbar fade-up visible">
            <div class="logo">✦ ДОНРАЙТ</div>
            <div class="nav">
                <a href="#why">Почему мы</a>
                <a href="#promo">Акции</a>
                <a href="#reviews">Отзывы</a>
                <a href="#guarantees">Гарантии</a>
                <a href="/career" class="btn-gold" style="padding: 8px 20px; font-size: 13px;"><i class="fas fa-briefcase"></i> Работа у нас</a>
                <a href="#form" class="btn-gold" style="padding: 8px 20px; font-size: 13px;"><i class="fas fa-pen"></i> Заявка</a>
            </div>
        </nav>

        <section class="hero">
            <div class="fade-up visible delay-1">
                <div class="city-tag"><i class="fas fa-map-pin"></i> Железногорск</div>
                <div style="display: inline-block; background: rgba(255, 215, 0, 0.08); border: 1px solid rgba(255, 215, 0, 0.1); color: #FFD700; padding: 4px 16px; border-radius: 60px; font-size: 12px; margin-bottom: 16px;">
                    <i class="fas fa-lock"></i> Оплата после одобрения
                </div>
                <h1>Решим вашу задачу.<br><span class="highlight">Без риска и предоплат.</span></h1>
                <p class="subtitle">Сантехника, электрика, сборка мебели. Отвечаем за результат. Если не нравится — переделаем за свой счёт.</p>
                <a href="#form" class="btn-gold" style="padding: 14px 40px; font-size: 16px;"><i class="fas fa-phone"></i> Вызвать мастера</a>
                <div class="badge-group">
                    <div class="stat"><span>4.9</span><p><i class="fas fa-star" style="color: #FFD700;"></i> Средний рейтинг</p></div>
                    <div class="stat"><span>0 ₽</span><p><i class="fas fa-wallet" style="color: #FFD700;"></i> Плата до результата</p></div>
                    <div class="stat"><span>24 ч</span><p><i class="fas fa-clock" style="color: #FFD700;"></i> Гарантийный срок</p></div>
                </div>
            </div>
            <div class="hero-image fade-up visible delay-2">
                <span class="big-icon">🛠️</span>
                <h3>Ваша безопасность — наш приоритет</h3>
                <p>Мастера в чистой обуви. Работаем строго по договору.</p>
                <span class="badge-gold"><i class="fas fa-check-circle"></i> Передача денег мастеру на руки запрещена</span>
            </div>
        </section>

        <section class="trust-counter fade-up delay-2">
            <div class="number" id="counter">0</div>
            <p><i class="fas fa-users" style="color: #FFD700;"></i> человек в Железногорске уже доверили нам свои задачи</p>
        </section>

        <section class="section-block" id="why">
            <h2 class="section-title fade-up"><i class="fas fa-gem"></i>Почему выбирают нас</h2>
            <div class="grid-4">
                <div class="card fade-up delay-1"><span class="icon">⚡</span><h4>Быстро</h4><p>Приезжаем в течение часа.</p></div>
                <div class="card fade-up delay-2"><span class="icon">💎</span><h4>Надёжно</h4><p>Гарантия 24 месяца.</p></div>
                <div class="card fade-up delay-3"><span class="icon">🤝</span><h4>Честно</h4><p>Цена без сюрпризов.</p></div>
                <div class="card fade-up delay-4"><span class="icon">🧹</span><h4>Аккуратно</h4><p>Убираем за собой.</p></div>
            </div>
        </section>

        <section class="section-block" id="promo">
            <h2 class="section-title fade-up"><i class="fas fa-fire" style="color: #FF8C00;"></i>Наши акции</h2>
            <div class="grid-3">
                <div class="card fade-up delay-1"><span class="tag">Скидка</span><h3 style="color: #FFD700; font-size: 22px;">10%</h3><p>По промокоду <strong style="color: #FFD700;">DONERIGHT10</strong></p></div>
                <div class="card fade-up delay-2"><span class="tag">Бонус</span><h3 style="color: #FFD700; font-size: 20px;">Приведи друга</h3><p>Скидка 10% на следующий заказ</p></div>
                <div class="card fade-up delay-3"><span class="tag">Акция</span><h3 style="color: #FFD700; font-size: 20px;">Пенсионерам</h3><p>Скидка 10% на все услуги</p></div>
            </div>
        </section>

        <section class="section-block" id="reviews">
            <h2 class="section-title fade-up"><i class="fas fa-comment-dots"></i>Отзывы</h2>
            <div class="grid-3">
                <div class="card fade-up delay-1"><span class="stars">★★★★★</span><p class="text">"Сантехника отлично. Приехали быстро, сделали качественно. Оплатил после проверки."</p><div class="author">— Александр, <span>Железногорск</span></div></div>
                <div class="card fade-up delay-2"><span class="stars">★★★★★</span><p class="text">"Собрали мебель. Всё чётко, аккуратно. Мастер со своим инструментом. Рекомендую!"</p><div class="author">— Екатерина, <span>Железногорск</span></div></div>
                <div class="card fade-up delay-3"><span class="stars">★★★★★</span><p class="text">"Электрику делали. Всё проверили, дали гарантию. Оплата после результата — супер."</p><div class="author">— Дмитрий, <span>Железногорск</span></div></div>
            </div>
        </section>

        <section class="section-block" id="steps">
            <h2 class="section-title fade-up"><i class="fas fa-route"></i>Как мы работаем</h2>
            <div class="grid-4">
                <div class="card fade-up delay-1"><div class="step-number">1</div><h4>Заявка</h4><p>Оставляете заявку на сайте или по телефону</p></div>
                <div class="card fade-up delay-2"><div class="step-number">2</div><h4>Оценка</h4><p>Оцениваем объём работ и называем точную цену</p></div>
                <div class="card fade-up delay-3"><div class="step-number">3</div><h4>Работа</h4><p>Выполняем задачу качественно и в срок</p></div>
                <div class="card fade-up delay-4"><div class="step-number">4</div><h4>Оплата</h4><p>Вы проверяете результат и платите только после одобрения</p></div>
            </div>
        </section>

        <section class="section-block" id="guarantees">
            <h2 class="section-title fade-up"><i class="fas fa-shield"></i>Наши гарантии</h2>
            <div class="grid-3 guarantees">
                <div class="card fade-up delay-1"><span class="icon" style="font-size: 32px;">💰</span><h4>Платите после</h4><p>Только после личной приёмки работы. Без скрытых комиссий.</p></div>
                <div class="card fade-up delay-2"><span class="icon" style="font-size: 32px;">🛡️</span><h4>Гарантия качества</h4><p>Сделали криво? Исправим за свой счёт или вернём деньги.</p></div>
                <div class="card fade-up delay-3"><span class="icon" style="font-size: 32px;">📄</span><h4>Работаем по закону</h4><p>Для заказов от 10 000 ₽ заключаем официальный договор.</p></div>
            </div>
        </section>

        <!-- ===== БЛОК КОНТАКТОВ ===== -->
        <section class="section-block" style="border-bottom: none; padding: 30px 0 40px;">
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; max-width: 800px; margin: 0 auto;">
                <a href="mailto:DoneRight.st@yandex.ru" style="display: flex; align-items: center; gap: 10px; color: #9CA3AF; text-decoration: none; padding: 10px 24px; background: rgba(255, 215, 0, 0.03); border-radius: 60px; border: 1px solid rgba(255, 215, 0, 0.06); transition: 0.3s;">
                    <i class="fas fa-envelope" style="color: #FFD700; font-size: 18px;"></i>
                    <span style="color: #fff;">DoneRight.st@yandex.ru</span>
                </a>
                <a href="https://vk.ru/doneright" target="_blank" style="display: flex; align-items: center; gap: 10px; color: #9CA3AF; text-decoration: none; padding: 10px 24px; background: rgba(255, 215, 0, 0.03); border-radius: 60px; border: 1px solid rgba(255, 215, 0, 0.06); transition: 0.3s;">
                    <i class="fab fa-vk" style="color: #4C75A3; font-size: 20px;"></i>
                    <span style="color: #fff;">Сообщество ВК</span>
                </a>
                <a href="https://t.me/DoneRight_bot" target="_blank" style="display: flex; align-items: center; gap: 10px; color: #9CA3AF; text-decoration: none; padding: 10px 24px; background: rgba(255, 215, 0, 0.03); border-radius: 60px; border: 1px solid rgba(255, 215, 0, 0.06); transition: 0.3s;">
                    <i class="fab fa-telegram-plane" style="color: #0088cc; font-size: 20px;"></i>
                    <span style="color: #fff;">Telegram-бот</span>
                </a>
            </div>
        </section>

        <!-- ===== ФОРМА ===== -->
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
                    <button type="submit" class="btn-gold btn-gold-full"><i class="fas fa-paper-plane"></i> Отправить заявку →</button>
                    <div class="small-note">
                        <i class="fas fa-check-circle" style="color: #FFD700;"></i> Никаких скрытых платежей.<br>
                        Нажимая «Отправить», вы соглашаетесь с <a href="#" id="openPolicy" style="color: #FFD700; text-decoration: underline;">политикой обработки персональных данных</a>.
                    </div>
                </form>
            </div>
        </section>

        <footer>
            <span>© 2026 ДОНРАЙТ. Работаем честно в Железногорске.</span>
            <span>
                <a href="#" id="openPolicy2" style="color: #6B7280; text-decoration: none; transition: 0.3s;"><i class="fas fa-lock" style="margin-right: 6px;"></i>Политика конфиденциальности</a>
                <span style="margin: 0 10px; color: #333;">|</span>
                <a href="#" id="openSupport" class="footer-link" style="color: #6B7280; text-decoration: none; transition: 0.3s;"><i class="fas fa-heart" style="margin-right: 4px;"></i>Поддержать ДОНРАЙТ</a>
            </span>
        </footer>
    </div>

    <!-- ПОПАПЫ -->
    <div class="popup-overlay" id="thankYouPopup">
        <div class="popup">
            <span class="icon">🎉</span>
            <h2>Заявка отправлена!</h2>
            <p>Мы перезвоним вам в течение 5 минут. Спасибо за доверие!</p>
            <button class="btn-gold" onclick="closePopup()"><i class="fas fa-check"></i> Отлично!</button>
        </div>
    </div>

    <div class="popup-overlay" id="policyPopup">
        <div class="popup" style="max-width: 700px; text-align: left; max-height: 80vh; overflow-y: auto;">
            <span class="icon" style="font-size: 48px;">📋</span>
            <h2 style="text-align: center;">Политика обработки персональных данных</h2>
            <div class="popup-text">
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
                <p>Вы имеете право отозвать своё согласие на обработку данных в любой момент, направив письменное уведомление на адрес: DoneRight.st@yandex.ru.</p>
                <p><strong>8. Контакты</strong></p>
                <p>По всем вопросам, связанным с обработкой ваших данных, вы можете обратиться к нам по email: DoneRight.st@yandex.ru.</p>
            </div>
            <button class="btn-gold" onclick="closePolicyPopup()" style="width: 100%; text-align: center; padding: 14px;"><i class="fas fa-check"></i> Закрыть</button>
        </div>
    </div>

    <div class="popup-overlay" id="supportPopup">
        <div class="popup">
            <span class="icon">💛</span>
            <h2 style="text-align: center;">Вы можете помочь нашей компании стать лучше!</h2>
            <div class="popup-text">
                <p>Если каждый из вас скинет по 1 рублю, мы сможем быстрее развиваться, покупать лучшие инструменты и нанимать больше мастеров.</p>
                <p><strong>Как это сделать?</strong></p>
                <p>Напишите нашему оператору или на почту <a href="mailto:DoneRight.st@yandex.ru" style="color: #FFD700;">DoneRight.st@yandex.ru</a>.</p>
                <p>Мы расскажем, как именно вы можете поддержать нас.</p>
                <p style="color: #6B7280; font-size: 14px; margin-top: 16px;">*Даже 1 рубль — это вклад в качество вашего сервиса.</p>
            </div>
            <button class="btn-gold" onclick="closeSupportPopup()" style="width: 100%; text-align: center; padding: 14px;"><i class="fas fa-check"></i> Закрыть</button>
        </div>
    </div>

    <!-- КНОПКА НАВЕРХ -->
    <button class="scroll-top" id="scrollTopBtn" style="position: fixed; bottom: 30px; right: 30px; background: linear-gradient(135deg, #FFD700, #FF8C00); color: #0A0A0A; width: 48px; height: 48px; border-radius: 50%; border: none; font-size: 20px; cursor: pointer; box-shadow: 0 0 20px rgba(255, 215, 0, 0.15); transition: all 0.3s ease; opacity: 0; visibility: hidden; z-index: 999;">
        <i class="fas fa-arrow-up"></i>
    </button>

    <script>
        // Счётчик
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

        // Анимация при скролле
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

        // Кнопка наверх
        const scrollBtn = document.getElementById('scrollTopBtn');
        window.addEventListener('scroll', () => {
            scrollBtn.classList.toggle('visible', window.scrollY > 300);
        });
        scrollBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // Плавный скролл
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

        // Форма
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

        // Политика
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

        // Поддержка
        function openSupportPopup() {
            document.getElementById('supportPopup').classList.add('active');
        }
        function closeSupportPopup() {
            document.getElementById('supportPopup').classList.remove('active');
        }
        document.getElementById('openSupport').addEventListener('click', function(e) {
            e.preventDefault();
            openSupportPopup();
        });
        document.getElementById('supportPopup').addEventListener('click', function(e) {
            if (e.target === this) {
                closeSupportPopup();
            }
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

# ============================================================
# СТРАНИЦА ДЛЯ МАСТЕРОВ / CAREER
# ============================================================
@app.get("/career", response_class=HTMLResponse)
async def career(request: Request):
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Работа в ДОНРАЙТ — стань частью команды</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #080808;
            color: #FFFFFF;
            line-height: 1.6;
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
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            position: relative;
            z-index: 1;
        }
        .fade-up {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease;
        }
        .fade-up.visible {
            opacity: 1;
            transform: translateY(0);
        }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.06);
        }
        .logo {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .nav a {
            color: #9CA3AF;
            text-decoration: none;
            margin-left: 24px;
            font-size: 14px;
            font-weight: 500;
            transition: 0.3s;
        }
        .nav a:hover { color: #fff; }
        .btn-gold {
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            color: #0A0A0A;
            padding: 12px 30px;
            border-radius: 60px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .btn-gold:hover { transform: scale(1.04); box-shadow: 0 0 30px rgba(255, 215, 0, 0.2); }
        .page-title {
            text-align: center;
            padding: 30px 0 20px;
        }
        .page-title h1 {
            font-size: 44px;
            font-weight: 800;
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .page-title p {
            color: #9CA3AF;
            font-size: 18px;
            margin-top: 8px;
        }
        .section-block {
            padding: 40px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.05);
        }
        .section-block:last-of-type { border-bottom: none; }
        .section-block h2 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 20px;
            color: #FFD700;
        }
        .section-block p {
            color: #D1D5DB;
            font-size: 16px;
            line-height: 1.8;
            max-width: 800px;
        }
        .section-block ul {
            list-style: none;
            padding: 0;
            margin-top: 12px;
        }
        .section-block ul li {
            color: #D1D5DB;
            font-size: 16px;
            padding: 6px 0;
            padding-left: 28px;
            position: relative;
        }
        .section-block ul li::before {
            content: '✦';
            color: #FFD700;
            position: absolute;
            left: 0;
        }
        .form-section {
            padding: 50px 0 60px;
            text-align: center;
        }
        .form-section h2 {
            font-size: 32px;
            font-weight: 700;
            color: #FFD700;
            margin-bottom: 8px;
        }
        .form-section .sub {
            color: #9CA3AF;
            font-size: 16px;
            margin-bottom: 32px;
        }
        .form-box {
            max-width: 520px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            padding: 36px 32px;
            border-radius: 24px;
            text-align: left;
        }
        .form-box label {
            font-weight: 500;
            color: #D1D5DB;
            font-size: 14px;
        }
        .form-box input, .form-box textarea, .form-box select {
            width: 100%;
            padding: 12px 16px;
            margin: 6px 0 18px;
            background: #121212;
            border: 1px solid #222;
            border-radius: 14px;
            color: #fff;
            font-size: 15px;
            transition: 0.3s;
        }
        .form-box input:focus, .form-box textarea:focus, .form-box select:focus {
            outline: none;
            border-color: #FFD700;
            box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.05);
        }
        .form-box select option { background: #121212; }
        .form-box .small-note {
            color: #6B7280;
            font-size: 12px;
            margin-top: 12px;
            text-align: center;
        }
        .btn-gold-full {
            width: 100%;
            text-align: center;
            padding: 14px;
            font-size: 15px;
        }
        .checkbox-group {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin: 12px 0 20px;
        }
        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-top: 2px;
            flex-shrink: 0;
            accent-color: #FFD700;
        }
        .checkbox-group label {
            font-weight: 400;
            color: #9CA3AF;
            font-size: 14px;
            line-height: 1.5;
            cursor: pointer;
        }
        .checkbox-group label a { color: #FFD700; text-decoration: underline; }
        footer {
            padding: 24px 0;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            color: #6B7280;
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            flex-wrap: wrap;
            gap: 10px;
        }
        footer a { color: #6B7280; text-decoration: none; transition: 0.3s; }
        footer a:hover { color: #FFD700; }
        .footer-link { cursor: pointer; }
        .popup-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.75);
            backdrop-filter: blur(4px);
            z-index: 9999;
            justify-content: center;
            align-items: center;
        }
        .popup-overlay.active { display: flex; }
        .popup {
            background: #121212;
            border: 1px solid rgba(255, 215, 0, 0.1);
            border-radius: 24px;
            padding: 32px 36px;
            max-width: 480px;
            text-align: center;
        }
        .popup .icon { font-size: 56px; display: block; margin-bottom: 16px; }
        .popup h2 { color: #FFD700; font-size: 24px; font-weight: 700; margin-bottom: 8px; }
        .popup p { color: #9CA3AF; font-size: 15px; margin-bottom: 24px; }
        .popup .popup-text {
            color: #D1D5DB;
            font-size: 14px;
            line-height: 1.7;
            text-align: left;
            margin: 16px 0 24px;
            max-height: 50vh;
            overflow-y: auto;
        }
        @media (max-width: 768px) {
            .page-title h1 { font-size: 30px; }
            .nav a { display: none; }
            .form-box { padding: 24px 16px; }
            footer { flex-direction: column; text-align: center; }
            .popup { padding: 24px 16px; }
        }
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="container">
        <nav class="navbar fade-up visible">
            <a href="/" style="text-decoration: none;"><div class="logo">✦ ДОНРАЙТ</div></a>
            <div class="nav">
                <a href="/#why">Почему мы</a>
                <a href="/#promo">Акции</a>
                <a href="/#reviews">Отзывы</a>
                <a href="/#guarantees">Гарантии</a>
                <a href="/" class="btn-gold" style="padding: 8px 20px; font-size: 13px;"><i class="fas fa-arrow-left"></i> На главную</a>
            </div>
        </nav>

        <div class="page-title fade-up visible">
            <h1>Стань частью команды ДОНРАЙТ</h1>
            <p>Мы ищем ответственных мастеров в Железногорске. Работай с нами — работай с уверенностью.</p>
        </div>

        <div class="section-block fade-up">
            <h2><i class="fas fa-users" style="color: #FFD700; margin-right: 12px;"></i>Почему работать на нас лучше?</h2>
            <p>В некоторых местах мастеров бросают как расходный материал: заказ дали — сделали — забыли. Никакой стабильности, никакой защиты.</p>
            <p style="margin-top: 12px;"><strong style="color: #FFD700;">У нас по-другому:</strong></p>
            <ul>
                <li>Ты не просто «исполнитель на час». Ты — часть команды, за которой стоит компания.</li>
                <li>Мы даём стабильный поток заказов, а не разовые смены.</li>
                <li>Мы несём ответственность за клиента и за тебя.</li>
            </ul>
        </div>

        <div class="section-block fade-up">
            <h2><i class="fas fa-clock" style="color: #FFD700; margin-right: 12px;"></i>Гибкий и свободный график</h2>
            <p>Ты сам выбираешь, когда работать:</p>
            <ul>
                <li>Хочешь взять выходной? — Пожалуйста.</li>
                <li>Хочешь работать по 5 часов в день? — Договоримся.</li>
                <li>Есть семья или учёба? — Подстроим график под тебя.</li>
            </ul>
        </div>

        <div class="section-block fade-up">
            <h2><i class="fas fa-coins" style="color: #FFD700; margin-right: 12px;"></i>Премии и бонусы</h2>
            <ul>
                <li><strong style="color: #FFD700;">Премия за качество</strong> — если клиент оставил 5⭐ и написал благодарность.</li>
                <li><strong style="color: #FFD700;">Премия за скорость</strong> — если сделал работу быстрее срока.</li>
                <li><strong style="color: #FFD700;">Премия за лояльность</strong> — если работаешь с нами больше 3 месяцев.</li>
            </ul>
            <p style="margin-top: 12px;">Бонусы выплачиваем отдельно, сверх зарплаты.</p>
        </div>

        <div class="section-block fade-up">
            <h2><i class="fas fa-arrow-trend-up" style="color: #FFD700; margin-right: 12px;"></i>От мастера до руководителя</h2>
            <ul>
                <li>Через 6–12 месяцев ты сможешь стать <strong style="color: #FFD700;">бригадиром</strong>.</li>
                <li>Через 1–2 года — <strong style="color: #FFD700;">руководителем направления</strong>.</li>
            </ul>
            <p style="margin-top: 12px;">Мы учим, поддерживаем и растем вместе.</p>
        </div>

        <div class="section-block fade-up">
            <h2><i class="fas fa-shield-halved" style="color: #FFD700; margin-right: 12px;"></i>Почему работать с нами лучше?</h2>
            <p>Когда ты работаешь на себя через доски объявлений:</p>
            <ul>
                <li>Ты сам ищешь заказы и платишь за продвижение.</li>
                <li>Клиенты могут не заплатить или «кинуть» на деньги.</li>
                <li>Никто не защищает тебя от недобросовестных заказчиков.</li>
            </ul>
            <p style="margin-top: 12px;"><strong style="color: #FFD700;">У нас:</strong></p>
            <ul>
                <li>Заказы мы даём тебе — ты только делаешь работу.</li>
                <li>Гарантируем оплату.</li>
                <li>Если клиент пытается обмануть — с ним разбираются наши юристы.</li>
            </ul>
        </div>

        <section class="form-section fade-up">
            <h2><i class="fas fa-pen-to-square" style="color: #FFD700; margin-right: 12px;"></i>Заполните форму</h2>
            <p class="sub">Оставьте свои данные, и мы перезвоним в течение 24 часов.</p>
            <div class="form-box">
                <form id="careerForm" action="/submit-career" method="post">
                    <label><i class="fas fa-user" style="color: #FFD700;"></i> Ваше имя</label>
                    <input type="text" name="name" placeholder="Иван Петров" required>
                    <label><i class="fas fa-phone" style="color: #FFD700;"></i> Телефон</label>
                    <input type="tel" name="phone" placeholder="+7 (999) 123-45-67" required>
                    <label><i class="fas fa-tools" style="color: #FFD700;"></i> Специализация</label>
                    <select name="specialization" required>
                        <option value="">Выберите специализацию</option>
                        <option value="Сантехник">Сантехник</option>
                        <option value="Электрик">Электрик</option>
                        <option value="Сборщик мебели">Сборщик мебели</option>
                        <option value="Отделочник">Отделочник</option>
                        <option value="Разнорабочий">Разнорабочий</option>
                        <option value="Другое">Другое</option>
                    </select>
                    <label><i class="fas fa-file-alt" style="color: #FFD700;"></i> Опыт работы</label>
                    <textarea name="experience" rows="4" placeholder="Расскажите о своём опыте..."></textarea>

                    <div class="checkbox-group">
                        <input type="checkbox" id="consentCareer" name="consent" required>
                        <label for="consentCareer">
                            Я соглашаюсь на <a href="#" id="openPolicyCareer" style="color: #FFD700; text-decoration: underline;">обработку персональных данных</a> и подтверждаю, что ознакомлен с политикой конфиденциальности.
                        </label>
                    </div>

                    <button type="submit" class="btn-gold btn-gold-full"><i class="fas fa-paper-plane"></i> Отправить заявку</button>
                    <div class="small-note">Поля, отмеченные *, обязательны для заполнения.</div>
                </form>
            </div>
        </section>

        <footer>
            <span>© 2026 ДОНРАЙТ. Работаем честно в Железногорске.</span>
            <span>
                <a href="#" id="openPolicyCareerFooter" style="color: #6B7280; text-decoration: none; transition: 0.3s;"><i class="fas fa-lock" style="margin-right: 6px;"></i>Политика конфиденциальности</a>
                <span style="margin: 0 10px; color: #333;">|</span>
                <a href="#" id="openSupportCareer" class="footer-link" style="color: #6B7280; text-decoration: none; transition: 0.3s;"><i class="fas fa-heart" style="margin-right: 4px;"></i>Поддержать ДОНРАЙТ</a>
            </span>
        </footer>
    </div>

    <div class="popup-overlay" id="thankYouCareerPopup">
        <div class="popup">
            <span class="icon">🎉</span>
            <h2>Заявка отправлена!</h2>
            <p>Мы свяжемся с вами в течение 24 часов. Спасибо!</p>
            <button class="btn-gold" onclick="closeCareerPopup()"><i class="fas fa-check"></i> Отлично!</button>
        </div>
    </div>

    <div class="popup-overlay" id="policyPopupCareer">
        <div class="popup" style="max-width: 700px; text-align: left; max-height: 80vh; overflow-y: auto;">
            <span class="icon" style="font-size: 48px;">📋</span>
            <h2 style="text-align: center;">Политика обработки персональных данных</h2>
            <div class="popup-text">
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
                <p>Вы имеете право отозвать своё согласие на обработку данных в любой момент, направив письменное уведомление на адрес: DoneRight.st@yandex.ru.</p>
                <p><strong>8. Контакты</strong></p>
                <p>По всем вопросам, связанным с обработкой ваших данных, вы можете обратиться к нам по email: DoneRight.st@yandex.ru.</p>
            </div>
            <button class="btn-gold" onclick="closePolicyCareerPopup()" style="width: 100%; text-align: center; padding: 14px;"><i class="fas fa-check"></i> Закрыть</button>
        </div>
    </div>

    <div class="popup-overlay" id="supportCareerPopup">
        <div class="popup">
            <span class="icon">💛</span>
            <h2 style="text-align: center;">Вы можете помочь нашей компании стать лучше!</h2>
            <div class="popup-text">
                <p>Если каждый из вас скинет по 1 рублю, мы сможем быстрее развиваться.</p>
                <p><strong>Как это сделать?</strong></p>
                <p>Напишите нашему оператору или на почту <a href="mailto:DoneRight.st@yandex.ru" style="color: #FFD700;">DoneRight.st@yandex.ru</a>.</p>
                <p style="color: #6B7280; font-size: 14px; margin-top: 16px;">*Даже 1 рубль — это вклад в качество вашего сервиса.</p>
            </div>
            <button class="btn-gold" onclick="closeSupportCareerPopup()" style="width: 100%; text-align: center; padding: 14px;"><i class="fas fa-check"></i> Закрыть</button>
        </div>
    </div>

    <button class="scroll-top" id="scrollTopBtnCareer" style="position: fixed; bottom: 30px; right: 30px; background: linear-gradient(135deg, #FFD700, #FF8C00); color: #0A0A0A; width: 48px; height: 48px; border-radius: 50%; border: none; font-size: 20px; cursor: pointer; box-shadow: 0 0 20px rgba(255, 215, 0, 0.15); transition: all 0.3s ease; opacity: 0; visibility: hidden; z-index: 999;">
        <i class="fas fa-arrow-up"></i>
    </button>

    <script>
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

        const scrollBtn = document.getElementById('scrollTopBtnCareer');
        window.addEventListener('scroll', () => {
            scrollBtn.classList.toggle('visible', window.scrollY > 300);
        });
        scrollBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

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

        document.getElementById('careerForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/submit-career', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    document.getElementById('thankYouCareerPopup').classList.add('active');
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

        function closeCareerPopup() {
            document.getElementById('thankYouCareerPopup').classList.remove('active');
        }
        document.getElementById('thankYouCareerPopup').addEventListener('click', function(e) {
            if (e.target === this) {
                closeCareerPopup();
            }
        });

        function openPolicyCareerPopup() {
            document.getElementById('policyPopupCareer').classList.add('active');
        }
        function closePolicyCareerPopup() {
            document.getElementById('policyPopupCareer').classList.remove('active');
        }
        document.querySelectorAll('#openPolicyCareer, #openPolicyCareerFooter').forEach(el => {
            el.addEventListener('click', function(e) {
                e.preventDefault();
                openPolicyCareerPopup();
            });
        });
        document.getElementById('policyPopupCareer').addEventListener('click', function(e) {
            if (e.target === this) {
                closePolicyCareerPopup();
            }
        });

        function openSupportCareerPopup() {
            document.getElementById('supportCareerPopup').classList.add('active');
        }
        function closeSupportCareerPopup() {
            document.getElementById('supportCareerPopup').classList.remove('active');
        }
        document.getElementById('openSupportCareer').addEventListener('click', function(e) {
            e.preventDefault();
            openSupportCareerPopup();
        });
        document.getElementById('supportCareerPopup').addEventListener('click', function(e) {
            if (e.target === this) {
                closeSupportCareerPopup();
            }
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

# ============================================================
# ОБРАБОТЧИКИ
# ============================================================
@app.post("/submit-career")
async def submit_career(
    name: str = Form(...),
    phone: str = Form(...),
    specialization: str = Form(""),
    experience: str = Form(""),
    consent: str = Form(...)
):
    if consent != "on":
        return RedirectResponse(url="/career?error=consent", status_code=303)

    print(f"📩 НОВАЯ ЗАЯВКА ОТ МАСТЕРА!")
    print(f"Имя: {name}")
    print(f"Телефон: {phone}")
    print(f"Специализация: {specialization if specialization else 'Не указана'}")
    print(f"Опыт: {experience if experience else 'Без описания'}")
    print("-" * 30)

    send_email(name, phone, specialization, experience, career=True)
    return RedirectResponse(url="/career#form", status_code=303)

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

    send_email(name, phone, address, message, career=False)
    return RedirectResponse(url="/#form", status_code=303)
