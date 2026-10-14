"""São Paulo periods, following the city's growth rather than decades. Same palette as Amsterdam's, oldest darkest.
The IPTU register dates almost nothing before 1919 (see s01_buildings), so the first period starts the city."""
PERIODS = [
    # (key, English label, Portuguese label, start, end, colour)
    ("p1", "Before 1930 Coffee and the railways", "Antes de 1930 Café e ferrovias", 1000, 1929, "#8c1c13"),
    ("p2", "1930–1949 Art deco and the first towers", "1930–1949 Art déco e os primeiros arranha-céus", 1930, 1949, "#d97a2b"),
    ("p3", "1950–1964 Modernism and the IV Centenário", "1950–1964 Modernismo e o IV Centenário", 1950, 1964, "#e5b13a"),
    ("p4", "1965–1979 The economic miracle", "1965–1979 O milagre econômico", 1965, 1979, "#8e9f3c"),
    ("p5", "1980–1994 The lost decade", "1980–1994 A década perdida", 1980, 1994, "#3f8f6b"),
    ("p6", "1995–2009 Berrini and the new centres", "1995–2009 Berrini e os novos centros", 1995, 2009, "#2c7391"),
    ("p7", "2010– The tower boom", "2010– O boom dos edifícios", 2010, 2100, "#6a3f8f"),
]


def period_index(year: int) -> int:
    for i, (_, _, _, a, b, _) in enumerate(PERIODS):
        if a <= year <= b:
            return i
    return 0
