#!/usr/bin/env python3
"""Generates the static pages of rafal.lagowski.es into the repository root.

The site itself has no build step: the generated HTML is committed and served
as is. This script only exists so the three languages stay in one place.
Run from the repository root:  python3 tools/gen.py
"""
import hashlib, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://rafal.lagowski.es'

# ---- values still waiting for Rafał (None = show a visible placeholder) ----
DAY_RATE = '800'
LINKEDIN = 'https://www.linkedin.com/in/rafallagowski/'
VIDEO = None             # YouTube video id (unlisted) or 'files/veracrew-demo.mp4'

GITHUB = 'https://github.com/rafeekpro'      # Rafał as a person
ORG = 'https://github.com/lagowski'          # project repositories
MEDIUM = 'https://rlagowski.medium.com/'
ARTICLE = 'https://rlagowski.medium.com/puede-la-ia-ayudar-contra-la-pobreza-o-solo-empeorarla-a51ecd1c382c'
NOTEBOOK = 'https://colab.research.google.com/github/rafeekpro/ai-social-benefits-demo/blob/main/ai_social_benefits_demo.ipynb'


def E(en, es, pl):
    """One text in three languages; English is the no-JS default."""
    return (f'<span class="l en" lang="en">{en}</span>'
            f'<span class="l es" lang="es">{es}</span>'
            f'<span class="l pl" lang="pl">{pl}</span>')


def pending(name):
    return f'<span class="pending">[{name}]</span>'


def v(path):
    """Cache-busting query from the file's content, so a new deploy never meets a stale stylesheet."""
    with open(os.path.join(ROOT, path), 'rb') as fh:
        return path + '?v=' + hashlib.sha256(fh.read()).hexdigest()[:10]


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


NAV = [
    ('index.html#solutions', E('Solutions', 'Soluciones', 'Rozwiązania'), None),
    ('work-with-me.html', E('How I work', 'Cómo trabajo', 'Jak pracuję'), 'work'),
    ('index.html#cases', E('Cases', 'Casos', 'Realizacje'), None),
    ('about.html', E('About', 'Sobre mí', 'O mnie'), 'about'),
    ('index.html#contact', E('Contact', 'Contacto', 'Kontakt'), None),
]

EARLY = ("<script>(function(){var l='es';try{var s=localStorage.getItem('lagowski-lang');"
         "if(s==='en'||s==='es'||s==='pl')l=s;else{var n=(navigator.language||'en').slice(0,2).toLowerCase();"
         "if(n==='es'||n==='en'||n==='pl')l=n}}catch(e){}window.__lang=l;document.body.className=l;document.documentElement.classList.add('js')})()</script>")


def cv_button(cls='btn primary'):
    """The CV is not published; it is sent on request through the contact form."""
    return f'<a class="{cls}" href="index.html?topic=role#contact">{E("Request my CV", "Pedir mi CV", "Poproś o CV")}</a>'


def linkedin_link(cls=''):
    if LINKEDIN:
        return f'<a href="{LINKEDIN}" rel="me">LinkedIn</a>'
    return ''


def contact_block():
    req = ' required'
    def o(v, t):
        es, en, pl = (t.split(' · ') + [t, t])[:3]
        return f'<option value="{v}" data-es="{es}" data-en="{en}" data-pl="{pl}">{es}</option>'
    opts = ''.join(o(v, t) for v, t in (
        ('automate', 'Automatizar procesos repetitivos · Automate repetitive processes · Automatyzacja powtarzalnych procesów'),
        ('documents', 'Procesar documentos o solicitudes · Process documents or requests · Dokumenty lub zgłoszenia'),
        ('ai_system', 'Construir o mejorar un sistema de IA · Build or improve an AI system · Budowa lub ulepszenie systemu AI'),
        ('role', 'Puesto / CV · Role / CV · Stanowisko / CV'),
        ('demo', 'Demo de veraCrew · veraCrew demo · Demo veraCrew'),
        ('other', 'Otro · Other · Inne')))
    budgets = ''.join(o(v, t) for v, t in (
        ('', '—'), ('3-5k', '3.000–5.000 €'), ('5-10k', '5.000–10.000 €'), ('10k+', '10.000 € +'),
        ('unknown', 'Aún no lo sé · Not sure yet · Jeszcze nie wiem')))
    return f'''<section class="contact" id="contact" aria-labelledby="contact-h"><h2 class="s" id="contact-h">{E('Tell me which process is costing you money', 'Cuéntame qué proceso te está costando dinero', 'Powiedz mi, który proces kosztuje Cię pieniądze')}</h2>
<p class="intro">{E('First conversation with no commitment. If AI adds no real value in your case, I will tell you. I reply by email within two working days.', 'Primera conversación sin compromiso. Si la IA no aporta valor real a tu caso, te lo diré. Respondo por correo en dos días laborables.', 'Pierwsza rozmowa bez zobowiązań. Jeśli AI nie wniesie realnej wartości w Twoim przypadku, powiem Ci to. Odpowiadam mailem w ciągu dwóch dni roboczych.')}</p>
<form class="cform" id="cform" action="/api/contact" method="post">
<div class="f2"><label>{E('Name', 'Nombre', 'Imię i nazwisko')}<input name="name" autocomplete="name" maxlength="120"{req}></label>
<label>{E('Email', 'Correo electrónico', 'E-mail')}<input name="email" type="email" autocomplete="email" maxlength="254"{req}></label></div>
<div class="f2"><label>{E('Company (optional)', 'Empresa (opcional)', 'Firma (opcjonalnie)')}<input name="company" autocomplete="organization" maxlength="160"></label>
<label>{E('Main challenge', 'Principal reto', 'Główne wyzwanie')}<select name="topic" id="ctopic">{opts}</select></label></div>
<label>{E('Indicative monthly budget (optional)', 'Presupuesto mensual orientativo (opcional)', 'Orientacyjny budżet miesięczny (opcjonalnie)')}<select name="budget">{budgets}</select></label>
<label>{E('Briefly describe your project', 'Describe brevemente tu proyecto', 'Krótko opisz swój projekt')}<textarea name="message" rows="5" minlength="10" maxlength="5000"{req}></textarea></label>
<div class="hp" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
<input type="hidden" name="t" id="ct"><input type="hidden" name="lang" id="clang" value="en">
<div class="fend"><button class="btn primary" type="submit">{E('Send', 'Enviar', 'Wyślij')}</button>
<p class="fnote">{E('Your details are used only to answer you and are not stored on this site.', 'Tus datos solo se usan para responderte y no se guardan en esta web.', 'Twoje dane służą wyłącznie do odpowiedzi i nie są przechowywane na tej stronie.')}</p></div>
<p class="fstatus" id="cstatus" role="status" aria-live="polite"></p>
</form>
<div class="links">{linkedin_link()}<a href="{GITHUB}" rel="me">GitHub</a><a href="{MEDIUM}" rel="me">Medium</a></div>
</section>'''


FOOTER = f'''<footer><nav aria-label="{esc('Footer')}"><a href="career.html">{E('Career', 'Carrera', 'Kariera')}</a><a href="veracrew.html">veraCrew</a><a href="about.html">{E('About', 'Sobre mí', 'O mnie')}</a><a href="process.html">{E('Process', 'Proceso', 'Proces')}</a><a href="faq.html">FAQ</a><a href="demos.html">{E('Demos', 'Demos', 'Dema')}</a><a href="work-with-me.html">{E('Work with me', 'Trabajar conmigo', 'Współpraca')}</a></nav>
<p>© 2026 Rafał Łagowski · Madrid · rafal.lagowski.es</p></footer>'''


def page(fname, key, titles, desc, main, extra_head='', scripts=('assets/site.js',), prefix=''):
    canon = BASE + '/' + ('' if fname == 'index.html' else fname)
    nav = ''.join(
        f'<a href="{prefix}{h}"{" aria-current=\"page\"" if k and k == key else ""}>{t}</a>' for h, t, k in NAV)
    t_en, t_es, t_pl = titles
    scr = ''.join(f'<script src="{prefix}{v(s)}" defer></script>' for s in scripts)
    canon_tag = '' if fname == '404.html' else f'<link rel="canonical" href="{canon}">'
    return f'''<!doctype html>
<html lang="en" data-title-en="{esc(t_en)}" data-title-es="{esc(t_es)}" data-title-pl="{esc(t_pl)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t_en}</title>
<meta name="description" content="{esc(desc)}">
{canon_tag}
<meta name="theme-color" content="#f6f5f2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#141317" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{prefix}favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png">
<link rel="preload" href="{prefix}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefix}{v('assets/fonts.css')}">
<link rel="stylesheet" href="{prefix}{v('assets/site.css')}">
<meta property="og:type" content="{'profile' if fname == 'index.html' else 'website'}">
<meta property="og:site_name" content="Rafał Łagowski">
<meta property="og:title" content="{esc(t_en)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rafał Łagowski, AI &amp; Agentic Systems Architect. AI in production, governed from day one.">
<meta property="og:locale" content="en_GB">
<meta property="og:locale:alternate" content="es_ES">
<meta property="og:locale:alternate" content="pl_PL">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(t_en)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}/assets/og.png">
{extra_head}</head>
<body>
{EARLY}
<a class="skip" href="#main">{E('Skip to content', 'Ir al contenido', 'Przejdź do treści')}</a>
<div class="wrap"><header>
  <a class="brand" href="{prefix}index.html">Rafał Łagowski<small>{E('AI &amp; Agentic Systems Architect', 'Arquitecto de IA y sistemas agénticos', 'Architekt AI i systemów agentowych')}</small></a>
  <div class="langs" role="group" aria-label="Language"><button type="button" data-l="en" aria-pressed="true">EN</button><button type="button" data-l="es" aria-pressed="false">ES</button><button type="button" data-l="pl" aria-pressed="false">PL</button></div>
  <button type="button" class="menu-btn" aria-expanded="false" aria-controls="mainnav"><span aria-hidden="true">☰</span> {E('Menu', 'Menú', 'Menu')}</button>
  <nav id="mainnav" aria-label="Main">{nav}</nav>
</header>
{art_band(fname, prefix)}
<main id="main">
{main}
</main>
{FOOTER}</div>
{scr}
</body>
</html>
'''


ART = sorted(d for d in os.listdir(os.path.join(ROOT, 'assets', 'art')) if os.path.isdir(os.path.join(ROOT, 'assets', 'art', d)))


def art_band(fname, prefix=''):
    """Full-width paper picture from labs.lagowski.es under the header; one of ART at random on every load."""
    sub = '' if fname == 'index.html' else ' sub'
    names = json.dumps(ART)
    first = ART[0]
    def css(n):
        b = f"/assets/art/{n}/"  # absolute: a url() inside a custom property resolves against site.css, not the page
        return f"--art-l:url({b}light-1672.webp);--art-d:url({b}dark-1672.webp)"
    # the inline script swaps the default for a random set before first paint
    return (f'<div class="art{sub}" id="art" aria-hidden="true" style="{css(first)}"></div>'
            f"<script>(function(){{var a={names},n=a[Math.floor(Math.random()*a.length)],b='/assets/art/'+n+'/',e=document.getElementById('art');"
            "e.style.setProperty('--art-l','url('+b+'light-1672.webp)');"
            "e.style.setProperty('--art-d','url('+b+'dark-1672.webp)')})()</script>")


def ph(h1, intro):
    return f'<h1 class="ph">{h1}</h1><p class="intro">{intro}</p>'


# ---------------------------------------------------------------- home
def video_slot():
    if VIDEO and VIDEO.endswith('.mp4'):
        return f'<div class="video"><video controls preload="none" src="{VIDEO}" aria-label="veraCrew demo"></video></div>'
    if VIDEO:
        return (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{VIDEO}" title="veraCrew demo, 90 seconds" '
                'loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div>')
    return ''  # no video yet: the veraCrew card is shown full width without a slot


