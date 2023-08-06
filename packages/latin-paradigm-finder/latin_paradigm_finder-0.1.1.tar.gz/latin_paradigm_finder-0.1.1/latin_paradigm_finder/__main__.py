print('Caricamento del programma...')

# ----------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------


import aiohttp
import asyncio
import sys
from base64 import b64encode
from pathlib import Path
from re import sub
from shutil import rmtree
from time import sleep
import clipboard
import hickle as hkl
import questionary
from bs4 import BeautifulSoup as bs
from termcolor import colored, cprint
from unidecode import unidecode as undcd
from os.path import isdir,join
from os import listdir
from pathvalidate import sanitize_filename

# ----------------------------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------------------------


urllist = []
home_path = Path.home()
temp_html_path = home_path.joinpath('.temp-html')
temp_html_path.mkdir(parents=True, exist_ok=True)
npar = 0
done = 0
db_path = home_path.joinpath('.db-latino')
db_path.mkdir(parents=True, exist_ok=True)
baseurl = 'https://www.dizionario-latino.com/'
################# CARICA PAGINE HTML ###############

# Liste permanenti poi salvate come file .hkl, in questo caso temporanee per la sessione

url_list = []  # Lista di tutti gli indirizzi web controllati
tipo_list = []  # Lista di tutti i tipi di parole controllati
paradigma_list = []  # Lista di tutti i paradigmi controllati

# Queste tre liste devono riferirsi agli stessi elementi.
# So che probabilmente c'è una via molto migliore, ma ne sono uscito con questa.
# Ciò vuol dire che la parola url_list[0] ha il suo tipo in tipo_list[0] e il suo paradigma in paradigma_list[0]

# Liste solo per la sessione temporanea

to_download = []  # URL delle parole scelte per la disambiguazione
paradigmi = []  # latin_paradigm_finder analizzati in questa sezione
parole = []  # Parole. Deve essere collegata agli indici di url_list e quelle altre.


# ----------------------------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------------------------

def list_dir(path,filterhidden=False): # List all files in a folder, if filterhidden=True don't list already saved files

    if filterhidden:
        folders = list(filter(lambda x: isdir(join(path, x)), listdir(path)))
        return [x for x in folders if x[0] != '.']
    else:
        return list(filter(lambda x: isdir(join(path, x)), listdir(path)))

def select_path(tmp_path): # Select a path to save a file
    save_path = ''
    while save_path != 'Salva qui il file':
        prev_path = tmp_path
        folders_list = list_dir(tmp_path,filterhidden=True)
        final_list = ['Salva qui il file'] + folders_list
        save_path = questionary.select(message=f'Scegli dove salvare il file contenente i paradigmi. Percorso corrente: {tmp_path}',choices=final_list,instruction='Usa i tasti freccia sopra e freccia sotto per selezionare una risposta. Quando il percorso è OK seleziona \' Salva qui il file \'.').ask()
        tmp_path = prev_path.joinpath(save_path)
    print('Percorso dove salverò il file: ' + colored(prev_path,'red'))
    default_name = questionary.confirm("Salvare con nome 'paradigmi.txt'?").ask()
    if default_name:
        return prev_path.joinpath('paradigmi.txt')
    else:
        path = questionary.text("Inserisci il nome del file",default='paradigmi.txt').ask()
        sanitized_path = sanitize_filename(path)
        print(path,sanitized_path)
        if path != sanitized_path:
            print('Il nome ' + colored(path,'red') + ' non è valido ed è stato automaticamente corretto con ' + colored(sanitized_path,'green'))
        return prev_path.joinpath(sanitized_path)

def filter_versione(text):  # Filter a text, leave only words; replace accents and remove text in brackets.
    text = " ".join(text.split())
    text = text.replace('\n', '').replace('.', ' ').replace(',', ' ').replace('«', '').replace('»', '')
    text = sub("[\(\[].*?[\)\]]", "", text)
    text = "".join(c for c in text if c.isalpha() or c == " ").split()
    return text


def return_index_of_duplicates(*nomilista):  # This function returns the index of duplicates in one or more lists
    uniquelist = []
    index2del = []
    lr = []
    for lista in nomilista:
        lr += lista
    c = 0
    for i in lr:
        if i not in uniquelist:
            uniquelist.append(i)
        elif i in uniquelist:
            index2del.append(c)
        c += 1
    return index2del


