#!/usr/bin/env python3
"""Generates the static pages of rafal.lagowski.es into the repository root.

The site itself has no build step: the generated HTML is committed and served
as is. This script only exists so the three languages stay in one place.
Run from the repository root:  python3 tools/gen.py
"""
import json, os

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


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


NAV = [
    ('index.html#work', E('Work', 'Proyectos', 'Projekty'), None),
    ('demos.html', E('Demos', 'Demos', 'Dema'), 'demos'),
    ('index.html#writing', E('Writing', 'Artículos', 'Teksty'), None),
    ('index.html#experience', E('Experience', 'Experiencia', 'Doświadczenie'), None),
    ('work-with-me.html', E('Work with me', 'Trabajar conmigo', 'Współpraca'), 'work'),
    ('about.html', E('About', 'Sobre mí', 'O mnie'), 'about'),
    ('index.html#contact', E('Contact', 'Contacto', 'Kontakt'), None),
]

EARLY = ("<script>(function(){var l='en';try{var s=localStorage.getItem('lagowski-lang');"
         "if(s==='en'||s==='es'||s==='pl')l=s;else{var n=(navigator.language||'en').slice(0,2).toLowerCase();"
         "if(n==='es'||n==='pl')l=n}}catch(e){}window.__lang=l;document.body.className=l})()</script>")


def cv_button(cls='btn primary'):
    """The CV is not published; it is sent on request through the contact form."""
    return f'<a class="{cls}" href="index.html?topic=cv#contact">{E("Request my CV", "Pedir mi CV", "Poproś o CV")}</a>'


def linkedin_link(cls=''):
    if LINKEDIN:
        return f'<a href="{LINKEDIN}" rel="me">LinkedIn</a>'
    return ''


def contact_block():
    req = ' required'
    opts = ''.join(f'<option value="{v}">{t}</option>' for v, t in (
        ('role', 'Role / position · Puesto · Stanowisko'),
        ('contract', 'Contract / freelance · Contrato · Kontrakt'),
        ('consulting', 'Consulting · Consultoría · Konsulting'),
        ('cv', 'CV request · Solicitar CV · Prośba o CV'),
        ('other', 'Other · Otro · Inne')))
    return f'''<section class="contact" id="contact" aria-labelledby="contact-h"><h2 class="s" id="contact-h">{E('Contact', 'Contacto', 'Kontakt')}</h2>
<p class="intro">{E('For roles, contracts, consulting and CV requests. I reply by email within two working days, in English, Spanish or Polish.',
 'Para puestos, contratos, consultoría o para pedir mi CV. Respondo por correo en dos días laborables, en español, inglés o polaco.',
 'W sprawie stanowisk, kontraktów, konsultacji lub CV. Odpowiadam mailem w ciągu dwóch dni roboczych, po polsku, angielsku lub hiszpańsku.')}</p>
<form class="cform" id="cform" action="/api/contact" method="post">
<div class="f2"><label>{E('Name', 'Nombre', 'Imię i nazwisko')}<input name="name" autocomplete="name" maxlength="120"{req}></label>
<label>{E('Email', 'Correo electrónico', 'E-mail')}<input name="email" type="email" autocomplete="email" maxlength="254"{req}></label></div>
<div class="f2"><label>{E('Company (optional)', 'Empresa (opcional)', 'Firma (opcjonalnie)')}<input name="company" autocomplete="organization" maxlength="160"></label>
<label>{E('Topic', 'Tema', 'Temat')}<select name="topic" id="ctopic">{opts}</select></label></div>
<label>{E('Message', 'Mensaje', 'Wiadomość')}<textarea name="message" rows="5" minlength="10" maxlength="5000"{req}></textarea></label>
<div class="hp" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
<input type="hidden" name="t" id="ct"><input type="hidden" name="lang" id="clang" value="en">
<div class="fend"><button class="btn primary" type="submit">{E('Send', 'Enviar', 'Wyślij')}</button>
<p class="fnote">{E('Your details are used only to answer you and are not stored on this site.', 'Tus datos solo se usan para responderte y no se guardan en esta web.', 'Twoje dane służą wyłącznie do odpowiedzi i nie są przechowywane na tej stronie.')}</p></div>
<p class="fstatus" id="cstatus" role="status" aria-live="polite"></p>
</form>
<div class="links">{linkedin_link()}<a href="{GITHUB}" rel="me">GitHub</a><a href="{MEDIUM}" rel="me">Medium</a></div>
</section>'''


FOOTER = f'''<footer><nav aria-label="{esc('Footer')}"><a href="about.html">{E('About', 'Sobre mí', 'O mnie')}</a><a href="process.html">{E('Process', 'Proceso', 'Proces')}</a><a href="faq.html">FAQ</a><a href="demos.html">{E('Demos', 'Demos', 'Dema')}</a><a href="work-with-me.html">{E('Work with me', 'Trabajar conmigo', 'Współpraca')}</a></nav>
<p>© 2026 Rafał Łagowski · Madrid · rafal.lagowski.es</p></footer>'''