def card(tag, title, body, stack='', links=''):
    s = f'<p class="stack">{stack}</p>' if stack else ''
    l = f'<div class="links">{links}</div>' if links else ''
    return f'<div class="card"><span class="tag">{tag}</span><h3>{title}</h3><p>{body}</p>{s}{l}</div>'


PLURI_EN = ('Co-founded Plurifarma (2007 – 2011), a health-tech company that prepared personalised medication doses for geriatric care centres: '
            'pills sorted and sealed into blister packs per patient and intake time. I built the technical infrastructure for this regulated, traceability-critical process.')
PLURI_ES = ('Cofundé Plurifarma (2007 – 2011), una empresa de tecnología sanitaria que preparaba dosis personalizadas de medicación para residencias geriátricas: '
            'pastillas clasificadas y selladas en blísteres por paciente y toma. Construí la infraestructura técnica de este proceso regulado, en el que la trazabilidad es crítica.')
PLURI_PL = ('Współzałożyłem Plurifarmę (2007 – 2011), firmę health-tech przygotowującą spersonalizowane dawki leków dla domów opieki geriatrycznej: '
            'tabletki sortowane i zgrzewane w blistry dla każdego pacjenta i pory przyjęcia. Zbudowałem infrastrukturę techniczną tego regulowanego procesu, w którym identyfikowalność jest kluczowa.')


def qa(q, a):
    return f'<details><summary>{q}</summary><p>{a}</p></details>'


STAGES = f'''<div class="cols3">
<div><h3>{E('1. Diagnosis', '1. Diagnóstico', '1. Diagnoza')} <span class="fnote">{E('(optional)', '(opcional)', '(opcjonalnie)')}</span></h3><p>{E('I analyse the process, the data and the systems. You get an estimate of what the process costs today, the possible benefit, the implementation cost and the payback period. A reasoned estimate, not a guarantee.', 'Analizo el proceso, los datos y los sistemas. Entrego una estimación del coste actual del proceso, el beneficio posible, el coste de implantación y el plazo de retorno. Es una estimación razonada, no una garantía.', 'Analizuję proces, dane i systemy. Dostajesz szacunek obecnego kosztu procesu, możliwej korzyści, kosztu wdrożenia i okresu zwrotu. To przemyślany szacunek, a nie gwarancja.')}</p></div>
<div><h3>{E('2. Implementation', '2. Implantación', '2. Wdrożenie')}</h3><p>{E('I build the solution and integrate it with the tools you already use. A success criterion agreed in writing, tests, human oversight where it matters and a record of every decision the system makes.', 'Construyo la solución y la integro con las herramientas que ya usas. Criterio de éxito acordado por escrito, pruebas, supervisión humana donde importa y registro de cada decisión del sistema.', 'Buduję rozwiązanie i integruję je z narzędziami, których już używasz. Kryterium sukcesu uzgodnione na piśmie, testy, nadzór człowieka tam, gdzie to ważne, i zapis każdej decyzji systemu.')}</p></div>
<div><h3>{E('3. Continuous improvement', '3. Evolución continua', '3. Stały rozwój')}</h3><p>{E('Monitoring, comparison with the starting point and successive improvements, with a monthly report. Scope and maximum hours are set in the contract: you know exactly what is included.', 'Monitorización, comparación con la situación de partida y mejoras sucesivas, con un informe mensual. Alcance y horas máximas definidos en el contrato: sabes exactamente qué incluye.', 'Monitoring, porównanie z punktem wyjścia i kolejne usprawnienia, z raportem miesięcznym. Zakres i maksymalna liczba godzin są w umowie: wiesz dokładnie, co obejmuje.')}</p></div>
</div>'''

