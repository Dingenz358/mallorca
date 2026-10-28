import json, sys, time, hashlib, io, urllib.request
sys.path.insert(0, sys.argv[1]); import commons
from PIL import Image
base = sys.argv[2]
r = json.load(open(base + '/results.json'))
pick = {"Kartause von Valldemossa":("Kartause von Valldemossa",1,""),"Altstadt & Geburtshaus Santa Catalina Thomàs":("VALLDEMOSSA",0,""),
"Robert-Graves-Haus, Deià":("Robert-Graves-Haus, Deià",0,""),"Son Marroig bei Deià":("Son Marroig bei Deià",0,""),"Cala Deià & Camí des Pintors":("Cala Deià & Camí des Pintors",1,""),
"Sa Foradada ab Son Marroig":("Sa Foradada ab Son Marroig",0,""),"Balm Tapas, Deià":("DEIA",0,"Ortsbild Deià"),"El Barrigón Xelini, Deià":("DEIA",0,"Ortsbild Deià"),
"Es Taller, Valldemossa":("VALLDEMOSSA",3,"Ortsbild Valldemossa"),"Tapas Bar an der Plaça Cartoixa":("Kartause von Valldemossa",0,"Plaça de la Cartoixa"),
"QuitaPenas, Valldemossa":("VALLDEMOSSA",1,"Ortsbild Valldemossa"),"Wochenmarkt Alcúdia":("Wochenmarkt Alcúdia",1,""),"Gastro-Abendmarkt":("Wochenmarkt Alcúdia",2,"Ortsbild Alcúdia"),
"Festa de les Ànimes":("Festa de les Ànimes",4,"Kirche Sant Jaume, Alcúdia"),"Altstadt & Pollentia":("ALCUDIA",0,""),"Cap de Formentor":("Cap de Formentor",1,""),
"Talaia d'Alcúdia & Penya des Migdia":("Talaia d'Alcúdia & Penya des Migdia",1,""),"Ermita de la Victòria":("Ermita de la Victòria",1,""),"Coll Baix":("Coll Baix",0,""),
"Naturpark S'Albufera":("Naturpark S'Albufera",0,""),"Platja de Muro":("Platja de Muro",0,"")}
meta = {}; done = {}
for t, (k, i, note) in pick.items():
    x = r[k][i]
    fid = hashlib.md5(x['title'].encode()).hexdigest()[:10]
    if fid not in done:
        time.sleep(2)
        raw = commons.get(x['thumb'])
        im = Image.open(io.BytesIO(raw)).convert('RGB'); im.thumbnail((720, 720))
        im.save(f"{base}/out/{fid}.jpg", quality=72, optimize=True, progressive=True)
        done[fid] = True
    meta[t] = {"file": f"{fid}.jpg", "credit": f"{x['artist'] or 'Unbekannt'} · {x['license']} · Wikimedia Commons", "page": x['page'], "note": note}
json.dump(meta, open(base + '/meta.json', 'w'), ensure_ascii=False, indent=1)
print(len(done), 'files')
