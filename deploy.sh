#!/bin/bash
# Deploy ouzcable.com: push to GitHub Pages + submit to IndexNow/Baidu + verify.
# Usage: bash deploy.sh <GITHUB_TOKEN>
set -e
cd "$(dirname "$0")"
TOKEN="$1"
if [ -z "$TOKEN" ]; then echo "Usage: bash deploy.sh <GITHUB_TOKEN>"; exit 1; fi

echo "== [1/5] Push to GitHub Pages =="
GIT_TERMINAL_PROMPT=0 git push "https://x-access-token:${TOKEN}@github.com/66ww77/ouzcable.git" main || {
  echo "push failed — token invalid or expired"; exit 1; }

echo "== [2/5] Wait for CDN refresh =="
sleep 50

echo "== [3/5] Verify online pages =="
for p in export quality solutions2 ai-computing; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://ouzcable.com/${p}.html?v=$(date +%s)")
  echo "  https://ouzcable.com/${p}.html -> HTTP $code"
  [ "$code" = "200" ] || { echo "  FAIL for ${p}.html"; exit 1; }
done

echo "== [4/5] IndexNow submission =="
KEY=592ade540307490c9d98edb5cc1d518d
cat > /tmp/in.json <<EOF
{"host":"ouzcable.com","key":"$KEY","keyLocation":"https://ouzcable.com/${KEY}.txt","urlList":[
"https://ouzcable.com/export.html","https://ouzcable.com/quality.html","https://ouzcable.com/solutions2.html",
"https://ouzcable.com/export.html?lang=en","https://ouzcable.com/export.html?lang=ru","https://ouzcable.com/export.html?lang=es","https://ouzcable.com/export.html?lang=ar","https://ouzcable.com/export.html?lang=zh","https://ouzcable.com/export.html?lang=fr","https://ouzcable.com/export.html?lang=uk","https://ouzcable.com/export.html?lang=tr","https://ouzcable.com/export.html?lang=de","https://ouzcable.com/export.html?lang=pt","https://ouzcable.com/export.html?lang=mn",
"https://ouzcable.com/quality.html?lang=en","https://ouzcable.com/quality.html?lang=ru","https://ouzcable.com/quality.html?lang=es","https://ouzcable.com/quality.html?lang=ar","https://ouzcable.com/quality.html?lang=zh","https://ouzcable.com/quality.html?lang=fr","https://ouzcable.com/quality.html?lang=uk","https://ouzcable.com/quality.html?lang=tr","https://ouzcable.com/quality.html?lang=de","https://ouzcable.com/quality.html?lang=pt","https://ouzcable.com/quality.html?lang=mn",
"https://ouzcable.com/solutions2.html?lang=en","https://ouzcable.com/solutions2.html?lang=ru","https://ouzcable.com/solutions2.html?lang=es","https://ouzcable.com/solutions2.html?lang=ar","https://ouzcable.com/solutions2.html?lang=zh","https://ouzcable.com/solutions2.html?lang=fr","https://ouzcable.com/solutions2.html?lang=uk","https://ouzcable.com/solutions2.html?lang=tr","https://ouzcable.com/solutions2.html?lang=de","https://ouzcable.com/solutions2.html?lang=pt","https://ouzcable.com/solutions2.html?lang=mn"
]}
EOF
c1=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d @/tmp/in.json https://api.indexnow.org/indexnow)
c2=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d @/tmp/in.json https://www.bing.com/indexnow)
echo "  IndexNow api.indexnow.org -> $c1 | bing.com -> $c2"

echo "== [5/5] Baidu submission (best-effort) =="
printf "https://ouzcable.com/export.html\nhttps://ouzcable.com/quality.html\nhttps://ouzcable.com/solutions2.html\n" > /tmp/bd.txt
bd=$(curl -s -X POST -H "Content-Type:text/plain" --data-binary @/tmp/bd.txt "http://data.zz.baidu.com/urls?site=https://ouzcable.com&token=M0Tw6c4qhTIU9ceb")
echo "  Baidu response: $bd"

echo "== DONE =="