def page(fname, key, titles, desc, main, extra_head='', scripts=('assets/site.js',), prefix=''):
    canon = BASE + '/' + ('' if fname == 'index.html' else fname)
    nav = ''.join(
        f'<a href="{prefix}{h}"{" aria-current=\"page\"" if k and k == key else ""}>{t}</a>' for h, t, k in NAV)
    t_en, t_es, t_pl = titles
    scr = ''.join(f'<script src="{prefix}{s}" defer></script>' for s in scripts)
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
<link rel="stylesheet" href="{prefix}assets/fonts.css">
<link rel="stylesheet" href="{prefix}assets/site.css">
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
  <nav aria-label="Main">{nav}</nav>
</header>
<main id="main">
{main}
</main>
{FOOTER}</div>
{scr}
</body>
</html>
'''


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


home_main = f'''<div class="hero">
<div>
<p class="eyebrow">{E('Madrid · CET · remote across Europe', 'Madrid · CET · en remoto por Europa', 'Madryt · CET · zdalnie w całej Europie')}</p>
<h1>Rafał <span class="hl">Łagowski</span></h1>
<p class="role">{E('AI &amp; Agentic Systems Architect', 'Arquitecto de IA y sistemas agénticos', 'Architekt AI i systemów agentowych')}</p>
<p class="tagline">{E('AI in production, governed from day one.', 'IA en producción, gobernada desde el primer día.', 'AI w produkcji, pod kontrolą od pierwszego dnia.')}</p>
<p class="lede">{E('I design and build agentic systems that behave predictably in production: LLM agents inside deterministic workflows, RAG over enterprise data, evaluation and observability, and governance that holds up to security reviews and the EU AI Act. 20+ years in software and cloud: founder or co-founder of four companies, then AI programmes at Accenture for FCC, MasOrange, CaixaBank and Zurich Seguros, now Lead Cloud &amp; AI Architect at a global manufacturer.',
 'Diseño y construyo sistemas agénticos que se comportan de forma predecible en producción: agentes LLM dentro de flujos deterministas, RAG sobre datos corporativos, evaluación y observabilidad, y un gobierno que supera revisiones de seguridad y el Reglamento Europeo de IA. Más de 20 años en software y cloud: fundador o cofundador de cuatro empresas, después programas de IA en Accenture para FCC, MasOrange, CaixaBank y Zurich Seguros, y hoy Lead Cloud &amp; AI Architect en un fabricante global.',
 'Projektuję i buduję systemy agentowe, które w produkcji zachowują się przewidywalnie: agenci LLM w deterministycznych przepływach, RAG na danych firmowych, ewaluacja i obserwowalność oraz nadzór, który przechodzi audyty bezpieczeństwa i wymogi AI Act. Ponad 20 lat w oprogramowaniu i chmurze: założyciel lub współzałożyciel czterech firm, potem programy AI w Accenture dla FCC, MasOrange, CaixaBank i Zurich Seguros, dziś Lead Cloud &amp; AI Architect w globalnej firmie produkcyjnej.')}</p>
<div class="cta">{cv_button()}<a class="btn" href="#contact">{E('Contact', 'Contacto', 'Kontakt')}</a></div>
</div>
<aside class="sheet" aria-labelledby="facts-h"><h2 id="facts-h">{E('Profile', 'Perfil', 'Profil')}</h2><dl>
<dt>{E('Based in', 'Base', 'Miejsce')}</dt><dd>Madrid · CET</dd>
<dt>{E('Work', 'Formato', 'Tryb')}</dt><dd>{E('remote or on site', 'remoto o presencial', 'zdalnie lub na miejscu')}</dd>
<dt>{E('Languages', 'Idiomas', 'Języki')}</dt><dd>EN · ES · PL · CS</dd>
<dt>{E('Clouds', 'Clouds', 'Chmury')}</dt><dd>Google Cloud · Azure · AWS</dd>
<dt>{E('Platforms', 'Plataformas', 'Platformy')}</dt><dd>Kubernetes · Terraform · Docker · CI/CD</dd>
<dt>{E('Focus', 'Foco', 'Specjalizacja')}</dt><dd>{E('AI agents · RAG · LLMOps · EU AI Act', 'Agentes · RAG · LLMOps · AI Act', 'Agenci · RAG · LLMOps · AI Act')}</dd>
<dt>{E('Experience', 'Experiencia', 'Doświadczenie')}</dt><dd>{E('20+ years', '20+ años', '20+ lat')}</dd>
</dl></aside>
</div>

<section id="work" aria-labelledby="work-h"><h2 class="s" id="work-h">{E('Selected work', 'Proyectos seleccionados', 'Wybrane projekty')}</h2>
<p class="intro">{E('Systems I designed and built. Each one says whether the code is open, private or built for a client.',
 'Sistemas que he diseñado y construido. Cada uno indica si el código es abierto, privado o para un cliente.',
 'Systemy, które zaprojektowałem i zbudowałem. Przy każdym widać, czy kod jest otwarty, prywatny, czy powstał dla klienta.')}</p>
