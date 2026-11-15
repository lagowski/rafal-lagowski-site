#!/usr/bin/env bash
# Usage: k8s/deploy.sh [kube-context]   (default: k3s-remote)
# Publishes the repository's static files to rafal.lagowski.es on the k3s cluster.
set -euo pipefail
CTX="${1:-k3s-remote}"
cd "$(dirname "$0")/.."
K="kubectl --context $CTX"
NS=rafal-site
$K apply -f k8s/manifest.yaml
cm() { # name, then --from-file args
  local name=$1; shift
  $K -n $NS create configmap "$name" "$@" --dry-run=client -o yaml | $K apply --server-side --force-conflicts -f -
}
cm rafal-site-html $(for f in *.html robots.txt sitemap.xml favicon.svg favicon.ico; do printf -- '--from-file=%s ' "$f"; done)
cm rafal-site-assets $(for f in assets/*; do [ -f "$f" ] && printf -- '--from-file=%s ' "$f"; done)
cm rafal-site-fonts --from-file=assets/fonts/
cm rafal-site-files-a $(for f in files/starter-pack-*.pdf files/Rafal_Lagowski_CV.pdf files/*.mp4; do [ -f "$f" ] && printf -- '--from-file=%s ' "$f"; done)
cm rafal-site-files-b $(for f in files/workshop-agendas-*.pdf; do printf -- '--from-file=%s ' "$f"; done)
cm rafal-site-conf --from-file=default.conf=k8s/nginx.conf
H=$(cat *.html robots.txt sitemap.xml favicon.* assets/*.* assets/fonts/* files/* k8s/nginx.conf | shasum | cut -c1-12)
$K -n $NS patch deploy rafal-site -p "{\"spec\":{\"template\":{\"metadata\":{\"annotations\":{\"content-hash\":\"$H\"}}}}}"
$K -n $NS rollout status deploy/rafal-site --timeout=120s
