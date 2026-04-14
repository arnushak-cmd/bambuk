import re

# 7 групп: id, ipv6, оплата, lon, lat, заезд, выезд
# запятая в координатах не мешает потому что поля через ;
# в ipv6 группе точка нужна для mapped ipv4 (::ffff:192.168.1.1)

pattern = re.compile(
    r"^(\d{9})"
    r";([0-9a-fA-F:.]+)"
    r";(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    r";(-?\d{1,3},\d{2})"
    r";(-?\d{1,2},\d{2})"
    r";(\d{4}-\d{2}-\d{2})"
    r";(\d{4}-\d{2}-\d{2})$"
)

fields = ["id", "ipv6", "paid_at", "lon", "lat", "checkin", "checkout"]


def parse(line):
    """None если строка кривая"""
    m = pattern.match(line.strip())
    if not m:
        return None
    return dict(zip(fields, m.groups()))


if __name__ == "__main__":
    # просто проверка что работает
    test = "438291056;2001:0db8:85a3::7334;2024-07-12 09:34:17;24,56;56,83;2024-08-01;2024-08-05"
    row = parse(test)
    if row:
        for k, v in row.items():
            print(f"  {k:<12s}  {v}")
    else:
        print("не матчится")