<div class="card"><span class="tag">{E('Accenture · Team Lead · 2024 – 2026', 'Accenture · Team Lead · 2024 – 2026', 'Accenture · Team Lead · 2024 – 2026')}</span>
<h3>{E('FCC · AI-powered bid generation', 'FCC · generación de ofertas con IA', 'FCC · generowanie ofert przetargowych z AI')}</h3>
<p>{E('I led a team of 6 developers building AI agents that analyse public tender specifications (pliegos) and generate bid proposals. The result: a 70% reduction in the time needed to create an offer.',
 'Lideré un equipo de 6 desarrolladores que construyó agentes de IA que analizan pliegos de licitaciones públicas y generan propuestas de oferta. Resultado: un 70% menos de tiempo para preparar una oferta.',
 'Prowadziłem zespół 6 programistów, który zbudował agentów AI analizujących specyfikacje przetargów publicznych (pliegos) i generujących propozycje ofert. Efekt: czas przygotowania oferty krótszy o 70%.')}</p>
<p class="stack">Azure OpenAI · Azure AI Search · CosmosDB · Python · FastAPI · Kubernetes · Docker</p></div>
<div class="proof">
{card(E('Accenture · Tech Lead · 2025 · Project of the Year', 'Accenture · Tech Lead · 2025 · Proyecto del Año', 'Accenture · Tech Lead · 2025 · Projekt Roku'), E('MasOrange · real-time AI for call centres', 'MasOrange · IA en tiempo real para call centers', 'MasOrange · AI w czasie rzeczywistym dla call center'),
 E('Real-time AI suggestions for call-centre operators during live calls, with an automated testing framework built on Cucumber. Recognised as Project of the Year (Feb – May 2025).',
   'Sugerencias de IA en tiempo real para los operadores del call center durante las llamadas, con un marco de pruebas automatizadas en Cucumber. Reconocido como Proyecto del Año (feb – may 2025).',
   'Podpowiedzi AI w czasie rzeczywistym dla konsultantów call center podczas rozmów, z frameworkiem testów automatycznych opartym na Cucumber. Wyróżniony jako Projekt Roku (lut – maj 2025).'),
 'GCP · Gemini · Speech-to-Text · Redis · BigQuery · FastAPI')}
{card(E('Real estate · pricing intelligence', 'Inmobiliario · inteligencia de precios', 'Nieruchomości · analityka cen'), 'P&amp;O Apartments',
 E('A system that collects property listings, stores them in a price database and exposes market prices through an API.',
   'Un sistema que recoge anuncios de inmuebles, los guarda en una base de datos de precios y expone los precios de mercado mediante una API.',
   'System, który zbiera ogłoszenia nieruchomości, zapisuje je w bazie cen i udostępnia ceny rynkowe przez API.'),
 'Python · ' + E('data pipelines', 'pipelines de datos', 'potoki danych') + ' · PostgreSQL · REST API', '<a href="https://pandoapartments.eu">pandoapartments.eu</a>')}
</div>
<div class="card"><span class="tag">{E('Own product · demo on request', 'Producto propio · demo bajo petición', 'Własny produkt · demo na życzenie')}</span>
<h3>veraCrew</h3>
<p>{E('An AI-driven software delivery system. Specialised agents take work from requirement to specification, planning, implementation, review and release, with an explicit human approval gate at every stage. I used it as the working proof for an AI implementation path at a global manufacturer: business ideas reach deployed solutions faster, with every decision traceable.',
 'Un sistema de entrega de software dirigido por IA. Agentes especializados llevan el trabajo desde el requisito a la especificación, la planificación, la implementación, la revisión y la publicación, con una aprobación humana explícita en cada etapa. Lo usé como prueba real de un camino de implantación de IA en un fabricante global: las ideas de negocio llegan antes a soluciones desplegadas, con cada decisión trazable.',
 'System dostarczania oprogramowania sterowany przez AI. Wyspecjalizowani agenci prowadzą pracę od wymagania przez specyfikację, planowanie, implementację i przegląd aż do wydania, z wyraźną akceptacją człowieka na każdym etapie. Posłużył mi jako działający dowód ścieżki wdrażania AI w globalnej firmie produkcyjnej: pomysły biznesowe szybciej stają się wdrożonymi rozwiązaniami, a każda decyzja jest możliwa do prześledzenia.')}</p>
<p class="stack">Python · multi-agent orchestration · Claude / OpenAI APIs · GitHub · CI/CD · {E('with Cortex, a companion system that structures project knowledge for the agents', 'con Cortex, un sistema que estructura el conocimiento del proyecto para los agentes', 'razem z Cortex, systemem porządkującym wiedzę o projekcie dla agentów')}</p>
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
{card(E('For a global manufacturer · 2026', 'Para un fabricante global · 2026', 'Dla globalnej firmy produkcyjnej · 2026'), 'Governed AI Gateway',
 E('A central gateway for compliant LLM access: multi-model routing, personal-data masking, policy lanes per use case and hash-chained audit logs aligned with Article 12 of the EU AI Act. It comes with an inventory of 37 AI use cases and 30+ business cases that drive model choice by cost, performance and risk.',
   'Una pasarela central para acceder a LLM cumpliendo la normativa: enrutado entre modelos, enmascarado de datos personales, carriles de política por caso de uso y registros de auditoría encadenados por hash, alineados con el artículo 12 del Reglamento Europeo de IA. Incluye un inventario de 37 casos de uso de IA y más de 30 casos de negocio que guían la elección de modelo por coste, rendimiento y riesgo.',
   'Centralna bramka do zgodnego z przepisami dostępu do LLM: routing między modelami, maskowanie danych osobowych, ścieżki polityk dla każdego przypadku użycia i łańcuchowane hashami logi audytowe zgodne z art. 12 AI Act. Towarzyszy jej inwentarz 37 przypadków użycia AI i ponad 30 business case’ów, które sterują wyborem modelu według kosztu, wydajności i ryzyka.'),
 'LiteLLM · Microsoft Presidio · OPA · Langfuse · OpenTelemetry · Azure')}
