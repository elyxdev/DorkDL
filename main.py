from colorama import Fore, init
from bs4 import BeautifulSoup
import requests
import os

def jilog(text):
    print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}+{Fore.LIGHTGREEN_EX}] {Fore.RESET}{text}")

class PdfDownloader:
    def __init__(self, valor, pages, ext):
        self.valor = valor
        self.pages = pages
        self.urls = []
        self.ext = ext

    def get_urls(self):
        for x in range(self.pages):
            url = "https://www.google.com/search?q={}+filetype:{}&start={}".format(self.valor.replace(" ", "+"), self.ext, x)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a")
            for link in links:
                href = link.get("href", "")
                if href.startswith("/url?q=") and href.split("&sa")[0].lower().endswith(f".{self.ext}"):
                    pdf_url = href[7:].split("&")[0]
                    self.urls.append(pdf_url)

    def descargar(self):
        jilog("Archivos a descargar: {}".format(len(self.urls)))
        for url in self.urls:
            file_name = url.split("/")[-1]
            file_path = "downloads/{}/{}".format(self.valor, file_name)
            if os.path.isfile(file_path):
                jilog("El archivo {} ya existe".format(file_name))
            else:
                try:
                    jilog("Descargando: {}".format(file_name))
                    response = requests.get(url)
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                except:
                    jilog("Error al descargar: {}".format(file_name))
                    pass

    def create_directory(self, directory):
        try:
            os.makedirs(directory)
            jilog("Se ha creado el directorio: {}".format(directory))
        except:
            jilog("La creación del directorio {} falló".format(directory))

def main():
    os.system("cls" if os.name == "nt" else "clear")
    argsname = input(f"{Fore.LIGHTGREEN_EX}Nombre a descargar > {Fore.RESET}")
    argspages = int(input(f"{Fore.LIGHTGREEN_EX}# Páginas a buscar > {Fore.RESET}"))
    exte = str(input(f"{Fore.LIGHTGREEN_EX}# Extension (pdf) > {Fore.RESET}"))
    pdf = PdfDownloader(argsname, argspages, exte)
    print()
    directory = "downloads/{}".format(argsname)
    if not os.path.isdir(directory):
        pdf.create_directory(directory)
    pdf.get_urls()
    pdf.descargar()
    jilog("Terminado!")


if __name__ == "__main__":
    try:
        init()
        main()
    except Exception as e:
        print()
        jilog("Cerrando programa...")
        os._exit(0)