home_main = f'''<div class="hero with-photo">
<figure class="portrait"><img src="assets/rafal-360.webp" srcset="assets/rafal-360.webp 360w, assets/rafal-720.webp 720w" sizes="(max-width:860px) 112px, 176px" width="176" height="176" alt="Rafał Łagowski" fetchpriority="high"></figure>
<div class="htext">
<p class="eyebrow">Rafał Łagowski · {E('AI architect and consultant · Madrid', 'Arquitecto de IA y consultor · Madrid', 'Architekt AI i konsultant · Madryt')}</p>
<h1 class="sell">{E('Your business does not need more AI tools. It needs results.', 'Tu empresa no necesita más herramientas de IA. Necesita resultados.', 'Twoja firma nie potrzebuje kolejnych narzędzi AI. Potrzebuje rezultatów.')}</h1>
<p class="lede">{E('I design and implement AI solutions that automate operations, connect systems and reduce costs, with human oversight where it matters.',
 'Diseño e implemento soluciones de inteligencia artificial que automatizan operaciones, conectan sistemas y reducen costes, con supervisión humana donde importa.',
 'Projektuję i wdrażam rozwiązania AI, które automatyzują operacje, łączą systemy i obniżają koszty, z nadzorem człowieka tam, gdzie to ważne.')}</p>
<p class="tagline">{E('Enterprise AI architecture. Practical implementation. One accountable person.', 'Arquitectura de IA empresarial. Implementación práctica. Un único responsable.', 'Architektura AI klasy enterprise. Praktyczne wdrożenie. Jedna osoba odpowiedzialna.')}</p>
<div class="cta"><a class="btn primary" href="#contact">{E('Tell me which process is costing you money', 'Cuéntame qué proceso te está costando dinero', 'Powiedz mi, który proces kosztuje Cię pieniądze')}</a><a class="btn" href="#solutions">{E('Explore custom AI solutions', 'Explorar soluciones de IA a medida', 'Poznaj rozwiązania AI na miarę')}</a></div>
<p class="fnote">{E('First conversation with no commitment. If AI adds no real value in your case, I will tell you.', 'Primera conversación sin compromiso. Si la IA no aporta valor real a tu caso, te lo diré.', 'Pierwsza rozmowa bez zobowiązań. Jeśli AI nie wniesie realnej wartości w Twoim przypadku, powiem Ci to.')}</p>
</div>
</div>
<div class="trust proofbar">
<div><b>{E('20+ years', '20+ años', '20+ lat')}</b><span>{E('of experience in technology', 'de experiencia en tecnología', 'doświadczenia w technologii')}</span></div>
<div><b>{E('Enterprise AI', 'IA empresarial', 'AI w enterprise')}</b><span>{E('architecture for banking, insurance, telecom and construction', 'arquitectura para banca, seguros, telecomunicaciones y construcción', 'architektura dla bankowości, ubezpieczeń, telekomunikacji i budownictwa')}</span></div>
<div><b>TechStar 2025</b><span>{E('recognition at Accenture', 'reconocimiento en Accenture', 'wyróżnienie w Accenture')}</span></div>
<div><b>{E('4 companies', '4 empresas', '4 firmy')}</b><span>{E('founded or co-founded', 'fundadas o cofundadas', 'założone lub współzałożone')}</span></div>
</div>

<section id="solutions" aria-labelledby="sol-h"><h2 class="s" id="sol-h">{E('Where is the cost that AI can reduce?', '¿Dónde está el coste que la IA puede reducir?', 'Gdzie jest koszt, który AI może zmniejszyć?')}</h2>
<p class="intro">{E('I do not start with the technology. I start with the work your team does by hand today.', 'No empiezo por la tecnología. Empiezo por el trabajo que hoy hace tu equipo a mano.', 'Nie zaczynam od technologii. Zaczynam od pracy, którą Twój zespół wykonuje dziś ręcznie.')}</p>
<div class="proof">
<div class="card"><h3>{E('Requests and customer service', 'Atención y solicitudes', 'Zgłoszenia i obsługa klienta')}</h3><p>{E('Enquiries, incidents and follow-ups classified, answered and routed without anyone copying them from one place to another.', 'Consultas, incidencias y seguimientos que se clasifican, responden y derivan sin que nadie los copie de un sitio a otro.', 'Zapytania, zgłoszenia i follow-upy klasyfikowane, obsługiwane i przekazywane dalej bez ręcznego przepisywania.')}</p></div>
<div class="card"><h3>{E('Documents', 'Documentos', 'Dokumenty')}</h3><p>{E('Invoices, contracts, tenders and forms: extract the data, validate it and take it to the system where it is used.', 'Facturas, contratos, pliegos y formularios: extraer los datos, validarlos y llevarlos al sistema donde se usan.', 'Faktury, umowy, specyfikacje przetargowe i formularze: wyciągnięcie danych, walidacja i przekazanie do systemu, w którym są używane.')}</p></div>
<div class="card"><h3>{E('Operations and coordination', 'Operaciones y coordinación', 'Operacje i koordynacja')}</h3><p>{E('Tasks, shifts, orders and alerts across the systems you already use: ERP, CRM, email, spreadsheets.', 'Tareas, turnos, pedidos y avisos entre los sistemas que ya utilizas: ERP, CRM, correo, hojas de cálculo.', 'Zadania, grafiki, zamówienia i powiadomienia między systemami, których już używasz: ERP, CRM, poczta, arkusze.')}</p></div>
<div class="card"><h3>{E('Custom AI systems', 'Sistemas de IA a medida', 'Systemy AI na miarę')}</h3><p>{E('Agents and assistants that work with your data, with evaluation, traceability and a person who approves critical decisions.', 'Agentes y asistentes que consultan tus datos, con evaluación, trazabilidad y una persona que aprueba las decisiones críticas.', 'Agenci i asystenci pracujący na Twoich danych, z ewaluacją, śledzeniem działań i człowiekiem zatwierdzającym krytyczne decyzje.')}</p></div>
</div>
<p class="note">{E('And if a spreadsheet or a simple integration solves the problem, I will tell you. Not every improvement needs AI.', 'Y si una hoja de cálculo o una integración sencilla resuelve el problema, te lo diré. No toda mejora necesita IA.', 'A jeśli problem rozwiąże arkusz kalkulacyjny albo prosta integracja, powiem Ci to. Nie każde usprawnienie potrzebuje AI.')}</p>
</section>

<section id="how" aria-labelledby="how-h"><h2 class="s" id="how-h">{E('How we work', 'Cómo trabajamos', 'Jak pracujemy')}</h2>
<p class="intro">{E('A collaboration in three stages. You do not have to go through all of them: if your process and your data are already clear, we start with the implementation.', 'Una colaboración en tres etapas. No hace falta pasar por todas: si tu proceso y tus datos ya están claros, empezamos directamente por la implantación.', 'Współpraca w trzech etapach. Nie trzeba przechodzić przez wszystkie: jeśli proces i dane są już jasne, zaczynamy od wdrożenia.')}</p>
{STAGES}
<p class="price"><b>{E('Ongoing collaboration from EUR 3,000 / month + VAT. Diagnoses and implementations with a custom quote.', 'Colaboración continua desde 3.000 €/mes + IVA. Diagnósticos e implementaciones con presupuesto personalizado.', 'Stała współpraca od 3 000 € / mies. + VAT. Diagnozy i wdrożenia wyceniane indywidualnie.')}</b> {E('Scope and price are agreed in writing before we start.', 'El alcance y el precio se cierran por escrito antes de empezar.', 'Zakres i cena są ustalane na piśmie przed startem.')}</p>
</section>

<section class="band" aria-labelledby="why-h"><h2 class="s" id="why-h">{E('Why work with me', 'Por qué conmigo', 'Dlaczego ze mną')}</h2>
<div class="ind">
<div><b>{E('One accountable person', 'Un único responsable', 'Jedna osoba odpowiedzialna')}</b><span>{E('You talk to the person who designs the architecture and answers for the result. No chain of intermediaries.', 'Hablas con quien diseña la arquitectura y responde del resultado. Sin cadenas de intermediarios.', 'Rozmawiasz z osobą, która projektuje architekturę i odpowiada za wynik. Bez łańcucha pośredników.')}</span></div>
<div><b>{E('Enterprise experience', 'Experiencia empresarial', 'Doświadczenie enterprise')}</b><span>{E('More than 20 years in technology: founder or co-founder of four companies, and cloud and AI architect at Accenture for banking, insurance, telecom and construction.', 'Más de 20 años en tecnología: fundador o cofundador de cuatro empresas y arquitecto de cloud e IA en Accenture para banca, seguros, telecomunicaciones y construcción.', 'Ponad 20 lat w technologii: założyciel lub współzałożyciel czterech firm oraz architekt chmury i AI w Accenture dla bankowości, ubezpieczeń, telekomunikacji i budownictwa.')}</span></div>
<div><b>{E('Responsible design', 'Diseño responsable', 'Odpowiedzialne projektowanie')}</b><span>{E('Solutions designed with security, traceability, human oversight and regulatory compliance in mind, including the European AI framework where it applies.', 'Soluciones diseñadas con criterios de seguridad, trazabilidad, supervisión humana y cumplimiento normativo, incluido el marco europeo de IA cuando corresponda.', 'Rozwiązania projektowane z myślą o bezpieczeństwie, śledzeniu działań, nadzorze człowieka i zgodności z przepisami, w tym z europejskimi ramami AI tam, gdzie mają zastosowanie.')}</span></div>
<div><b>{E('Faster delivery', 'Entrega más ágil', 'Szybsza realizacja')}</b><span>{E('I use my own agent systems to speed up building and testing. Architecture decisions, quality control and accountability stay with me.', 'Uso mis propios sistemas de agentes para acelerar la construcción y las pruebas. Las decisiones de arquitectura, el control de calidad y la responsabilidad siguen siendo míos.', 'Korzystam z własnych systemów agentowych, żeby przyspieszyć budowę i testy. Decyzje architektoniczne, kontrola jakości i odpowiedzialność zostają po mojej stronie.')}</span></div>
<div><b>{E('Clear rules', 'Reglas claras', 'Jasne zasady')}</b><span>{E('Your data stays yours. Ownership of the custom development and the licences of reusable components are set out clearly in the contract.', 'Tus datos siguen siendo tuyos. La propiedad del desarrollo específico y las licencias de los componentes reutilizables quedan definidas claramente en el contrato.', 'Twoje dane pozostają Twoje. Własność rozwiązania tworzonego dla Ciebie i licencje komponentów wielokrotnego użytku są jasno określone w umowie.')}</span></div>
</div></section>

<section id="cases" aria-labelledby="cases-h"><h2 class="s" id="cases-h">{E('Cases', 'Casos', 'Realizacje')}</h2>
<div class="proof">
{card(E('Team Lead · Accenture project for FCC · 2024 – 2026', 'Team Lead · proyecto de Accenture para FCC · 2024 – 2026', 'Team Lead · projekt Accenture dla FCC · 2024 – 2026'), E('Bid generation from tender documents', 'Generación de ofertas a partir de pliegos', 'Generowanie ofert ze specyfikacji przetargowych'),
 E('I led a team of 6 developers that built AI agents to analyse public tender specifications and draft the bid proposal. Not a client of my independent practice.', 'Lideré un equipo de 6 desarrolladores que construyó agentes de IA para analizar pliegos de licitaciones públicas y redactar la propuesta de oferta. No es un cliente de mi actividad independiente.', 'Kierowałem zespołem 6 programistów, który zbudował agentów AI analizujących specyfikacje przetargów publicznych i przygotowujących projekt oferty. To nie jest klient mojej niezależnej działalności.'),
 'Azure OpenAI · Azure AI Search · Python · Kubernetes')}
{card(E('Tech Lead · Accenture project for MasOrange · 2025', 'Tech Lead · proyecto de Accenture para MasOrange · 2025', 'Tech Lead · projekt Accenture dla MasOrange · 2025'), E('Real-time AI assistance for call-centre operators', 'Asistencia con IA en tiempo real para operadores', 'Asystent AI w czasie rzeczywistym dla konsultantów'),
 E('A system that suggests answers to operators during the live call, with an automated testing framework. Not a client of my independent practice.', 'Sistema que sugiere respuestas a los operadores durante la llamada en directo, con un marco de pruebas automatizadas. No es un cliente de mi actividad independiente.', 'System podpowiadający konsultantom odpowiedzi w trakcie rozmowy na żywo, z frameworkiem testów automatycznych. To nie jest klient mojej niezależnej działalności.'),
 'Google Cloud · Gemini · Speech-to-Text · BigQuery')}
</div>
<div class="card" style="margin-top:16px"><span class="tag">{E('Own system · in daily use', 'Sistema propio · en uso diario', 'Własny system · w codziennym użyciu')}</span><h3>{E('veraCrew: how I deliver faster', 'veraCrew: cómo entrego más rápido', 'veraCrew: jak dostarczam szybciej')}</h3>
<p>{E('A virtual team of AI agents that splits the work into tasks, writes the tests first, runs continuous integration, AI review and human approval, and only then deploys. It lets me implement quickly without giving up control: every step is recorded and a person makes the final decision. Automation speeds the work up; tests and review guarantee the quality.',
 'Un equipo virtual de agentes de IA que divide el trabajo en tareas, escribe primero las pruebas, pasa por integración continua, revisión con IA y aprobación humana, y solo entonces despliega. Me permite implantar con agilidad sin renunciar al control: cada paso queda registrado y la decisión final la toma una persona. La automatización acelera el trabajo; la calidad la garantizan las pruebas y la revisión.',
 'Wirtualny zespół agentów AI, który dzieli pracę na zadania, najpierw pisze testy, przechodzi przez ciągłą integrację, przegląd AI i akceptację człowieka, a dopiero potem wdraża. Pozwala mi wdrażać szybko bez rezygnacji z kontroli: każdy krok jest zapisany, a ostateczną decyzję podejmuje człowiek. Automatyzacja przyspiesza pracę; jakość zapewniają testy i przegląd.')}</p>
<p><a class="more" href="veracrew.html">{E('How veraCrew works →', 'Cómo funciona veraCrew →', 'Jak działa veraCrew →')}</a></p></div>
</section>

<section id="me" aria-labelledby="me-h"><h2 class="s" id="me-h">{E('About me', 'Sobre mí', 'O mnie')}</h2>
<p class="intro">{E('I am Rafał Łagowski, AI and cloud architect and telecommunications engineer, from Poland, based in Madrid. Before working with large companies I founded and ran my own, so I know what a process that does not work on Monday morning costs. I work in Spanish, English, Polish and Czech, and with companies in Spain and Poland.',
 'Soy Rafał Łagowski, arquitecto de IA y cloud e ingeniero de telecomunicaciones, polaco, afincado en Madrid. Antes de trabajar con grandes empresas fundé y dirigí las mías, así que sé lo que cuesta un proceso que no funciona el lunes por la mañana. Trabajo en español, inglés, polaco y checo, y colaboro con empresas en España y Polonia.',
 'Jestem Rafał Łagowski, architekt AI i chmury oraz inżynier telekomunikacji, Polak mieszkający w Madrycie. Zanim zacząłem pracować z dużymi firmami, zakładałem i prowadziłem własne, więc wiem, ile kosztuje proces, który nie działa w poniedziałek rano. Pracuję po hiszpańsku, angielsku, polsku i czesku, z firmami w Hiszpanii i w Polsce.')}</p>
<p><a class="btn" href="about.html">{E('More about me', 'Más sobre mí', 'Więcej o mnie')}</a> <span class="fnote">{E('Looking for a profile for your team?', '¿Buscas un perfil para tu equipo?', 'Szukasz kogoś do zespołu?')} <a href="career.html">{E('Career and CV', 'Carrera y CV', 'Kariera i CV')}</a></span></p>
</section>

<section id="faq" aria-labelledby="faqh-h"><h2 class="s" id="faqh-h">{E('Frequently asked questions', 'Preguntas frecuentes', 'Najczęstsze pytania')}</h2>
<div class="faq">
{qa(E('How much does it cost?', '¿Cuánto cuesta?', 'Ile to kosztuje?'), E('Ongoing collaboration starts at EUR 3,000 a month + VAT. Diagnoses and implementations are quoted by scope. Everything is agreed in writing before we start.', 'La colaboración continua empieza en 3.000 € al mes + IVA. Los diagnósticos y las implementaciones se presupuestan según el alcance. Todo se cierra por escrito antes de empezar.', 'Stała współpraca zaczyna się od 3 000 € miesięcznie + VAT. Diagnozy i wdrożenia są wyceniane według zakresu. Wszystko ustalamy na piśmie przed startem.'))}
{qa(E('Do I have to change my systems?', '¿Tengo que cambiar mis sistemas?', 'Czy muszę zmieniać swoje systemy?'), E('No. I integrate the solution with what you already use. If something cannot be integrated reasonably, I tell you before we start.', 'No. Integro la solución con lo que ya usas. Si algo no se puede integrar de forma razonable, te lo digo antes de empezar.', 'Nie. Integruję rozwiązanie z tym, czego już używasz. Jeśli czegoś nie da się rozsądnie zintegrować, mówię o tym przed startem.'))}
{qa(E('What happens to my data?', '¿Qué pasa con mis datos?', 'Co dzieje się z moimi danymi?'), E('It stays yours and under your control. I design with personal-data protection and access logging. Depending on the technical and security requirements, we can assess deployment in your own cloud infrastructure.', 'Siguen siendo tuyos y bajo tu control. Diseño con protección de datos personales y registro de accesos. Según los requisitos técnicos y de seguridad, podemos evaluar el despliegue en la infraestructura cloud del cliente.', 'Pozostają Twoje i pod Twoją kontrolą. Projektuję z ochroną danych osobowych i rejestrem dostępu. W zależności od wymagań technicznych i bezpieczeństwa możemy ocenić wdrożenie w Twojej infrastrukturze chmurowej.'))}
{qa(E('How long does it take?', '¿Cuánto tarda?', 'Ile to trwa?'), E('It depends on the process and the integrations. The concrete timeline is set in writing in the proposal.', 'Depende del proceso y de las integraciones. El plazo concreto se fija por escrito en la propuesta.', 'To zależy od procesu i integracji. Konkretny termin jest zapisany w ofercie.'))}
{qa(E('What if the AI makes a mistake?', '¿Y si la IA se equivoca?', 'A jeśli AI się pomyli?'), E('That is why there is human oversight of critical decisions, tests before every change and a record of what the system did and why.', 'Por eso hay supervisión humana en las decisiones críticas, pruebas antes de cada cambio y un registro de lo que hizo el sistema y por qué.', 'Dlatego krytyczne decyzje nadzoruje człowiek, każda zmiana jest testowana, a system zapisuje, co zrobił i dlaczego.'))}
{qa(E('Does it comply with the EU AI Act?', '¿Cumple el Reglamento Europeo de IA?', 'Czy to jest zgodne z AI Act?'), E('Where it applies to your system, I do the technical and organisational work: inventory, risk classification and traceability. For the legal opinion I work with your lawyers.', 'Cuando aplica a tu sistema, hago el trabajo técnico y organizativo: inventario, clasificación de riesgo y trazabilidad. Para el dictamen jurídico trabajo con tus abogados.', 'Tam, gdzie AI Act dotyczy Twojego systemu, wykonuję pracę techniczną i organizacyjną: inwentarz, klasyfikację ryzyka i śledzenie działań. Opinię prawną przygotowuję razem z Twoimi prawnikami.'))}
</div></section>
{contact_block()}'''

person = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    'name': 'Rafał Łagowski',
    'alternateName': 'Rafal Lagowski',
    'jobTitle': 'AI & Agentic Systems Architect',
    'url': BASE + '/',
    'image': BASE + '/assets/rafal-720.webp',
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Madrid', 'addressCountry': 'ES'},
    'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Czech Technical University in Prague'},
    'knowsLanguage': ['en', 'es', 'pl', 'cs'],
    'sameAs': [u for u in (LINKEDIN, GITHUB, MEDIUM) if u],
    'knowsAbout': ['Generative AI', 'AI agents', 'RAG', 'LLMOps', 'EU AI Act', 'Google Cloud', 'Azure'],
}
home_head = '<script type="application/ld+json">' + json.dumps(person, ensure_ascii=False) + '</script>\n'

# ---------------------------------------------------------------- work with me
def rate():
    if DAY_RATE:
        r = f'EUR {DAY_RATE}'
        head = E("from " + r + " / day", "desde " + r + " / día", "od " + r + " / dzień")
    else:
        head = E("Day rate on request", "Tarifa diaria bajo petición", "Stawka dzienna na zapytanie")
    return (f'<div class="rate"><b>{head}</b>'
            f'<span>{E("Fixed price agreed in writing before work starts. Prices exclude VAT.", "Precio cerrado acordado por escrito antes de empezar. Precios sin IVA.", "Stała cena uzgodniona na piśmie przed rozpoczęciem pracy. Ceny nie zawierają VAT.")}</span></div>')


def row(title, desc, time):
    return f'<div class="row"><b>{title}</b><span class="d">{desc}</span><span class="t">{time}</span><span></span></div>'


COMMITMENTS = f'''<section class="band" aria-labelledby="commit-h"><h2 class="s" id="commit-h">{E('Four commitments before the first invoice', 'Cuatro compromisos antes de la primera factura', 'Cztery zobowiązania przed pierwszą fakturą')}</h2>
<p class="intro">{E('AI work is hard to judge from the outside. These are the rules I work by, so the risk does not fall on you alone.', 'El trabajo con IA es difícil de juzgar desde fuera. Estas son las reglas con las que trabajo, para que el riesgo no recaiga solo en ti.', 'Pracę z AI trudno ocenić z zewnątrz. Oto zasady, według których pracuję, żeby ryzyko nie spadało tylko na Ciebie.')}</p>
<div class="trust">
<div><b>{E('Free first call', 'Primera llamada gratis', 'Pierwsza rozmowa za darmo')}</b><span>{E('30 minutes and a written recommendation, no commitment.', '30 minutos y una recomendación por escrito, sin compromiso.', '30 minut i pisemna rekomendacja, bez zobowiązań.')}</span></div>
<div><b>{E('Fixed price before we start', 'Precio cerrado antes de empezar', 'Stała cena przed startem')}</b><span>{E('Scope, timeline and deliverable agreed in writing. No surprise hours.', 'Alcance, plazos y entregable acordados por escrito. Sin horas sorpresa.', 'Zakres, terminy i rezultat uzgodnione na piśmie. Bez niespodziewanych godzin.')}</span></div>
<div><b>{E('Code and data stay yours', 'El código y los datos son tuyos', 'Kod i dane zostają u Ciebie')}</b><span>{E('Repository, documentation and access are handed over at the end. No dependence on me.', 'Repositorio, documentación y accesos se entregan al final. Sin depender de mí.', 'Repozytorium, dokumentacja i dostępy przekazane na koniec. Bez uzależnienia ode mnie.')}</span></div>
<div><b>{E('I tell you when not to use AI', 'Te digo cuándo no usar IA', 'Mówię, kiedy nie używać AI')}</b><span>{E('If a spreadsheet solves the problem, I will say so.', 'Si una hoja de cálculo resuelve el problema, te lo diré.', 'Jeśli problem rozwiąże arkusz kalkulacyjny, powiem o tym.')}</span></div>
</div></section>'''

work_main = ph(E('How I work', 'Cómo trabajo', 'Jak pracuję'),
 E('Diagnosis, implementation and continuous improvement. Ongoing collaboration from EUR 3,000 / month + VAT; diagnoses and implementations with a custom quote.',
   'Diagnóstico, implantación y evolución continua. Colaboración continua desde 3.000 €/mes + IVA; diagnósticos e implementaciones con presupuesto personalizado.',
   'Diagnoza, wdrożenie i stały rozwój. Stała współpraca od 3 000 € / mies. + VAT; diagnozy i wdrożenia wyceniane indywidualnie.')) + f'''
<section class="tight">{STAGES}</section>
{COMMITMENTS}
<section class="tight"><div class="callout"><b>{E('What this is not', 'Lo que no es', 'Czego nie obejmuje')}</b>{E('I am an architect, not a lawyer. The EU AI Act work is technical and organisational; for a legal opinion I work with your counsel. I am vendor-independent and take no commissions.',
 'Soy arquitecto, no abogado. El trabajo sobre el Reglamento de IA es técnico y organizativo; para el dictamen jurídico trabajo con tus abogados. Soy independiente de proveedores y no cobro comisiones.',
 'Jestem architektem, nie prawnikiem. Praca nad AI Act ma charakter techniczny i organizacyjny; opinię prawną przygotowuję razem z Twoimi prawnikami. Nie jestem związany z żadnym dostawcą i nie biorę prowizji.')}</div></section>
{contact_block()}'''

career_main = ph(E('Career', 'Carrera', 'Kariera'),
 E('For recruiters and hiring managers: the roles I am open to, my experience and my CV.', 'Para reclutadores y responsables de contratación: los puestos que me interesan, mi experiencia y mi CV.', 'Dla rekruterów i osób zatrudniających: stanowiska, na które jestem otwarty, moje doświadczenie i CV.')) + f'''
<section class="tight"><div class="proof">
{card(E('Employment · long contracts', 'Empleo · contratos largos', 'Etat · długie kontrakty'), E('Hire me', 'Contrátame', 'Zatrudnij mnie'),
 E('Open to permanent roles and long contracts as Lead AI or Cloud Architect, AI &amp; Agentic Systems Architect or Senior AI Engineer. Remote across Europe, or on site in Madrid. Google Cloud Professional certified: Cloud Architect, Machine Learning Engineer, Data Engineer, Cloud Database Engineer and Cloud DevOps Engineer. English (C1), Spanish, Polish and Czech.',
   'Abierto a puestos fijos y contratos largos como Lead AI o Cloud Architect, arquitecto de IA y sistemas agénticos o Senior AI Engineer. En remoto en toda Europa o presencial en Madrid. Certificaciones Google Cloud Professional: Cloud Architect, Machine Learning Engineer, Data Engineer, Cloud Database Engineer y Cloud DevOps Engineer. Inglés (C1), español, polaco y checo.',
   'Jestem otwarty na etat i długie kontrakty jako Lead AI lub Cloud Architect, architekt AI i systemów agentowych albo Senior AI Engineer. Zdalnie w całej Europie lub na miejscu w Madrycie. Certyfikaty Google Cloud Professional: Cloud Architect, Machine Learning Engineer, Data Engineer, Cloud Database Engineer i Cloud DevOps Engineer. Angielski (C1), hiszpański, polski i czeski.'),
 '', cv_button('more') + f'<a href="index.html?topic=role#contact">' + E('Talk about a role', 'Hablar de un puesto', 'Porozmawiajmy o stanowisku') + '</a>')}
</div></section>
<section id="experience" aria-labelledby="xp-h"><h2 class="s" id="xp-h">{E('Experience', 'Experiencia', 'Doświadczenie')}</h2>
<p class="intro"><span class="tag">TechStar 2025</span><br>{E('TechStar 2025 at Accenture.', 'TechStar 2025 en Accenture.', 'TechStar 2025 w Accenture.')}</p>
<ol class="xp" reversed>
<li><span class="when"><span class="now">{E('2026 – present', '2026 – actualidad', '2026 – obecnie')}</span></span><div><b>Lead Cloud &amp; AI Architect</b><span class="org">{E('In-house role', 'Puesto interno', 'Etat w firmie')}</span></div></li>
<li><span class="when">{E('Apr 2023 – Mar 2026', 'abr 2023 – mar 2026', 'kwi 2023 – mar 2026')}</span><div><b>Senior Cloud &amp; AI Architect, Tech Lead</b><span class="org">Accenture · Associate Manager</span>
<p>{E('Tech lead and architect on AI programmes for CaixaBank, MasOrange, Zurich Seguros and FCC. TechStar 2025.',
 'Tech lead y arquitecto en programas de IA para CaixaBank, MasOrange, Zurich Seguros y FCC. TechStar 2025.',
 'Tech lead i architekt w programach AI dla CaixaBank, MasOrange, Zurich Seguros i FCC. TechStar 2025.')}</p></div></li>
<li><span class="when">{E('Apr 2021 – May 2023', 'abr 2021 – may 2023', 'kwi 2021 – maj 2023')}</span><div><b>Cloud Architect</b><span class="org">Accenture</span>
<p>{E('Cloud migration and architecture on GCP for Renault; infrastructure transformation on GCP for Carrefour; data architecture and pipelines on AWS for Banco de España.',
 'Migración y arquitectura cloud en GCP para Renault; transformación de infraestructura en GCP para Carrefour; arquitectura de datos y pipelines en AWS para el Banco de España.',
 'Migracja i architektura chmurowa na GCP dla Renault; transformacja infrastruktury na GCP dla Carrefour; architektura danych i potoki danych na AWS dla Banco de España.')}</p></div></li>
<li><span class="when">{E('Oct 2019 – Dec 2020', 'oct 2019 – dic 2020', 'paź 2019 – gru 2020')}</span><div><b>{E('Co-Founder, CTO &amp; AI Engineer', 'Cofundador, CTO e ingeniero de IA', 'Współzałożyciel, CTO i inżynier AI')}</b><span class="org">Webrain Esports</span>
<p>{E('Computer vision with YOLO, FastAPI and Flask APIs, React and Kubernetes on AWS.', 'Visión artificial con YOLO, APIs con FastAPI y Flask, React y Kubernetes en AWS.', 'Widzenie komputerowe z YOLO, API we FastAPI i Flasku, React i Kubernetes na AWS.')}</p></div></li>
<li><span class="when">{E('Jul 2010 – Oct 2021', 'jul 2010 – oct 2021', 'lip 2010 – paź 2021')}</span><div><b>{E('Founder &amp; CTO', 'Fundador y CTO', 'Założyciel i CTO')}</b><span class="org">PRO4 Internet y Promoción</span>
<p>{E('More than 100 client projects in Spain and Poland with teams of up to 8 people; the stack evolved from PHP and MySQL to Python, cloud and AI.', 'Más de 100 proyectos para clientes en España y Polonia con equipos de hasta 8 personas; el stack evolucionó de PHP y MySQL a Python, cloud e IA.', 'Ponad 100 projektów dla klientów w Hiszpanii i Polsce, zespoły do 8 osób; stos technologiczny przeszedł od PHP i MySQL do Pythona, chmury i AI.')}</p></div></li>
<li><span class="when">{E('Feb 2007 – Aug 2011', 'feb 2007 – ago 2011', 'lut 2007 – sie 2011')}</span><div><b>{E('Co-Founder &amp; Technical Director', 'Cofundador y director técnico', 'Współzałożyciel i dyrektor techniczny')}</b><span class="org">Plurifarma</span>
<p>{E(PLURI_EN, PLURI_ES, PLURI_PL)}</p></div></li>
<li><span class="when">{E('Jun 2004 – Aug 2011', 'jun 2004 – ago 2011', 'cze 2004 – sie 2011')}</span><div><b>{E('Co-Founder &amp; CTO', 'Cofundador y CTO', 'Współzałożyciel i CTO')}</b><span class="org">Creaciones Virtuales</span>
<p>{E('Web and multimedia studio in Madrid.', 'Estudio web y multimedia en Madrid.', 'Studio internetowe i multimedialne w Madrycie.')}</p></div></li>
<li><span class="when">2000 – 2002</span><div><b>Senior System Administrator</b><span class="org">Lucent Technologies · Bell Labs</span>
<p>{E('Unix high-availability systems.', 'Sistemas Unix de alta disponibilidad.', 'Systemy Unix wysokiej dostępności.')}</p></div></li>
<li><span class="when">{E('Education', 'Formación', 'Wykształcenie')}</span><div><b>{E('Telecommunications Engineering', 'Ingeniería de Telecomunicaciones', 'Inżynieria telekomunikacyjna')}</b><span class="org">{E('Czech Technical University in Prague', 'Universidad Técnica Checa de Praga', 'Politechnika Czeska w Pradze')}</span>
<p>{E('Faculty of Electrical Engineering.', 'Facultad de Ingeniería Eléctrica.', 'Wydział Elektrotechniki.')}</p></div></li>
</ol>
</section>

<section class="band" id="industries" aria-labelledby="ind-h"><h2 class="s" id="ind-h">{E('Industries', 'Sectores', 'Branże')}</h2>
<p class="intro">{E('Sectors where I have delivered work. Legal is the one listed by typical use cases rather than a delivered project.', 'Sectores en los que he entregado proyectos. Legal es el único que aparece por casos de uso típicos y no por un proyecto entregado.', 'Branże, w których zrealizowałem projekty. Prawo to jedyna pozycja opisana typowymi zastosowaniami, a nie zrealizowanym projektem.')}</p>
<div class="ind">
<div><b>{E('Banking &amp; financial services', 'Banca y servicios financieros', 'Bankowość i usługi finansowe')}</b><span>{E('CaixaBank and Banco de España (with Accenture).', 'CaixaBank y Banco de España (con Accenture).', 'CaixaBank i Banco de España (z Accenture).')}</span></div>
<div><b>{E('Insurance', 'Seguros', 'Ubezpieczenia')}</b><span>{E('Zurich Seguros (with Accenture). Typical use cases: claims and document intake, underwriting assistants with cited sources and human sign-off.', 'Zurich Seguros (con Accenture). Casos de uso típicos: entrada de siniestros y documentos, asistentes de suscripción con fuentes citadas y validación humana.', 'Zurich Seguros (z Accenture). Typowe zastosowania: przyjmowanie szkód i dokumentów, asystenci underwritingu z cytowanymi źródłami i akceptacją człowieka.')}</span></div>
<div><b>{E('Telecommunications', 'Telecomunicaciones', 'Telekomunikacja')}</b><span>{E('MasOrange (with Accenture): real-time AI assistance for call-centre operators.', 'MasOrange (con Accenture): asistencia con IA en tiempo real para operadores.', 'MasOrange (z Accenture): asystent AI w czasie rzeczywistym dla konsultantów.')}</span></div>
<div><b>{E('Construction &amp; infrastructure', 'Construcción e infraestructuras', 'Budownictwo i infrastruktura')}</b><span>{E('FCC (with Accenture).', 'FCC (con Accenture).', 'FCC (z Accenture).')}</span></div>
<div><b>{E('Real estate', 'Inmobiliario', 'Nieruchomości')}</b><span>{E('P&amp;O Apartments: pricing system that collects listings, stores them in a price database and serves market prices through an API. Typical use cases: listing and price data pipelines, document and contract assistants.',
 'P&amp;O Apartments: sistema de precios que recoge anuncios, los guarda en una base de datos de precios y sirve precios de mercado mediante una API. Casos de uso típicos: pipelines de datos de anuncios y precios, asistentes para documentos y contratos.',
 'P&amp;O Apartments: system cenowy, który zbiera ogłoszenia, zapisuje je w bazie cen i udostępnia ceny rynkowe przez API. Typowe zastosowania: potoki danych o ofertach i cenach, asystenci do dokumentów i umów.')}</span></div>
<div><b>{E('Pharmaceuticals &amp; healthcare', 'Farmacéutico y sanitario', 'Farmacja i ochrona zdrowia')}</b><span>{E(PLURI_EN, PLURI_ES, PLURI_PL)}</span></div>
<div><span class="k">{E('Typical use cases', 'Casos de uso típicos', 'Typowe zastosowania')}</span><b>{E('Legal', 'Legal', 'Prawo')}</b><span>{E('Contract review and clause extraction with RAG, governed document assistants.', 'Revisión de contratos y extracción de cláusulas con RAG, asistentes documentales gobernados.', 'Przegląd umów i ekstrakcja klauzul z RAG, kontrolowani asystenci dokumentów.')}</span></div>
</div>
</section>
{contact_block()}'''

