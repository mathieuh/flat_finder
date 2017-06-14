"""."""
import sys
import os
import argparse
import requests
import json
import smtplib

from bs4 import BeautifulSoup

urls = {
    'seloger': 'http://www.seloger.com/list.htm?idtt=2&naturebien=1,2,4&idtypebien=1,2&ci=330063&tri=d_dt_crea&pxmin=250000&pxmax=450000&surfacemin=80&si_terrasse=1&nb_balconsmin=1',
    #'pap': 'http://www.pap.fr/annonce/vente-appartement-maison-bordeaux-33-g43588-entre-250000-et-450000-euros-a-partir-de-80-m2',
    'leboncoin': 'https://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?th=1&location=Bordeaux%2033000&parrot=0&ps=10&pe=16&sqs=9&ret=1&ret=2',
    'foncia': 'https://fr.foncia.com/achat/bordeaux-33/appartement--maison/(params)/on/(surface_min)/80/(prix_min)/250000/(prix_max)/450000/(balcon)/1',
}


def send_mail(message, site):
    gmail_user = 'newappartmentfound@gmail.com'
    gmail_password = 'hUn-spf-sRF-Z88'

    from_ = gmail_user
    to = ['first@email.fr','second@email.com']
    subject = 'Nouvelle annonce sur ' + site
    body = 'Hey,\n\nVoici un nouveau bien qui correspond a votre recherche :\n' + message + '\n\n- Flat Finder'

    email_text = 'Subject: {}\n\n{}'.format(subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(from_, to, email_text)
        server.close()
        return True
    except:
        return False


def parse_seloger(content):
    entries = []
    page = BeautifulSoup(content, 'html.parser')
    res_section = page.find('section', class_='liste_resultat')
    for e in res_section.find_all('article'):
        ref_id = e['data-listing-id']
        url = e.find('a', class_='listing_link')['href']
        write = True
        with open('seloger', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == ref_id:
                    write = False
        if write:
            sent = send_mail(url, 'seloger')
            if sent:
                entries.append({'id': ref_id, 'url': url})

    with open('seloger', 'a+') as file:
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
        with open('pap', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == ref_id:
                    write = False
        if write:
            sent = send_mail(url, 'pap')
            if sent:
                entries.append({'id': ref_id, 'url': url})

    with open('pap', 'a+') as file:
        file.writelines((json.dumps(l) + '\n' for l in entries))

    return entries


def parse_leboncoin(content):
    entries = []
    page = BeautifulSoup(content, 'html.parser')
    res_section = page.find('section', class_='tabsContent')
    for e in res_section.find_all('li'):
        infos = json.loads(e.find('a')['data-info'].encode('utf-8'))
        url = 'https:' + e.find('a')['href']
        write = True
        with open('leboncoin', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == infos['ad_listid']:
                    write = False
        if write:
            sent = send_mail(url, 'leboncoin')
            if sent:
                entries.append({'id': infos['ad_listid'], 'url': url})

    with open('leboncoin', 'a+') as file:
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
        with open('foncia', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == ref_id:
                    write = False
        if write:
            sent = send_mail(url, 'foncia')
            if sent:
                entries.append({'id': ref_id, 'url': url})

    with open('foncia', 'a+') as file:
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
        with open('logicimmo', 'r') as file:
            for line in file:
                l = json.loads(line)
                if l['id'] == ref_id:
                    write = False
        if write:
            sent = send_mail(url, 'logicimmo')
            if sent:
                entries.append({'id': ref_id, 'url': url})

    with open('logicimmo', 'a+') as file:
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