<a class="card big" href="demos.html"><span class="tag">{E('Runs in your browser', 'Funciona en tu navegador', 'Działa w przeglądarce')}</span><h3>{E('Interactive demos', 'Demos interactivas', 'Interaktywne dema')}</h3>
<p>{E('Four small demos with sample data and no model calls: an EU AI Act risk classifier, an assistant that only answers with cited sources, a bias audit and an outreach simulator.',
 'Cuatro demos pequeñas con datos de ejemplo y sin llamadas a modelos: un clasificador de riesgo del Reglamento de IA, un asistente que solo responde citando fuentes, una auditoría de sesgo y un simulador de alcance.',
 'Cztery małe dema na przykładowych danych, bez wywołań modeli: klasyfikator ryzyka według AI Act, asystent odpowiadający wyłącznie z cytowanymi źródłami, audyt stronniczości i symulator dotarcia.')}</p><span class="more">{E('Open the demos →', 'Abrir las demos →', 'Otwórz dema →')}</span></a>
</div>
<p class="note">{E('Also open source:', 'También en abierto:', 'Również open source:')} <a href="{ORG}/ClaudeAutoPM">ClaudeAutoPM</a>{E(', a multi-agent project management framework published as npm packages (39 stars on GitHub).', ', un framework multiagente de gestión de proyectos publicado como paquetes npm (39 estrellas en GitHub).', ', wieloagentowy framework do zarządzania projektami opublikowany jako pakiety npm (39 gwiazdek na GitHubie).')}</p>
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

<section id="experience" aria-labelledby="xp-h"><h2 class="s" id="xp-h">{E('Experience', 'Experiencia', 'Doświadczenie')}</h2>
<p class="intro"><span class="tag">TechStar 2025</span><br>{E('TechStar 2025 at Accenture; MasOrange engagement named Project of the Year.', 'TechStar 2025 en Accenture; el proyecto de MasOrange fue elegido Proyecto del Año.', 'TechStar 2025 w Accenture; projekt dla MasOrange wyróżniony jako Projekt Roku.')}</p>
<ol class="xp" reversed>
<li><span class="when"><span class="now">{E('2026 – present', '2026 – actualidad', '2026 – obecnie')}</span></span><div><b>Lead Cloud &amp; AI Architect</b><span class="org">{E('Global consumer goods manufacturer', 'Fabricante global de bienes de consumo', 'Globalny producent dóbr konsumpcyjnych')}</span>
<p>{E('Own the AI platform architecture and the implementation path for delivering AI solutions across business teams. Architecture lead for cloud migration and AI around an SAP S/4HANA transformation.',
 'Responsable de la arquitectura de la plataforma de IA y del camino de implantación de soluciones de IA para las áreas de negocio. Líder de arquitectura de la migración a cloud y de la IA en torno a una transformación SAP S/4HANA.',
 'Odpowiadam za architekturę platformy AI i ścieżkę wdrażania rozwiązań AI w zespołach biznesowych. Lider architektury migracji do chmury i AI w programie transformacji SAP S/4HANA.')}</p></div></li>
