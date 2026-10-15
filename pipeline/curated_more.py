"""More hand-curated context layers, in the format of curated.py, each with a `section`.

Every entry: (name, address, story, wikipedia "lang:Title", checks). Every string in `checks` appears literally
in the plain-text extract of that article; every address resolves to itself as the first PDOK Locatieserver hit.

Dropped candidates and why:
- Kloveniersdoelen / Doelen Hotel (Nieuwe Doelenstraat): the Night Watch hung in the doelen, but the hotel only
  stands on its site; the building of 1638 is gone.
- Rembrandt's last home, Rozengracht 184: the article gives the address, not whether his house still stands.
- Vondel's family shop, Warmoesstraat 39; Gerard Reve's birthplace, Van Hallstraat 25: same problem.
- Rembrandt and Saskia's rooms with Hendrick van Uylenburgh, Jodenbreestraat 2: no article confirms the house.
- Oost-Indisch Zeemagazijn (Oostenburg): collapsed on 14 April 1822.
- Huis van Bewaring I, Weteringschans: demolished; the raids of 1944 have no standing building.
- Gewestelijk Arbeidsbureau, Passeerdersgracht 28-32 (Gerrit van der Veen's arson, 1943): the article gives a
  range of numbers and the building's survival is not stated.
- Februaristaking 1941 meeting on the Noordermarkt, the Dokwerker, the Nationaal Monument, the Homomonument,
  Het Lieverdje: monuments or squares, not buildings. The strike is told through the Lloyd Hotel instead.
- Vondelkerk (Vondelstraat 120): partly collapsed in the fire of New Year's night 2026.
- Kweekschool voor de Zeevaart: no current address in the article.
- Jacob van Lennep's childhood home, "now Keizersgracht 473": no such address in BAG/PDOK.
- Sint-Nicolaasbasiliek (Prins Hendrikkade 73) and Sint-Olofskapel (Zeedijk 2): both addresses exist, but PDOK
  ranks another address first ("Prins Hendrikkade 189A-73", "Zeedijk 103A-2"), so they fail the strict check.
- Paleis voor Volksvlijt (Sarphati): burned in 1929. Sarphati is told through the Amstel Hotel.
- Six family at Amstel 218: the article names only the foundation, not the house.
- De Telegraaf building, where Trouw and Het Parool were printed after 1945: the article gives no address.
- Stopera as the place of the first same-sex weddings (2001): no article ties the weddings to the building.
- Trippenhuis as seat of the Royal Academy: kept out of a third new layer; it carries the Trips and the Rijksmuseum.
- Kleine Komedie in the royal layer (Louis Napoleon and William I as regulars): kept in music and theatre only.
- Vondel and Hooft are told through the Nieuwe Kerk; Rembrandt's grave through the Westerkerk; Comenius through
  the Huis met de Hoofden (whose legend is already in "secrets").
"""

