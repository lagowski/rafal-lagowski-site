#!/usr/bin/env python3
"""Contact form backend for rafal.lagowski.es (stdlib only).

POST /api/contact  (application/x-www-form-urlencoded)
  fields: name, email, company, topic, message, lang, website (honeypot), t (ms timestamp set by JS)
  With "Accept: application/json" it answers JSON; otherwise it redirects (303) to /sent.html or /not-sent.html,
  so the form also works without JavaScript.

Environment: SMTP_USER, SMTP_PASS (Google app password), CONTACT_TO (default rafal@lagowski.es),
             SMTP_HOST (default smtp.gmail.com), SMTP_PORT (default 587).
The visitor's address only goes into Reply-To; the message is always sent from SMTP_USER to CONTACT_TO.
"""
import json, os, re, smtplib, ssl, sys, threading, time
from email.message import EmailMessage
from email.utils import formataddr
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASS = os.environ.get('SMTP_PASS', '')
CONTACT_TO = os.environ.get('CONTACT_TO', 'rafal@lagowski.es')

TOPICS = {'role': 'Role / position', 'contract': 'Contract / freelance', 'consulting': 'Consulting enquiry',
          'cv': 'CV request', 'other': 'Other'}
EMAIL_RE = re.compile(r'^[^@\s<>"]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,24}$')
LIMIT, WINDOW = 5, 3600          # messages per IP per hour
GLOBAL_LIMIT = 40                # messages per hour in total
hits, lock = {}, threading.Lock()


def clean(v, n):
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', v or '').strip()[:n]


def one_line(v, n):
    return re.sub(r'[\r\n]+', ' ', clean(v, n))


def allowed(ip):
    now = time.time()
    with lock:
        for k in list(hits):
            hits[k] = [t for t in hits[k] if now - t < WINDOW]
            if not hits[k]:
                del hits[k]
        if len(hits.get(ip, [])) >= LIMIT or sum(len(v) for v in hits.values()) >= GLOBAL_LIMIT:
            return False
        hits.setdefault(ip, []).append(now)
        return True


def send(f, ip):
    m = EmailMessage()
    topic = TOPICS.get(f['topic'], 'Other')
    m['Subject'] = f'[rafal.lagowski.es] {topic}: {f["name"]}'
    m['From'] = formataddr(('rafal.lagowski.es', SMTP_USER))
    m['To'] = CONTACT_TO
    m['Reply-To'] = formataddr((f['name'], f['email']))
    m.set_content(f'Name: {f["name"]}\nEmail: {f["email"]}\nCompany: {f["company"] or "-"}\nTopic: {topic}\n'
                  f'Page language: {f["lang"]}\nIP: {ip}\n\n{f["message"]}\n')
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as s:
        s.starttls(context=ssl.create_default_context())
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(m)


class H(BaseHTTPRequestHandler):
    server_version = 'contact'
    sys_version = ''

    def log_message(self, fmt, *a):
        sys.stderr.write('%s %s\n' % (time.strftime('%Y-%m-%dT%H:%M:%S'), fmt % a))

    def reply(self, ok, code, err=''):
        if 'application/json' in (self.headers.get('Accept') or ''):
            body = json.dumps({'ok': ok, 'error': err}).encode()
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(303)
            self.send_header('Location', '/sent.html' if ok else '/not-sent.html')
            self.send_header('Content-Length', '0')
            self.end_headers()

    def do_GET(self):
        if self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-Length', '2')
            self.end_headers()
            self.wfile.write(b'ok')
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path.split('?')[0] != '/api/contact':
            return self.send_error(404)
        try:
            n = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            n = -1
        if n <= 0 or n > 20000:
            return self.reply(False, 413, 'size')
        raw = parse_qs(self.rfile.read(n).decode('utf-8', 'replace'))
        g = lambda k: (raw.get(k) or [''])[0]
        ip = (self.headers.get('X-Forwarded-For') or self.client_address[0]).split(',')[0].strip()
        # bots: honeypot filled or the form was submitted faster than a person can type
        try:
            age = time.time() * 1000 - float(g('t'))
        except ValueError:
            age = None
        if g('website') or (age is not None and age < 3000):
            self.log_message('dropped bot-like submission from %s', ip)
            return self.reply(True, 200)
        f = {'name': one_line(g('name'), 120), 'email': one_line(g('email'), 254), 'company': one_line(g('company'), 160),
             'topic': g('topic') if g('topic') in TOPICS else 'other', 'message': clean(g('message'), 5000),
             'lang': g('lang') if g('lang') in ('en', 'es', 'pl') else 'en'}
        if not f['name'] or not EMAIL_RE.match(f['email']) or len(f['message']) < 10:
            return self.reply(False, 400, 'invalid')
        if not allowed(ip):
            return self.reply(False, 429, 'rate')
        try:
            send(f, ip)
        except Exception as e:  # noqa: BLE001 - report any SMTP failure to the visitor as "not sent"
            self.log_message('smtp error: %r', e)
            return self.reply(False, 502, 'smtp')
        self.log_message('sent message from %s (%s)', ip, f['topic'])
        self.reply(True, 200)


if __name__ == '__main__':
    if not (SMTP_USER and SMTP_PASS):
        sys.stderr.write('warning: SMTP_USER / SMTP_PASS not set; every message will fail\n')
    ThreadingHTTPServer(('0.0.0.0', 8080), H).serve_forever()
