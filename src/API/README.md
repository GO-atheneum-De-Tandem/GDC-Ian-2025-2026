# Source Code API
Hier in deze folder kan je alle source code van de API terug vinden. Dit zal de meest actieve folder zijn waar het meest in zal gewerkt worden.

## Deployment Docker Container

De API is opgezet om te draaien in een Docker container. Om de container te bouwen en te starten, volg je de onderstaande stappen:

1. Zorg ervoor dat Docker is geïnstalleerd op je machine.

2. Zorg ervoor dat je een PostgreSQL database hebt, lokaal of remote, de API maakt hier verbinding mee.  
Zorg ervoor dat de database de juiste layout heeft zoals beschreven in de documentatie.  
Zie `src/DB/structure/dbdiagram.dmbl` & `src/DB/structure/structure_postgre.sql` voor de layout.  
Je zult de credentials later moeten invullen in de environment variables van de Docker container.

3. Kies voor de versie unsafe of safe.
4. Upload de volledige folder van de gekozen versie. Zowel de docker files, requirements.txt als de app folder.
5. Navigeer in de terminal naar de directory waar de bestanden zijn geüpload. Zorg dat je in deze directory blijft voor de volgende stappen.
6. Voer eventuele aanpassingen uit in het Dockerfile & compose file indien nodig.

7. Er worden geen aantal workers meegestuurd in de Dockerfile, je kan deze zelf toevoegen afhankelijk van je server capaciteit.  
   Pas de `CMD` regel aan in het Dockerfile, bijvoorbeeld:
   ```Dockerfile
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--http", "httptools", "--workers", "4"]
   ```

8. Maak een `.env` bestand aan in dezelfde directory als het Dockerfile & compose file.  
Vul hierin de volgende environment variables in met de juiste waarden:
   ```env
   DB_HOST=your_database_host
   DB_PORT=your_database_port
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   ```

8. Voer het volgende commando uit om de Docker image te bouwen & Docker container te bouwen:  
Zorg ervoor dat je in de directory bent waar het Dockerfile & compose file zich bevindt.
   ```bash
   docker compose up --build -d
   ```

9. Voor het herbouwen van de container na aanpassingen, voer je het volgende commando uit:
   ```bash
   docker compose build
   ```