CURATED_MORE = [
    dict(
        id="merchants", section="Trade and empire", title="Golden Age merchants", era="1617–1781",
        intro=("The money of the Golden Age went into houses. Arms dealers, cloth merchants and company directors "
               "built along the new canals, competed in façades, and left houses that later owners, from bankers "
               "to the mayor, still live and work in."),
        entries=[
            ("Trippenhuis", "Kloveniersburgwal 29",
             "Built in 1660–1662 by Justus Vingboons for the arms dealers Louys and Hendrick Trip: two houses behind "
             "one palace front, meant to outshine the house of their rival Louis de Geer.",
             "nl:Trippenhuis", ("Kloveniersburgwal 29", "Louys", "Justus Vingboons", "Louis de Geer", "1660-1662")),
            ("Bartolotti House", "Herengracht 172",
             "Built around 1617 for Willem van den Heuvel, who inherited a fortune from the Bologna merchant Giovanni "
             "Battista Bartolotti on condition that he take his name; the design is attributed to Hendrick de Keyser.",
             "nl:Huis Bartolotti", ("Herengracht 170", "1617", "Giovanni Battista Bartolotti", "Hendrick de Keyser")),
            ("Coymanshuis", "Keizersgracht 177",
             "The first known design by Jacob van Campen, a front of 1625 for the merchant Balthasar Coymans; since "
             "2003 the Dutch head office of Amnesty International.",
             "nl:Coymanshuis", ("Keizersgracht 177", "1625", "Balthasar Coymans", "Amnesty International")),
            ("Huis Marseille", "Keizersgracht 401",
             "Built around 1665 for the French merchant Isaac Focquier, who put a map of the port of Marseille on "
             "the front; since 1999 a museum of photography.",
             "nl:Huis Marseille", ("Keizersgracht 401", "1665", "Isaac Focquier", "Marseille", "1999")),
            ("Cromhouthuizen", "Herengracht 366",
             "Four houses built in 1660–1662 by Philips Vingboons for the merchant Jacob Cromhout, who lived at "
             "number 366, behind a stone carved with a crooked piece of wood.",
             "nl:Cromhouthuizen", ("1660-1662", "Philips Vingboons", "Jacob Cromhout", "366", "krom stuk hout")),
            ("Museum Van Loon", "Keizersgracht 672",
             "Built in 1671–1672 by Adriaan Dortsman for the Flemish merchant Jeremias van Raey; owned by the Van "
             "Loon family since 1884, and a museum since 1973.",
             "nl:Museum Van Loon", ("Keizersgracht 672", "1671-1672", "Jeremias van Raey", "Adriaan Dortsman", "1884")),
            ("Huis met de Kolommen", "Herengracht 502",
             "Built in 1672 for Paulus Godin, a director of the West India Company; Cornelis van Aalst gave it to the "
             "city in 1927, and it has been the official residence of the mayor of Amsterdam since.",
             "nl:Herengracht 502", ("Herengracht 502", "Paulus Godin", "1672", "West-Indische Compagnie", "1927")),
            ("Huis Willet-Holthuysen", "Herengracht 605",
             "Built in 1685–1687 for Jacob Hop, pensionary of Amsterdam; the collectors Abraham Willet and Louisa "
             "Holthuysen left house and collection to the city in 1895.",
             "nl:Museum Willet-Holthuysen", ("Herengracht 605", "Jacob Hop", "Abraham Willet", "1895")),
            ("Huis Van Brienen", "Herengracht 284",
             "Rebuilt from 1728 for the Mennonite merchant David Rutgers; bought in 1781 by Arnold Johan van Brienen, "
             "whose son Willem Joseph van Brienen was mayor under King Louis Napoleon.",
             "nl:Huis Van Brienen", ("Herengracht 284", "David Rutgers", "1781", "Willem Joseph van Brienen",
                                     "Lodewijk Napoleon")),
            ("Huis van der Graeff", "Herengracht 446",
             "The double house of Andries de Graeff, seven times mayor of Amsterdam, in the middle of the Golden Bend.",
             "nl:Andries de Graeff", ("Herengracht (thans nr. 446)", "zevenmaal burgemeester", "Gouden Bocht")),
            ("Huis De Neufville", "Herengracht 475",
             "A house of 1731, often called the finest on the Golden Bend.",
             "nl:Gouden Bocht", ("Huis de Neufville (1731), Herengracht 475", "mooiste Huis aan de Bocht")),
        ]),
    dict(
        id="painters", section="Art and craft", title="Rembrandt and the painters", era="1639–today",
        intro=("Rembrandt worked, went bankrupt and was buried in Amsterdam. The city's painters left their houses, "
               "graves and guild halls, and their work moved through a chain of museums, from a canal house to the "
               "Museumplein."),
        entries=[
            ("Rembrandt House", "Jodenbreestraat 4",
             "Rembrandt bought this house on 5 January 1639 for 13,000 guilders and lost it after his bankruptcy; it "
             "was auctioned in 1658. Opened as a museum on 10 June 1911, on the initiative of the painter Jozef Israëls.",
             "nl:Rembrandthuis", ("5 januari 1639", "dertienduizend gulden", "1658", "10 juni 1911", "Jozef Israëls")),
            ("Oude Kerk", "Oudekerksplein 23",
             "Saskia van Uylenburgh (1612–1642), Rembrandt's wife, is buried in the Oude Kerk.",
             "nl:Oude Kerk (Amsterdam)", ("Saskia van Uylenburgh (1612-1642)", "Oudekerksplein")),
            ("Westerkerk", "Prinsengracht 279",
             "Rembrandt (died 1669) and his son Titus (died 1668) were buried here; the place of Rembrandt's grave is "
             "unknown, and a memorial was placed in 1906.",
             "nl:Westerkerk (Amsterdam)", ("Rembrandt van Rijn (1606/1607-1669)", "Titus van Rijn (1641-1668)",
                                          "plaats van het graf onbekend", "1906")),
            ("Trippenhuis", "Kloveniersburgwal 29",
             "From 1817 to 1885 the Trip brothers' palace housed the Rijksmuseum, before the museum moved to its own "
             "building.",
             "nl:Trippenhuis", ("Van 1817 tot 1885", "Rijksmuseum")),
            ("Rijksmuseum", "Museumstraat 1",
             "The national museum of art and history, in Pierre Cuypers's building since 1885; it reopened on 13 April "
             "2013 after ten years of rebuilding.",
             "nl:Rijksmuseum Amsterdam", ("1885", "Pierre Cuypers", "13 april 2013")),
            ("Van Gogh Museum", "Museumplein 6",
             "Built to a design by Gerrit Rietveld for the collection that Vincent van Gogh left to his brother Theo "
             "and that Jo van Gogh-Bonger kept together; it opened in 1973.",
             "nl:Van Gogh Museum", ("Gerrit Rietveld", "Theo van Gogh", "Jo van Gogh-Bonger", "1973")),
            ("Stedelijk Museum", "Museumplein 10",
             "The city's museum of modern art, founded in 1874, opened in this building by Adriaan Willem Weissman in "
             "1895; Willem Sandberg became its director after the occupation.",
             "nl:Stedelijk Museum Amsterdam", ("1874", "1895", "Adriaan Willem Weissman",
                                              "Na de bezetting werd Sandberg directeur")),
            ("Rijksakademie", "Sarphatistraat 470",
             "The academy of fine arts founded by King William III in 1870, where Breitner and Mondrian studied; since "
             "1992 in a former cavalry barracks.",
             "nl:Rijksakademie van beeldende kunsten", ("1870", "Willem III", "Piet Mondriaan", "1992",
                                                       "Sarphatistraat 470")),
            ("Jacob de Wit's house", "Keizersgracht 385",
             "The painter Jacob de Wit, master of painted ceilings, bought this house in 1741 and lived and worked here "
             "until his death in 1754.",
             "nl:Jacob de Wit", ("Keizersgracht 383 en 385", "1741", "1754")),
            ("Goudstikker's gallery", "Herengracht 458",
             "From 1927 the art dealer Jacques Goudstikker ran his gallery here, under ceilings by Gerard de Lairesse; "
             "he died at sea aboard the Bodegraven on 16 May 1940.",
             "nl:Jacques Goudstikker", ("Herengracht 458", "1927", "Gerard de Lairesse", "a/b van de Bodegraven",
                                       "16 mei 1940")),
            ("Arti et Amicitiae", "Rokin 112",
             "The society of artists founded in 1839, whose members included George Hendrik Breitner; its rooms on the "
             "corner of the Spui were partly designed by Berlage.",
             "nl:Arti et Amicitiae", ("Rokin 112", "1839", "George Hendrik Breitner", "Berlage")),
        ]),
    dict(
        id="port", section="Trade and empire", title="The port and the navy", era="1642–1934",
        intro=("East of the old city, the Admiralty and the East India Company built islands of yards, ropewalks "
               "and warehouses. When steam came, shipping lines built new docks along the IJ; their warehouses now "
               "hold offices, flats and a hotel."),
        entries=[
            ("'s Lands Zeemagazijn, Scheepvaartmuseum", "Kattenburgerplein 1",
             "The storehouse of the Admiralty of Amsterdam, built in 1655–1656 under Daniël Stalpaert; the largest "
             "surviving 17th-century warehouse, and the maritime museum since 1973.",
             "nl:'s Lands Zeemagazijn", ("1655-1656", "Daniël Stalpaert", "Admiraliteit van Amsterdam", "1973")),
            ("Gate of the naval yard", "Kattenburgerstraat 7",
             "The 17th-century gate of the navy's yard on Kattenburg, designed by Daniël Stalpaert; one of only two "
             "original buildings left on the Marineterrein.",
             "nl:Marineterrein (Amsterdam)", ("Kattenburgerstraat 7", "Daniël Stalpaert", "poortgebouw")),
            ("VOC ropewalk", "Oostenburgergracht 77",
             "The front building of 1660 of the East India Company's ropewalk on Oostenburg, with the company's "
             "monogram in its pediment; from 1950 to 2011 it housed the Werkspoor Museum.",
             "nl:Lijnbaan van de Verenigde Oost-Indische Compagnie", ("1660", "Oostenburgergracht", "A VOC",
                                                                    "Werkspoormuseum")),
            ("Admiralty ropewalk", "Oostenburgergracht 81",
             "The Admiralty's ropewalk of 1660; a plaque recalls Tsar Peter the Great, who may have stayed here while "
             "he trained in Amsterdam in 1697.",
             "nl:Admiraliteitslijnbaan", ("1660", "Oostenburgergracht", "Peter de Grote", "1697")),
            ("West India Warehouse", "'s-Gravenhekje 1A",
             "Built in 1642 for the West India Company, which stored hides from New Amsterdam here; from 1647 to 1674 "
             "it was the company's headquarters, running a trade in gold, sugar and enslaved people.",
             "nl:West-Indisch Pakhuis", ("1642", "Nieuw-Amsterdam", "1647 en 1674", "slaven")),
            ("Werf 't Kromhout", "Hoogte Kadijk 147",
             "A shipyard on an old sea dyke, named after Doede Janszn. Kromhout, whose wife bought the site in 1757; "
             "it closed in 1967 and has been a working yard museum since 1973.",
             "nl:Werf 't Kromhout", ("Hoogte Kadijk", "Doede Janszn. Kromhout", "1757", "1967", "1973")),
            ("Lloyd Hotel", "Oostelijke Handelskade 34",
             "Built for the Koninklijke Hollandsche Lloyd and opened in 1921 to lodge emigrants to South America, many "
             "of them Jews from Eastern Europe fleeing pogroms.",
             "nl:Lloyd Hotel (hotel)", ("Koninklijke Hollandsche Lloyd", "1921", "Zuid-Amerika", "pogroms")),
            ("Pakhuis De Zwijger", "Piet Heinkade 179",
             "A cold store of 1933–1934 for perishable goods on the Eastern Docks, saved when the Jan Schaeferbrug "
             "was built straight through it in 2001.",
             "nl:Pakhuis De Zwijger", ("1933-1934", "Jan Schaeferbrug", "2001")),
        ]),
    dict(
        id="science", section="Science and learning", title="Science and medicine", era="1470–today",
        intro=("Long before it had a university, Amsterdam had a school of illustrious learning in a convent chapel, "
               "a medicinal garden, an anatomist who sold his collection to a tsar, a zoo founded by a bookseller "
               "and a laboratory built for a physicist."),
        entries=[
            ("Agnietenkapel", "Oudezijds Voorburgwal 231",
             "A convent chapel of 1470 that became the Athenaeum Illustre in 1631; Gerardus Vossius and Caspar "
             "Barlaeus gave their inaugural lectures here in January 1632, the start of the University of Amsterdam.",
             "nl:Agnietenkapel (Amsterdam)", ("Oudezijds Voorburgwal 231", "1470", "1631", "Gerardus Vossius",
                                             "Caspar Barlaeus", "Universiteit van Amsterdam")),
            ("Oudemanhuispoort", "Oudemanhuispoort 4",
             "Built around 1601 as a home for old men and women, with shop stalls in its passage from 1757; "
             "now the University of Amsterdam's humanities faculty.",
             "nl:Oudemanhuispoort", ("1601", "1757", "Universiteit van Amsterdam")),
            ("University Library", "Singel 421",
             "The library goes back to the books of the Nieuwe Kerk, handed to the Athenaeum Illustre in 1632; since "
             "1881 it has been in the former Handboogdoelen on the Singel.",
             "nl:Universiteitsbibliotheek van Amsterdam", ("1632", "Athenaeum Illustre", "1881", "Singel 421",
                                                          "Handboogdoelen")),
            ("Hortus Botanicus", "Plantage Middenlaan 2A",
             "Amsterdam's medicinal garden, founded in 1638, was laid out anew here in 1682 by Jan Commelin and Joan "
             "Huydecoper; its palm house dates from 1912.",
             "nl:Hortus Botanicus Amsterdam", ("1638", "1682", "Jan Commelin", "Joan Huydecoper", "1912")),
            ("Artis", "Plantage Kerklaan 38",
             "The zoo of the society Natura Artis Magistra, founded on 1 May 1838 by the bookseller Gerardus Frederik "
             "Westerman, Johann Wilhelm Heinrich Werlemann and Jan Jacob Wijsmuller; the oldest zoo in the Netherlands.",
             "nl:Artis", ("Natura Artis Magistra", "1 mei 1838", "Gerardus Frederik Westerman", "Wijsmuller",
                          "oudste dierentuin")),
            ("Ruysch's house", "Bloemgracht 15",
             "The anatomist Frederik Ruysch bought this house for his family; in 1698 the mayor Nicolaes Witsen "
             "brought Tsar Peter the Great to him, and Ruysch sold the tsar part of his collection.",
             "nl:Frederik Ruysch", ("Bloemgracht 15", "1698", "Nicolaes Witsen", "Peter de Grote")),
            ("Felix Meritis", "Keizersgracht 324",
             "Built for the society Felix Meritis, founded in 1777 to practise the arts and sciences, and opened on 31 "
             "October 1788; from 1947 to 1981 the headquarters of the Dutch Communist Party.",
             "nl:Felix Meritis", ("Keizersgracht 324", "1777", "31 oktober 1788", "Communistische Partij van Nederland")),
            ("Zeeman Laboratory", "Plantage Muidergracht 4A",
             "A physics laboratory built in 1923 for Pieter Zeeman, with vibration-free tables for his magnetic and "
             "optical experiments; it was named after him in 1940.",
             "nl:Zeemanlaboratorium", ("Plantage Muidergracht, nummer 4", "1923", "Pieter Zeeman", "1940")),
            ("Allard Pierson", "Oude Turfmarkt 127",
             "The university's archaeology museum, named after the professor Allard Pierson and opened on 12 November "
             "1934; its first collections included those of Jan Six.",
             "nl:Allard Pierson Museum", ("Oude Turfmarkt 127", "Allard Pierson (1831-1896)", "12 november 1934",
                                         "Jan Six")),
            ("NEMO Science Museum", "Oosterdok 2",
             "A hands-on science museum in a building of 1997 by Renzo Piano, on the foundations of the IJ tunnel; its "
             "shape stands for the tunnel's entrance.",
             "nl:NEMO (museum)", ("1997", "Renzo Piano", "fundamenten van de IJ-tunnel", "ingang van de IJ-tunnel")),
        ]),
    dict(
        id="resistance", section="War and occupation", title="Resistance and liberation", era="1941–1945",
        intro=("Amsterdam fought the occupation from its first winter: a brawl in an ice-cream parlour, the "
               "February strike, an attack on the population register. Liberation came with a massacre on the Dam."),
        entries=[
            ("Koco ice-cream parlour", "Van Woustraat 149",
             "On 19 February 1941 a squad of Jewish and non-Jewish neighbours defended the parlour of the German-Jewish "
             "refugees Alfred Kohn and Ernst Cahn against the German police. Days later the occupier raided the Jewish "
             "quarter for the first time.",
             "nl:Razzia van Amsterdam", ("Van Woustraat 149", "19 februari", "Alfred Kohn", "Ernst Cahn")),
            ("Lloyd Hotel, Huis van Bewaring III", "Oostelijke Handelskade 34",
             "During the war the emigrants' hotel served as a prison; in 1941 some 150 strikers of the February strike "
             "were locked up here.",
             "nl:Lloyd Hotel (hotel)", ("Huis van Bewaring III", "1941", "Februaristakers")),
            ("Population register", "Plantage Kerklaan 36",
             "On the night of 27 March 1943 a group led by Gerrit van der Veen and Willem Arondéus set fire to the "
             "city's population register, held in Artis' former concert hall, to destroy the records of some 70,000 "
             "Jews.",
             "nl:Aanslag op het Amsterdams bevolkingsregister", ("27 maart 1943", "Plantage Kerklaan 36",
                                                               "Gerrit van der Veen", "Willem Arondéus", "70.000")),
            ("Stedelijk Museum", "Museumplein 10",
             "Its curator Willem Sandberg narrowly escaped arrest and in 1943 fled into the dunes by bicycle when the "
             "Germans came for him.",
             "nl:Stedelijk Museum Amsterdam", ("Willem Sandberg", "ontsnapte ternauwernood", "1943",
                                              "per fiets de duinen")),
            ("Vrankrijk", "Spuistraat 216",
             "During the war part of the building was used by the cartoonist Marten Toonder, who had the resistance "
             "make false papers for people in hiding here.",
             "nl:Vrankrijk", ("Spuistraat 216", "Marten Toonder", "valse papieren")),
            ("Huis van Bewaring II", "Havenstraat 6",
             "The prison where Johannes Kleiman and Victor Kugler, helpers of the Frank family, were held, and from "
             "which Hannie Schaft was taken to be shot on 17 April 1945.",
             "nl:Huis van Bewaring II (Amstelveenseweg)", ("Havenstraat 6", "Johannes Kleiman", "Victor Kugler",
                                                          "Hannie Schaft", "17 april 1945")),
            ("De Groote Club", "Dam 16",
             "On 7 May 1945, as crowds waited on the Dam for the Canadian liberators, German navy men opened fire from "
             "the balconies of this club building, killing at least 32 people.",
             "nl:De Groote Club", ("Dam 16", "7 mei 1945", "Duitse Marine", "32 doden")),
            ("Verzetsmuseum", "Plantage Kerklaan 61A",
             "Built in 1874–1876 for the Jewish men's choir Oefening Baart Kunst; since 1999 the Resistance Museum.",
             "nl:Gebouw Plancius", ("Plantage Kerklaan 61", "1876", "Oefening Baart Kunst", "1999",
                                    "Verzetsmuseum Amsterdam")),
        ]),
    dict(
        id="counterculture", section="The modern city", title="Provo, squatters and the free city",
        era="1965–today",
        intro=("From the Provo happenings on the Spui in 1965, Amsterdam's young took over churches, factories and "
               "canal houses: hippies made pop venues, squatters fought the police for empty buildings, and "
               "hashish found its first coffeeshop."),
        entries=[
            ("Paradiso", "Weteringschans 6",
             "The 1880 meeting hall of the free-thinking Vrije Gemeente, squatted by hippies in October 1967; it opened as "
             "a youth centre in 1968, with Pink Floyd among the first bands.",
             "nl:Paradiso (Amsterdam)", ("1880", "Vrije Gemeente", "oktober 1967", "1968", "Pink Floyd")),
            ("Melkweg", "Lijnbaansgracht 234",
             "A former sugar refinery and milk factory that became a summer project for young people in 1970 and a "
             "permanent cultural centre in 1973.",
             "nl:Melkweg (Amsterdam)", ("suikerraffinaderij", "1970", "1973")),
            ("Fantasio and Kosmos", "Prins Hendrikkade 142",
             "From the 1960s the youth centre Fantasio and then the meditation centre de Kosmos used this house.",
             "nl:Prins Hendrikkade", ("jongerencentrum Fantasio", "meditatiecentrum de Kosmos")),
            ("Mellow Yellow", "Weesperzijde 53",
             "In 1972 Wernard Bruining and friends squatted a former bakery here; as Mellow Yellow it became "
             "Amsterdam's first coffeeshop.",
             "nl:Mellow Yellow (coffeeshop)", ("Weesperzijde 53", "1972", "Wernard Bruining", "eerste Amsterdamse coffeeshop")),
            ("De Groote Keijser", "Keizersgracht 242",
             "Six canal houses, offices of the Technische Unie until 1978, squatted on 1 November 1978; with the "
             "Vondelstraat and the Lucky Luyk one of the key events of the squatters' movement.",
             "nl:Groote Keijser", ("242 tot 252", "Technische Unie", "1 november 1978", "Vondelstraat", "Lucky Luyk")),
            ("Vondelstraat 72", "Vondelstraat 72",
             "Re-squatted on 29 February 1980; three platoons of riot police were driven off and barricades went up, "
             "the first great squatters' riots of Amsterdam.",
             "nl:Vondelstraatrellen", ("29 februari", "nummer 72 in de Vondelstraat", "Mobiele Eenheid")),
            ("Lucky Luyk", "Jan Luijkenstraat 3",
             "An Art Nouveau house of 1908–1909, squatted on 4 April 1981; it became known through the squatters' "
             "riots of 1982.",
             "nl:Lucky Luyk", ("Jan Luijkenstraat 3", "1908-1909", "4 april 1981", "1982")),
            ("Tetterode", "Bilderdijkstraat 165",
             "The former type foundry Tetterode, squatted in 1981, grew into a community of several hundred people.",
             "nl:De Trut", ("lettergieterij Tetterode", "1981", "enkele honderden mensen")),
            ("OCCII", "Amstelveenseweg 134",
             "A horse-tram depot by Abraham Salm, squatted in 1984 and legalised in 1989; a venue for independent "
             "music since 1992.",
             "nl:OCCII", ("Amstelveenseweg 134", "paardentramremise", "Abraham Salm", "1984", "1989", "1992")),
            ("Vrankrijk", "Spuistraat 216",
             "A building of 1875 that became a squat inhabited by autonomists, with a café and a weekly squatting "
             "advice hour.",
             "nl:Vrankrijk", ("Spuistraat 216", "1875", "autonomen", "kraakspreekuur")),
        ]),
    dict(
        id="queer", section="Discover", title="Queer Amsterdam", era="1927–today",
        intro=("A café on the Zeedijk run by a woman on a motorbike, a club founded in 1946 that grew into the COC, "
               "Europe's largest gay discotheque, women's cafés and an archive: the places of a century of gay and "
               "lesbian Amsterdam, which in 2001 saw the first same-sex marriages in the world."),
        entries=[
            ("Café 't Mandje", "Zeedijk 63",
             "Bet van Beeren took over this café in 1927 and made it one of the first where gay men and lesbians did "
             "not have to hide; it closed in 1983 and reopened in 2008.",
             "nl:Café 't Mandje", ("Zeedijk 63", "Bet van Beeren", "1927", "1983", "2008")),
            ("Café De la Paix", "Leidsestraat 67",
             "On 7 December 1946 about 150 people met in the café here to found the Shakespeare Club, the start of "
             "the COC, then the largest gathering of gay people ever in the Netherlands.",
             "nl:COC Nederland", ("7 december 1946", "Shakespeare Club", "Leidsestraat 67-71", "150 mensen")),
            ("DOK, De Odeon Kelder", "Singel 460",
             "In 1952 the COC opened a club in the cellar here; its treasurer Lou Charité took it over and made it the "
             "largest gay discotheque in Europe.",
             "nl:De Schakel (sociëteit)", ("1952", "Singel 460", "Lou Charité", "grootste homodiscotheek van Europa")),
            ("De Schakel", "Korte Leidsedwarsstraat 49",
             "The COC's club from 1955 to 1978, hugely popular with gay men and foreign visitors.",
             "nl:De Schakel (sociëteit)", ("Korte Leidsedwarsstraat 49", "1955", "1978")),
            ("Amstel Taveerne", "Amstel 54",
             "Ad van Besouw opened the Amstel Taveerne on 27 August 1964, a gay bar known for Dutch songs sung by its "
             "guests.",
             "nl:Amstel Taveerne", ("Amstel 54", "27 augustus 1964", "Ad (in de volksmond: Adje) van Besouw")),
            ("Café Saarein", "Elandsstraat 119",
             "The oldest women's café in Amsterdam still open, taken over in 1978 by a collective of ten women.",
             "nl:Saarein", ("Elandsstraat 119", "1978", "oudste nog bestaande vrouwencafé")),
            ("Vivelavie", "Nieuwezijds Voorburgwal 171",
             "Mieke Martelhoff opened a café in the basement here in 1980; within weeks it became a café for lesbian "
             "women.",
             "nl:Vivelavie", ("Nieuwezijds Voorburgwal 171", "1980", "Mieke Martelhoff")),
            ("Cockring", "Warmoesstraat 96",
             "A gay discotheque from 1987 to 2010.",
             "nl:Cockring (discotheek)", ("Warmoesstraat 96", "1987", "2010")),
            ("De Trut", "Bilderdijkstraat 165",
             "A non-commercial queer disco in the cellar of the squatted Tetterode complex since December 1985.",
             "nl:De Trut", ("Bilderdijkstraat 165E", "december 1985", "Tetterode")),
            ("Remonstrant church Vrijburg", "Diepenbrockstraat 46",
             "On 31 January 1987 the first church blessing of a marriage between two men took place here.",
             "nl:Amsterdam als homohoofdstad", ("31 januari 1987", "Vrijburg", "Diepenbrockstraat")),
            ("IHLIA, in the public library", "Oosterdokskade 143",
             "Since 2007 the LGBTI heritage archive IHLIA, formed in 1999 from the Homodok and the Lesbian Archive, has "
             "been housed in the Openbare Bibliotheek Amsterdam.",
             "nl:IHLIA LGBTI Heritage", ("1999", "Homodok", "Lesbisch Archief Amsterdam", "juli 2007",
                                        "Openbare Bibliotheek Amsterdam")),
        ]),
    dict(
        id="stage", section="Art and craft", title="Music and theatre", era="1786–today",
        intro=("Amsterdam's stages run from a French theatre of 1786 to concert halls on the IJ: a circus that "
               "became a royal theatre, a cinema palace whose founder was murdered in Auschwitz, a jazz club that "
               "began in a furniture showroom."),
        entries=[
            ("De Kleine Komedie", "Amstel 56",
             "Built in 1786 as a French theatre, where Louis Napoleon and King William I were regulars; the oldest "
             "theatre in Amsterdam, reopened as De Kleine Komedie in 1947 and now the temple of Dutch cabaret.",
             "nl:De Kleine Komedie", ("1786", "Lodewijk Napoleon", "Koning Willem I", "oudste theater van Amsterdam",
                                      "1947")),
            ("Frascati", "Nes 63",
             "Built in 1824 as a concert and leisure hall beside an 18th-century coffee house of the same name.",
             "nl:Frascati (theater)", ("1824", "koffiehuis")),
            ("Theater Bellevue", "Leidsekade 90",
             "A building of around 1840 for two societies, chaired at first by the writer Jacob van Lennep; on 15 "
             "December 1935 the last game of the world chess championship between Alexander Alekhine and Max Euwe was "
             "played here.",
             "nl:Theater Bellevue", ("1840", "Jacob van Lennep", "15 december 1935", "Aljechin", "Max Euwe")),
            ("Carré", "Amstel 115",
             "Opened on 3 December 1887 by Oscar Carré as a stone circus; it has been a royal theatre since its "
             "centenary in 1987.",
             "nl:Koninklijk Theater Carré", ("3 december 1887", "Oscar Carré", "1987")),
            ("Concertgebouw", "Concertgebouwplein 10",
             "Opened on 11 April 1888 to a design by Adolf Leonard van Gendt; under the occupation its orchestra had "
             "to dismiss its seventeen Jewish members.",
             "nl:Concertgebouw (Amsterdam)", ("11 april 1888", "Adolf Leonard van Gendt", "zeventien Joodse leden")),
            ("Stadsschouwburg", "Leidseplein 26",
             "The city theatre of 1894 by Jan Springer and Adolf Leonard van Gendt, built after its predecessor burned "
             "down on 20 February 1890; the first stone theatre of 1637 was by Jacob van Campen.",
             "nl:Stadsschouwburg (Amsterdam)", ("1894", "Jan Springer", "20 februari 1890", "Jacob van Campen", "1637")),
            ("Tuschinski", "Reguliersbreestraat 26",
             "Opened on 28 October 1921 by Abraham Tuschinski, a Jewish cinema owner from Poland; he was arrested in "
             "1942 and murdered in Auschwitz.",
             "nl:Tuschinski Theater", ("28 oktober 1921", "Abraham Tuschinski", "18 augustus 1942", "Auschwitz")),
            ("Stopera", "Amstel 3",
             "City hall and opera house in one, by Wilhelm Holzbauer and Cees Dam, opened on 23 September 1986 in the "
             "old Jewish quarter; it was controversial from the start.",
             "nl:Stopera", ("Wilhelm Holzbauer", "Cees Dam", "23 september 1986")),
            ("Muziekgebouw aan 't IJ", "Piet Heinkade 1",
             "A concert hall of 2005 by the Danish firm 3XN, built over the IJ tunnel, with a ceiling that moves to "
             "change the acoustics.",
             "nl:Muziekgebouw aan 't IJ", ("2005", "3XN", "IJ-tunnel")),
            ("Bimhuis", "Piet Heinkade 3",
             "The jazz club opened on 1 October 1974 in a former furniture showroom on the Oudeschans and moved into "
             "its glass-walled hall on the IJ in 2005.",
             "nl:Bimhuis", ("1 oktober 1974", "meubelshowroom", "2005")),
            ("Eye Filmmuseum", "IJpromenade 1",
             "The film museum's building by Roman Delugan and Elke Delugan-Meissl, opened on 4 April 2012.",
             "nl:Eye Filmmuseum", ("Roman Delugan", "Elke Delugan-Meissl", "4 april 2012")),
        ]),
    dict(
        id="royal", section="Discover", title="Royal Amsterdam", era="1580–2013",
        intro=("Amsterdam is the capital, but the court sits in The Hague. The House of Orange comes to the city to "
               "be inaugurated, to marry and to receive state guests, and its princes have stayed and ridden here "
               "since the Revolt."),
        entries=[
            ("Prinsenhof", "Oudezijds Voorburgwal 197",
             "A convent that lodged high guests after 1578 and probably took its name from William of Orange, who "
             "stayed in 1580 or 1581; Maria de' Medici was a guest in 1638. It served as the city hall from 1808 to "
             "1988.",
             "nl:Prinsenhof (Amsterdam)", ("Willem van Oranje", "1580 of 1581", "Maria de' Medici", "1808 en 1988")),
            ("Royal Palace", "Dam 1",
             "Built from 1648 to 1665 as the city hall to a design by Jacob van Campen and inaugurated on 29 July "
             "1655; today the royal family's palace for receptions and state visits.",
             "nl:Paleis op de Dam", ("1648 en 1665", "Jacob van Campen", "29 juli 1655", "ontvangstpaleis")),
            ("Nieuwe Kerk", "Dam 12",
             "Sovereign Prince William swore his oath on the constitution here on 30 March 1814; every Dutch monarch "
             "since has been inaugurated here, Beatrix on 30 April 1980 and Willem-Alexander in 2013.",
             "nl:Nieuwe Kerk (Amsterdam)", ("30 maart 1814", "30 april 1980", "Willem-Alexander")),
            ("Beurs van Berlage", "Damrak 243",
             "Willem-Alexander and Máxima were married in a civil ceremony in Berlage's exchange on 2 February 2002.",
             "nl:Nieuwe Kerk (Amsterdam)", ("2 februari 2002", "Beurs van Berlage")),
            ("Westerkerk", "Prinsengracht 279",
             "Princess Beatrix married Claus von Amsberg here on 10 March 1966, because the Nieuwe Kerk was being "
             "restored.",
             "nl:Westerkerk (Amsterdam)", ("10 maart 1966", "Claus von Amsberg", "werd gerestaureerd")),
            ("Hollandsche Manege", "Vondelstraat 140",
             "The oldest riding school in the Netherlands, rebuilt in 1882 on the model of the Spanish Riding School "
             "in Vienna, where Amsterdam's well-to-do and members of the royal house learned to ride.",
             "nl:Hollandsche Manege", ("oudste rijschool", "1882", "Spaanse rijschool in Wenen",
                                       "leden van het koninklijk huis")),
            ("Centraal Station, royal waiting room", "Stationsplein 15",
             "On the east side of the station is the Koningspaviljoen, today the royal waiting room, with its own "
             "indoor parking place, once for a carriage.",
             "nl:Station Amsterdam Centraal", ("Koningspaviljoen", "Koninklijke wachtkamer", "koets")),
            ("Olympisch Stadion", "Olympisch Stadion 2",
             "Jan Wils's stadium for the Olympic Games of 1928; Prince Hendrik attended both the laying of the first "
             "stone on 18 May 1927 and the opening on 28 July 1928.",
             "nl:Olympisch Stadion (Amsterdam)", ("Jan Wils", "18 mei 1927", "28 juli 1928", "Prins Hendrik")),
        ]),
    dict(
        id="nineteenth", section="The modern city", title="The 19th-century city", era="1825–1914",
        intro=("After a century of decline, Amsterdam grew again: a doctor planned a grand hotel, a brewer moved "
               "out to the new edge of town, a gas works lit the streets, and a new station rose on an "
               "island in the IJ."),
        entries=[
            ("Paleis van Justitie", "Prinsengracht 436",
             "Jan de Greef rebuilt the Aalmoezeniersweeshuis, an orphanage of 1663–1665, into the courts of justice; "
             "they moved in from the Prinsenhof on 4 October 1836.",
             "nl:Paleis van Justitie (Amsterdam)", ("Prinsengracht 436", "Jan de Greef", "Aalmoezeniersweeshuis",
                                                   "4 oktober 1836")),
            ("Oranje-Nassau Kazerne", "Sarphatistraat 600",
             "A barracks built on Napoleon's orders, with a front 278 metres long; converted to flats and offices in "
             "1990.",
             "nl:Oranje-Nassau Kazerne", ("Napoleon", "278 meter", "1990")),
            ("Amstel Hotel", "Prof. Tulpplein 1",
             "The doctor Samuel Sarphati saw the need for a first-class hotel; building began on 26 April 1866 and the "
             "hotel opened in the summer of 1867.",
             "nl:Amstel Hotel", ("Professor Tulpplein 1", "Samuel Sarphati", "26 april 1866", "1867")),
            ("Heineken Brewery", "Stadhouderskade 78",
             "Gerard Adriaan Heineken bought the brewery De Hooiberg on 15 February 1863 and in 1867 moved it to this "
             "new site on the edge of the city.",
             "nl:Heineken Brouwerij (Amsterdam)", ("15 februari 1863", "Gerard Adriaan Heineken", "De Hooiberg", "1867")),
            ("Krasnapolsky", "Dam 9",
             "Adolph Wilhelm Krasnapolsky bought a failing coffee house in 1865 and added hotel rooms and a glass "
             "winter garden in 1879–1880; the winter garden is said to have inspired Gerard Philips.",
             "nl:Grand Hotel Krasnapolsky", ("Adolph Wilhelm Krasnapolsky", "1865", "1879/1880", "Gerard Philips")),
            ("Hollandsche Manege", "Vondelstraat 140",
             "A riding school of 1882 with an iron roof and an iron-and-glass entrance hall, modelled on the Spanish "
             "Riding School in Vienna.",
             "nl:Hollandsche Manege", ("1882", "Spaanse rijschool in Wenen", "ijzeren dakkap")),
            ("Westergasfabriek", "Haarlemmerweg 8",
             "Built in 1883 for the British Imperial Continental Gas Association, the largest coal gas works in the "
             "Netherlands, mostly designed by Isaac Gosschalk.",
             "nl:Westergas", ("1883", "Imperial Continental Gas Association", "Isaac Gosschalk")),
            ("Centraal Station", "Stationsplein 15",
             "Built in 1881–1889 to designs by Pierre Cuypers and Dolf van Gendt, on an island made in the IJ.",
             "nl:Station Amsterdam Centraal", ("1881 en 1889", "Pierre Cuypers", "Dolf van Gendt", "Stationseiland")),
            ("Main Post Office, Magna Plaza", "Nieuwezijds Voorburgwal 182",
             "The main post office of 1895–1899 by the government architect C.H. Peters, behind the palace; now a "
             "shopping centre.",
             "nl:Magna Plaza", ("1895-1899", "C.H. Peters", "winkelcentrum")),
            ("American Hotel", "Leidseplein 28",
             "The hotel of 1882 was replaced in 1902 by an Art Nouveau building by Willem Kromhout and H.G. Jansen, "
             "home of the Café Américain.",
             "nl:American Hotel", ("Leidseplein 28", "1882", "1902", "Willem Kromhout", "Café Americain")),
        ]),
    dict(
        id="churches", section="Faith and community", title="Churches of the city", era="1306–1881",
        intro=("The Reformation of 1578 gave the medieval churches to the Calvinists, who then built the first "
               "Protestant churches of the Republic. Catholics, Mennonites and Remonstrants worshipped out of sight "
               "until the 19th century let them build in the street again."),
        entries=[
            ("Oude Kerk", "Oudekerksplein 23",
             "Begun around 1250 and consecrated in 1306 to Saint Nicholas, the oldest building in Amsterdam; it "
             "passed to the Protestants at the Alteration of 1578.",
             "nl:Oude Kerk (Amsterdam)", ("oudste nog bestaande gebouw van Amsterdam", "1306", "Alteratie (1578)")),
            ("Zuiderkerk", "Zandstraat 17",
             "The first church in Amsterdam designed for Protestant worship, begun in 1603 to a design by Hendrick de "
             "Keyser, who was buried in it in 1621.",
             "nl:Zuiderkerk (Amsterdam)", ("eerste voor de protestantse eredienst ontworpen kerk", "1603",
                                          "Hendrick de Keyser", "Zandstraat no. 17",
                                          "Toen Hendrick de Keyser in 1621 overleed, werd hij in de Zuiderkerk begraven")),
            ("Noorderkerk", "Noordermarkt 48",
             "Hendrick de Keyser's church in the shape of a Greek cross, built in 1620–1623 for the growing Jordaan; "
             "the first service was held on 16 April 1623.",
             "nl:Noorderkerk (Amsterdam)", ("Hendrick de Keyser", "1620 en 1623", "Grieks kruis", "16 april 1623")),
            ("Singelkerk", "Singel 452",
             "A Mennonite church hidden behind house fronts, on land bought in 1607 for a meeting barn of the Flemish "
             "Mennonites.",
             "nl:Singelkerk (Amsterdam)", ("doopsgezinde", "schuilkerk", "1607")),
            ("De Rode Hoed", "Keizersgracht 102",
             "A former hidden church of the Remonstrants, now a centre for public debate.",
             "nl:Rode Hoed", ("remonstrantse schuilkerk", "Keizersgracht op nummer 102", "debatcentrum")),
            ("Amstelkerk", "Amstelveld 10",
             "A wooden church by Daniël Stalpaert of 1668–1670, meant as a temporary 'preaching barn' until a stone "
             "church could be built.",
             "nl:Amstelkerk (Amsterdam)", ("houten kerkgebouw", "1668 en 1670", "Daniël Stalpaert", "predikschuur")),
            ("Oosterkerk", "Kleine Wittenburgerstraat 1",
             "The church of the eastern islands, with a bell cast by Pieter Hemony in 1671.",
             "nl:Oosterkerk (Amsterdam)", ("Wittenburg", "Pieter Hemony", "1671")),
            ("Mozes en Aäronkerk", "Waterlooplein 205",
             "A Catholic church that grew out of a Franciscan hidden church, from 1641 in the house 'Moyses' on the "
             "Jodenbreestraat, to which the house 'Aäron' was added in 1682.",
             "nl:Mozes en Aäronkerk", ("schuilkerk", "1641", "Moyses", "1682")),
            ("De Duif", "Prinsengracht 756",
             "A church of 1857 with a neo-Baroque front on the canal; since 1974 the home of the ecumenical "
             "congregation De Duif.",
             "nl:De Duif (kerk)", ("1857", "Prinsengracht 756", "1974", "oecumenische")),
            ("Posthoornkerk", "Haarlemmerstraat 124",
             "Pierre Cuypers designed this church in 1860 to replace the decaying hidden church De Posthoorn.",
             "nl:Posthoornkerk", ("1860", "schuilkerk De Posthoorn")),
            ("De Krijtberg", "Singel 448",
             "The Jesuits' neo-Gothic church by Alfred Tepe, begun in 1881 in place of a hidden church in a house "
             "called Crijtberg, in use since 1654.",
             "nl:De Krijtberg", ("jezuïeten", "1654", "Crijtberg", "1881", "Alfred Tepe")),
        ]),
    dict(
        id="writers", section="Science and learning", title="Writers and thinkers", era="1614–2010",
        intro=("Vondel worked at the pawnbank, Comenius lived with a family of arms dealers, Multatuli was born in an "
               "alley between two canals: the houses, workplaces and graves of Amsterdam's writers."),
        entries=[
            ("Huis met de Hoofden", "Keizersgracht 123",
             "The De Geer family, arms dealers, let the Czech thinker Jan Amos Comenius live here; since 2017 the "
             "Embassy of the Free Mind, home of the Bibliotheca Philosophica Hermetica.",
             "nl:Huis met de Hoofden", ("Keizersgracht 123", "Jan Amos Comenius", "2017", "Embassy of the Free Mind",
                                       "Bibliotheca Philosophica Hermetica")),
            ("Stadsbank van Lening", "Oudezijds Voorburgwal 300",
             "The city's pawnbank, founded in 1614; the poet Joost van den Vondel worked here as an attendant from 1658 "
             "for more than ten years.",
             "nl:Stadsbank van Lening (Amsterdam)", ("1614", "In 1658 werd Vondel aangesteld", "ruim tien jaar")),
            ("Nieuwe Kerk", "Dam 12",
             "Joost van den Vondel and Pieter Corneliszoon Hooft are buried here; memorial stones honour writers "
             "from Hooft to Hella Haasse, and in 2020 King Willem-Alexander unveiled one for Multatuli.",
             "nl:Nieuwe Kerk (Amsterdam)", ("Joost van den Vondel (1587-1679)", "Pieter Corneliszoon Hooft (1581-1647)",
                                           "Hella Haasse", "17 februari 2020", "Multatuli")),
            ("Multatuli Museum", "Korsjespoortsteeg 20",
             "Eduard Douwes Dekker, the writer Multatuli, was born in this house in the Korsjespoortsteeg.",
             "nl:Eduard Douwes Dekker", ("Korsjespoortsteeg (tegenwoordig: nr. 20)", "Multatuli")),
            ("Athenaeum Boekhandel", "Spui 14",
             "The bookshop on the Spui opened in September 1966 by the publishers Johan Polak and Rob van Gennep.",
             "nl:Athenaeum Boekhandel", ("Spui", "september 1966", "Johan Polak", "Rob van Gennep")),
            ("De Amsterdammer", "Spuistraat 218",
             "In 1877 the weekly De Amsterdammer, today's De Groene Amsterdammer, was printed here by the steam "
             "lithographers Harms & Co.",
             "nl:Vrankrijk", ("218", "Harms & Co", "1877", "De Amsterdammer", "De Groene Amsterdammer")),
            ("Theo Thijssen Museum", "Eerste Leliedwarsstraat 16",
             "The birthplace of the writer and teacher Theo Thijssen, rebuilt in its original form in 1991–1995 and "
             "now a museum about him.",
             "nl:Theo Thijssen Museum", ("Eerste Leliedwarsstraat 16", "geboortehuis", "1991 en 1995")),
            ("Harry Mulisch Huis", "Leidsekade 103",
             "Harry Mulisch moved into this house on the Leidsekade in 1958 and worked here until his death in 2010; "
             "his study is kept as he left it.",
             "nl:Harry Mulisch Huis", ("Leidsekade", "1958", "2010")),
        ]),
]