<li><span class="when">{E('Apr 2023 – Mar 2026', 'abr 2023 – mar 2026', 'kwi 2023 – mar 2026')}</span><div><b>Senior Cloud &amp; AI Architect, Tech Lead</b><span class="org">Accenture · Associate Manager</span>
<p>{E('AI programmes for FCC (AI bid generation, team lead), MasOrange (real-time AI for call centres, Project of the Year), CaixaBank and Zurich Seguros. At CaixaBank (Sep 2024 – Jan 2025), as Cloud Solutions Architect, I designed cloud architectures for AI-driven media analytics and a Responsible AI framework with multi-agent GenAI systems under financial-grade compliance (GCP, Vertex AI, Cloud Composer, Cloud Run). TechStar 2025.',
 'Programas de IA para FCC (generación de ofertas con IA, como team lead), MasOrange (IA en tiempo real para call centers, Proyecto del Año), CaixaBank y Zurich Seguros. En CaixaBank (sep 2024 – ene 2025), como Cloud Solutions Architect, diseñé arquitecturas cloud para analítica de medios basada en IA y un marco de IA responsable con sistemas GenAI multiagente bajo cumplimiento de nivel financiero (GCP, Vertex AI, Cloud Composer, Cloud Run). TechStar 2025.',
 'Programy AI dla FCC (generowanie ofert z AI, jako team lead), MasOrange (AI w czasie rzeczywistym dla call center, Projekt Roku), CaixaBank i Zurich Seguros. W CaixaBank (wrz 2024 – sty 2025), jako Cloud Solutions Architect, projektowałem architektury chmurowe dla analityki mediów opartej na AI oraz framework odpowiedzialnej AI z wieloagentowymi systemami GenAI w reżimie zgodności sektora finansowego (GCP, Vertex AI, Cloud Composer, Cloud Run). TechStar 2025.')}</p></div></li>
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
<div><b>{E('Banking &amp; financial services', 'Banca y servicios financieros', 'Bankowość i usługi finansowe')}</b><span>{E('CaixaBank (Sep 2024 – Jan 2025, with Accenture): cloud architectures for AI-driven media analytics and a Responsible AI framework with multi-agent GenAI systems under financial-grade compliance. Banco de España (2023, with Accenture): data architecture and pipelines on AWS.',
 'CaixaBank (sep 2024 – ene 2025, con Accenture): arquitecturas cloud para analítica de medios basada en IA y un marco de IA responsable con sistemas GenAI multiagente bajo cumplimiento de nivel financiero. Banco de España (2023, con Accenture): arquitectura de datos y pipelines en AWS.',
 'CaixaBank (wrz 2024 – sty 2025, z Accenture): architektury chmurowe dla analityki mediów opartej na AI i framework odpowiedzialnej AI z wieloagentowymi systemami GenAI w reżimie zgodności sektora finansowego. Banco de España (2023, z Accenture): architektura danych i potoki danych na AWS.')}</span></div>
<div><b>{E('Insurance', 'Seguros', 'Ubezpieczenia')}</b><span>{E('GenAI projects for Zurich Seguros (with Accenture). Typical use cases: claims and document intake, underwriting assistants with cited sources and human sign-off.',
 'Proyectos de IA generativa para Zurich Seguros (con Accenture). Casos de uso típicos: entrada de siniestros y documentos, asistentes de suscripción con fuentes citadas y validación humana.',
 'Projekty GenAI dla Zurich Seguros (z Accenture). Typowe zastosowania: przyjmowanie szkód i dokumentów, asystenci underwritingu z cytowanymi źródłami i akceptacją człowieka.')}</span></div>
<div><b>{E('Telecommunications', 'Telecomunicaciones', 'Telekomunikacja')}</b><span>{E('MasOrange (2025, with Accenture): real-time AI suggestions for call-centre operators during live calls; Project of the Year.',
 'MasOrange (2025, con Accenture): sugerencias de IA en tiempo real para operadores de call center durante las llamadas; Proyecto del Año.',
 'MasOrange (2025, z Accenture): podpowiedzi AI w czasie rzeczywistym dla konsultantów call center podczas rozmów; Projekt Roku.')}</span></div>
<div><b>{E('Construction &amp; infrastructure', 'Construcción e infraestructuras', 'Budownictwo i infrastruktura')}</b><span>{E('FCC (2024 – 2026, with Accenture): AI agents that analyse public tender specifications and generate bid proposals; 70% less time to create an offer.',
 'FCC (2024 – 2026, con Accenture): agentes de IA que analizan pliegos de licitaciones públicas y generan propuestas de oferta; un 70% menos de tiempo para preparar una oferta.',
 'FCC (2024 – 2026, z Accenture): agenci AI analizujący specyfikacje przetargów publicznych i generujący propozycje ofert; czas przygotowania oferty krótszy o 70%.')}</span></div>
<div><b>{E('Real estate', 'Inmobiliario', 'Nieruchomości')}</b><span>{E('P&amp;O Apartments: pricing system that collects listings, stores them in a price database and serves market prices through an API. Typical use cases: listing and price data pipelines, document and contract assistants.',
 'P&amp;O Apartments: sistema de precios que recoge anuncios, los guarda en una base de datos de precios y sirve precios de mercado mediante una API. Casos de uso típicos: pipelines de datos de anuncios y precios, asistentes para documentos y contratos.',
 'P&amp;O Apartments: system cenowy, który zbiera ogłoszenia, zapisuje je w bazie cen i udostępnia ceny rynkowe przez API. Typowe zastosowania: potoki danych o ofertach i cenach, asystenci do dokumentów i umów.')}</span></div>
<div><b>{E('Manufacturing', 'Industria', 'Produkcja')}</b><span>{E('AI platform, governed AI gateway and AI use-case inventory for a global manufacturer.', 'Plataforma de IA, pasarela de IA gobernada e inventario de casos de uso para un fabricante global.', 'Platforma AI, kontrolowana bramka AI i inwentarz przypadków użycia dla globalnej firmy produkcyjnej.')}</span></div>
<div><b>{E('Pharmaceuticals &amp; healthcare', 'Farmacéutico y sanitario', 'Farmacja i ochrona zdrowia')}</b><span>{E(PLURI_EN, PLURI_ES, PLURI_PL)}</span></div>
<div><span class="k">{E('Typical use cases', 'Casos de uso típicos', 'Typowe zastosowania')}</span><b>{E('Legal', 'Legal', 'Prawo')}</b><span>{E('Contract review and clause extraction with RAG, governed document assistants.', 'Revisión de contratos y extracción de cláusulas con RAG, asistentes documentales gobernados.', 'Przegląd umów i ekstrakcja klauzul z RAG, kontrolowani asystenci dokumentów.')}</span></div>
</div>
</section>

