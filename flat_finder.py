"""."""
import sys
import os
import argparse
import requests
import json
import smtplib

from bs4 import BeautifulSoup

urls = {
    'seloger': 'http://www.seloger.com/list.htm?pxmax=1850&surfacemin=55&idtt=1&idtypebien=1&ci=750109,750117,750118&tri=d_dt_crea&nb_pieces=3,4,5%20et%20%2b',
    'pap': 'http://www.pap.fr/annonce/location-appartement-maison-paris-9e-g37776g37777g37784g37785-du-3-pieces-au-5-pieces-a-partir-de-2-chambres-jusqu-a-1850-euros-a-partir-de-55-m2',
    'leboncoin': 'https://www.leboncoin.fr/locations/offres/ile_de_france/?th=1&location=Paris%2075018%2CParis%2075017%2CParis%2075009&parrot=0&mre=2000&sqs=6&ros=3&ret=1&ret=2&furn=2',
    'logicimmo': 'http://www.logic-immo.com/location-immobilier-paris-18e-75018,paris-17e-75017,paris-9e-75009,23597_2,23596_2,23609_2/options/groupprptypesids=1,2,6,7/pricemax=1850/areamin=55/nbrooms=3/nbbedrooms=2/order=update_date_desc',
    # 'bienici': 'https://www.bienici.com/recherche/location/bordeaux-33000/3-pieces-et-plus?prix-max=1500&surface-min=60',
    'foncia': 'https://fr.foncia.com/location/paris-75018--paris-75017--paris-75010--paris-75009/appartement--maison/(params)/on/(surface_min)/55/(prix_max)/1850/(pieces)/3--4--5',
}


def send_mail(message, site):
    gmail_user = 'newappartmentfound@gmail.com'
    gmail_password = 'hUn-spf-sRF-Z88'

    from_ = gmail_user
    to = ['your@email.com', 'your2nd@email.com']
    subject = 'Nouvelle annonce sur ' + site
    body = 'Hey,\n Voici un nouveau bien qui correspond a votre recherche :\n' + message + '\n\n- Mathieu'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (from_, ", ".join(to), subject, body)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(from_, to, email_text)
        server.close()
        print 'Email sent!'
    except:
        print 'Something went wrong...'


def parse_seloger(content):
    """."""
    #'div.content_result>section.liste_resultat>article'
    entries = []
    page = BeautifulSoup(content, 'html.parser')
    res_section = page.find('section', class_='liste_resultat')
    for e in res_section.find_all('article'):
        id = e['data-listing-id']
        url = e.find('a')['href']
        write = True
        with open('seloger-panam', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == ref_id:
                    write = False
        if write:
            # send_mail(url, 'seloger')
            entries.append({'id': ref_id, 'url': url})

    with open('seloger-panam', 'a+') as file:
        file.writelines((json.dumps(l) + '\n' for l in entries))

    return entries


def parse_pap(content):
    entries = []
    page = BeautifulSoup(content, 'html.parser')
    res_section = page.find('section', class_='search-results-container')
    for e in res_section.find_all('div', class_='search-results-item'):
        ref_id = e.find('a', class_='title-item')['name']
        url = 'http://www.pap.fr/' + e.find('a', class_='title-item')['href']
        write = True
        with open('pap-panam', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == ref_id:
                    write = False
        if write:
            # send_mail(url, 'pap')
            entries.append({'id': ref_id, 'url': url})

    with open('pap-panam', 'a+') as file:
        file.writelines((json.dumps(l) + '\n' for l in entries))

    return entries


def parse_leboncoin(content):
    entries = []
    page = BeautifulSoup(content, 'html.parser')
    res_section = page.find('section', class_='tabsContent')
    for e in res_section.find_all('li'):
        infos = json.loads(e.find('a')['data-info'].encode('utf-8'))
        url = e.find('a')['href']
        write = True
        with open('leboncoin-panam', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == infos['ad_listid']:
                    write = False
        if write:
            # send_mail(url, 'leboncoin')
            entries.append({'id': infos['ad_listid'], 'url': url})

    with open('leboncoin-panam', 'a+') as file:
        file.writelines((json.dumps(l) + '\n' for l in entries))

    return entries


def parse_foncia(content):
    entries = []
    page = BeautifulSoup(content, 'html.parser')
    res_section = page.find('div', class_='AjaxContainer')
    for e in res_section.find_all('article'):
        ref_id = e.find('span')['data-reference']
        url = 'https://fr.foncia.com' + e.find('a')['href']
        write = True
        with open('foncia-panam', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == ref_id:
                    write = False
        if write:
            # send_mail(url, 'foncia')
            entries.append({'id': ref_id, 'url': url})

    with open('foncia-panam', 'a+') as file:
        file.writelines((json.dumps(l) + '\n' for l in entries))

    return entries


def parse_bienici(content):
    entries = []
    # page = BeautifulSoup(content, 'html.parser')
    # print(page)
    # res_section = page.find('section', class_='photos')
    # print(res_section)
    # for e in res_section.find_all('li'):
    #     infos = json.loads(e.find('a')['data-info'].encode('utf-8'))
    #     url = e.find('a')['href']
    #     write = True
    #     with open('leboncoin', 'r') as file:
    #         for line in file:
    #             l = json.loads(line)
    #             if l['id'] == infos['ad_listid']:
    #                 write = False
    #     if write:

    #         entries.append({'id': infos['ad_listid'], 'url': url})

    # with open('leboncoin', 'a+') as file:
    #     file.writelines((json.dumps(l) + '\n' for l in entries))

    return entries

def parse_logicimmo(content):
    entries = []
    page = BeautifulSoup(content, 'html.parser')
    res_section = page.find('div', class_='row offer-list-row')
    for e in res_section.find_all('div', itemtype='http://schema.org/ApartmentComplex'):
        ref_id = e.find('button')['data-offerid']
        url = e.find('p', class_='offer-type').find('a')['href']
        write = True
        with open('logicimmo-panam', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == ref_id:
                    write = False
        if write:
            # send_mail(url, 'logicimmo')
            entries.append({'id': ref_id, 'url': url})

    with open('logicimmo-panam', 'a+') as file:
        file.writelines((json.dumps(l) + '\n' for l in entries))

    return entries


def get_content(url):
    """."""
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'}
    r = requests.get(url, headers=headers)

    return r.text


def run():
    """."""
    for name, url in urls.items():
        entries = globals()['parse_%s' % name](get_content(url))

        # print(entries)


if __name__ == '__main__':
    run()