def del_from_lists(indexes, *liste):  # This function deletes from one or more list elements based on their index
    for lista in liste:
        delete_offset = 0
        for indice in indexes:
            del lista[indice - delete_offset]
            delete_offset += 1


def db_load(nome):  # This function returns the value of a loaded list from the database, saved in .hkl format
    path = db_path / nome
    myfile = Path(path).absolute()
    if myfile.is_file():
        return hkl.load(myfile)
    elif not myfile.is_file():
        cprint('Il database non è presente sul disco', 'red')
        return []


def db_save(lista, nome,
            preserve=True):  # This function saves on the database a list, with the option to preserve or not the previous content ( append or overwrite )
    cprint('Salvando sul database', 'yellow', end=' ')
    cprint(nome, 'red')
    path = db_path / nome
    myfile = Path(path).absolute()
    if len(lista) > 0:
        if myfile.is_file() == True and preserve == True:
            try:
                listacaricata = hkl.load(myfile)
                lf = (lista + listacaricata)
                hkl.dump(lf, myfile)  # L' eliminazione dei duplicati avverrà su un' altra funzione
                cprint('salvato sul database senza alcun problema.', 'green')
            except Exception as e:
                print('È avvenuto un errore (', colored(e, "red"),
                      ') inaspettato nell\' aggiornamento del database.\n' + colored(
                          '\n\nCiò non è fonte di alcun problema per l\' utente finale, quindi prosegui pure nella ricerca di paradigmi.\n\n',
                          'red', 'on_white') + ' \n Se vuoi andare più a fondo puoi aprire una issue su GitHub.')
                hkl.dump(lista, myfile)
        elif myfile.is_file() == False or preserve == False:
            Path(myfile).touch()
            hkl.dump(lista, myfile)
            cprint('File', 'green', end=' ')
            cprint(nome, 'red', end=' ')
            cprint('salvato sul database senza alcun problema.', 'green')
    elif len(lista) < 1:
        cprint(
            'Non salverò un file vuoto. Se hai appena trovato i paradigmi di una versione e trovato questo errore, contattami a borto@tuta.io ',
            'red')

def standard_delete_duplicates():  # This is a bad function. It deletes duplicates from db, but names are hardcoded.
    # I know, I shouldn't hardcode names like this. If you have suggestions open a pull request
    listaurl = db_load('url_list')
    doppi = return_index_of_duplicates(listaurl)
    tipi = db_load('tipo_list')
    paradigmi = db_load('paradigma_list')
    print(f'Trovate {len(doppi)} entrate doppie nel database su {len(listaurl)} entrate totali.')
    if len(doppi) > 0:
        del_from_lists(doppi, tipi, paradigmi, listaurl)
        db_save(listaurl, 'url_list', preserve=False)
        db_save(tipi, 'tipo_list', preserve=False)
        db_save(paradigmi, 'paradigma_list', preserve=False)


def progress(count, total, status=''):  # Print progress of doing a task
    bar_len = 32
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


async def task(name, work_queue):
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            global done, npar
            url = await work_queue.get()
            x = temp_html_path / b64encode(url.encode()).decode()
            if x.is_file() == False:
                async with session.get(url) as response:
                    html = await response.text()
                    with open(temp_html_path / b64encode(url.encode()).decode(), "w") as file:
                        file.write(html)
                    sleep(0.16)  # Sennò potrebbe parere un attacco DDoS
            done += 1
            progress(done, npar, status=(
                    colored('Scaricamento', 'yellow') + colored(f'  {done}', 'green') + colored(f' su {npar}', 'red')))


async def main(lista):
    # This is the main entry point for the webpage downloader
    # Create the queue of work
    work_queue = asyncio.Queue()
    # Put some work in the queue
    for url in lista:
        await work_queue.put(url)
    # Run the tasks
    await asyncio.gather(
        asyncio.create_task(task("One", work_queue)),
        asyncio.create_task(task("Two", work_queue)),
        asyncio.create_task(task("Three", work_queue)),
        asyncio.create_task(task("Four", work_queue)),
        asyncio.create_task(task("Five", work_queue)),
        asyncio.create_task(task("Six", work_queue)),
        asyncio.create_task(task("Seven", work_queue)),
        asyncio.create_task(task("Eight", work_queue))
    )