<section aria-labelledby="wwm-h"><h2 class="s" id="wwm-h">{E('Working with me', 'Trabajar conmigo', 'Współpraca')}</h2>
<div class="cols3">
<div><h3>{E('Architecture &amp; EU AI Act review', 'Revisión de arquitectura y Reglamento de IA', 'Przegląd architektury i AI Act')}</h3><p>{E('Architecture, security, observability and cost, plus an AI system inventory and risk classification with a prioritised plan.', 'Arquitectura, seguridad, observabilidad y coste, más un inventario de sistemas de IA y su clasificación de riesgo con un plan priorizado.', 'Architektura, bezpieczeństwo, obserwowalność i koszty oraz inwentarz systemów AI z klasyfikacją ryzyka i planem według priorytetów.')}</p></div>
<div><h3>{E('Agentic system / RAG build', 'Construcción de sistemas agénticos / RAG', 'Budowa systemu agentowego / RAG')}</h3><p>{E('From a validated use case to an agent or assistant in production, with evaluation, human oversight and logging.', 'De un caso de uso validado a un agente o asistente en producción, con evaluación, supervisión humana y registro.', 'Od zweryfikowanego przypadku użycia do agenta lub asystenta w produkcji, z ewaluacją, nadzorem człowieka i logowaniem.')}</p></div>
<div><h3>{E('Team workshops', 'Talleres para equipos', 'Warsztaty dla zespołów')}</h3><p>{E('Half a day to two days on governance or agents, built around your own use cases, with a written report.', 'De medio día a dos días sobre gobierno o agentes, con vuestros propios casos de uso y un informe escrito.', 'Od pół dnia do dwóch dni o nadzorze nad AI lub agentach, na Waszych przypadkach użycia, z pisemnym raportem.')}</p></div>
</div>
<p style="margin-top:24px"><a class="btn" href="work-with-me.html">{E('Engagements and rates', 'Formatos y tarifas', 'Formy współpracy i stawki')}</a></p>
</section>
{contact_block()}'''

person = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    'name': 'Rafał Łagowski',
    'alternateName': 'Rafal Lagowski',
    'jobTitle': 'AI & Agentic Systems Architect',
    'url': BASE + '/',
    'image': BASE + '/assets/og.png',
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

work_main = ph(E('Work with me', 'Trabajar conmigo', 'Współpraca'),
 E('Selected engagements for companies that want AI in production and under control: remote, or on site in Madrid. Three formats, each with a written scope and a fixed price.',
   'Proyectos seleccionados para empresas que quieren IA en producción y bajo control: en remoto o presencial en Madrid. Tres formatos, cada uno con alcance por escrito y precio cerrado.',
   'Wybrane projekty dla firm, które chcą AI w produkcji i pod kontrolą: zdalnie lub na miejscu w Madrycie. Trzy formaty, każdy z pisemnym zakresem i stałą ceną.')) + f'''
<section class="tight"><div class="rows">
{row(E('Architecture &amp; EU AI Act review', 'Revisión de arquitectura y Reglamento de IA', 'Przegląd architektury i AI Act'),
 E('Review of an AI system or platform: models, data, security, observability and cost, every decision documented. Plus an inventory of AI systems, risk classification by your role (provider or deployer), gaps in logging, documentation and human oversight, and a plan ordered by risk and effort.',
   'Revisión de un sistema o plataforma de IA: modelos, datos, seguridad, observabilidad y coste, con cada decisión documentada. Además, inventario de sistemas de IA, clasificación de riesgo según tu papel (proveedor o responsable del despliegue), carencias de registro, documentación y supervisión humana, y un plan ordenado por riesgo y esfuerzo.',
   'Przegląd systemu lub platformy AI: modele, dane, bezpieczeństwo, obserwowalność i koszty, każda decyzja udokumentowana. Do tego inwentarz systemów AI, klasyfikacja ryzyka według Twojej roli (dostawca lub podmiot wdrażający), luki w logowaniu, dokumentacji i nadzorze człowieka oraz plan uporządkowany według ryzyka i nakładu pracy.'),
 E('1–4 weeks', '1–4 semanas', '1–4 tygodnie'))}
{row(E('Agentic system / RAG build', 'Construcción de sistemas agénticos / RAG', 'Budowa systemu agentowego / RAG'),
 E('From a validated use case to an agent or a RAG assistant in real use: integration, evaluation against an agreed success criterion, human oversight, audit logging and handover to your team. Can start as a proof of concept on your data.',
   'De un caso de uso validado a un agente o asistente RAG en uso real: integración, evaluación frente a un criterio de éxito acordado, supervisión humana, registro de auditoría y traspaso a tu equipo. Puede empezar como prueba de concepto con tus datos.',
   'Od zweryfikowanego przypadku użycia do agenta lub asystenta RAG w realnym użyciu: integracja, ewaluacja względem uzgodnionego kryterium sukcesu, nadzór człowieka, logi audytowe i przekazanie Twojemu zespołowi. Można zacząć od proof of concept na Twoich danych.'),
 E('3–14 weeks', '3–14 semanas', '3–14 tygodni'))}
{row(E('Team workshops', 'Talleres para equipos', 'Warsztaty dla zespołów'),
 E('EU AI Act and AI governance for IT, risk and compliance leads, or AI agents for business and operations teams, built around your own cases. A written 8 to 12 page report within five working days and a 30-minute follow-up session.',
   'Reglamento de IA y gobierno de la IA para responsables de TI, riesgos y cumplimiento, o agentes de IA para equipos de negocio y operaciones, con vuestros propios casos. Informe escrito de 8 a 12 páginas en cinco días laborables y una sesión de seguimiento de 30 minutos.',
   'AI Act i nadzór nad AI dla liderów IT, ryzyka i compliance albo agenci AI dla zespołów biznesowych i operacyjnych, na Waszych przypadkach. Pisemny raport na 8–12 stron w ciągu pięciu dni roboczych i 30-minutowa sesja pytań.'),
 E('0.5–2 days', '0,5–2 días', '0,5–2 dni'))}
