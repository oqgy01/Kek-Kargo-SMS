#Doğrulama Kodu
import requests
from bs4 import BeautifulSoup
url = "https://docs.google.com/spreadsheets/d/1AP9EFAOthh5gsHjBCDHoUMhpef4MSxYg6wBN0ndTcnA/edit#gid=0"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
first_cell = soup.find("td", {"class": "s2"}).text.strip()
if first_cell != "Aktif":
    exit()
first_cell = soup.find("td", {"class": "s1"}).text.strip()
print(first_cell)


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from colorama import init, Fore, Style


pd.options.mode.chained_assignment = None
init(autoreset=True)

print(" ")
print(Fore.BLUE + "Released 1.11.2023")

print(" ")
print("Oturum Açma Başarılı Oldu")
print(" /﹋\ ")
print("(҂`_´)")
print("<,︻╦╤─ ҉ - -")
print("/﹋\\")
print("(Kod Bekçisi)")
print("Mustafa ARI")
print(" ")





# Kullanıcı adı ve şifre
username = "mustafa_kod@haydigiy.com"
password = "123456"

# Oturum açılacak web sitesi
login_url = "https://task.haydigiy.com/kullanici-giris/?ReturnUrl=%2Fadmin"

# İstek başlıkları
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Referer": "https://task.haydigiy.com/",
}

# Oturum açma işlemi
session = requests.Session()
response = session.get(login_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
token = soup.find("input", {"name": "__RequestVerificationToken"}).get("value")
login_data = {
    "EmailOrPhone": username,
    "Password": password,
    "__RequestVerificationToken": token,
}
response = session.post(login_url, data=login_data, headers=headers)

# Veriyi indir
url = "https://task.haydigiy.com/FaprikaOrderXls/9YNS3K/1/"
df = pd.read_excel(url)

# İstenen sütunları seç
istenen_sutunlar = ["Id", "KargoFirmasi", "KargoTarihi", "TeslimatAdiSoyadi", "TeslimatTelefon"]
df = df[istenen_sutunlar]

# "KargoTarihi" sütunundaki boşluktan sonrasını temizle
df["KargoTarihi"] = df["KargoTarihi"].str.split().str[0]

# KargoTarihi sütununu tarih formatına çevir
df["KargoTarihi"] = pd.to_datetime(df["KargoTarihi"], format="%d.%m.%Y")

# Bugünün tarihini al
bugun = datetime.now().date()

# Son 5 günü hesapla
son5gun = bugun - timedelta(days=5)

# Tarihi son 5 günden önce olan satırları sil
df = df[df["KargoTarihi"].dt.date < son5gun]

# "KargoFirmasi" sütunundaki verileri küçük harfe çevirin ve boşlukları kaldırın
df["KargoFirmasi"] = df["KargoFirmasi"].str.lower().str.replace(" ", "")

# "KargoTarihi" sütununu sil
df = df.drop("KargoTarihi", axis=1)

df["Id"] = df["Id"].astype(str)  # df['Id'] sütununu string türüne dönüştür

# "KargoFirmasiLink" sütununu oluşturun
df["KargoFirmasiLink"] = "https://task.haydigiy.com/admin/" + df["KargoFirmasi"] + "/admintracking/?orderId=" + df["Id"] + "&btnId=btnRefreshPage&formId=order-form"

# "KargoFirmasi" sütununu sil
df = df.drop("KargoFirmasi", axis=1)

# Verileri Excel dosyasına kaydet
df.to_excel("mustafa.xlsx", index=False)

# Excel dosyasını okuma
df = pd.read_excel("mustafa.xlsx")

# Verileri saklamak için bir veri çerçevesi oluşturun
veriler = pd.DataFrame(columns=["KargoFirmasi", "Durum", "Tarih", "Aciklama"])

# "KargoFirmasiLink" sütunundaki linklere get istekleri gönderme ve verileri al
def get_kargo_data(link):
    try:
        response = session.get(link, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        kargo_firmasi = soup.find("td").text.strip()
        durum = soup.find_all("td")[1].text.strip()
        tarih = soup.find_all("td")[2].text.strip()
        aciklama = soup.find_all("td")[3].text.strip()
        return kargo_firmasi, durum, tarih, aciklama
    except AttributeError:
        return None, None, None, None

with ThreadPoolExecutor(max_workers=15) as executor:
    kargo_data_list = list(tqdm(executor.map(get_kargo_data, df["KargoFirmasiLink"]), total=len(df)))

# Verileri Excel dosyasına kaydet
veriler = pd.DataFrame(kargo_data_list, columns=["KargoFirmasi", "Durum", "Tarih", "Aciklama"])
veriler.to_excel("veriler.xlsx", index=False)

# "mustafa.xlsx" ve "veriler.xlsx" dosyalarını oku
df_mustafa = pd.read_excel("mustafa.xlsx")
df_veriler = pd.read_excel("veriler.xlsx")

# İki veri çerçevesini sütunlar yan yana birleştir
birlesik_df = pd.concat([df_mustafa, df_veriler], axis=1)


# Sonucu yeni bir Excel dosyasına kaydet
birlesik_df.to_excel("Kek Kargo SMS.xlsx", index=False)

import os
# "mustafa.xlsx" ve "veriler.xlsx" dosyalarını sil
os.remove("mustafa.xlsx")
os.remove("veriler.xlsx")