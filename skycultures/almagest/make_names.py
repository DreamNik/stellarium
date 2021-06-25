import sys
CAT_FILE = 'almstars/cat1.dat'
PROPER_NAMES = {
    #      Toomer          Greek          @sushoff                     HIP
    110: ('Arcturus',     'Ἀρκτοῦρος',   '(Arkturos, Guard)'),       # 69673
    149: ('Lyra',         'λύρα',        '(Lyra)'),                  # 91262
    222: ('Capella',      'αἴξ',         '(Goat)'),                  # 24608
    227: ('Haedi 1',      'Ἔριφοι',      '(Kids [of the Goat]) I'),  # 23767
    228: ('Haedi 2',      'Ἔριφοι',      '(Kids [of the Goat]) II'), # 23767
    288: ('Aquila',       'ἀετός',       '(Eagle)'),                 # 97649
    449: ('Praesepe',     'φάτνη',       '(Manger)'),                # -----   (NGC 2632, M 44)
    452: ('Aselli 1',     'ὄνος',        '(Ass) I'),                 # 42806   (Translated as 'asses' in a footnote.)
    453: ('Aselli 2',     'ὄνος',        '(Ass) II'),                # 42911
    469: ('Regulus',      'βασιλίσκος',  '(Princelet)'),             # 49669
    509: ('Vindemiatrix', 'Προτρυγητήρ', '(Harbinger of Vintage)'),  # 63608   (In fn.: προτρυγητήρ 'Harbinger of Vintage'.)
    510: ('Spica',        'στάχυς',      '(Ear of Grain)'),          # 65474   (In fn.: στάχυς, an ear of wheat or other cereal.)
    553: ('Antares',      'ἀντάρης',     '(Antares)'),               # 80763
    818: ('the Dog',      'κύων',        '(Dog)'),                   # 32349
                                                                     # 37279   (before the dog)
    848: ('Procyon',      'Προκύων',     '(Prokyon, The One [rising] before the Dog)'),     
    892: ('Canopus',      'Κάνωβος',     '(Kanobos)'),               # 30438
}
OUTSIDE = { # 'n' = nearby, 'u' = under, 'a' = around, 'r' = round (?)
#    I                 II                IV                V                 VII
    'UMi': (8, 'n'),  'UMa': (28, 'u'), 'Cep': (12, 'a'), 'Boo': (23, 'u'), 'Her': (29, ''),
#    IX                XI                XIII              XXII              XXIII
    'Cyg': (18, 'a'), 'Per': (27, ''),  'Oph': (25, 'a'), 'Ari': (14, 'a'), 'Tau': (34, 'a'),
#    XXV               XXIV              XXVI              XXVII             XXVIII
    'Cnc': (10, 'a'), 'Gem': (19, 'a'), 'Leo': (28, 'a'), 'Vir': (27, 'a'), 'Lib': (9, 'a'),
#    XXIX              XXXII             XXXIII            XXXVIII           XLI 
    'Sco': (22, 'a'), 'Aqr': (43, 'r'), 'Psc': (35, 'r'), 'CMa': (19, 'r'), 'Hya': (26, 'r'), 
#    XLVIII
    'PsA': (13, 'r'),
}
NEBULAE = [
    # almagest,    modern,     greek,       english
    ('Tau 30-33', 'M 45',     'Πλειάδες',  'Pleiades'),
    ('Tau 11-15', 'Mel 25',   'ʿΥάδες',     'Hyades'),
    ('Leo 33',    'Mel 111',  'πλόκαμος',  'Coma'),
    ('sco 22',    'NGC 6441', '',          ''),
]

STARS_FILE = 'star_names.fab'
DSO_FILE = 'dso_names.fab'
# HIP           SAO     HD      HR
CROSS_ID = '../../stars/default/cross-id.dat'
HIP = 0
HR = 4
DSO = {
    'NGC 869/884': ['NGC 869', 'NGC 884'],
    'NGC 2632 M44': ['M 44'],
    'NGC 5139': ['NGC 5139'],
}

def parse_cross_id(path):
    hr_to_hip = {}
    with open(path) as f:
        next(f, None)   # skip header line
        for line in f:
            parts = line.split('\t')
            hip = int(parts[HIP])
            hr = parts[HR].strip()
            if hr:
                hr_to_hip[int(hr)] = hip
    return hr_to_hip

CAT_CON = slice(5, 8)     # constellation abbreviation
CAT_IDX = slice(9, 11)    # index within constellation
CAT_HR = slice(30, 34)    # HR number
CAT_ID = slice(35, 48)    # modern Bayer/Flamsteed ID
CAT_DESC = slice(48, None)
def parse_cat(path):
    with open(path) as f:
        print(next(f, None).strip())   # skip header line
        for line in f:
            con = line[CAT_CON]
            idx = int(line[CAT_IDX])
            hr = int(line[CAT_HR].strip())
            modern_id = line[CAT_ID].strip()
            desc = line[CAT_DESC].strip()
            yield con, idx, hr, modern_id, desc

hr_to_hip = parse_cross_id(CROSS_ID)
hr_to_mid = {}
hr_to_con = {}
alm_to_desc = {}
with open(STARS_FILE, 'w') as stars, open(DSO_FILE, 'w') as dso:
    for i, (con, idx, hr, modern_id, desc) in enumerate(parse_cat(CAT_FILE), 1):
        if hr:
            if hr in hr_to_mid and modern_id != hr_to_mid[hr]:
                print(f'discrepancy in modern id for HR {hr}: '
                      f'{modern_id} != {hr_to_mid[hr]}')
            else:
                hr_to_mid[hr] = modern_id
            hr_to_con.setdefault(hr, []).append(con)
        tag = hr_to_hip.get(hr)
        if tag is not None:
            file = stars
            tags = [tag]
        elif tags is not None:
            file = dso
            tags = DSO.get(modern_id, [])
        else:
            file, tags = None, []
        if file is not None:
            for tag in tags:
                name, greek, s = PROPER_NAMES.get(i, (None, ) * 3)
                if name is not None:
                    print(f'{tag}|_("{greek} {s}")', file=file)
                if con in OUTSIDE and idx >= OUTSIDE[con][0]:
                    con = con.lower()
                print(f'{tag}|("{con} {idx}")', file=file)
                print(f'{tag}|_("{desc}")', file=file)
                alm_to_desc[f"{con} {idx}"] = desc
        else:
            print(f'No HIP number found for HR {hr} ({modern_id})', file=sys.stderr)
    for almagest, modern, greek, english in NEBULAE:
        if greek:
            print(f'{modern}|_("{greek} ({english})")', file=dso)
        print(f'{modern}|_("{almagest}")', file=dso)
        desc = alm_to_desc.get(almagest)
        if desc is not None:
            print(f'{modern}|_("{desc}")', file=dso)

print(f'  found {len(hr_to_mid)} unique stars and {len(PROPER_NAMES)} proper names')
for hr, cons in hr_to_con.items():
    if len(cons) > 1:
        mid = hr_to_mid[hr]
        print(f'{mid} (HR {hr}) is in {", ".join(cons)}.')