# ---------------------------------------------------------------- about
about_main = f'''<figure class="portrait about-photo"><img src="assets/rafal-360.webp" srcset="assets/rafal-360.webp 360w, assets/rafal-720.webp 720w" sizes="144px" width="144" height="144" alt="Rafał Łagowski"></figure>
<h1 class="ph">Rafał Łagowski</h1>
<div class="about"><div>
<p>{E('AI and cloud architect and telecommunications engineer, from Poland, based in Madrid.', 'Arquitecto de IA y cloud e ingeniero de telecomunicaciones, polaco, afincado en Madrid.', 'Architekt AI i chmury, inżynier telekomunikacji, Polak mieszkający w Madrycie.')}</p>
<p>{E('I have built technology for more than 20 years: first as founder or co-founder of four companies, then as cloud and AI architect and tech lead at Accenture for MasOrange, CaixaBank, Zurich Seguros and FCC, now as Lead Cloud &amp; AI Architect in an in-house role. That mix taught me how to build a system that has to work on Monday, and how to explain a technical decision to the person who signs the budget.',
 'Llevo más de 20 años construyendo tecnología: primero como fundador o cofundador de cuatro empresas, después como arquitecto cloud y de IA y tech lead en Accenture para MasOrange, CaixaBank, Zurich Seguros y FCC, y hoy como Lead Cloud &amp; AI Architect en un puesto interno. Esa mezcla me enseñó a construir un sistema que tiene que funcionar el lunes y a explicar una decisión técnica a quien firma el presupuesto.',
 'Od ponad 20 lat buduję technologię: najpierw jako założyciel lub współzałożyciel czterech firm, potem jako architekt chmury i AI oraz tech lead w Accenture dla MasOrange, CaixaBank, Zurich Seguros i FCC, dziś jako Lead Cloud &amp; AI Architect na etacie w firmie. To połączenie nauczyło mnie budować system, który musi działać w poniedziałek, i tłumaczyć decyzję techniczną osobie, która podpisuje budżet.')}</p>
<p>{E('I care about AI that can be explained to an auditor and to a finance director in the same words: with sources, with traces and with a person who decides. I work in English, Spanish, Polish and Czech.',
 'Me importa una IA que se pueda explicar a un auditor y a un director financiero con las mismas palabras: con fuentes, con trazas y con una persona que decide. Trabajo en español, inglés, polaco y checo.',
 'Zależy mi na AI, którą da się wyjaśnić audytorowi i dyrektorowi finansowemu tymi samymi słowami: ze źródłami, ze śladami i z człowiekiem, który decyduje. Pracuję po polsku, angielsku, hiszpańsku i czesku.')}</p>
<div class="cta" style="margin-top:20px">{cv_button()}<a class="btn" href="career.html#experience">{E('Experience', 'Experiencia', 'Doświadczenie')}</a></div>
</div>
<div><h2 class="s sm">{E('What I work with', 'Con qué trabajo', 'Z czym pracuję')}</h2>
<div class="chips"><span>Python</span><span>LangGraph</span><span>LangChain</span><span>RAG</span><span>LLMOps</span><span>Langfuse</span><span>OpenTelemetry</span><span>LiteLLM</span><span>Presidio</span><span>OPA</span><span>Google Cloud · Vertex AI</span><span>Azure OpenAI · AI Search</span><span>AWS</span><span>Kubernetes</span><span>Terraform</span><span>FastAPI</span><span>EU AI Act</span></div>
<h2 class="s sm" style="margin-top:32px">{E('What I do not do', 'Lo que no hago', 'Czego nie robię')}</h2>
<ul class="ticks">
<li>{E('Resell licences or take vendor commissions.', 'Revender licencias ni cobrar comisiones de proveedores.', 'Nie odsprzedaję licencji i nie biorę prowizji od dostawców.')}</li>
<li>{E('Give legal advice.', 'Dar asesoramiento jurídico.', 'Nie udzielam porad prawnych.')}</li>
<li>{E('Leave decisions about people to an unsupervised model.', 'Dejar decisiones sobre personas a un modelo sin supervisión.', 'Nie zostawiam decyzji o ludziach modelowi bez nadzoru.')}</li>
</ul></div></div>
<section id="projects" aria-labelledby="work-h"><h2 class="s" id="work-h">{E('Projects', 'Proyectos', 'Projekty')}</h2>
<p class="intro">{E('Systems I designed and built. Each one says whether the code is open, private or built for a client.',
 'Sistemas que he diseñado y construido. Cada uno indica si el código es abierto, privado o para un cliente.',
 'Systemy, które zaprojektowałem i zbudowałem. Przy każdym widać, czy kod jest otwarty, prywatny, czy powstał dla klienta.')}</p>
<div class="card"><span class="tag">{E('Own product · my proudest project · demo on request', 'Producto propio · el proyecto del que más orgulloso estoy · demo bajo petición', 'Własny produkt · projekt, z którego jestem najbardziej dumny · demo na życzenie')}</span>
<h3>veraCrew</h3>
<p>{E('A virtual consulting company run by AI agents. It picks the right agents for each job, breaks work into smaller tasks, has the tests written, controls the workflow, sets up and runs CI/CD, deploys, and presents the result as a slide deck or a video. A person approves at every gate. Co-created with <a href="https://github.com/Dixter999">Daniel Łagowski</a>.',
 'Una consultora virtual dirigida por agentes de IA. Elige los agentes adecuados para cada trabajo, divide el trabajo en tareas más pequeñas, encarga la escritura de los tests, controla el flujo de trabajo, configura y ejecuta el CI/CD, despliega y presenta el resultado en una presentación o un vídeo. Una persona aprueba en cada etapa. Creado junto con <a href="https://github.com/Dixter999">Daniel Łagowski</a>.',
 'Wirtualna firma konsultingowa prowadzona przez agentów AI. Dobiera odpowiednich agentów do każdego zadania, dzieli pracę na mniejsze zadania, zleca napisanie testów, pilnuje przepływu pracy, tworzy i uruchamia CI/CD, wdraża, a wynik pokazuje w prezentacji lub na wideo. Człowiek zatwierdza każdy etap. Współtworzony z <a href="https://github.com/Dixter999">Danielem Łagowskim</a>.')}</p>
<p class="stack">Python · multi-agent orchestration · Claude / OpenAI APIs · GitHub · CI/CD · {E('with Cortex, a companion system that structures project knowledge for the agents', 'con Cortex, un sistema que estructura el conocimiento del proyecto para los agentes', 'razem z Cortex, systemem porządkującym wiedzę o projekcie dla agentów')}</p>
<p><a class="more" href="veracrew.html">{E('How veraCrew works →', 'Cómo funciona veraCrew →', 'Jak działa veraCrew →')}</a></p>
{video_slot()}</div>
<div class="proof">
{card(E('Open source', 'Código abierto', 'Open source'), 'DAP · Deterministic Agent Pipeline',
 E('A framework that runs LLM agents inside deterministic state machines, so workflows are reproducible, testable and auditable instead of free-running agent loops.',
   'Un framework que ejecuta agentes LLM dentro de máquinas de estados deterministas, para que los flujos sean reproducibles, comprobables y auditables en lugar de bucles de agentes sin control.',
   'Framework, który uruchamia agentów LLM wewnątrz deterministycznych maszyn stanów, dzięki czemu przepływy są powtarzalne, testowalne i audytowalne zamiast swobodnych pętli agentów.'),
 'LangGraph.js · Fastify · Next.js', f'<a href="{ORG}/dap">GitHub</a>')}
{card(E('Internal tool', 'Herramienta interna', 'Narzędzie wewnętrzne'), 'PR Review Gate',
 E('Governed AI pull-request review: one rubric, swappable model engines and a council mode in which several models compare their judgement. AI reviews; a person still merges.',
   'Revisión de pull requests con IA gobernada: una sola rúbrica, motores de modelo intercambiables y un modo consejo en el que varios modelos contrastan su criterio. La IA revisa; una persona sigue fusionando.',
   'Kontrolowany przegląd pull requestów przez AI: jedna rubryka, wymienne silniki modeli i tryb rady, w którym kilka modeli porównuje swoje oceny. AI recenzuje, a scala nadal człowiek.'),
 'Claude · Gemini · OpenRouter · GitHub Actions')}
{card(E('Open source · 39 stars', 'Código abierto · 39 estrellas', 'Open source · 39 gwiazdek'), 'ClaudeAutoPM',
 E('A multi-agent project management framework published as npm packages, with GitHub and Azure DevOps integration.',
   'Un framework multiagente de gestión de proyectos publicado como paquetes npm, integrado con GitHub y Azure DevOps.',
   'Wieloagentowy framework do zarządzania projektami opublikowany jako pakiety npm, zintegrowany z GitHubem i Azure DevOps.'),
 'Node.js · npm · GitHub · Azure DevOps', f'<a href="{ORG}/ClaudeAutoPM">GitHub</a>')}
{card(E('Real estate · pricing intelligence', 'Inmobiliario · inteligencia de precios', 'Nieruchomości · analityka cen'), 'P&amp;O Apartments',
 E('A system that collects property listings, stores them in a price database and exposes market prices through an API.',
   'Un sistema que recoge anuncios de inmuebles, los guarda en una base de datos de precios y expone los precios de mercado mediante una API.',
   'System, który zbiera ogłoszenia nieruchomości, zapisuje je w bazie cen i udostępnia ceny rynkowe przez API.'),
 'Python · ' + E('data pipelines', 'pipelines de datos', 'potoki danych') + ' · PostgreSQL · REST API', '<a href="https://pandoapartments.eu">pandoapartments.eu</a>')}
<a class="card big wide" href="demos.html"><span class="tag">{E('Runs in your browser', 'Funciona en tu navegador', 'Działa w przeglądarce')}</span><h3>{E('Interactive demos', 'Demos interactivas', 'Interaktywne dema')}</h3>
<p>{E('Four small demos with sample data and no model calls: an EU AI Act risk classifier, an assistant that only answers with cited sources, a bias audit and an outreach simulator.',
 'Cuatro demos pequeñas con datos de ejemplo y sin llamadas a modelos: un clasificador de riesgo del Reglamento de IA, un asistente que solo responde citando fuentes, una auditoría de sesgo y un simulador de alcance.',
 'Cztery małe dema na przykładowych danych, bez wywołań modeli: klasyfikator ryzyka według AI Act, asystent odpowiadający wyłącznie z cytowanymi źródłami, audyt stronniczości i symulator dotarcia.')}</p><span class="more">{E('Open the demos →', 'Abrir las demos →', 'Otwórz dema →')}</span></a>
</div>
</section>

<section id="writing" aria-labelledby="writing-h"><h2 class="s" id="writing-h">{E('Writing', 'Artículos', 'Teksty')}</h2>
<p class="intro">{E('I write about governed enterprise AI and publish the method so it can be repeated.', 'Escribo sobre IA corporativa gobernada y publico el método para que se pueda repetir.', 'Piszę o kontrolowanej AI w firmach i publikuję metodę, żeby można ją było powtórzyć.')}</p>
<div class="proof">
<div class="card"><span class="tag">{E('Article + notebook · in Spanish', 'Artículo + notebook', 'Artykuł + notebook · po hiszpańsku')}</span><h3>{E('Can AI help against poverty?', '¿Puede la IA ayudar contra la pobreza?', 'Czy AI może pomóc w walce z ubóstwem?')}</h3>
<p>{E('With AIReF and Eurostat data and a synthetic-data simulation: a simple rule finds eligible households with 85% precision, and a model trained on a biased history reproduces the bias. Measured by group, with an open notebook.',
 'Con datos de la AIReF y Eurostat y una simulación con datos sintéticos: una regla sencilla encuentra hogares con derecho con un 85% de precisión, y un modelo entrenado con un historial sesgado reproduce el sesgo. Medido por grupo, con un notebook abierto.',
 'Na danych AIReF i Eurostatu oraz symulacji na danych syntetycznych: prosta reguła znajduje uprawnione gospodarstwa z 85% precyzją, a model wytrenowany na stronniczej historii powiela tę stronniczość. Mierzone w podziale na grupy, z otwartym notebookiem.')}</p>
<div class="links"><a href="{ARTICLE}">Medium</a><a href="{NOTEBOOK}">Notebook</a></div></div>
<a class="card big" href="{MEDIUM}"><span class="tag">Medium</span><h3>{E('All articles', 'Todos los artículos', 'Wszystkie artykuły')}</h3>
<p>{E('Governed enterprise AI, the EU AI Act in practice, agent architecture and what works in production.', 'IA corporativa gobernada, el Reglamento de IA en la práctica, arquitectura de agentes y lo que funciona en producción.', 'Kontrolowana AI w firmach, AI Act w praktyce, architektura agentów i to, co działa w produkcji.')}</p><span class="more">rlagowski.medium.com →</span></a>
</div>
</section>
{contact_block()}'''

