# rafal.lagowski.es

Personal expert profile of Rafał Łagowski, AI & Agentic Systems Architect.
Plain static HTML, CSS and vanilla JS, served by nginx on the k3s cluster
(namespace `rafal-site`, Traefik ingress, Let's Encrypt via cert-manager). No build step, no framework, no trackers. Fonts are self-hosted; colours follow labs.lagowski.es.

Languages: EN (default), ES, PL. The switch sets a class on `<body>` and stores
the choice in `localStorage` under `lagowski-lang`; first visits follow the
browser language when it is Spanish or Polish.

## Deploying

    k8s/deploy.sh            # kube context defaults to k3s-remote

The script loads the files into ConfigMaps and rolls the nginx pod.
DNS: `rafal.lagowski.es` A record -> the cluster IP.

## Editing

The pages are generated from `tools/gen.py` so the three languages stay in one
place, and the generated HTML is committed:

    python3 tools/gen.py
    python3 -m http.server 8765    # preview at http://localhost:8765

Values still to fill in sit at the top of `tools/gen.py`: `DAY_RATE`,
`LINKEDIN`, `VIDEO`. Rerun the script after any change.

## Contact form

No email address is published. The form posts to `/api/contact`, served by
`k8s/contact.py` (stdlib Python, honeypot + minimum fill time + an hourly cap of 30 messages),
which mails the message to rafal@lagowski.es through Google SMTP with the
visitor in Reply-To. The CV is not published; it is sent on request (topic
"CV request"). Credentials live in the Secret `rafal-site-smtp`
(keys `SMTP_USER`, `SMTP_PASS` = a Google app password), created by hand:

    read -s P; kubectl -n rafal-site create secret generic rafal-site-smtp \
      --from-literal=SMTP_USER=rafal@lagowski.es --from-literal=SMTP_PASS="$P"; unset P
    kubectl -n rafal-site rollout restart deploy/rafal-contact

`tools/og.html` is the source of `assets/og.png` (1200x630 social card) and
`tools/icon.html` of the touch icon; both are rendered with headless Chrome.

The interactive demos and the starter-pack / workshop PDFs come from the
lagowski.es services site, which stays a separate project.
