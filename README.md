# projekt-grupa-plg-bartektroszka

Plik func.py zawiera definicje funkcji API.

Plik main.py zawiera parser wczytujący polecenia i wywołujący funkcje.

Plik init.sql zawiera konfigurację bazy danych oraz inicjalizację tabel i indexów przy pierwszym uruchomieniu.

Program powinien zostać uruchomiony z wiersza poleceń z parametrem --init: 
python3 main.py --init

Polecenie:

Napisz system ułatwiający prowadzenie firmy organizującej wycieczki rowerowe. Firma obsługuje wiele punktów, w których zaczynają się i kończą etapy poszczególnych wycieczek. Pomiędzy punktami klienci podróżują na własną rękę. Trasa wycieczki to lista punktów pomiędzy jej etapami. Każda wycieczka rozpoczyna się pierwszego dnia rano w pierwszym punkcie trasy. Następnie klient ma cały dzień na dojechanie do kolejnego punktu trasy, w pobliżu którego spędza noc. Rano następnego dnia rozpoczyna w tym samym punkcie kolejny etap i tak aż dojedzie do ostatniego punktu trasy. Uwaga - trasa nie obejmuje punktów przez które klient być może przejeżdża w trakcie etapu ale tam nie nocuje. Wszystkie trasy są skatalogowane. Klienci mają zawsze cały dzień na przejechanie jednego etapu więc rezerwując wycieczkę podaje się datę jej rozpoczęcia oraz wersję trasy z katalogu.

Funkcje API
node

node <node> <lat> <lon> <description>

Dodaj nowy punkt z identyfikatorem <node>, ulokowany w miejscu o współrzędnych <lat>, <lon>. Wartość <description> to tekstowy opis dla klienta

// nie zwraca krotek,
catalog

catalog <version> <nodes>

Dodaje nową standardową wycieczkę o (unikalnym) numerze <version>, <nodes> to tablica zawierająca identyfikatory kolejnych punktów na trasie wycieczki (tj. identyfikatory <node>). Załóż, że wszystkie te punkty zostały wcześniej dodane wywołaniami funkcji node. Każda wycieczka składa się z co najmniej 2 punktów (niekoniecznie różnych).

// nie zwraca krotek

trip

trip <cyclist> <date> <version> 

Rezerwacja nowej wycieczki dla klienta <cyclist>, <date> to data dnia, w której wycieczka się rozpoczyna w pierwszym punkcie trasy, każdy kolejny punkt na trasie to kolejny dzień wycieczki, <version> to numer wycieczki z katalogu,

<cyclist> może być nowym klientem lub jednym z dotychczasowych klientów.

Atrybuty zwracanej krotek

// nie zwraca krotek

closest_nodes

closest_nodes <ilat> <ilon>

Znajdź i zwróć dane 3 punktów położonych najbliżej współrzędnych <ilat> <ilon> - dla każdego z tych 3 punktów zwróć identyfikator <node>, jego współprzędne <olat>, <olon> oraz odległość <distance>. W przypadku gdy liczba punktów w bazie jest mniejsza niż 3 to zwróć wszystkie te punkty. Wynik posortuj rosnąco wg <distance>, w drugiej kolejności rosnąco wg <node>.

// <node> <olat> <olon> <distance>

party

party <icyclist> <date>

Znajdź i zwróć listę rowerzystów (różnych od <icyclist>) nocujących w promieniu 20 km od miejsca nocowania klienta <icyclist> w dniu <date>. Jeśli <icyclist> nie bierze w dniu <date> udziału w wycieczce to zwróć pusty wynik. Dla każdego rowerzysty podaj jego id <ocyclist>, id <node> punktu, w którym nocuje oraz odległość <distance> pomiędzy tym punktem, a miejscem nocowania rowerzysty <icyclist>. Wyniki posortuj rosnąco wg <distance>, w drugiej kolejności rosnąco wg <ocyclist>.

// <ocyclist> <node> <distance>

guests

guests <node> <date>

Dla punktu <node> zwróć listę rowerzystów <cyclist>, którzy bedą w nim nocować w dniu <date>. Załóż, że <node> jest w bazie. Wyniki posortuj rosnąco wg <cyclist>.

// <cyclist>

cyclists

cyclists <limit>

Zwróć ranking rowerzystów - wynik ogranicz do pierwszych <limit> krotek. Dla każdego rowerzysty <cyclist> zwróć ile do tej pory zarezerwował wycieczek <no_trips> oraz ile (co najmniej) kilometrów obejmowały łącznie te wycieczki <distance> (zsumuj odległości po linii prostej pomiędzy etapami, nie przejmuj się ew. błędem gdy jakiś punkt na trasie powtarza się). Wyniki posortuj rosnąco wg <distance>, w drugiej kolejności rosnąco wg <cyclist>.

// <cyclist> <no_trips> <distance>