def download(lista):  # Dowload a list of urls asynchronously
    print('Caricata una lista di', len(lista), 'parole')
    global npar, done
    npar = len(lista)
    done = 0
    asyncio.run(main(lista))


def trova(url, parola=None):  # Analyze the HTML file of a Dizionario Latino Olivetti definition of a word
    global parole
    if parola is not None:
        parole.append(parola)
    else:
        parole = []
    try:
        global urllista, tipolista, paradigmalista
        i = urllista.index(url)
        if paradigmalista[i] != 0:
            cprint('DB |', 'blue', end=' ')
            cprint('Paradigma:', 'green', 'on_white', end=' ')
            cprint(paradigmalista[i], 'yellow', end=' | ')
            cprint('Tipo:', 'blue', end=' ')
            cprint(tipolista[i], 'yellow')
            paradigmi.append(paradigmalista[i])
        elif paradigmalista[i] == 0:
            cprint('DB |', 'blue', end=' ')
            cprint('La seguente parola non è un verbo', end='')
            if tipolista[i] != 0:
                cprint(', bensì un', end=' ')
                cprint(tipolista[i], 'yellow')
            elif tipolista[i] == 0:
                print('.')
    except:
        file_name = temp_html_path / b64encode(url.encode()).decode()
        with open(file_name, 'r') as file:
            html = file.read()
        soup = bs(html, 'lxml')
        grammatica = soup.find_all('span', {'class': 'grammatica'})  # [0].get_text()
        if "Si prega di controllare l'ortografia" in str(soup):
            cprint('Errore: Pagina non esistente', 'red', 'on_white')
            url_list.append(0)
            paradigma_list.append(0)
            tipo_list.append(0)
        elif len(
                grammatica) > 0:  # Questo significa che la pagina web è presente ed è quella di traduzione di una parola
            tipo = grammatica[0].get_text()
            paradigmal = soup.findAll('span', {"class": "paradigma"})
            if len(paradigmal) > 0 and ('verbo' in tipo or 'coniug' in tipo):
                paradigma = paradigmal[0].get_text()
                paradigma = undcd(paradigma.replace("[", "").replace("]", ""))
                cprint(f'Paradigma:', 'green', 'on_white', end=' ')
                cprint(paradigma, 'yellow')
                url_list.append(url)
                paradigma_list.append(paradigma)
                tipo_list.append(tipo)
                paradigmi.append(paradigma)
            elif len(paradigmal) > 0 and 'verbo' not in tipo and 'coniug' not in tipo:
                cprint(f'La seguente parola non è un verbo, bensì un {tipo}', 'white', 'on_grey')
                url_list.append(url)
                paradigma_list.append(0)
                tipo_list.append(tipo)
            else:
                tags = soup.find_all('td', {'width': '80%'})
                links, text = [], []
                for tag in tags:
                    if 'verbo' in str(tag) or 'coniug' in str(tag):
                        text.append('VERBO      | ' + tag.get_text())
                        links.append(baseurl + str(tag.find_all('a', href=True)[0]['href']))
                    else:
                        text.append('NO VERBO   | ' + tag.get_text())
                        links.append(None)

                if len(list(filter(None, links))) > 0:
                    cprint('-' * 30 + '\n', 'yellow')
                    if len(parole) > 6:
                        try:
                            cprint('CONTESTO PER ORIENTARSI, PAROLE FINO A', end=' ')
                            cprint(parole[-1].upper(), 'red')
                            cprint(" ".join(parole[-6:-1]), 'blue', 'on_white', end='  ')
                            cprint('  ' + parole[-1] + '  ', 'red', 'on_white', end='\n\n')
                        except Exception as e:
                            print('ERRORE IMPREVISTO:' + colored(e, 'red') + '\n' + colored(
                                'Ricorda che quest\' errore non crea nessun problema all\' utente finale! Puoi continuare a tradurre! Don\'t worry!',
                                'red', 'on_grey') + colored('\nSe ne sei capace, segnala una issue su GitHub\n',
                                                            'blue'))
                    x = questionary.select("Disambiguazione: scegli una possibile traduzione.", choices=text).ask()
                    indice = text.index(x)
                    traduzione = links[indice]
                    cprint('\n' + '-' * 30, 'yellow')
                    if traduzione is not None:
                        to_download.append(traduzione)
                else:
                    cprint(f'La seguente parola non può essere tradotta come verbo', 'white', 'on_grey')
                    url_list.append(url)
                    paradigma_list.append(0)
                    tipo_list.append(0)


