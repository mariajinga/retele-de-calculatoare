♡ 𝓟𝓡𝓞𝓘𝓔𝓒𝓣  𝓡𝓔𝓣𝓔𝓛𝓔  𝓓𝓔  𝓒𝓐𝓛𝓒𝓤𝓛𝓐𝓣𝓞𝓐𝓡𝓔 - 𝓒𝓞𝓓𝓔 𝓑𝓐𝓑𝓔𝓢 ♡

Cerinte proiect retele de calculatoare - echipa Code Babes

Proiectul va consta intr-o aplicatie client - server pe socket-uri sau cu apel de metode la distanta, 
implementata intr-un limbaj la alegere (C#, Java, C++/C, etc.), putand fi realizat individual sau in echipa de maxim trei persoane, 
si va fi prezentat pe calculator in ultima activitate de seminar, pe o tema aleasa din lista de mai jos:

21.	Distribuirea procesarii:
o	Server-ul asculta pachetele venite pe adresa de loopback a subretelei pe un anumit port si tine o lista cu toti clientii activi;

o	Clientii cand pornesc trimit un pachet pe adresa de loopback si portul pe care asculta server-ul prin care se inregistreaza in lista clientilor activi;

o	Fiecare aplicatie client deschide un port pe care asteapta cereri de procesare, la inregistrarea cu server-ul comunicandu-i acest port;

o	Inainte de inchidere, aplicatia client trimite un mesaj pe adresa de loopback si portul pe care asculta server-ul pentru stergerea clientului din lista clientilor activi;

o	Server-ul asculta pe un port cereri de procesare de la clienti care constau in executia unui task custom furnizat la momentul cererii impreuna cu argumentele de apel, rezultatul executiei intors de server clientului constand in exit code-ul executiei task-ului;

o	La primirea unui task de procesare, server-ul alege urmatorul client de procesare la rand, ii trimite pe portul de procesare codul binar al task-ului si argumentele de apel, clientul de procesare lansand in executie task-ul primit in local cu argumentele date, intorcand dupa terminarea executiei exit code-ul procesului care a rulat task-ul, care este apoi trimit de server clientului ce a solicitat excutia task-ului respectiv.
