"""The city's ontology: people, events and organisations, tied to the buildings where they left a trace.

An entity is linked to a building when its pattern appears in a checked text about that building: a story of a
curated layer (checked against Wikipedia by s08_curated) or a 'Did you know' fact (s11_facts). Well-known residents
(s09_residents) join as people with their quote. s13_graph.py builds the graph.

(id, type, English label, Dutch label, years, regex on the English text)
"""

PERSON, EVENT, ORG = "person", "event", "organisation"

ENTITIES = [
    # people
    ("rembrandt", PERSON, "Rembrandt", "Rembrandt", "1606–1669", r"Rembrandt"),
    ("dekeyser", PERSON, "Hendrick de Keyser", "Hendrick de Keyser", "1565–1621", r"Hendrick de Keyser"),
    ("berlage", PERSON, "H.P. Berlage", "H.P. Berlage", "1856–1934", r"Berlage"),
    ("deklerk", PERSON, "Michel de Klerk", "Michel de Klerk", "1884–1923", r"de Klerk"),
    ("descartes", PERSON, "René Descartes", "René Descartes", "1596–1650", r"Descartes"),
    ("louisnapoleon", PERSON, "Louis Napoleon", "Lodewijk Napoleon", "1778–1846", r"Louis Napoleon"),
    ("hudson", PERSON, "Henry Hudson", "Henry Hudson", "c. 1565–1611", r"Hudson"),
    ("annefrank", PERSON, "The Frank family", "De familie Frank", "1933–1944", r"Frank family"),
    ("hillesum", PERSON, "Etty Hillesum", "Etty Hillesum", "1914–1943", r"Hillesum"),
    ("polak", PERSON, "Henri Polak", "Henri Polak", "1868–1943", r"Henri Polak"),
    ("tuschinski", PERSON, "Abraham Tuschinski", "Abraham Tuschinski", "1886–1942", r"Tuschinski"),
    ("carre", PERSON, "Oscar Carré", "Oscar Carré", "1846–1911", r"Oscar Carré"),
    ("vanderveen", PERSON, "Gerrit van der Veen", "Gerrit van der Veen", "1902–1944", r"Gerrit van der Veen"),
    ("hope", PERSON, "The Hope family", "De familie Hope", "", r"\bHope"),
    ("trip", PERSON, "The Trip brothers", "De gebroeders Trip", "", r"\bTrips?\b"),
    ("depinto", PERSON, "The De Pinto family", "De familie De Pinto", "", r"De Pinto"),
    ("devicq", PERSON, "François de Vicq", "François de Vicq", "", r"de Vicq"),
    ("slicher", PERSON, "Wigbold Slicher", "Wigbold Slicher", "", r"Slicher"),
    ("asscher", PERSON, "The Asscher family", "De familie Asscher", "", r"Asscher"),
    # events
    ("occupation", EVENT, "The German occupation", "De Duitse bezetting", "1940–1945",
     r"occupation|occupier|German office|Sicherheitsdienst"),
    ("deportation", EVENT, "The deportation of the Jews", "De deportatie van de Joden", "1942–1944",
     r"deport|Auschwitz|murdered|hidden|hiding|betrayed"),
    ("olympics1928", EVENT, "The 1928 Olympic Games", "De Olympische Spelen van 1928", "1928", r"Olympic"),
    ("frenchrule", EVENT, "French rule", "De Franse tijd", "1795–1813", r"Louis Napoleon|French invasion"),
    ("ukraine2022", EVENT, "Russia's invasion of Ukraine", "De Russische inval in Oekraïne", "2022", r"invaded Ukraine"),
    # organisations and communities
    ("voc", ORG, "Dutch East India Company (VOC)", "Verenigde Oost-Indische Compagnie (VOC)", "1602–1799",
     r"\bVOC\b|East India Company"),
    ("wic", ORG, "West India Company", "West-Indische Compagnie", "1621–1792", r"West India Company"),
    ("suriname", ORG, "Society of Suriname", "Sociëteit van Suriname", "1683–1795", r"Society of Suriname"),
    ("sephardim", ORG, "Portuguese-Jewish community", "Portugees-Joodse gemeente", "", r"Portuguese-Jewish|Sephardic"),
    ("ashkenazim", ORG, "Ashkenazi community", "Hoogduits-Joodse gemeente", "", r"Ashkenazi"),
    ("walloon", ORG, "Walloon and Huguenot Protestants", "Waalse en hugenootse protestanten", "", r"Walloon|Huguenot"),
    ("lutherans", ORG, "Lutherans", "Lutheranen", "", r"Lutheran"),
    ("english", ORG, "English and Scottish community", "Engelse en Schotse gemeenschap", "", r"English|Scottish"),
    ("catholics", ORG, "Hidden Catholic churches", "Schuilkerken", "", r"Catholic"),
    ("amsterdamschool", ORG, "Amsterdam School", "Amsterdamse School", "1910–1930", r"Amsterdam School"),
    ("diamond", ORG, "Diamond trade", "Diamanthandel", "", r"diamond"),
    ("hermitage", ORG, "Hermitage Amsterdam", "Hermitage Amsterdam", "2009–2023", r"Hermitage"),
]
