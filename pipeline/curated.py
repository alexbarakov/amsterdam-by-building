"""Hand-curated layers: buildings tied to a country or a community, each with a short story and a source.

Every entry names the Wikipedia article it rests on; s08_curated.py checks that the article exists and
mentions the street and house number, then geocodes the address to a BAG building (PDOK Locatieserver).
Entries that fail either check are dropped and reported.
"""

# (name, address, story, wikipedia "lang:Title", checks) — every string in `checks` must appear in the article.
CURATED = [
    dict(
        id="russia", title="Russia", era="1697–2022",
        intro=("Peter the Great learned shipbuilding on the VOC yards at Oostenburg in 1697; none of those yards "
               "stands. What remains is money and art: the bank that lent to the tsars, and a museum that shared "
               "its collections with St Petersburg until the invasion of Ukraine."),
        entries=[
            ("Amstelhof, H'ART Museum", "Amstel 51",
             "From 2009 the Hermitage Amsterdam showed loans from the State Hermitage in St Petersburg. After Russia "
             "invaded Ukraine in 2022 the museum cut its ties and reopened as H'ART in 2023.",
             "en:H'ART Museum", ("Amstel", "2009", "2023")),
            ("Hope & Co", "Keizersgracht 444",
             "The bank of the Hope family, founded in 1762, did much of its business in Russia and invested there "
             "in the early 1800s.",
             "nl:Hope & Co", ("Keizersgracht 444", "Rusland", "1762")),
        ]),
    dict(
        id="britain", title="Britain", era="1607–today",
        intro=("English and Scottish merchants, Puritan refugees and soldiers made Amsterdam their home from the "
               "1600s; they worshipped in their own churches, and a Scottish family built one of Europe's great banks."),
        entries=[
            ("English Reformed Church", "Begijnhof 48",
             "Since 1607 the church of English and Scottish Presbyterians in Amsterdam, who were given the Begijnhof's "
             "medieval chapel.", "nl:Engelse Hervormde Kerk (Amsterdam)", ("Begijnhof", "1607")),
            ("Christ Church", "Groenburgwal 42",
             "A former cloth hall turned into the Anglican church of Amsterdam's English community, one of the first "
             "Anglican churches on the Continent.", "nl:Christ Church (Amsterdam)", ("Groenburgwal", "lakenhal")),
            ("Hope & Co", "Keizersgracht 444",
             "The Hopes were a Scottish family; their Amsterdam bank, founded in 1762, became one of the most "
             "powerful in Europe.", "nl:Hope & Co", ("Keizersgracht 444", "Schot", "1762")),
        ]),
    dict(
        id="france", title="France", era="1586–2016",
        intro=("French-speaking Protestants fled to Amsterdam from the 1580s, and again after 1685. In 1806 Napoleon "
               "made his brother Louis king of Holland, and the city hall on the Dam became a royal palace."),
        entries=[
            ("Walloon Church", "Walenpleintje 159",
             "The church of the French-speaking Walloon and Huguenot Protestants who fled the Spanish Netherlands and "
             "France.", "nl:Waalse Kerk (Amsterdam)", ("Walenpleintje 159", "Wallonne")),
            ("Royal Palace", "Dam 1",
             "Built as the city hall; in 1808 Louis Napoleon, king of Holland, made it his palace, and it has been a "
             "royal palace since.", "en:Royal Palace of Amsterdam", ("Louis", "1808")),
            ("Maison Descartes", "Vijzelgracht 2",
             "The Walloon orphanage from 1671; from 1971 to 2016 the French institute Maison Descartes and the "
             "French consulate.", "nl:Vijzelgracht (Amsterdam)", ("Maison Descartes", "1671", "2016")),
            ("Descartes' house", "Westermarkt 6",
             "René Descartes lived here in 1634, during his twenty years in the Dutch Republic.",
             "nl:René Descartes", ("Westermarkt 6", "1634")),
        ]),
    dict(
        id="germany", title="Germany", era="1633–1945",
        intro=("For three centuries Germans came to Amsterdam to work and worship in their Lutheran churches; in the "
               "1930s German Jews fled here. From 1940 the city was run by the German occupier, who organised the "
               "deportation of its Jews from offices that still stand."),
        entries=[
            ("Old Lutheran Church", "Singel 411",
             "Built in 1632–1633 for Amsterdam's Lutherans, on the site of the warehouse where they had worshipped "
             "since 1600.",
             "nl:Oude Lutherse Kerk (Amsterdam)", ("Singel 411", "1632-1633", "pakhuis")),
            ("Round Lutheran Church", "Singel 11",
             "The second Lutheran church, opened in 1671 when the old one on the Spui grew too small.",
             "en:Ronde Lutherse Kerk", ("Singel", "1671")),
            ("Merwedeplein 37", "Merwedeplein 37",
             "The Frank family fled Frankfurt for Amsterdam in 1933 and lived in this flat until they went into "
             "hiding in 1942.", "en:Anne Frank", ("Merwedeplein", "1933", "Frankfurt")),
            ("Zentralstelle für jüdische Auswanderung", "Adama van Scheltemaplein 1",
             "The German office that organised the deportation of the Jews of the Netherlands had its first offices here.",
             "nl:Zentralstelle für jüdische Auswanderung in Amsterdam", ("Adama van Scheltemaplein",)),
            ("SD headquarters, Euterpestraat", "Gerrit van der Veenstraat 99",
             "A girls' school that housed the headquarters of the German Sicherheitsdienst (SD) during the occupation; "
             "the street, then Euterpestraat, was renamed after the resistance fighter Gerrit van der Veen.",
             "nl:Gerrit van der Veenstraat", ("Sicherheitsdienst", "nr. 99", "Euterpestraat")),
        ]),
    dict(
        id="sephardic", title="Portugal and Spain", era="1600–today",
        intro=("Jews expelled from Spain and Portugal, and their descendants who had lived as Catholics, settled in "
               "Amsterdam around 1600. Their merchants helped build the Golden Age; their synagogue still runs by "
               "candlelight."),
        entries=[
            ("Portuguese Synagogue", "Mr. Visserplein 3",
             "Inaugurated in 1675 by the Portuguese-Jewish community, then the largest synagogue in the world.",
             "en:Portuguese Synagogue (Amsterdam)", ("1675", "largest")),
            ("Huis De Pinto", "Sint Antoniesbreestraat 69",
             "Named after the Sephardic De Pinto family, who bought the house in 1651 and gave it its Italianate front.",
             "nl:Huis De Pinto", ("Sint Antoniesbreestraat", "1651")),
        ]),
    dict(
        id="asia", title="Asia and the East Indies", era="1606–today",
        intro=("The Dutch East India Company ran an empire in Asia from Amsterdam. Its offices, the shipping lines "
               "that followed it and the colonial institute still stand, beside the temple of today's Chinese community."),
        entries=[
            ("East India House", "Oude Hoogstraat 24",
             "Headquarters of the Dutch East India Company (VOC), built in 1604.", "nl:Oost-Indisch Huis", ("Oude Hoogstraat", "1604")),
            ("Scheepvaarthuis", "Prins Hendrikkade 108",
             "Offices of six shipping companies that sailed to the Dutch East Indies, built 1913–1916.",
             "en:Scheepvaarthuis", ("1916", "six")),
            ("Tropenmuseum, Colonial Institute", "Linnaeusstraat 2",
             "Founded in 1864 as the Colonial Museum; this building, opened in 1926, was made to display the Dutch "
             "colonies.",
             "nl:Tropenmuseum", ("Koloniaal Museum", "1864")),
            ("He Hua Temple", "Zeedijk 110",
             "A Buddhist temple of Fo Guang Shan in Chinatown, opened in 2000.", "nl:He Hua Tempel", ("Zeedijk", "2000")),
        ]),
    dict(
        id="atlantic", title="The Atlantic and slavery", era="1621–1863",
        intro=("The West India Company traded enslaved Africans across the Atlantic, and Amsterdam co-owned the colony "
               "of Suriname through the Society of Suriname. The men who ran them lived on the canals."),
        caveat="A first selection. The city archive's research on Amsterdam and slavery names many more addresses.",
        entries=[
            ("West India House", "Herenmarkt 99",
             "Headquarters of the West India Company from 1623 to 1647, which ran the slave trade and the colony of "
             "New Netherland.", "en:West-Indisch Huis", ("1623", "1647")),
            ("Herengracht 537", "Herengracht 537",
             "Home of Wigbold Slicher, director of the Society of Suriname from 1708 to 1729.",
             "nl:Gouden Bocht", ("Herengracht 537", "Slicher", "Suriname")),
            ("Huis De Vicq", "Herengracht 476",
             "Built in 1670 for François de Vicq, regent, director of the West India Company and of the Society of "
             "Suriname.", "nl:Huis De Vicq", ("476", "1670", "François de Vicq")),
        ]),
]

