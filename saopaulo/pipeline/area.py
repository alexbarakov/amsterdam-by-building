"""The part of São Paulo on the map: the centro expandido, roughly the city inside the Tietê and Pinheiros
rivers and the Bandeirantes–Salim Farah Maluf ring, as GeoSampa districts (names as in its file names).
The whole municipality has some 2.8 million buildings, too many for one page; add districts here to grow the map."""

DISTRICTS = [
    "SE", "REPUBLICA", "BELA_VISTA", "CONSOLACAO", "LIBERDADE", "CAMBUCI", "SANTA_CECILIA", "BOM_RETIRO",
    "PARI", "BRAS", "BELEM", "MOOCA", "BARRA_FUNDA", "PERDIZES", "PINHEIROS", "JARDIM_PAULISTA",
    "ITAIM_BIBI", "MOEMA", "VILA_MARIANA", "ALTO_DE_PINHEIROS", "LAPA", "IPIRANGA", "AGUA_RASA",
    "TATUAPE", "CAMPO_BELO", "SAUDE",
]

# Local frame origin: Praça da Sé, marco zero of the city, in SIRGAS 2000 / UTM zone 23S (EPSG:31983).
ORIGIN = (333221.0, 7394609.0)
CRS = 31983
