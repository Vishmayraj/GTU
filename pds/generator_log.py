"""
Synthetic Apache/Nginx Combined Log Format generator for PDS practicals.
Produces a realistic access.log with:
  - Normal benign browsing traffic (majority)
  - SQL injection attempts
  - Path traversal attempts
  - Brute-force login attempts (repeated POST /login from same IP)
  - A sprinkling of bot/scanner traffic (404s, weird UAs)
This gives Practicals 1-9 real signal to work with (labeling, feature
engineering, balancing, aggregation, viz, classification all become possible).
"""
import random
from datetime import datetime, timedelta

random.seed(42)

NUM_BENIGN = 40000
NUM_SQLI = 1200
NUM_TRAVERSAL = 1000
NUM_BRUTEFORCE_IPS = 150
BRUTEFORCE_ATTEMPTS_PER_IP = (8, 25)   # range of attempts per attacking IP
NUM_BOT_SCAN = 3000
# ^ Tune these to change dataset size. Rough total = sum of all NUM_* plus
# brute-force attempts (NUM_BRUTEFORCE_IPS * ~16 avg). Keep attack:benign
# ratio roughly similar so labeling/balancing practicals stay meaningful.

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
]

BOT_AGENTS = [
    "masscan/1.3 (https://github.com/robertdavidgraham/masscan)",
    "Mozilla/5.0 (compatible; InternetMeasurement/1.0; +https://internet-measurement.com/)",
    "python-requests/2.31.0",
    "sqlmap/1.7.2#stable (http://sqlmap.org)",
    "curl/7.88.1",
]

BENIGN_PATHS = [
    "/", "/index.html", "/about", "/contact", "/products", "/products/1",
    "/products/2", "/cart", "/checkout", "/style.css", "/script.js",
    "/images/logo.png", "/blog", "/blog/post-1", "/api/products",
    "/api/users/profile", "/search?q=shoes", "/search?q=laptop",
    "/login", "/register", "/dashboard", "/faq", "/help",
]

REFERRERS = ["https://google.com", "https://example.com", "https://bing.com", "-",
             "https://facebook.com", "https://twitter.com"]

SQLI_PAYLOADS = [
    "/login?user=admin' OR 1=1 --",
    "/products?id=1' OR '1'='1",
    "/search?q=%27%20UNION%20SELECT%20username%2Cpassword%20FROM%20users--",
    "/api/users?id=1; DROP TABLE users;--",
    "/products?id=1' AND SLEEP(5)--",
]

TRAVERSAL_PAYLOADS = [
    "/../../../../etc/passwd",
    "/images/../../../../etc/shadow",
    "/download?file=../../../../windows/win.ini",
    "/..%2f..%2f..%2fetc%2fpasswd",
    "/static/../../config/database.yml",
]

def random_ip(private=False):
    if private:
        return f"192.168.1.{random.randint(2, 254)}"
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def fmt_time(dt):
    return dt.strftime("%d/%b/%Y:%H:%M:%S +0530")

start = datetime(2026, 8, 1, 0, 0, 0)
end = datetime(2026, 8, 14, 23, 59, 59)
span_seconds = int((end - start).total_seconds())

def random_time():
    return start + timedelta(seconds=random.randint(0, span_seconds))

rows = []  # (datetime, line)

# ---- Benign traffic ----
for _ in range(NUM_BENIGN):
    ip = random_ip(private=random.random() < 0.05)
    t = random_time()
    method = random.choices(["GET", "POST"], weights=[0.9, 0.1])[0]
    path = random.choice(BENIGN_PATHS)
    status = random.choices([200, 200, 200, 200, 304, 404, 500],
                             weights=[70, 10, 5, 5, 5, 4, 1])[0]
    size = random.randint(200, 9000)
    ref = random.choice(REFERRERS)
    ua = random.choice(USER_AGENTS)
    line = f'{ip} - - [{fmt_time(t)}] "{method} {path} HTTP/1.1" {status} {size} "{ref}" "{ua}"'
    rows.append((t, line))

# ---- SQL injection attempts ----
for _ in range(NUM_SQLI):
    ip = random_ip()
    t = random_time()
    path = random.choice(SQLI_PAYLOADS)
    status = random.choices([200, 403, 500], weights=[2, 5, 3])[0]
    size = random.randint(100, 800)
    ua = random.choice(USER_AGENTS + BOT_AGENTS)
    line = f'{ip} - - [{fmt_time(t)}] "GET {path} HTTP/1.1" {status} {size} "-" "{ua}"'
    rows.append((t, line))

# ---- Path traversal attempts ----
for _ in range(NUM_TRAVERSAL):
    ip = random_ip()
    t = random_time()
    path = random.choice(TRAVERSAL_PAYLOADS)
    status = random.choices([403, 404, 200], weights=[6, 3, 1])[0]
    size = random.randint(100, 600)
    ua = random.choice(USER_AGENTS + BOT_AGENTS)
    line = f'{ip} - - [{fmt_time(t)}] "GET {path} HTTP/1.1" {status} {size} "-" "{ua}"'
    rows.append((t, line))

# ---- Brute-force login attempts ----
for _ in range(NUM_BRUTEFORCE_IPS):
    ip = random_ip()
    n_attempts = random.randint(*BRUTEFORCE_ATTEMPTS_PER_IP)
    t0 = random_time()
    ua = random.choice(USER_AGENTS + BOT_AGENTS)
    for i in range(n_attempts):
        t = t0 + timedelta(seconds=i * random.randint(1, 4))
        status = 401 if i < n_attempts - 1 else random.choice([302, 401])
        size = random.randint(100, 400)
        line = f'{ip} - - [{fmt_time(t)}] "POST /login HTTP/1.1" {status} {size} "https://example.com/login" "{ua}"'
        rows.append((t, line))

# ---- Bot / scanner noise ----
for _ in range(NUM_BOT_SCAN):
    ip = random_ip()
    t = random_time()
    path = random.choice(["/", "/admin", "/wp-login.php", "/.env", "/phpmyadmin",
                           "/config.php", "/robots.txt", "/api/v1/health"])
    status = random.choices([404, 403, 200], weights=[6, 3, 1])[0]
    size = random.randint(100, 1200)
    ua = random.choice(BOT_AGENTS)
    line = f'{ip} - - [{fmt_time(t)}] "GET {path} HTTP/1.1" {status} {size} "-" "{ua}"'
    rows.append((t, line))

rows.sort(key=lambda r: r[0])

with open("logs/access.log", "w") as f:
    for _, line in rows:
        f.write(line + "\n")

print(f"Total lines written: {len(rows)}")
print(f"Benign: {NUM_BENIGN}, SQLi: {NUM_SQLI}, Traversal: {NUM_TRAVERSAL}, "
      f"Brute-force: sum of per-IP attempts, Bot/scan: {NUM_BOT_SCAN}")