# ----------------------------------------------------------------------------------------------
# Variables which need functions to be declared properly
# ----------------------------------------------------------------------------------------------


try:
    # Liste permanenti caricate per tutta la sessione che vengono aggiornate.
    urllista = db_load('url_list')
    tipolista = db_load('tipo_list')
    paradigmalista = db_load('paradigma_list')
except Exception as e:
    print(e)


# ----------------------------------------------------------------------------------------------
# Noob-like code
# ----------------------------------------------------------------------------------------------

def find():
    print('Caricamento completato')
    text = questionary.text("Incolla qui il testo della versione --> ").ask()
    parole = filter_versione(text)
    print(
        'Se analizzando le forme flesse potrai avere meno paradigmi falsi positivi però ci vorrà più tempo per scegliere le possibili traduzioni, siccome saranno di più.')
    cprint(
        'Esempio: senza le forme flesse la parola adverso viene considerata come verbo, invece analizzando le forme flesse si scopre che adverso potrebbe essere dativo e ablativo della parola adversus',
        'yellow')
    cprint(
        'TL;DR Con le forme flesse avrai più precisione nel rilevamento di falsi paradigmi, ma ciò necessiterà di maggior tempo e attenzione da parte tua.',
        'red', 'on_white')
    mdff = questionary.confirm("Vuoi analizzare le forme flesse di queste parole?").ask()
    cprint('Compilando la lista degli indirizzi web da controllare...', 'yellow')
    urllist = []
    if mdff:
        for i in parole: urllist.append(
            f"https://www.dizionario-latino.com/dizionario-latino-italiano.php?parola={i}&md=ff")
    elif not mdff:
        for i in parole: urllist.append(f"https://www.dizionario-latino.com/dizionario-latino-italiano.php?parola={i}")
    print('La lista è stata compilata.')
    try:
        urllista = db_load('url_list')
        listafinale = (set(urllist)) - set(urllista)
        percent = round(len(listafinale) * 100 / len(urllist), 1)
        if percent != 0:
            cprint(f'INFO: Il', 'yellow', end=' ')
            cprint(f'{100 - percent}%', 'red', end=' ')
            cprint('delle parole era già presente nel database, quindi non ha bisogno di essere scaricato di nuovo.',
                   'yellow')
        download(listafinale)
    except Exception as e:
        download(urllist)
    cprint('\nTutte le pagine web scaricate :)', 'green')
    c = 0
    for url in urllist:
        trova(url, parola=parole[c])
        c += 1
    db_save(url_list, 'url_list')
    db_save(tipo_list, 'tipo_list')
    db_save(paradigma_list, 'paradigma_list')
    cprint('Ho finito di analizzare tutti i paradigmi', 'green')
    if len(to_download) > 0:
        cprint('Scarico le pagine web dei verbi scelti durante la disambiguazione....')
        download(to_download)
        cprint('Aggiungo alla lista dei paradigmi i verbi scelti durante la disambiguazione....')
        parole = None
        for url in to_download:
            trova(url)
    db_save(url_list, 'url_list')
    db_save(tipo_list, 'tipo_list')
    db_save(paradigma_list, 'paradigma_list')
    rmtree(temp_html_path)
    print(f'Ho creato una lista di ben {len(paradigmi)} paradigmi!')
    paradigmifull = '\n\n'.join(paradigmi)
    c = questionary.confirm("Vuoi copiare negli appunti la lista dei paradigmi?").ask()
    if c:
        clipboard.copy(paradigmifull)
        cprint('I paradigmi sono stati copiati negli appunti! Puoi premere CTRL + V per incollarli!', 'green')
    c = questionary.confirm("Vuoi salvare in un file la lista dei paradigmi?").ask()
    if c:
        try:
            file = select_path(home_path)
            f = open(file, 'w')
            f.write(paradigmifull)
            f.close()
            cprint(f'Il file {file} è stato salvato!', 'green')
        except Exception as e:
            print('È avvenuto un errore inaspettato (', colored(e, "red"), ') ed il file contenente i paradigmi non è stato salvato.')
    sys.exit(0)
find()