CURATED.append(dict(
    id="jewish", title="Jewish Amsterdam", era="1600–1945",
    intro=("In 1940 some 75,000 to 80,000 Jews lived in Amsterdam, a little under a tenth of the city. Sephardic and "
           "Ashkenazi communities had built synagogues, schools and a world centre of the diamond trade; under German "
           "occupation about three in four of them were deported and murdered."),
    caveat=("The homes of the victims are not shown: the dataset linking the Joods Monument to buildings has no "
            "open licence. joodsmonument.nl lists every person and address."),
    groups=[("community", "Community, worship and work"),
            ("persecution", "Persecution 1940–1945"), ("hiding", "Hiding and rescue"), ("lives", "Lives remembered")],
    entries=[
        ("Portuguese Synagogue", "Mr. Visserplein 3",
         "Inaugurated in 1675 by the Portuguese-Jewish community, then the largest synagogue in the world.",
         "en:Portuguese Synagogue (Amsterdam)", ("1675", "largest"), "community"),
        ("Great Synagogue, Jewish Museum", "Nieuwe Amstelstraat 1",
         "The Great Synagogue of the Ashkenazi community, opened in 1671, now part of the Jewish Museum.",
         "nl:Grote Synagoge (Amsterdam)", ("1671", "Joods Museum"), "community"),
        ("Uilenburger Synagogue", "Nieuwe Uilenburgerstraat 91",
         "A synagogue of 1766 on the island of Uilenburg, once one of the poorest Jewish neighbourhoods.",
         "nl:Uilenburgersjoel", ("1766",), "community"),
        ("Lekstraat Synagogue", "Lekstraat 63",
         "A synagogue of the 1930s for the Jews who moved to the new southern districts.",
         "nl:Lekstraatsynagoge", ("Lekstraat 63", "193"), "community"),
        ("Gerard Dou Synagogue", "Gerard Doustraat 238",
         "A synagogue of 1892 in the Pijp, a working-class district with many Jewish families.",
         "nl:Synagoge Gerard Doustraat", ("1892",), "community"),
        ("Huis De Pinto", "Sint Antoniesbreestraat 69",
         "Named after the Sephardic De Pinto family, who bought the house in 1651.",
         "nl:Huis De Pinto", ("Sint Antoniesbreestraat", "1651"), "community"),
        ("Burcht van Berlage", "Henri Polaklaan 9",
         "Headquarters of the diamond workers' union ANDB, led by Henri Polak, built by Berlage in 1900.",
         "nl:De Burcht (Amsterdam)", ("Henri Polak", "ANDB"), "community"),
        ("Asscher Diamond Factory", "Tolstraat 127",
         "The Asscher family's diamond works of 1907, where the Cullinan, the largest diamond ever found, was cut.",
         "nl:Diamantbuurt (Amsterdam)", ("Asscher", "Cullinan"), "community"),
        ("Hollandsche Schouwburg", "Plantage Middenlaan 24",
         "A theatre the occupier turned into the assembly point for Jews awaiting deportation, 1942–1943.",
         "en:Hollandsche Schouwburg", ("1942", "deport"), "persecution"),
        ("Zentralstelle für jüdische Auswanderung", "Adama van Scheltemaplein 1",
         "The German office that organised the deportation of the Jews of the Netherlands had its first offices here.",
         "nl:Zentralstelle für jüdische Auswanderung in Amsterdam", ("Adama van Scheltemaplein",), "persecution"),
        ("Joodsche Invalide", "Weesperplein 1",
         "A Jewish home for the elderly and disabled; its residents were deported in a single night in 1943.",
         "nl:De Joodse Invalide", ("1943",), "persecution"),
        ("Hervormde Kweekschool", "Plantage Middenlaan 27",
         "From this teacher training college, opposite the Schouwburg, hundreds of Jewish children were smuggled "
         "out and hidden. It now houses the National Holocaust Museum.",
         "nl:Nationaal Holocaustmuseum", ("Kweekschool", "kinderen"), "hiding"),
        ("Anne Frank House", "Prinsengracht 263",
         "The Frank family hid in the rear annex here from 1942 until they were betrayed in 1944.",
         "en:Anne Frank House", ("1942", "1944"), "hiding"),
        ("Merwedeplein 37", "Merwedeplein 37",
         "The Frank family's flat after they fled Frankfurt in 1933.", "en:Anne Frank", ("Merwedeplein", "1933"), "lives"),
        ("Etty Hillesum's house", "Gabriël Metsustraat 6",
         "Etty Hillesum wrote her diaries here, 1941–1943, before she was murdered in Auschwitz.",
         "nl:Etty Hillesum", ("Gabriël Metsustraat",), "lives"),
        ("Rembrandt House", "Jodenbreestraat 4",
         "Rembrandt lived here from 1639 to 1658, among the Sephardic neighbours who appear in his work.",
         "en:Rembrandt House Museum", ("1639", "1658"), "lives"),
    ]))