# ---------------------------------------------------------------- process
def step(t, x, b):
    return f'<li><div><b>{t}</b><span class="x">{x}</span></div><span class="badge">{b}</span></li>'


process_main = ph(E('How an engagement works', 'Cómo funciona un proyecto', 'Jak przebiega współpraca'),
 E('The first two steps cost nothing and commit you to nothing.', 'Los dos primeros pasos no cuestan nada ni te comprometen a nada.', 'Pierwsze dwa kroki nic nie kosztują i do niczego nie zobowiązują.')) + f'''
<section class="tight"><ol class="steps vert">
{step(E('30-minute call', 'Llamada de 30 minutos', '30-minutowa rozmowa'), E('The problem, the data you have and the deadline.', 'El problema, los datos que tienes y el plazo.', 'Problem, dane, którymi dysponujesz, i termin.'), E('Free', 'Gratis', 'Za darmo'))}
{step(E('Written recommendation', 'Recomendación escrita', 'Pisemna rekomendacja'), E('One page within three working days: what I would do, what I would not, risks and a price. It can say “do not use AI”.', 'Una página en tres días laborables: qué haría, qué no, riesgos y precio. Puede decir «no uses IA».', 'Jedna strona w ciągu trzech dni roboczych: co bym zrobił, czego nie, ryzyka i cena. Może brzmieć „nie używaj AI”.'), E('Free', 'Gratis', 'Za darmo'))}
{step(E('Proposal with a success criterion', 'Propuesta con criterio de éxito', 'Oferta z kryterium sukcesu'), E('Scope, milestones, deliverables, a fixed price and a measurable success criterion, agreed in writing.', 'Alcance, hitos, entregables, precio cerrado y un criterio de éxito medible, acordados por escrito.', 'Zakres, kamienie milowe, rezultaty, stała cena i mierzalne kryterium sukcesu, uzgodnione na piśmie.'), E('Signed', 'Firmado', 'Podpisane'))}
{step(E('Build in short deliveries', 'Construcción en entregas cortas', 'Budowa w krótkich iteracjach'), E('Real progress and passing tests every week. Each phase ends with a decision: continue, adjust or stop.', 'Avance real y tests en verde cada semana. Cada fase termina con una decisión: seguir, ajustar o parar.', 'Realny postęp i zielone testy co tydzień. Każda faza kończy się decyzją: kontynuować, skorygować lub zatrzymać.'), E('Per milestone', 'Por hito', 'Za kamień milowy'))}
{step(E('Handover', 'Traspaso', 'Przekazanie'), E('Repository, documentation, access and training. Your team carries on without me.', 'Repositorio, documentación, accesos y formación. Tu equipo sigue sin mí.', 'Repozytorium, dokumentacja, dostępy i szkolenie. Twój zespół działa dalej beze mnie.'), E('At the end', 'Al final', 'Na koniec'))}
</ol>
<ul class="ticks" style="margin-top:32px">
<li>{E('If scope changes, we agree it in writing before continuing.', 'Si cambia el alcance, lo acordamos por escrito antes de seguir.', 'Jeśli zmienia się zakres, uzgadniamy to na piśmie przed dalszą pracą.')}</li>
<li>{E('Confidentiality by contract from the first conversation involving data.', 'Confidencialidad por contrato desde la primera conversación con datos.', 'Poufność zapewniona umową od pierwszej rozmowy dotyczącej danych.')}</li>
<li>{E('If a project needs more hands than I have, I say so before quoting.', 'Si un proyecto necesita más manos de las que tengo, lo digo antes de presupuestar.', 'Jeśli projekt wymaga więcej rąk, niż mam, mówię o tym przed wyceną.')}</li>
</ul></section>
{contact_block()}'''

# ---------------------------------------------------------------- faq
def qa(q, a):
    return f'<details><summary>{q}</summary><p>{a}</p></details>'


