

---
# Vektor App-Backend
Opis projektu:

Jest to backend dla różnych usług napisany w pythonie. Głównie służy jako Master Server dla listy serwerów gier sieciowych. Projekt udostępnia prosty interfejs do: 
- Dodawania serwerów do list.
- wyświetlania podstawowych jak i również detalicznych informacji dotyczące serwera, który znajduje się na liście.
- blokowania, oraz usuwania wybranego serwera z listy.

Dodatkową funkcjonalnością jest udostępniony backend do zarządzania treścia dla strony internetowej sekcji naukowej. Są dostępne specjalne "Routy", które umożliwiają manipulacje treścią, logowaniem i wylogowaniem użytkowników, jak i również zbieraniem ilości członków, którzy należą do koła naukowego.
___
**Użyte technologie:**

Wszystko to głównie napędza biblioteka Flask, dla środowiska Python. Służy on do obłsugi zapytań HTTP dla poszczególnych dostępnych usług w Backendzie. Discord.py służy do zbierania ilości członków koła naukowego(Każdy członek koła, musi być na komunikatorze Discord).
Jako serwer bazo-danowy używana jest technologia "Realtime database" od Firebase'a.