CURATED.append(dict(
    id="secrets", title="Secrets of the city", era="1420–today",
    intro=("Hidden churches in attics, houses no wider than a door, wooden façades that survived the fire bans, "
           "courtyards behind unmarked gates: places that are easy to walk past."),
    entries=[
        ("Our Lord in the Attic", "Oudezijds Voorburgwal 38",
         "In 1661 a stocking merchant bought this canal house and fitted out a Catholic church in its attics, at a "
         "time when Catholics could not worship in public.", "nl:Ons' Lieve Heer op Solder", ("1661",), "secrets"),
        ("Het Houten Huis", "Begijnhof 34",
         "One of the city's last wooden houses, from around 1528, with wooden front and back walls; entirely wooden houses no longer exist in the old centre.", 'nl:Begijnhof (Amsterdam)', ('Begijnhof 34', '1528', 'Geheel houten huizen'), "secrets"),
        ("In 't Aepjen", "Zeedijk 1",
         "Built around 1550, one of the oldest wooden houses still standing; the saying 'in de aap gelogeerd zijn', to be in a fix, is said to come from here.", "nl:In 't Aepjen", ('1550', 'houten', 'in de aap gelogeerd'), "secrets"),
        ("The smallest house", "Oude Hoogstraat 22",
         '2.02 metres wide and 5 metres deep: often called the smallest house in Amsterdam.', 'nl:Kleinste huis van Amsterdam', ('2,02 meter',), "secrets"),
        ("The narrowest front", "Singel 7",
         "The narrowest house front in Amsterdam; the house widens behind it.",
         "nl:Singel 166 (Amsterdam)", ("nummer 7 heeft de smalste voorgevel",), "secrets"),
        ("The Little Trip House", "Kloveniersburgwal 26",
         "A narrow house across the canal from the Trips' palace, built in the same style as its grand neighbour.",
         "nl:Trippenhuis",
         ("Kloveniersburgwal 26", "Klein Trippenhuis"), "secrets"),
        ("The Begijnhof", "Begijnhof 29",
         'The only hofje founded in medieval Amsterdam: a courtyard of houses behind a gate off the Spui, lying almost a metre below the street.', 'nl:Begijnhof (Amsterdam)', ('enige hofje', 'bijna een meter lager'), "secrets"),
        ("De Papegaai", "Kalverstraat 58",
         'A clandestine Catholic church of the Republic, still entered from the Kalverstraat shopping street.', 'nl:De Papegaai (Amsterdam)', ('schuilkerk', 'Kalverstraat'), "secrets"),
        ("Schreierstoren", "Prins Hendrikkade 94",
         "A defensive tower built around 1487. Legend says sailors' wives wept farewell here, which gave it its name, but the story is probably untrue.", 'nl:Schreierstoren', ('1487', 'vrouwen afscheid', 'waarschijnlijk apocrief'), "secrets"),
        ("De Gooyer", "Funenkade 5",
         'A windmill in the middle of the city: two wooden octagons stacked on a brick base.', 'nl:De Gooyer (Amsterdam)', ('twee op elkaar geplaatste houten achtkanten',), "secrets"),
        ("Montelbaanstoren", "Oudeschans 2",
         'A defensive tower of 1516; Hendrick de Keyser added its spire in 1606, and Rembrandt, who lived nearby, drew it in 1644.', 'nl:Montelbaanstoren', ('1516', '1606', '1644', 'Hendrick de Keyser'), "secrets"),
        ("Huis met de Hoofden", "Keizersgracht 123",
         'Named after six heads on its front. Legend says they are robbers beheaded one by one by the kitchen maid; they are in fact busts of six classical gods.', 'nl:Huis met de Hoofden', ('zes rovers', 'keukenmeid', 'zes goden'), "secrets"),
        ("Bartolotti House", "Herengracht 170",
         'Its front has two kinks so that it follows the bend of the Herengracht.', 'nl:Huis Bartolotti', ('twee knikken', 'bocht'), "secrets"),
        ("De Waag", "Nieuwmarkt 4",
         "A city gate of 1488 that became a weighhouse; Rembrandt's 'Anatomy Lesson of Dr Tulp' was painted for "
         "the surgeons who met upstairs.", "nl:Waag (Amsterdam)", ("1488", "Tulp"), "secrets"),
        ("Café Karpershoek", "Martelaarsgracht 2",
         "Its building dates from 1629, and the café is said to be the oldest bar in Amsterdam.",
         "nl:Martelaarsgracht", ("1629", "oudste kroeg"), "secrets"),
    ]))


# Twelve more layers (merchants, painters, port, science, resistance, counterculture, queer Amsterdam, stage, royal
# Amsterdam, the 19th-century city, churches, writers), each entry checked the same way.
from .curated_more import CURATED_MORE  # noqa: E402
CURATED += CURATED_MORE