faq_main = ph(E('Frequently asked questions', 'Preguntas frecuentes', 'Najczęstsze pytania'),
 E('Answered plainly.', 'Respondidas sin rodeos.', 'Odpowiedzi wprost.')) + f'''
<section class="tight faq">
{qa(E('Are you available for permanent roles or long contracts?', '¿Estás disponible para puestos fijos o contratos largos?', 'Czy jesteś dostępny na stałe stanowiska lub długie kontrakty?'),
 E('I am open to conversations about senior architecture roles and longer engagements. Write to me with the scope and the timeline.', 'Estoy abierto a hablar de puestos sénior de arquitectura y de colaboraciones largas. Escríbeme con el alcance y los plazos.', 'Jestem otwarty na rozmowy o seniorskich rolach architektonicznych i dłuższych projektach. Napisz do mnie, podając zakres i terminy.'))}
{qa(E('How do you price work?', '¿Cómo cobras?', 'Jak wyceniasz pracę?'),
 E('Ongoing collaboration starts at EUR 3,000 a month + VAT; diagnoses and implementations are quoted by scope. Every engagement has a scope and price agreed in writing before it starts. The first call is free.', 'La colaboración continua empieza en 3.000 € al mes + IVA; los diagnósticos y las implementaciones se presupuestan según el alcance. Cada proyecto tiene alcance y precio cerrados por escrito antes de empezar. La primera llamada es gratuita.', 'Stała współpraca zaczyna się od 3 000 € miesięcznie + VAT; diagnozy i wdrożenia są wyceniane według zakresu. Każdy projekt ma zakres i cenę ustalone na piśmie przed startem. Pierwsza rozmowa jest bezpłatna.'))}
{qa(E('Who owns the code and the results?', '¿De quién son el código y los resultados?', 'Do kogo należy kod i wyniki?'),
 E('You do. Everything is delivered in a repository you own, with documentation and access. Open-source tools I reuse keep their licences, and I list them.', 'Tuyos. Todo se entrega en un repositorio de tu propiedad, con documentación y accesos. Las herramientas abiertas que reutilizo mantienen su licencia y te las detallo.', 'Do Ciebie. Wszystko trafia do Twojego repozytorium, z dokumentacją i dostępami. Narzędzia open source, których używam, zachowują swoje licencje i wymieniam je.'))}
{qa(E('What happens to our data?', '¿Qué pasa con nuestros datos?', 'Co dzieje się z naszymi danymi?'),
 E('They stay in your infrastructure and I work with your accounts. I sign a confidentiality agreement and, where personal data is involved, a data-processing agreement. I do not use your data to train models.', 'Se quedan en tu infraestructura y trabajo con tus cuentas. Firmo un acuerdo de confidencialidad y, si hay datos personales, un contrato de encargo de tratamiento. No uso tus datos para entrenar modelos.', 'Zostają w Twojej infrastrukturze, a ja pracuję na Twoich kontach. Podpisuję umowę o poufności, a przy danych osobowych umowę powierzenia przetwarzania. Nie używam Twoich danych do trenowania modeli.'))}
{qa(E('Will you give a legal opinion on the EU AI Act?', '¿Das un dictamen jurídico sobre el Reglamento de IA?', 'Czy wydajesz opinię prawną o AI Act?'),
 E('No. I do the technical and organisational work: inventory, classification, gaps and plan. For the legal opinion I work with your counsel, and I confirm the dates in force in each engagement because the timetable has shifted.', 'No. Hago el trabajo técnico y organizativo: inventario, clasificación, carencias y plan. Para el dictamen trabajo con tus abogados, y confirmo en cada proyecto las fechas en vigor porque el calendario ha cambiado.', 'Nie. Wykonuję pracę techniczną i organizacyjną: inwentarz, klasyfikacja, luki i plan. Opinię prawną przygotowuję z Twoimi prawnikami, a obowiązujące terminy potwierdzam w każdym projekcie, bo harmonogram się zmieniał.'))}
{qa(E('Which models and vendors do you use?', '¿Qué modelos y proveedores usas?', 'Jakich modeli i dostawców używasz?'),
 E('Whichever fits the case: Azure OpenAI, Google Gemini, Anthropic, OpenAI or open models. I am vendor-independent and take no commissions.', 'El que encaje en cada caso: Azure OpenAI, Google Gemini, Anthropic, OpenAI o modelos abiertos. Soy independiente y no cobro comisiones.', 'Tych, które pasują do przypadku: Azure OpenAI, Google Gemini, Anthropic, OpenAI lub modele otwarte. Jestem niezależny i nie biorę prowizji.'))}
{qa(E('Which languages do you work in?', '¿En qué idiomas trabajas?', 'W jakich językach pracujesz?'),
 E('English, Spanish, Polish and Czech, in meetings and in documentation.', 'Español, inglés, polaco y checo, en reuniones y en documentación.', 'Po polsku, angielsku, hiszpańsku i czesku, na spotkaniach i w dokumentacji.'))}
</section>
{contact_block()}'''

# ---------------------------------------------------------------- demos (reused from the services site)
demos_main = open(os.path.join(ROOT, 'tools', 'demos_main.html'), encoding='utf-8').read().strip()

# ---------------------------------------------------------------- veraCrew
def vstep(n, en, es, pl, den, des, dpl, gate=False):
    g = ' gate' if gate else ''
    return f'<li class="vs{g}" style="--i:{n}"><b>{E(en, es, pl)}</b><span>{E(den, des, dpl)}</span></li>'


def feat(en, es, pl, den, des, dpl):
    return f'<div><h3>{E(en, es, pl)}</h3><p>{E(den, des, dpl)}</p></div>'


veracrew_main = f'''<div class="hero">
<div>
<p class="eyebrow">{E('Own product, co-created with <a href="https://github.com/Dixter999">Daniel Łagowski</a> · in daily use since July 2026', 'Producto propio, creado junto con <a href="https://github.com/Dixter999">Daniel Łagowski</a> · en uso diario desde julio de 2026', 'Własny produkt, współtworzony z <a href="https://github.com/Dixter999">Danielem Łagowskim</a> · w codziennym użyciu od lipca 2026')}</p>
<h1>vera<span class="hl">Crew</span></h1>
<p class="role">{E('A virtual consulting company run by AI agents.', 'Una consultora virtual dirigida por agentes de IA.', 'Wirtualna firma konsultingowa prowadzona przez agentów AI.')}</p>
<p class="tagline">{E('Vera means truth: it shows what really happened, not what an agent says happened.', 'Vera significa verdad: muestra lo que pasó de verdad, no lo que un agente dice que pasó.', 'Vera znaczy prawda: pokazuje, co naprawdę się stało, a nie to, co agent twierdzi, że się stało.')}</p>
<p class="lede">{E('You give it a milestone. veraCrew splits the work into small tasks, picks the right specialist agents, has the tests written, runs CI/CD, deploys only what changed, and hands you a client-ready report as a slide deck. A person approves at every gate, and every action is in the audit log.',
 'Le das un hito. veraCrew divide el trabajo en tareas pequeñas, elige a los agentes especialistas adecuados, encarga los tests, ejecuta el CI/CD, despliega solo lo que cambió y te entrega un informe listo para el cliente en forma de presentación. Una persona aprueba en cada etapa y cada acción queda en el registro de auditoría.',
 'Dajesz mu kamień milowy. veraCrew dzieli pracę na małe zadania, dobiera właściwych agentów-specjalistów, zleca napisanie testów, uruchamia CI/CD, wdraża tylko to, co się zmieniło, i oddaje raport gotowy dla klienta w formie prezentacji. Człowiek zatwierdza każdy etap, a każda akcja trafia do dziennika audytu.')}</p>
<div class="cta"><a class="btn primary" href="index.html?topic=demo#contact">{E('Ask for a demo', 'Pedir una demo', 'Poproś o demo')}</a><a class="btn" href="#how">{E('How it works', 'Cómo funciona', 'Jak to działa')}</a></div>
</div>
<aside class="sheet" aria-labelledby="vc-facts"><h2 id="vc-facts">{E('At a glance', 'De un vistazo', 'W skrócie')}</h2><dl>
<dt>{E('Status', 'Estado', 'Status')}</dt><dd>{E('in daily use', 'en uso diario', 'w codziennym użyciu')}</dd>
<dt>{E('Co-created', 'Cocreado', 'Współtwórca')}</dt><dd>{E('with <a href="https://github.com/Dixter999">Daniel Łagowski</a>', 'con <a href="https://github.com/Dixter999">Daniel Łagowski</a>', '<a href="https://github.com/Dixter999">Daniel Łagowski</a>')}</dd>
<dt>{E('Merged PRs', 'PR fusionadas', 'Scalone PR')}</dt><dd>{E('1,600+ in its own repo', '1.600+ en su propio repo', '1600+ we własnym repo')}</dd>
<dt>{E('Since', 'Desde', 'Od')}</dt><dd>{E('July 2026', 'julio 2026', 'lipca 2026')}</dd>
<dt>{E('Hub', 'Hub', 'Hub')}</dt><dd>FastAPI · React · PostgreSQL · k3s</dd>
<dt>{E('Workers', 'Workers', 'Workery')}</dt><dd>{E('headless Claude Code on several machines', 'Claude Code headless en varias máquinas', 'headless Claude Code na kilku maszynach')}</dd>
<dt>{E('Output', 'Resultado', 'Rezultat')}</dt><dd>{E('merged, deployed PRs + client deck', 'PR fusionadas y desplegadas + presentación', 'scalone, wdrożone PR + prezentacja')}</dd>
</dl></aside>
</div>

<section id="how" aria-labelledby="how-h"><h2 class="s" id="how-h">{E('How a job moves through veraCrew', 'Cómo avanza un trabajo en veraCrew', 'Jak praca przechodzi przez veraCrew')}</h2>
<p class="intro">{E('One milestone, taken one item at a time. The lime pulse is the work; the dark steps are where a gate decides.', 'Un hito, elemento a elemento. El pulso lima es el trabajo; los pasos oscuros son donde decide una puerta.', 'Jeden kamień milowy, po jednym zadaniu naraz. Limonkowy puls to praca; ciemne kroki to miejsca, gdzie decyduje bramka.')}</p>
<ol class="vpipe">
{vstep(0,'Milestone in','Entra un hito','Kamień milowy','Issues with type, area and size labels; epics and too-broad items are held, not dispatched.','Issues con etiquetas de tipo, área y tamaño; las épicas y lo demasiado amplio se retienen, no se despachan.','Zadania z etykietami typu, obszaru i rozmiaru; epiki i zbyt szerokie zadania są wstrzymywane, a nie wysyłane.')}
{vstep(1,'Split','Dividir','Podział','Broad work is split into small, dispatchable tasks.','El trabajo amplio se divide en tareas pequeñas y despachables.','Szeroka praca jest dzielona na małe zadania gotowe do wysłania.')}
{vstep(2,'Pick agents','Elegir agentes','Dobór agentów','The hub picks a worker with the right contract on a machine that is really alive.','El hub elige un worker con el contrato adecuado en una máquina que de verdad está viva.','Hub wybiera workera z właściwym kontraktem na maszynie, która naprawdę działa.')}
{vstep(3,'Tests and code','Tests y código','Testy i kod','A headless Claude Code worker writes the tests and the change and commits before any fragile step.','Un worker de Claude Code sin interfaz escribe los tests y el cambio, y hace commit antes de cualquier paso frágil.','Headless worker Claude Code pisze testy i zmianę, a commit robi przed każdym ryzykownym krokiem.')}
{vstep(4,'CI + AI review','CI + revisión IA','CI + przegląd AI','Every pull request runs CI and passes an AI review gate; failures go back as fix rounds.','Cada pull request pasa el CI y una puerta de revisión con IA; los fallos vuelven como rondas de corrección.','Każdy pull request przechodzi CI i bramkę przeglądu AI; błędy wracają jako rundy poprawek.', True)}
{vstep(5,'Merge and deploy','Fusionar y desplegar','Scalenie i wdrożenie','Merged only when approved and green, then only what changed is rolled out and checked: served equals merged.','Se fusiona solo con aprobación y en verde; después se despliega solo lo que cambió y se comprueba que lo servido es lo fusionado.','Scalane tylko po akceptacji i na zielono; potem wdrażane jest tylko to, co się zmieniło, i sprawdzane, że działa dokładnie to, co scalono.', True)}
{vstep(6,'Human gate','Puerta humana','Bramka człowieka','The final merge to the main branch stays a human decision, by policy.','La fusión final a la rama principal sigue siendo una decisión humana, por política.','Ostateczne scalenie do głównej gałęzi z zasady pozostaje decyzją człowieka.', True)}
{vstep(7,'Report','Informe','Raport','A delivery report per walk, as a web page and a PowerPoint deck for the client, with nothing internal in it.','Un informe de entrega por recorrido, como página web y como presentación PowerPoint para el cliente, sin nada interno.','Raport z każdego przebiegu, jako strona i prezentacja PowerPoint dla klienta, bez danych wewnętrznych.')}
</ol>
</section>

<section aria-labelledby="vc-what"><h2 class="s" id="vc-what">{E('What it takes off your hands', 'Lo que te quita de encima', 'Co bierze na siebie')}</h2>
<div class="cols3 vfeat">
{feat('Planning and dispatch','Planificación y reparto','Planowanie i rozdział pracy','Walks take a milestone in order, one item at a time, and refuse what a machine should not pick up: epics, too-broad issues, non-code work.','Los recorridos toman un hito en orden, elemento a elemento, y rechazan lo que una máquina no debería coger: épicas, issues demasiado amplios, trabajo que no es código.','Przebiegi realizują kamień milowy po kolei, po jednym zadaniu, i odrzucają to, czego maszyna nie powinna brać: epiki, zbyt szerokie zadania, pracę niebędącą kodem.')}
{feat('A fleet of workers','Una flota de workers','Flota workerów','Node agents on several machines dial out to the hub, supervise local workers and come back on their own after sleep or reboot.','Agentes de nodo en varias máquinas se conectan al hub, supervisan workers locales y vuelven solos tras una suspensión o un reinicio.','Agenci węzłów na kilku maszynach łączą się z hubem, nadzorują lokalnych workerów i sami wracają po uśpieniu lub restarcie.')}
{feat('Quality gates','Puertas de calidad','Bramki jakości','CI, an AI review gate and a scope guard on every PR; one deploy at a time, never with an admin override.','CI, una puerta de revisión con IA y un control de alcance en cada PR; un despliegue cada vez, nunca forzado con permisos de administrador.','CI, bramka przeglądu AI i kontrola zakresu przy każdym PR; jedno wdrożenie naraz, nigdy wymuszone uprawnieniami administratora.')}
{feat('Honest status','Estado honesto','Uczciwy status','The panel answers three questions: what needs me, what is stuck, is the fleet healthy. Status comes from live sources, never from an agent saying it is fine.','El panel responde tres preguntas: qué me necesita, qué está atascado, si la flota está sana. El estado sale de fuentes vivas, nunca de un agente que dice que todo va bien.','Panel odpowiada na trzy pytania: co wymaga mojej uwagi, co utknęło, czy flota jest zdrowa. Status pochodzi z żywych źródeł, nigdy z deklaracji agenta, że wszystko gra.')}
{feat('Cost and delivery','Coste y entrega','Koszt i dostarczenie','Cost per run and per walk, capacity, and what was actually delivered, including production changes with their evidence.','Coste por ejecución y por recorrido, capacidad, y lo que de verdad se entregó, incluidos cambios en producción con su evidencia.','Koszt każdego uruchomienia i przebiegu, przepustowość oraz to, co faktycznie dostarczono, łącznie ze zmianami produkcyjnymi i dowodami.')}
{feat('Client portal and deck','Portal y presentación para el cliente','Portal i prezentacja dla klienta','Clients see only their own walks and reports, with no cost, machine or log data, and get the result as a slide deck.','Los clientes ven solo sus recorridos e informes, sin costes, máquinas ni logs, y reciben el resultado como presentación.','Klienci widzą tylko swoje przebiegi i raporty, bez kosztów, maszyn i logów, a wynik dostają jako prezentację.')}
</div>
</section>

<section class="band" aria-labelledby="vc-rules"><h2 class="s" id="vc-rules">{E('The rules it runs on', 'Las reglas con las que funciona', 'Zasady, na których działa')}</h2>
<div class="trust">
<div><b>{E('Truth over confabulation', 'Verdad antes que invención', 'Prawda zamiast konfabulacji')}</b><span>{E('A row that says running when nothing runs is worse than no row. Status is derived, not self-reported.', 'Una fila que dice “en marcha” cuando nada corre es peor que ninguna. El estado se deriva, no se autodeclara.', 'Wiersz „działa”, gdy nic nie działa, jest gorszy niż brak wiersza. Status jest wyliczany, a nie deklarowany.')}</span></div>
<div><b>{E('Durable work', 'Trabajo duradero', 'Trwała praca')}</b><span>{E('Commit before the fragile step; a rate-limited run keeps its worktree and resumes without redoing work.', 'Commit antes del paso frágil; una ejecución limitada conserva su worktree y se reanuda sin rehacer trabajo.', 'Commit przed ryzykownym krokiem; przerwane uruchomienie zachowuje worktree i wznawia pracę bez powtarzania.')}</span></div>
<div><b>{E('People at the gates', 'Personas en las puertas', 'Ludzie przy bramkach')}</b><span>{E('Agents do the work; approvals and the final merge stay with people.', 'Los agentes hacen el trabajo; las aprobaciones y la fusión final siguen siendo de las personas.', 'Agenci wykonują pracę; akceptacje i ostateczne scalenie zostają przy ludziach.')}</span></div>
<div><b>{E('Everything audited', 'Todo auditado', 'Wszystko w audycie')}</b><span>{E('Every dispatch, gate and deploy is in the history, from issue to PR to run to report.', 'Cada envío, puerta y despliegue queda en el historial, del issue a la PR, a la ejecución y al informe.', 'Każde zlecenie, bramka i wdrożenie jest w historii: od zadania przez PR i uruchomienie po raport.')}</span></div>
</div>
</section>

<section aria-labelledby="vc-stack"><h2 class="s sm" id="vc-stack">{E('Built with', 'Construido con', 'Zbudowane z')}</h2>
<div class="chips"><span>FastAPI</span><span>React · Vite</span><span>PostgreSQL</span><span>Python node-agent</span><span>Claude Code workers</span><span>k3s · Kubernetes</span><span>GitHub Actions</span><span>WebSockets</span><span>python-pptx</span></div>
</section>

<section class="cta-band"><h2 class="s">{E('Want to see it on a real backlog?', '¿Quieres verlo con un backlog real?', 'Chcesz zobaczyć to na prawdziwym backlogu?')}</h2>
<p class="intro">{E('I can show a live walk: from a milestone of issues to merged, deployed pull requests and the client deck.', 'Puedo enseñarte un recorrido en directo: de un hito de issues a pull requests fusionadas y desplegadas, y la presentación para el cliente.', 'Mogę pokazać przebieg na żywo: od kamienia milowego z zadaniami do scalonych, wdrożonych pull requestów i prezentacji dla klienta.')}</p>
<a class="btn primary" href="index.html?topic=demo#contact">{E('Ask for a demo', 'Pedir una demo', 'Poproś o demo')}</a></section>
'''

