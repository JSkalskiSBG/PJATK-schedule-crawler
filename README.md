# PJATK Schedule Crawler
Crawler zbierający pełne dane z Planu Zajęć PJATK ( https://planzajec.pjwstk.edu.pl/PlanOgolny.aspx ) z najbliższych 30 dni.
Dane są wyświetlane w formacie JSON. Skanowanie 30 dni zajmuje około 2 godzin (ze względu na wydajność serwerów PJATK).
Program kończy działanie po wczytaniu 30 dni lub jeśli strona z planem zawiera błędy (podczas testów 31 maja tabela była pusta!) 

Zebrane dane są prezentowane w formie tabeli na stronie WWW.
Do tabeli jest podpięte DataTables które pozwala na przeszukiwanie pełnotekstowe i SZYBKIE ODNALEZIENIE WYKŁADOWCY.

Program został napisany w Pythonie 3 z wykorzystaniem Selenium.
Domyślnie skonfigurowany dla Linuxa z Chromium + ChromeDriver.

## Instalacja
#### Na Debian 9
Wgrać do folderu serwera WWW pliki aplikacji.
W przykładzie będzie to folder **/var/www/html**, a użytkownik w systemie będzie nazywał się **testowy**

##### Crawler
Nie wymaga środowiska graficznego.
Na użytkowniku **root**:
```
apt install chromedriver python3 python3-pip python3-selenium
chown -R testowy /var/www/html/crawler
```
Na użytkowniku **testowy** (wymagane Selenium w wersji ^3.0):
```
pip3 install selenium
```
Odpalanie:
```
python3 crawler.py > data.json
```
Wpis do CRONa aktualizujący dane o 2 w nocy:
```
0 2 * * * /usr/bin/python3 /var/www/html/crawler/crawler.py > /var/www/html/crawler/data.json
```
##### Strona WWW
Serwer WWW z obsługą PHP w wersji 5 lub wyższej.

Link do strony z planem którą hostuję jest na http://skalski.pro/