</div>
{rate()}
<p class="note">{E('Free material, no form:', 'Material gratuito, sin formulario:', 'Darmowe materiały, bez formularza:')} {E('starter pack', 'kit de inicio', 'pakiet startowy')} (<a href="files/starter-pack-en.pdf">EN</a> · <a href="files/starter-pack-es.pdf">ES</a> · <a href="files/starter-pack-pl.pdf">PL</a>) · {E('workshop agendas', 'agendas de los talleres', 'agendy warsztatów')} (<a href="files/workshop-agendas-en.pdf">EN</a> · <a href="files/workshop-agendas-es.pdf">ES</a> · <a href="files/workshop-agendas-pl.pdf">PL</a>). {E('The templates are indicative and are not legal advice.', 'Las plantillas son orientativas y no constituyen asesoramiento jurídico.', 'Szablony są orientacyjne i nie stanowią porady prawnej.')}</p>
<div class="callout"><b>{E('What this is not', 'Lo que no es', 'Czego nie obejmuje')}</b>{E('I am an architect, not a lawyer. The EU AI Act work is technical and organisational; for a legal opinion I work with your counsel. I am vendor-independent and take no commissions.',
 'Soy arquitecto, no abogado. El trabajo sobre el Reglamento de IA es técnico y organizativo; para el dictamen jurídico trabajo con tus abogados. Soy independiente de proveedores y no cobro comisiones.',
 'Jestem architektem, nie prawnikiem. Praca nad AI Act ma charakter techniczny i organizacyjny; opinię prawną przygotowuję razem z Twoimi prawnikami. Nie jestem związany z żadnym dostawcą i nie biorę prowizji.')}</div>
</section>
{COMMITMENTS}
<section aria-labelledby="how-h"><h2 class="s sm" id="how-h">{E('How an engagement starts', 'Cómo empieza un proyecto', 'Jak zaczyna się współpraca')}</h2>
<p class="intro">{E('A free 30-minute call, then a one-page written recommendation within three working days. Money only moves after that.', 'Una llamada gratuita de 30 minutos y, en tres días laborables, una recomendación escrita de una página. El dinero solo se mueve después.', 'Bezpłatna 30-minutowa rozmowa, a w ciągu trzech dni roboczych jednostronicowa pisemna rekomendacja. Pieniądze pojawiają się dopiero potem.')} <a href="process.html">{E('The full process', 'El proceso completo', 'Cały proces')}</a> · <a href="faq.html">FAQ</a></p>
</section>
{contact_block()}'''

# ---------------------------------------------------------------- about
about_main = f'''<h1 class="ph">Rafał Łagowski</h1>
<div class="about"><div>
<p>{E('AI and cloud architect and telecommunications engineer, from Poland, based in Madrid.', 'Arquitecto de IA y cloud e ingeniero de telecomunicaciones, polaco, afincado en Madrid.', 'Architekt AI i chmury, inżynier telekomunikacji, Polak mieszkający w Madrycie.')}</p>
<p>{E('I have built technology for more than 20 years: first as founder or co-founder of four companies, then as cloud and AI architect and tech lead at Accenture for FCC, MasOrange, CaixaBank and Zurich Seguros, now as Lead Cloud &amp; AI Architect at a global manufacturer. That mix taught me how to build a system that has to work on Monday, and how to explain a technical decision to the person who signs the budget.',
 'Llevo más de 20 años construyendo tecnología: primero como fundador o cofundador de cuatro empresas, después como arquitecto cloud y de IA y tech lead en Accenture para FCC, MasOrange, CaixaBank y Zurich Seguros, y hoy como Lead Cloud &amp; AI Architect en un fabricante global. Esa mezcla me enseñó a construir un sistema que tiene que funcionar el lunes y a explicar una decisión técnica a quien firma el presupuesto.',
 'Od ponad 20 lat buduję technologię: najpierw jako założyciel lub współzałożyciel czterech firm, potem jako architekt chmury i AI oraz tech lead w Accenture dla FCC, MasOrange, CaixaBank i Zurich Seguros, dziś jako Lead Cloud &amp; AI Architect w globalnej firmie produkcyjnej. To połączenie nauczyło mnie budować system, który musi działać w poniedziałek, i tłumaczyć decyzję techniczną osobie, która podpisuje budżet.')}</p>
