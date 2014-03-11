__author__ = 'maximk'

from Bio import Entrez
from ftplib import FTP

Entrez.email = 'kuleshov.max.v@gmail.com'

def cel(ftp_adress):
    """
    Проверяет наличие CEL-файлов
    """
    cel_pres = '-'
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login()
    ftp.cwd(ftp_adress[26:])
    files_list = ftp.mlsd()
    if 'suppl' in files_list:
        ftp.cwd('suppl')
    files_list = ftp.mlsd()
    if 'filelist.txt' in files_list:
        ftp.retrbinary('RETR filelist.txt', open('filelist.txt', 'wb').write)

    filelist = open('/home/maximk/PycharmProjects/heroscope/filelist.txt', 'r').read()
    for line in filelist.split(sep='\n'):
        if 'CEL' in line:
            cel_pres = '+'
            ftp.quit()
            return cel_pres
    ftp.quit()
    return cel_pres

def platform(gpl):
    """
    Возвращает название платформы
    """
    platforms = []
    gpl_id = '1' + (8-len(str(gpl)))*'0' + str(gpl)
    handle = Entrez.esummary(db="gds", id=gpl_id)
    summary = Entrez.read(handle)
    platforms.append(summary[0]['title'])
    return platforms

def check_presence(drug_name, title, summary):
    """
    Проверяет, на самом ли деле в названии или описании эксперимента говорится о заданном лекарстве
    """
    check = False
    if (drug_name in title)and(drug_name in summary):
        check = True
    return check

def retrieve_record(query):
    """
    Возвращает выбранные параметры для всех записией по данному запросу
    """
    drug_name = 'morphine'
    pattern = '((expression profiling by array[DataSet Type])OR(expression profiling by high throughput sequencing[DataSet Type]))AND(gse[Filter])AND((%s[Description])OR(%s[Title]))AND(homo sapiens[Organism])' % (drug_name, drug_name)
    handle = Entrez.esearch(db='gds', retmax=200, term=pattern)
    record = Entrez.read(handle)
    for geo_id in record['IdList']:
            handle = Entrez.esummary(db='gds', id=geo_id)
            summary = Entrez.read(handle)
            if check_presence(drug_name, summary[0]['title'], summary[0]['summary']):
                cel_presence = cel(summary[0]['FTPLink'])
                for c in str(summary[0]['GPL']).split(sep = ';'):
                    #print('GEO Series ID: %s\nName: %s\nSamples: %s\nCEL files: %s\nGEO Platform ID: GPL%s\nPlatform: %s' % (summary[0]['Accession'], summary[0]['title'], len(summary[0]['Samples']), cel_presence, c, ','.join(platform(c))))
                    print('%s;%s;%s;%s;GPL%s;%s' % (summary[0]['Accession'], summary[0]['title'], len(summary[0]['Samples']), cel_presence, c, ','.join(platform(c))))
                    #print()

    return None

retrieve_record('')
#cel('ftp.debian.org')