# ---------------------------------------------------------------- 404
nf_main = ph(E('Page not found', 'Página no encontrada', 'Nie znaleziono strony'),
 E('The address may have changed.', 'Puede que la dirección haya cambiado.', 'Adres mógł się zmienić.')) + \
 f'<p><a class="btn primary" href="/index.html">{E("Go to the home page", "Ir a la página principal", "Przejdź na stronę główną")}</a></p>'

PAGES = [
    ('index.html', None, ('Rafał Łagowski · AI architecture and implementation for businesses', 'Rafał Łagowski · Arquitectura e implantación de IA para empresas', 'Rafał Łagowski · Architektura i wdrożenia AI dla firm'),
     'Diseño e implemento soluciones de IA que automatizan operaciones, conectan sistemas y reducen costes, con supervisión humana. Rafał Łagowski, arquitecto de IA en Madrid.',
     home_main, home_head, ('assets/site.js',)),
    ('work-with-me.html', 'work', ('How I work · Rafał Łagowski', 'Cómo trabajo · Rafał Łagowski', 'Jak pracuję · Rafał Łagowski'),
     'Diagnóstico, implantación y evolución continua de soluciones de IA. Colaboración continua desde 3.000 €/mes + IVA; alcance y precio por escrito.',
     work_main, '', ('assets/site.js',)),
    ('veracrew.html', 'veracrew', ('veraCrew · a virtual consulting company run by AI agents', 'veraCrew · una consultora virtual dirigida por agentes de IA', 'veraCrew · wirtualna firma konsultingowa prowadzona przez agentów AI'),
     'veraCrew by Rafał Łagowski: AI agents that split a milestone into tasks, write tests, run CI/CD, deploy and report to the client as a slide deck, with people at every gate.',
     veracrew_main, '', ('assets/site.js',)),
    ('demos.html', 'demos', ('Interactive AI demos · Rafał Łagowski', 'Demos de IA interactivas · Rafał Łagowski', 'Interaktywne dema AI · Rafał Łagowski'),
     'Four in-browser demos: an EU AI Act risk classifier, an assistant with cited sources, a bias audit and an outreach simulator. Sample data, no model calls.',
     demos_main, '', ('assets/site.js', 'assets/demos.js')),
    ('career.html', None, ('Career · Rafał Łagowski', 'Carrera · Rafał Łagowski', 'Kariera · Rafał Łagowski'),
     'Rafał Łagowski for recruiters: roles, experience, Google Cloud certifications, languages and CV on request.',
     career_main, '', ('assets/site.js',)),
    ('about.html', 'about', ('About · Rafał Łagowski', 'Sobre mí · Rafał Łagowski', 'O mnie · Rafał Łagowski'),
     'About Rafał Łagowski: AI and cloud architect and telecommunications engineer based in Madrid, 20+ years building technology.',
     about_main, '', ('assets/site.js',)),
    ('process.html', None, ('Process · Rafał Łagowski', 'Proceso · Rafał Łagowski', 'Proces · Rafał Łagowski'),
     'How an engagement with Rafał Łagowski works: free call, written recommendation, fixed-price proposal, short deliveries and handover.',
     process_main, '', ('assets/site.js',)),
    ('faq.html', None, ('FAQ · Rafał Łagowski', 'Preguntas frecuentes · Rafał Łagowski', 'FAQ · Rafał Łagowski'),
     'Frequently asked questions about working with Rafał Łagowski: availability, pricing, ownership, data, the EU AI Act and languages.',
     faq_main, '', ('assets/site.js',)),
]

for fname, key, titles, desc, main, head, scripts in PAGES:
    with open(os.path.join(ROOT, fname), 'w', encoding='utf-8') as f:
        f.write(page(fname, key, titles, desc, main, head, scripts))

for fname, titles, main in (
    ('sent.html', ('Message sent · Rafał Łagowski', 'Mensaje enviado · Rafał Łagowski', 'Wiadomość wysłana · Rafał Łagowski'),
     ph(E('Thank you, your message is on its way', 'Gracias, tu mensaje está en camino', 'Dziękuję, wiadomość została wysłana'),
        E('I reply by email within two working days.', 'Respondo por correo en dos días laborables.', 'Odpowiem mailem w ciągu dwóch dni roboczych.'))),
    ('not-sent.html', ('Message not sent · Rafał Łagowski', 'Mensaje no enviado · Rafał Łagowski', 'Wiadomość nie została wysłana · Rafał Łagowski'),
     ph(E('The message could not be sent', 'No se pudo enviar el mensaje', 'Nie udało się wysłać wiadomości'),
        E('Check that every field is filled in and try again in a few minutes, or write to me on LinkedIn.', 'Comprueba que todos los campos están completos e inténtalo de nuevo en unos minutos, o escríbeme por LinkedIn.', 'Sprawdź, czy wszystkie pola są wypełnione, i spróbuj ponownie za kilka minut albo napisz do mnie na LinkedIn.'))),
):
    with open(os.path.join(ROOT, fname), 'w', encoding='utf-8') as f:
        f.write(page(fname, None, titles, titles[0], main + f'<p><a class="btn" href="index.html">{E("Back to the home page", "Volver al inicio", "Wróć na stronę główną")}</a></p>',
                     '<meta name="robots" content="noindex">\n', ('assets/site.js',)))

with open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8') as f:
    f.write(page('404.html', None, ('Page not found · Rafał Łagowski', 'Página no encontrada · Rafał Łagowski', 'Nie znaleziono strony · Rafał Łagowski'),
                 'Page not found.', nf_main, '<meta name="robots" content="noindex">\n', ('assets/site.js',), prefix='/'))

with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for fname, *_ in PAGES:
        f.write(f'  <url><loc>{BASE}/{"" if fname == "index.html" else fname}</loc></url>\n')
    f.write('</urlset>\n')

print('generated', len(PAGES) + 1, 'pages')
