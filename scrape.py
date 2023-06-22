import requests, re

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
search_tez_url = 'https://tez.yok.gov.tr/UlusalTezMerkezi/SearchTez'
till = 798285
payload_str = 'uniad=&Universite=0&Tur=0&yil1=0&yil2=0&ensad=&Enstitu=0&izin=0&abdad=&ABD=0&Durum=3&TezAd=&bilim=&BilimDali=0&Dil=0&AdSoyad=&Konu=&EnstituGrubu=&DanismanAdSoyad=&Dizin=&Metin=&islem=2&Bolum=0&-find=++Bul++'
payload_d = {i : j for i, j in [i.split('=') for i in payload_str.split('&')]}
id_pattern = 'onclick=tezDetay\(\'(.*?)\','
tez_detay_url = 'https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id={id_t}'
pdf_pattern = '<a href="TezGoster\?key=(.*?)"'
download_url = 'https://tez.yok.gov.tr/UlusalTezMerkezi/TezGoster?key={key_t}'
for i in range(1, till+1):
    form_data = payload_d.copy()
    form_data['TezNo'] = i
    search_tez_response = session.post(search_tez_url, data=form_data)
    if search_tez_response.status_code == 200:
        text = search_tez_response.text
        id_search = re.search(id_pattern, text)
        if id_search:
            id_t = id_search.group(1)
            tez_detay_response = session.get(tez_detay_url.format(id_t=id_t))
            if tez_detay_response.status_code == 200:
                text = tez_detay_response.text
                pdf_search = re.search(pdf_pattern, text)
                if pdf_search:
                    key_t = pdf_search.group(1)
                    download_response = session.get(download_url.format(key_t=key_t))
                    if download_response.status_code == 200:
                        with open(f'{i}.pdf', 'wb') as f:
                            f.write(download_response.content)
                            print(f'{i}.pdf saved')