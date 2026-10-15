"""Dutch versions of every text the pipeline writes: layer titles, intros, caveats, group labels, stories.

Keyed by the English text. s05_layers.py adds a `<field>_nl` next to each field it finds here, and reports
the English texts that have no Dutch version yet.
"""

NL = {
    # sections
    "Discover": "Ontdekken",
    "Architecture": "Architectuur",
    "Trade and empire": "Handel en wereldrijk",
    "Faith and community": "Geloof en gemeenschap",
    "The modern city": "De moderne stad",
    "War and occupation": "Oorlog en bezetting",

    # eras
    "1600–1800": "1600–1800", "1613–1665": "1613–1665", "1400–1900": "1400–1900", "1850–1940": "1850–1940",
    "1870–1940": "1870–1940", "1901–1940": "1901–1940", "1915–1980": "1915–1980", "1940–1945": "1940–1945",
    "1943": "1943", "1945–1985": "1945–1985", "1987–today": "1987–heden", "All periods": "Alle perioden",
    "1586–today": "1586–heden", "1600–1945": "1600–1945", "1420–today": "1420–heden", "1600–today": "1600–heden",

    # gables
    "Gables": "Gevels",
    "A canal house shows its age in its top. Stepped gables belong to the early 1600s, neck gables to the middle of the century, bell gables to the decades around 1700, and the flat cornice to the 1700s, when the richest owners hid the roof altogether.":
        "Een grachtenhuis verraadt zijn leeftijd aan de top. Trapgevels horen bij het begin van de 17de eeuw, halsgevels bij het midden ervan, klokgevels bij de decennia rond 1700 en de rechte lijst bij de 18de eeuw, toen de rijkste eigenaren het dak helemaal verborgen.",
    "Listed houses only: the register of national monuments names the gable of each.":
        "Alleen monumenten: het rijksmonumentenregister noemt bij elk huis de gevel.",
    "Rijksmonumentenregister, RCE": "Rijksmonumentenregister, RCE",
    "Stepped gable": "Trapgevel", "Neck gable": "Halsgevel", "Bell gable": "Klokgevel", "Cornice": "Rechte lijst",

    # trade
    "Warehouses and the companies": "Pakhuizen en de compagnieën",
    "Amsterdam stored the goods of the world in its houses. Warehouses with shutters, hoisting beams and stacked loading doors line the Brouwersgracht, the western islands and the Entrepotdok. The East and West India Companies ran their trade from a handful of buildings that still stand.":
        "Amsterdam sloeg de goederen van de wereld op in zijn huizen. Pakhuizen met luiken, hijsbalken en boven elkaar gestapelde laaddeuren staan langs de Brouwersgracht, op de Westelijke Eilanden en aan het Entrepotdok. De VOC en de WIC dreven hun handel vanuit een handvol gebouwen dat er nog staat.",
    "Warehouse": "Pakhuis", "VOC and WIC buildings": "Gebouwen van VOC en WIC",

    # canal ring
    "The canal ring": "De grachtengordel",
    "The seventeenth-century ring of canals, dug in three phases and built up with merchants' houses, has been a UNESCO World Heritage site since 2010. The buffer zone around it protects the views.":
        "De zeventiende-eeuwse grachtengordel, in drie fasen gegraven en bebouwd met koopmanshuizen, staat sinds 2010 op de Werelderfgoedlijst van UNESCO. De bufferzone eromheen beschermt de zichtlijnen.",
    "Gemeente Amsterdam, UNESCO zones": "Gemeente Amsterdam, UNESCO-zones",
    "World Heritage site": "Werelderfgoed", "Buffer zone": "Bufferzone",

    # faith
    "Faith and charity": "Geloof en liefdadigheid",
    "Under the Republic, Catholics worshipped in hidden churches behind house fronts, Jews from Portugal and Central Europe built the city's great synagogues, and wealthy citizens founded hofjes: courtyards of almshouses for the elderly poor.":
        "In de Republiek kerkten katholieken in schuilkerken achter woonhuisgevels, bouwden Joden uit Portugal en Midden-Europa de grote synagogen van de stad en stichtten welgestelde burgers hofjes voor arme ouderen.",
    "Gemeente Amsterdam, monuments register": "Gemeente Amsterdam, monumentenregister",
    "Church": "Kerk", "Synagogue": "Synagoge", "Hofje": "Hofje",

    # styles
    "Architecture styles": "Bouwstijlen",
    "Between Cuypers' Rijksmuseum and the white blocks of the Nieuwe Bouwen, Amsterdam tried on a style a generation. Berlage stripped ornament back to brick; his pupils of the Amsterdam School turned brick into sculpture across the new housing districts.":
        "Tussen het Rijksmuseum van Cuypers en de witte blokken van het Nieuwe Bouwen probeerde Amsterdam elke generatie een nieuwe stijl. Berlage bracht het ornament terug tot baksteen; zijn leerlingen van de Amsterdamse School maakten van baksteen beeldhouwwerk in de nieuwe woonwijken.",
    "Listed buildings only: the register tags the style of about one national monument in three.":
        "Alleen monumenten: het register noemt de stijl van ongeveer één op de drie rijksmonumenten.",
    "Neo-Renaissance": "Neorenaissance", "Eclecticism": "Eclecticisme", "Art Nouveau": "Jugendstil",
    "Berlage school": "School van Berlage", "Amsterdam School": "Amsterdamse School", "Nieuwe Bouwen": "Nieuwe Bouwen",

    # architects
    "Architects": "Architecten",
    "A few names built much of the city that visitors photograph: Cuypers the Rijksmuseum and Centraal Station, Van Gendt the Concertgebouw, Berlage the Exchange, the Amsterdam School architects the housing blocks of Zuid and West, the city's own Public Works its schools and bridges, and the Nieuwe Bouwen its first glass and concrete.":
        "Een paar namen bouwden veel van de stad die bezoekers fotograferen: Cuypers het Rijksmuseum en Centraal Station, Van Gendt het Concertgebouw, Berlage de Beurs, de architecten van de Amsterdamse School de woonblokken in Zuid en West, de eigen dienst Publieke Werken de scholen en bruggen, en het Nieuwe Bouwen het eerste glas en beton.",
    "From the monuments register and the city's survey of cultural-historical value, which names the architect for the centre and the districts built up to 1965.":
        "Uit het monumentenregister en de orde-inventarisatie van de gemeente, die de architect noemt voor het centrum en de wijken die tot 1965 zijn gebouwd.",
    "Gemeente Amsterdam, monuments register and orde survey": "Gemeente Amsterdam, monumentenregister en orde-inventarisatie",
    "Cuypers": "Cuypers", "Berlage": "Berlage", "Van Gendt": "Van Gendt",
    "Amsterdam School architects": "Architecten van de Amsterdamse School", "Public Works": "Publieke Werken",

    # housing
    "Housing Act homes": "Woningwetwoningen",
    "The Housing Act of 1901 let housing associations build with public money. Within forty years they had replaced the slums with whole districts of sound workers' homes, and they still own these blocks today.":
        "Dankzij de Woningwet van 1901 konden woningbouwverenigingen met publiek geld bouwen. Binnen veertig jaar vervingen ze de krotten door hele wijken degelijke arbeiderswoningen, en ze bezitten die blokken nog steeds.",
    "Buildings built 1901–1940 in blocks a housing association owns today; some were bought later.":
        "Gebouwen uit 1901–1940 in blokken die nu van een woningcorporatie zijn; sommige zijn later aangekocht.",
    "AFWC, housing associations' stock 2025": "AFWC, corporatiebezit 2025",
    "Housing association, built 1901–1940": "Corporatiebezit, gebouwd 1901–1940",

    # planned city
    "The planned city": "De geplande stad",
    "Twentieth-century Amsterdam grew by plan: Berlage's Plan Zuid, the concrete village of Betondorp, Van Eesteren's garden cities in the west, the honeycomb high-rise of the Bijlmermeer and the 1980s renewal of IJplein. The city now protects each of them as a cityscape.":
        "Het twintigste-eeuwse Amsterdam groeide volgens plan: Plan Zuid van Berlage, het betonnen dorp Betondorp, de tuinsteden van Van Eesteren in het westen, de honingraatflats van de Bijlmermeer en de stadsvernieuwing van het IJplein in de jaren tachtig. De gemeente beschermt ze nu als stadsgezicht.",
    "Gemeente Amsterdam, protected cityscapes": "Gemeente Amsterdam, beschermde stadsgezichten",
    "Plan Zuid": "Plan Zuid", "Admiralenbuurt": "Admiralenbuurt", "Betondorp": "Betondorp",
    "Western garden cities": "Westelijke Tuinsteden", "IJplein": "IJplein", "Bijlmermeer": "Bijlmermeer",
    "Plan Van Gool": "Plan Van Gool",

    # war
    "Under fire, 1940–1945": "Onder vuur, 1940–1945",
    "Amsterdam was spared the destruction of Rotterdam, yet bombs, shells and crashing aircraft still hit hundreds of addresses. The city archive mapped each incident from the reports of the time.":
        "Amsterdam bleef de verwoesting van Rotterdam bespaard, maar bommen, granaten en neerstortende vliegtuigen troffen toch honderden adressen. Het Stadsarchief bracht elk incident in kaart op basis van de rapporten uit die tijd.",
    "Buildings within 15 m of a recorded incident; some stand on the site of the building that was hit.":
        "Gebouwen binnen 15 m van een vastgelegd incident; sommige staan op de plek van het getroffen gebouw.",
    "Stadsarchief Amsterdam, WWII incidents": "Stadsarchief Amsterdam, incidenten WO II",
    "Bombs, shells and gunfire": "Bommen, granaten en beschietingen", "Aircraft crash": "Neergestort vliegtuig",
    "Damage nearby": "Schade in de omgeving",
    "The raid on Noord, 17 July 1943": "Het bombardement op Noord, 17 juli 1943",
    "Allied bombers aimed at the Fokker aircraft works in Noord and missed: their bombs fell on the streets around it and killed 158 people. Buildings near the impacts that date from after the war mark what had to be rebuilt.":
        "Geallieerde bommenwerpers mikten op de Fokkerfabriek in Noord en misten: hun bommen vielen op de woonwijken eromheen en doodden 158 mensen. Gebouwen bij de inslagen die van na de oorlog zijn, laten zien wat herbouwd moest worden.",
    "Buildings within 40 m of a recorded impact of that day.": "Gebouwen binnen 40 m van een vastgelegde inslag van die dag.",
    "Gemeente Amsterdam, wartime impacts": "Gemeente Amsterdam, inslagen in oorlogstijd",
    "Built after 1943": "Gebouwd na 1943", "Standing before 1943": "Stond er al vóór 1943",

    # wall art
    "Art on the walls": "Kunst op de muur",
    "After the war the city spent a share of every public building's budget on art. Reliefs, mosaics, murals and glass were built into schools, offices and housing blocks; the city has surveyed them and ranked the best.":
        "Na de oorlog besteedde de stad een deel van het budget van elk openbaar gebouw aan kunst. Reliëfs, mozaïeken, muurschilderingen en glas werden in scholen, kantoren en woonblokken verwerkt; de gemeente heeft ze geïnventariseerd en de beste gewaardeerd.",
    "Gemeente Amsterdam, wall art survey": "Gemeente Amsterdam, inventarisatie wandkunst",
    "Of top value": "Topwaarde", "Valuable": "Waardevol",

    # arcam
    "Prize-winning architecture": "Bekroonde architectuur",
    "Every year ARCAM, Amsterdam's architecture centre, nominates the best new buildings in the city for the Amsterdam Architecture Prize, chosen by a jury and by the public.":
        "Elk jaar nomineert ARCAM, het architectuurcentrum van Amsterdam, de beste nieuwe gebouwen van de stad voor de Amsterdamse Architectuur Prijs, gekozen door een jury en door het publiek.",
    "ARCAM, Amsterdam Architecture Prize": "ARCAM, Amsterdamse Architectuur Prijs",
    "Winner": "Winnaar", "Nominated": "Genomineerd",

    # heritage
    "Protected heritage": "Beschermd erfgoed",
    "About one building in twelve is a listed monument: by the State for national significance, or by the city for local value.":
        "Ongeveer één op de twaalf gebouwen is een monument: van het Rijk om nationale betekenis, of van de gemeente om lokale waarde.",
    "National monument": "Rijksmonument", "Municipal monument": "Gemeentelijk monument",

    # world
    "The world in Amsterdam": "De wereld in Amsterdam",
    "Refugees, merchants, occupiers and colonies tied Amsterdam to the world. Each colour is a country or a community; every building carries its own story and source.":
        "Vluchtelingen, kooplieden, bezetters en koloniën verbonden Amsterdam met de wereld. Elke kleur is een land of een gemeenschap; elk gebouw heeft zijn eigen verhaal en bron.",
    "Wikipedia, per building": "Wikipedia, per gebouw",
    "Russia": "Rusland", "Britain": "Groot-Brittannië", "France": "Frankrijk", "Germany": "Duitsland",
    "Portugal and Spain": "Portugal en Spanje", "Asia and the East Indies": "Azië en Oost-Indië",
    "The Atlantic and slavery": "De Atlantische wereld en slavernij",
    "Amstelhof, H'ART Museum": "Amstelhof, H'ART Museum",
    "From 2009 the Hermitage Amsterdam showed loans from the State Hermitage in St Petersburg. After Russia invaded Ukraine in 2022 the museum cut its ties and reopened as H'ART in 2023.":
        "Vanaf 2009 toonde de Hermitage Amsterdam bruiklenen van de Staatshermitage in Sint-Petersburg. Na de Russische inval in Oekraïne in 2022 verbrak het museum de banden en heropende het in 2023 als H'ART.",
    "Hope & Co": "Hope & Co",
    "The bank of the Hope family, founded in 1762, did much of its business in Russia and invested there in the early 1800s.":
        "De bank van de familie Hope, opgericht in 1762, deed veel zaken in Rusland en investeerde daar in het begin van de 19de eeuw.",
    "English Reformed Church": "Engelse Kerk",
    "Since 1607 the church of English and Scottish Presbyterians in Amsterdam, who were given the Begijnhof's medieval chapel.":
        "Sinds 1607 de kerk van de Engelse en Schotse presbyterianen in Amsterdam, die de middeleeuwse kapel van het Begijnhof kregen.",
    "Christ Church": "Christ Church",
    "A former cloth hall turned into the Anglican church of Amsterdam's English community, one of the first Anglican churches on the Continent.":
        "Een voormalige lakenhal, verbouwd tot de anglicaanse kerk van de Engelse gemeenschap, een van de eerste anglicaanse kerken op het vasteland.",
    "Walloon Church": "Waalse Kerk",
    "The church of the French-speaking Walloon and Huguenot Protestants who fled the Spanish Netherlands and France.":
        "De kerk van de Franstalige Waalse en hugenootse protestanten die de Spaanse Nederlanden en Frankrijk ontvluchtten.",
    "Royal Palace": "Koninklijk Paleis",
    "Built as the city hall; in 1808 Louis Napoleon, king of Holland, made it his palace, and it has been a royal palace since.":
        "Gebouwd als stadhuis; in 1808 maakte Lodewijk Napoleon, koning van Holland, er zijn paleis van, en sindsdien is het een koninklijk paleis.",
    "Maison Descartes": "Maison Descartes",
    "The Walloon orphanage from 1671; from 1971 to 2016 the French institute Maison Descartes and the French consulate.":
        "Vanaf 1671 het Waalse weeshuis; van 1971 tot 2016 het Franse instituut Maison Descartes en het Franse consulaat.",
    "Descartes' house": "Huis van Descartes",
    "René Descartes lived here in 1634, during his twenty years in the Dutch Republic.":
        "René Descartes woonde hier in 1634, tijdens zijn twintig jaar in de Republiek.",
    "Old Lutheran Church": "Oude Lutherse Kerk",
    "Built in 1632–1633 for Amsterdam's Lutherans, on the site of the warehouse where they had worshipped since 1600.":
        "Gebouwd in 1632–1633 voor de Amsterdamse lutheranen, op de plek van het pakhuis waar ze sinds 1600 kerkten.",
    "Round Lutheran Church": "Ronde Lutherse Kerk",
    "The second Lutheran church, opened in 1671 when the old one on the Spui grew too small.":
        "De tweede lutherse kerk, geopend in 1671 toen de oude aan het Spui te klein werd.",
    "Merwedeplein 37": "Merwedeplein 37",
    "The Frank family fled Frankfurt for Amsterdam in 1933 and lived in this flat until they went into hiding in 1942.":
        "De familie Frank vluchtte in 1933 van Frankfurt naar Amsterdam en woonde in deze flat tot ze in 1942 onderdook.",
    "Zentralstelle für jüdische Auswanderung": "Zentralstelle für jüdische Auswanderung",
    "The German office that organised the deportation of the Jews of the Netherlands had its first offices here.":
        "Het Duitse bureau dat de deportatie van de Nederlandse Joden organiseerde, had hier zijn eerste kantoor.",
    "SD headquarters, Euterpestraat": "Hoofdkwartier van de SD, Euterpestraat",
    "A girls' school that housed the headquarters of the German Sicherheitsdienst (SD) during the occupation; the street, then Euterpestraat, was renamed after the resistance fighter Gerrit van der Veen.":
        "Een meisjes-HBS waarin tijdens de bezetting het hoofdkwartier van de Duitse Sicherheitsdienst (SD) zat; de straat, toen Euterpestraat, werd later vernoemd naar verzetsstrijder Gerrit van der Veen.",
    "Portuguese Synagogue": "Portugese Synagoge",
    "Inaugurated in 1675 by the Portuguese-Jewish community, then the largest synagogue in the world.":
        "In 1675 ingewijd door de Portugees-Joodse gemeente, toen de grootste synagoge ter wereld.",
    "Huis De Pinto": "Huis De Pinto",
    "Named after the Sephardic De Pinto family, who bought the house in 1651 and gave it its Italianate front.":
        "Genoemd naar de sefardische familie De Pinto, die het huis in 1651 kocht en het zijn Italiaans aandoende gevel gaf.",
    "Named after the Sephardic De Pinto family, who bought the house in 1651.":
        "Genoemd naar de sefardische familie De Pinto, die het huis in 1651 kocht.",
    "East India House": "Oost-Indisch Huis",
    "Headquarters of the Dutch East India Company (VOC), built in 1604.": "Hoofdkantoor van de VOC, gebouwd in 1604.",
    "Scheepvaarthuis": "Scheepvaarthuis",
    "Offices of six shipping companies that sailed to the Dutch East Indies, built 1913–1916.": "Kantoor van zes rederijen die op Nederlands-Indië voeren, gebouwd in 1913–1916.",
    "Tropenmuseum, Colonial Institute": "Tropenmuseum, Koloniaal Instituut",
    "Founded in 1864 as the Colonial Museum; this building, opened in 1926, was made to display the Dutch colonies.":
        "Opgericht in 1864 als Koloniaal Museum; dit gebouw, geopend in 1926, werd gemaakt om de Nederlandse koloniën te tonen.",
    "He Hua Temple": "He Hua Tempel",
    "A Buddhist temple of Fo Guang Shan in Chinatown, opened in 2000.":
        "Een boeddhistische tempel van Fo Guang Shan in Chinatown, geopend in 2000.",
    "West India House": "West-Indisch Huis",
    "Headquarters of the West India Company from 1623 to 1647, which ran the slave trade and the colony of New Netherland.":
        "Van 1623 tot 1647 het hoofdkantoor van de West-Indische Compagnie, die de slavenhandel en de kolonie Nieuw-Nederland bestuurde.",
    "Herengracht 537": "Herengracht 537",
    "Home of Wigbold Slicher, director of the Society of Suriname from 1708 to 1729.":
        "Woonhuis van Wigbold Slicher, directeur van de Sociëteit van Suriname van 1708 tot 1729.",
    "Huis De Vicq": "Huis De Vicq",
    "Built in 1670 for François de Vicq, regent, director of the West India Company and of the Society of Suriname.":
        "Gebouwd in 1670 voor François de Vicq, regent, bewindhebber van de WIC en directeur van de Sociëteit van Suriname.",

    # Jewish Amsterdam
    "Jewish Amsterdam": "Joods Amsterdam",
    "In 1940 some 75,000 to 80,000 Jews lived in Amsterdam, a little under a tenth of the city. Sephardic and Ashkenazi communities had built synagogues, schools and a world centre of the diamond trade; under German occupation about three in four of them were deported and murdered.":
        "In 1940 woonden er zo'n 75.000 tot 80.000 Joden in Amsterdam, iets minder dan een tiende van de stad. Sefardische en Asjkenazische gemeenschappen hadden synagogen, scholen en een wereldcentrum van de diamanthandel gebouwd; onder de Duitse bezetting werden ongeveer drie op de vier van hen gedeporteerd en vermoord.",
    "The homes of the victims are not shown: the dataset linking the Joods Monument to buildings has no open licence. joodsmonument.nl lists every person and address.":
        "De woonhuizen van de slachtoffers staan er niet in: de dataset die het Joods Monument aan gebouwen koppelt, heeft geen open licentie. joodsmonument.nl noemt iedere persoon en elk adres.",
    "Community and worship": "Gemeenschap en eredienst", "Work and the diamond trade": "Werk en diamanthandel",
    "Persecution 1940–1945": "Vervolging 1940–1945", "Hiding and rescue": "Onderduik en redding",
    "Lives remembered": "Levens herdacht",
    "Great Synagogue, Jewish Museum": "Grote Synagoge, Joods Museum",
    "The Great Synagogue of the Ashkenazi community, opened in 1671, now part of the Jewish Museum.":
        "De Grote Synagoge van de Asjkenazische gemeente, geopend in 1671, nu deel van het Joods Museum.",
    "Uilenburger Synagogue": "Uilenburgersjoel",
    "A synagogue of 1766 on the island of Uilenburg, once one of the poorest Jewish neighbourhoods.":
        "Een synagoge uit 1766 op het eiland Uilenburg, ooit een van de armste Joodse buurten.",
    "Lekstraat Synagogue": "Lekstraatsynagoge",
    "A synagogue of the 1930s for the Jews who moved to the new southern districts.":
        "Een synagoge uit de jaren dertig voor de Joden die naar de nieuwe zuidelijke wijken verhuisden.",
    "Gerard Dou Synagogue": "Synagoge Gerard Doustraat",
    "A synagogue of 1892 in the Pijp, a working-class district with many Jewish families.":
        "Een synagoge uit 1892 in de Pijp, een arbeiderswijk met veel Joodse gezinnen.",
    "Burcht van Berlage": "Burcht van Berlage",
    "Headquarters of the diamond workers' union ANDB, led by Henri Polak, built by Berlage in 1900.":
        "Hoofdkantoor van de diamantbewerkersbond ANDB onder leiding van Henri Polak, gebouwd door Berlage in 1900.",
    "Asscher Diamond Factory": "Diamantslijperij Asscher",
    "The Asscher family's diamond works of 1907, where the Cullinan, the largest diamond ever found, was cut.":
        "De diamantslijperij van de familie Asscher uit 1907, waar de Cullinan, de grootste diamant ooit gevonden, werd geslepen.",
    "Hollandsche Schouwburg": "Hollandsche Schouwburg",
    "A theatre the occupier turned into the assembly point for Jews awaiting deportation, 1942–1943.":
        "Een theater dat de bezetter in 1942–1943 gebruikte als verzamelplaats voor Joden die op deportatie wachtten.",
    "Joodsche Invalide": "Joodsche Invalide",
    "A Jewish home for the elderly and disabled; its residents were deported in a single night in 1943.":
        "Een Joods tehuis voor ouderen en gehandicapten; de bewoners werden in 1943 in één nacht gedeporteerd.",
    "Hervormde Kweekschool": "Hervormde Kweekschool",
    "From this teacher training college, opposite the Schouwburg, hundreds of Jewish children were smuggled out and hidden. It now houses the National Holocaust Museum.":
        "Vanuit deze kweekschool tegenover de Schouwburg werden honderden Joodse kinderen weggesmokkeld en ondergebracht. Nu is hier het Nationaal Holocaustmuseum.",
    "Anne Frank House": "Anne Frank Huis",
    "The Frank family hid in the rear annex here from 1942 until they were betrayed in 1944.":
        "De familie Frank zat hier vanaf 1942 ondergedoken in het Achterhuis, tot ze in 1944 werd verraden.",
    "The Frank family's flat after they fled Frankfurt in 1933.":
        "De woning van de familie Frank nadat ze in 1933 uit Frankfurt was gevlucht.",
    "Etty Hillesum's house": "Huis van Etty Hillesum",
    "Etty Hillesum wrote her diaries here, 1941–1943, before she was murdered in Auschwitz.":
        "Etty Hillesum schreef hier in 1941–1943 haar dagboeken, voordat ze in Auschwitz werd vermoord.",
    "Rembrandt House": "Rembrandthuis",
    "Rembrandt lived here from 1639 to 1658, among the Sephardic neighbours who appear in his work.":
        "Rembrandt woonde hier van 1639 tot 1658, tussen de sefardische buren die in zijn werk terugkomen.",

    # secrets
    "Secrets of the city": "Geheimen van de stad",
    "Hidden churches in attics, houses no wider than a door, wooden façades that survived the fire bans, courtyards behind unmarked gates: places that are easy to walk past.":
        "Schuilkerken op zolders, huizen niet breder dan een deur, houten gevels die de brandverboden overleefden, hofjes achter onopvallende poorten: plekken waar je makkelijk langs loopt.",
    "Our Lord in the Attic": "Ons' Lieve Heer op Solder",
    "In 1661 a stocking merchant bought this canal house and fitted out a Catholic church in its attics, at a time when Catholics could not worship in public.":
        "In 1661 kocht een kousenkoopman dit grachtenhuis en richtte op de zolders een katholieke kerk in, in een tijd dat katholieken niet openlijk mochten kerken.",
    "Het Houten Huis": "Het Houten Huys",
    "One of the city's last wooden houses, from around 1528, with wooden front and back walls; entirely wooden houses no longer exist in the old centre.":
        "Een van de laatste houten huizen van de stad, van rond 1528, met een houten voor- en achtergevel; geheel houten huizen zijn er in het oude centrum niet meer.",
    "In 't Aepjen": "In 't Aepjen",
    "Built around 1550, one of the oldest wooden houses still standing; the saying 'in de aap gelogeerd zijn', to be in a fix, is said to come from here.":
        "Gebouwd rond 1550, een van de oudste houten huizen die nog staan; de uitdrukking 'in de aap gelogeerd zijn' zou hier vandaan komen.",
    "The smallest house": "Het kleinste huis",
    "2.02 metres wide and 5 metres deep: often called the smallest house in Amsterdam.":
        "2,02 meter breed en 5 meter diep: vaak het kleinste huis van Amsterdam genoemd.",
    "The narrowest front": "De smalste gevel",
    "The narrowest house front in Amsterdam; the house widens behind it.":
        "De smalste voorgevel van Amsterdam; erachter wordt het huis breder.",
    "The Little Trip House": "Het Kleine Trippenhuis",
    "A narrow house across the canal from the Trips' palace, built in the same style as its grand neighbour.":
        "Een smal huis aan de overkant van het paleis van de Trippen, gebouwd in dezelfde stijl als zijn grote buur.",
    "The Begijnhof": "Het Begijnhof",
    "The only hofje founded in medieval Amsterdam: a courtyard of houses behind a gate off the Spui, lying almost a metre below the street.":
        "Het enige hofje dat in het middeleeuwse Amsterdam werd gesticht: een hof met huizen achter een poort aan het Spui, bijna een meter lager dan de straat.",
    "De Papegaai": "De Papegaai",
    "A clandestine Catholic church of the Republic, still entered from the Kalverstraat shopping street.":
        "Een katholieke schuilkerk uit de tijd van de Republiek, nog altijd bereikbaar vanuit de winkelstraat Kalverstraat.",
    "Schreierstoren": "Schreierstoren",
    "A defensive tower built around 1487. Legend says sailors' wives wept farewell here, which gave it its name, but the story is probably untrue.":
        "Een verdedigingstoren van rond 1487. Volgens de legende namen vrouwen hier huilend afscheid van hun zeelieden, vandaar de naam, maar dat verhaal is waarschijnlijk apocrief.",
    "De Gooyer": "De Gooyer",
    "A windmill in the middle of the city: two wooden octagons stacked on a brick base.":
        "Een molen midden in de stad: twee op elkaar geplaatste houten achtkanten op een stenen onderbouw.",
    "Montelbaanstoren": "Montelbaanstoren",
    "A defensive tower of 1516; Hendrick de Keyser added its spire in 1606, and Rembrandt, who lived nearby, drew it in 1644.":
        "Een verdedigingstoren uit 1516; Hendrick de Keyser zette er in 1606 de spits op, en Rembrandt, die in de buurt woonde, tekende hem in 1644.",
    "Huis met de Hoofden": "Huis met de Hoofden",
    "Named after six heads on its front. Legend says they are robbers beheaded one by one by the kitchen maid; they are in fact busts of six classical gods.":
        "Genoemd naar de zes hoofden op de gevel. Volgens de legende zijn het rovers die de keukenmeid een voor een onthoofdde; in werkelijkheid zijn het borstbeelden van zes klassieke goden.",
    "Bartolotti House": "Huis Bartolotti",
    "Its front has two kinks so that it follows the bend of the Herengracht.":
        "De gevel heeft twee knikken, zodat hij de bocht van de Herengracht volgt.",
    "De Waag": "De Waag",
    "A city gate of 1488 that became a weighhouse; Rembrandt's 'Anatomy Lesson of Dr Tulp' was painted for the surgeons who met upstairs.":
        "Een stadspoort uit 1488 die een waag werd; Rembrandts 'Anatomische les van Dr. Tulp' werd geschilderd voor de chirurgijns die boven vergaderden.",
    "Café Karpershoek": "Café Karpershoek",
    "Its building dates from 1629, and the café is said to be the oldest bar in Amsterdam.":
        "Het pand dateert uit 1629 en het café zou de oudste kroeg van Amsterdam zijn.",

    # residents
    "Who lived here": "Wie woonde hier",
    "Painters, writers, scientists and sailors whose Wikipedia biography names the Amsterdam address where they lived or worked. Pick a name to fly to the house.":
        "Schilders, schrijvers, wetenschappers en zeelieden van wie de Wikipedia-biografie het Amsterdamse adres noemt waar ze woonden of werkten. Kies een naam om naar het huis te vliegen.",
    "Found automatically in Dutch Wikipedia and matched to today's address; house numbers have sometimes changed, and some houses were rebuilt since.":
        "Automatisch gevonden in de Nederlandstalige Wikipedia en gekoppeld aan het huidige adres; huisnummers zijn soms veranderd en sommige huizen zijn sindsdien herbouwd.",
    "Dutch Wikipedia, via Wikidata": "Nederlandstalige Wikipedia, via Wikidata",
    "Home of a well-known resident": "Woonhuis van een bekende bewoner",

    # street art
    "Street art": "Straatkunst", "1990–today": "1990–heden",
    "Amsterdam paints its blank walls: portraits of Johan Cruijff and Ramses Shaffy, Eduardo Kobra's Anne Frank, and dozens of murals commissioned for whole housing blocks in Nieuw-West and Noord. Each work links to its article or its map entry.":
        "Amsterdam beschildert zijn blinde muren: portretten van Johan Cruijff en Ramses Shaffy, de Anne Frank van Eduardo Kobra en tientallen muurschilderingen voor hele woonblokken in Nieuw-West en Noord. Elk werk linkt naar zijn artikel of kaartvermelding.",
    "Murals and graffiti with a Wikidata item or an OpenStreetMap entry, placed on the nearest building.":
        "Muurschilderingen en graffiti met een Wikidata-item of een vermelding in OpenStreetMap, op het dichtstbijzijnde gebouw geplaatst.",
    "Wikidata, Wikipedia and OpenStreetMap": "Wikidata, Wikipedia en OpenStreetMap",
    "Mural": "Muurschildering", "Graffiti and street art": "Graffiti en straatkunst",
}


# The twelve layers of curated_more.py, translated with them.
import json as _json
from pathlib import Path as _Path
NL.update(_json.loads((_Path(__file__).parent / "curated_more_nl.json").read_text()))
NL.update({
    "Wall art": "Wandkunst", "Murals and street art": "Muurschilderingen en straatkunst",
    "Community, worship and work": "Gemeenschap, geloof en werk",
    "Bijlmermeer, IJplein, Plan Van Gool": "Bijlmermeer, IJplein, Plan Van Gool",
    "Art and craft": "Kunst en ambacht", "Science and learning": "Wetenschap en onderwijs",
})
# Building names in those layers are Dutch already: they stay as they are.
from .curated_more import CURATED_MORE as _MORE  # noqa: E402
NL.update({e[0]: e[0] for L in _MORE for e in L["entries"] if e[0] not in NL})