<p>{E('I care about AI that can be explained to an auditor and to a finance director in the same words: with sources, with traces and with a person who decides. I work in English, Spanish, Polish and Czech.',
 'Me importa una IA que se pueda explicar a un auditor y a un director financiero con las mismas palabras: con fuentes, con trazas y con una persona que decide. Trabajo en español, inglés, polaco y checo.',
 'Zależy mi na AI, którą da się wyjaśnić audytorowi i dyrektorowi finansowemu tymi samymi słowami: ze źródłami, ze śladami i z człowiekiem, który decyduje. Pracuję po polsku, angielsku, hiszpańsku i czesku.')}</p>
<div class="cta" style="margin-top:20px">{cv_button()}<a class="btn" href="index.html#experience">{E('Experience', 'Experiencia', 'Doświadczenie')}</a></div>
</div>
<div><h2 class="s sm">{E('What I work with', 'Con qué trabajo', 'Z czym pracuję')}</h2>
<div class="chips"><span>Python</span><span>LangGraph</span><span>LangChain</span><span>RAG</span><span>LLMOps</span><span>Langfuse</span><span>OpenTelemetry</span><span>LiteLLM</span><span>Presidio</span><span>OPA</span><span>Google Cloud · Vertex AI</span><span>Azure OpenAI · AI Search</span><span>AWS</span><span>Kubernetes</span><span>Terraform</span><span>FastAPI</span><span>EU AI Act</span><span>SAP S/4HANA</span></div>
<h2 class="s sm" style="margin-top:32px">{E('What I do not do', 'Lo que no hago', 'Czego nie robię')}</h2>
<ul class="ticks">
<li>{E('Resell licences or take vendor commissions.', 'Revender licencias ni cobrar comisiones de proveedores.', 'Nie odsprzedaję licencji i nie biorę prowizji od dostawców.')}</li>
<li>{E('Give legal advice.', 'Dar asesoramiento jurídico.', 'Nie udzielam porad prawnych.')}</li>
<li>{E('Leave decisions about people to an unsupervised model.', 'Dejar decisiones sobre personas a un modelo sin supervisión.', 'Nie zostawiam decyzji o ludziach modelowi bez nadzoru.')}</li>
</ul></div></div>
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
 E('Indicatively by day rate, but every engagement has a fixed price agreed in writing before it starts. The first call and the written recommendation are free.', 'De forma orientativa por tarifa diaria, pero cada proyecto tiene un precio cerrado acordado por escrito antes de empezar. La primera llamada y la recomendación escrita son gratis.', 'Orientacyjnie według stawki dziennej, ale każdy projekt ma stałą cenę uzgodnioną na piśmie przed startem. Pierwsza rozmowa i pisemna rekomendacja są bezpłatne.'))}
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

# ---------------------------------------------------------------- 404
nf_main = ph(E('Page not found', 'Página no encontrada', 'Nie znaleziono strony'),
 E('The address may have changed.', 'Puede que la dirección haya cambiado.', 'Adres mógł się zmienić.')) + \
 f'<p><a class="btn primary" href="/index.html">{E("Go to the home page", "Ir a la página principal", "Przejdź na stronę główną")}</a></p>'

PAGES = [
    ('index.html', None, ('Rafał Łagowski · AI & Agentic Systems Architect', 'Rafał Łagowski · Arquitecto de IA y sistemas agénticos', 'Rafał Łagowski · Architekt AI i systemów agentowych'),
     'Rafał Łagowski, AI & Agentic Systems Architect in Madrid. Agentic systems, RAG, LLMOps and EU AI Act governance in production. Projects, experience and contact.',
     home_main, home_head, ('assets/site.js',)),
    ('work-with-me.html', 'work', ('Work with me · Rafał Łagowski', 'Trabajar conmigo · Rafał Łagowski', 'Współpraca · Rafał Łagowski'),
     'Architecture and EU AI Act reviews, agentic system and RAG builds, and team workshops by Rafał Łagowski. Day rate and fixed price agreed in writing.',
     work_main, '', ('assets/site.js',)),
    ('demos.html', 'demos', ('Interactive AI demos · Rafał Łagowski', 'Demos de IA interactivas · Rafał Łagowski', 'Interaktywne dema AI · Rafał Łagowski'),
     'Four in-browser demos: an EU AI Act risk classifier, an assistant with cited sources, a bias audit and an outreach simulator. Sample data, no model calls.',
     demos_main, '', ('assets/site.js', 'assets/demos.js')),
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
