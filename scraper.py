import requests
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_pdf_files(till=798285):
    """
    Fetches PDF files from a website using a search and download process.

    This function sends requests to a website, searches for PDF files, and downloads them
    based on a given range of TezNo values.

    Args:
    - till (int): The upper limit (inclusive) of the TezNo range. Defaults to 798285.

    Returns:
    None
    """

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

    search_tez_url = 'https://tez.yok.gov.tr/UlusalTezMerkezi/SearchTez'
    tez_detay_url = 'https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id={id_t}'
    download_url = 'https://tez.yok.gov.tr/UlusalTezMerkezi/TezGoster?key={key_t}'

    payload_str = 'uniad=&Universite=0&Tur=0&yil1=0&yil2=0&ensad=&Enstitu=0&izin=0&abdad=&ABD=0&Durum=3&TezAd=&bilim=&BilimDali=0&Dil=1&AdSoyad=&Konu=&EnstituGrubu=&DanismanAdSoyad=&Dizin=&Metin=&islem=2&Bolum=0&-find=++Bul++'
    payload_d = {i: j for i, j in [i.split('=') for i in payload_str.split('&')]}

    id_pattern = re.compile('onclick=tezDetay\(\'(.*?)\',')
    pdf_pattern = re.compile('<a href="TezGoster\?key=(.*?)"')

    for i in range(1, till + 1):
        form_data = payload_d.copy()
        form_data['TezNo'] = i

        try:
            # Send search request
            search_tez_response = session.post(search_tez_url, data=form_data)
            search_tez_response.raise_for_status()

            text = search_tez_response.text

            # Extract tezDetay id
            id_search = id_pattern.search(text)
            if id_search:
                id_t = id_search.group(1)

                # Send tezDetay request
                tez_detay_response = session.get(tez_detay_url.format(id_t=id_t))
                tez_detay_response.raise_for_status()

                text = tez_detay_response.text

                # Extract PDF key
                pdf_search = pdf_pattern.search(text)
                if pdf_search:
                    key_t = pdf_search.group(1)

                    # Send download request
                    download_response = session.get(download_url.format(key_t=key_t))
                    download_response.raise_for_status()

                    # Save PDF file
                    with open(f'pdf/{i}.pdf', 'wb') as f:
                        f.write(download_response.content)
                        logger.info(f'{i}.pdf saved')

        except (requests.RequestException, IOError) as e:
            logger.error(f'Error occurred while fetching PDF for TezNo {i}: {str(e)}')

        except Exception as e:
            logger.error(f'Unexpected error occurred while fetching PDF for TezNo {i}: {str(e)}')

# Call the function to start fetching PDF files
fetch_pdf_files()
