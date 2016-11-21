# -*- coding: utf-8 -*-

import os
import shutil
from subprocess import Popen
import sys
import zipfile

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from nsis import NsisScript


def statusbar(current, total):
    step = total / 20.0
    sys.stdout.write("\r[%-20s] %3.2f%%" % (
        '=' * int(current / step),
        current * 100.0 / total
    ))
    sys.stdout.flush()


def copyfileobj(fsrc, fdst, callback=None, length=16*1024):
    copied = 0

    while True:
        chunk = fsrc.read(length)

        if not chunk:
            break

        fdst.write(chunk)
        copied += len(chunk)

        if callback:
            callback(copied)


def download_file(url, dest=None):
    if dest and not os.path.exists(dest):
        os.makedirs(dest)

    filename = os.path.abspath(os.path.join(dest or '', os.path.basename(url)))
    response = urlopen(url)
    info = response.info()
    total = int(info.get('Content-Length'))

    if os.path.exists(filename) and (os.path.getsize(filename) == total):
        return filename

    with open(filename, 'wb') as out_file:
        copyfileobj(response, out_file)
        return filename


def extract_file(filename, dest=None):
    name, ext = os.path.splitext(os.path.basename(filename))

    if not dest:
        dest = os.getcwd()

    if ext == '.zip':
        with zipfile.ZipFile(filename) as z:
            z.extractall(dest)
            return z.namelist()

    if ext == '.tar.gz':
        return


files = extract_file(
    download_file('https://nssm.cc/release/nssm-2.24.zip'), 'for_copy'
)
nssm = files[0].strip('/')

files = extract_file(
    download_file('http://nginx.org/download/nginx-1.11.6.zip'), 'for_copy'
)
filename = files[0].strip('/')


LANG_RUSSIAN = 'LANG_RUSSIAN'

script = NsisScript(template='installer.nsi')


section = script.add_section(nssm, template='install/nssm.nsi')
section.add_description(u'The Non-Sucking Service Manager')
section.add_description(u'Сервис-менеджер', lang=LANG_RUSSIAN)


section = script.add_section(filename, template='install/nginx.nsis')
section.add_description(u'HTTP and reverse proxy server')
section.add_description(u'HTTP-сервер и обратный прокси-сервер', lang=LANG_RUSSIAN)


section = script.add_uninstall_section(filename, template='uninstall/nginx.nsi')
section = script.add_uninstall_section(nssm, template='uninstall/nssm.nsi')

script.update_context({
    'APP_NAME': u'dev-workflow',
    'APP_TITLE': u'DevWorkflow',
    'APP_VERSION': u'1.0.0.0',
    'ICON': u'resources/favicon.ico',
    'MUI_HEADERIMAGE_BITMAP': u'',
    'COMPANY': u'ЦДПО НИУ ИТМО',
    'COPYRIGHT': u'profi.ifmo.ru',
    'DESCRIPTION': u'The developer workflow installer',
    'APP_WEB_SITE': 'http://profi.ifmo.ru',
    'NSSMDIR': nssm,
    'NGINXDIR': filename,
})

script.generate(u'script.nsis')
Popen(['makensis', 'script.nsis'])
