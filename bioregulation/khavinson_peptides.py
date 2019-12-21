khav_pept = {
 "Epitalon": "AEDG",
 "Pinealon": "EDR",
 "Chonluten": "EDG",
 "Vilon": "KE",
 "Thymogen": "EW",
 "Pancragen": "KEDW",
 "Bronchogen": "AEDL",
 "Cartalax": "AED",
 "Vesugen": "KED",
 "Crystagen": "EDP",
 "Ovagen": "EDL",
 "Prostasmax": "KEDP",
 "Livagen": "KEDA",
 "Cortagen": "AEDP",
 "Cardiogen": "AEDR",
 "Testagen": "KEDG",
 "Leucyllysine": "LK",
 "GA": "ED",
 "D2": "DW",
 "D4": "DG",
 "D5": "DL",
 "D7": "DS",
 "A8": "DE",
}
for value in khav_pept.values():
    print(value)

pharm_groups = {
 "immunomodulators": ["KE", "EW", "EDP"],
 "omnimodulator": ["AEDG"],
 "neurorotectors": ["DG", "AEDP", "EDR"],
 "bronchoprotectors": ["EDG", "AEDL", "DE"],
 "pancreoprotectors": ["KEDW"],
 "vasoprotectors": ["KED", "DS"],
 "hepatoprotectors": ["EDL", "DL"],
 "malereproduct": ["KEDP", "KEDG"],
 "cardioprotector": ["AEDR"],
 "hondroprotectors": ["AED"],
 "skinregulators": ["LK", "AEDG", "AED", "KE", "KED"],
 "nefroprotectors": ["DW", "EDL", "AED"],
 "onkostatics": ["AEDG", "KE", "EW", "EDG"],
 "mochpuz": ["ED"]
}

pharm_groups_filtered = {
 "immunomodulators": ["KE", "EW"],
 "omnimodulator": ["AEDG"],
 "neurorotectors": ["AEDP", "EDR"],
 "bronchoprotectors": ["EDG", "AEDL"],
 "pancreoprotectors": ["KEDW"],
 "vasoprotectors": ["KED"],
 "hepatoprotectors": ["EDL"],
 "malereproduct": ["KEDP", "KEDG"],
 "cardioprotector": ["AEDR"],
 "hondroprotectors": ["AED"],
 "skinregulators": [ "AED", "KED"],
 "nefroprotectors": ["EDL", "AED"],
 "onkostatics": ["AEDG", "KE", "EW"],
 "mochpuz": ["ED"]
}


