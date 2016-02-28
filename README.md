# Zadania_okresowe
Do Raspberry  Pi został podłączony cyfrowy czujnik temperatury oraz wilgotności (DHT11). Temperatura jest odczytywana za pomocą gotowego programu udostępnionego przez producenta czujnika. W uzyskanym programie należało tylko odpowiednio zainicjalizować zmienne. Użyty czujnik jest dosyć wolny, więc  program zawraca wartość średnio po pięciu próbach, aby mieć pewność, że będą dodawane do bazy poprawne wartości napisałem program, który sprawdza odpowiedź programu pobierającego dane z czujnika. Jeżeli odpowiedź jest prawidłowa dopiero wtedy doda wartość do bazy danych w przeciwnym wypadku będzie się wywoływał tyle razy ile to konieczne.

Test.py – program producenta czujnika Adafruit DHT11 umożliwiający odczyt z czujnika.
Test1.py- Program sprawdzający poprawność odpowiedzi programu test.py oraz dodający wartości do bazy danych. 

Program test.py jest wywoływany przez program test1.py.

Następnie został ustawiony Cron, aby uruchamiał program co 10 minut.
*/10 * * * * sudo python /home/pi/libraries/Adafruit-Raspberry-Pi-Python-Code/Adafruit_DHT_Driver/test1.py > /dev/null 2>&1
