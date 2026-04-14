import random
import sys
from datetime import datetime, timedelta

from regex import parse

ipv6_pool = [
    "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "fd12:3456:789a:1::1",
    "2607:f8b0:4004:0800::200e",
    "2a02:6b8::2:242",
    "::ffff:192.168.1.1",
    "2001:4860:4860::8888",
    "fe80::1",
    "2001:0db8:0001:0000:0000:0ab9:C0A8:0102",
    "2600:1f18:243d:8200::1",
    "2a00:1450:4001:0801::200e",
]

# специально набрал разные регионы чтоб были + и - координаты
places = [
    (24.56, 56.83),     # рига
    (-3.71, 40.42),     # мадрид
    (100.53, 13.76),    # бангкок
    (37.62, 55.75),     # мск
    (139.69, 35.68),    # токио
    (-73.97, 40.73),    # нью-йорк
    (151.21, -33.87),   # сидней
    (12.49, 41.89),     # рим
    (-43.17, -22.91),   # рио, оба минуса
    (28.98, 41.01),     # стамбул
]


def make_one():
    bid = random.randint(100_000_000, 999_999_999)
    ip = random.choice(ipv6_pool)

    t0 = datetime(2023, 1, 1)
    paid = t0 + timedelta(seconds=random.randint(0, 1095 * 86400))

    lon, lat = random.choice(places)
    lon_s = f"{lon:.2f}".replace(".", ",")
    lat_s = f"{lat:.2f}".replace(".", ",")

    checkin = paid.date() + timedelta(days=random.randint(1, 90))
    checkout = checkin + timedelta(days=random.randint(1, 14))

    return f"{bid};{ip};{paid:%Y-%m-%d %H:%M:%S};{lon_s};{lat_s};{checkin};{checkout}"


def generate(n=10, seed=42):
    random.seed(seed)
    return [make_one() for _ in range(n)]


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    lines = generate(n)

    ok = sum(1 for s in lines if parse(s))
    print(f"сгенерил {n}, regex прошли {ok}/{n}")

    out = "sample_bookings.csv"
    with open(out, "w") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"-> {out}")

    print()
    for i, line in enumerate(lines[:5], 1):
        print(f"  {i}. {line}")
    if n > 5:
        print(f"  ... ещё {n - 5}")
