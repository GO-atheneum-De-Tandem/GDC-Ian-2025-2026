# GDC-2025-2026
Onderzoek naar welke beveiligingsproblemen er kunnen voorkomen bij REST-API's en hun authenticatiesystemen, hoe deze problemen voorkomen kunnen worden en wat de gevaren zijn. Dit wordt onderzocht aan de hand van Python met FastAPI &amp; PostgreSQL.

## Onderzoeksvraag
Welke beveiligingsproblemen komen voor bij web- en REST-API’s en hun authenticatiesystemen, en hoe kunnen deze problemen worden voorkomen?

## Hypothese
Bij web- en REST-API’s komen beveiligingsproblemen zoals Cross-Site Scripting, Lack of Rate Limiting en Excessive Data Exposure voor. Hoe deze problemen voorkomen kunnen worden zal duidelijk worden na verder onderzoek.

## Welke Security Problemen zullen onderzocht worden
### Officieel voor GDC
> [!NOTE]
> De hieronder vermelde security problemen worden onderzocht en besproken voor de GDC. Documentatie is te vinden bij `/docs/Official/`

- XSS - Cross-Site Scripting
- CSRF - Cross-Site Request Forgery
- 

---
### Extra Onderzoek

> [!NOTE] 
> Extra onderzoek zal uitgevoerd worden naar andere, hieronder vermelde, security problemen voor eigen doeleinden en het vak Informaticawetenschappen.
> Deze onderwerpen komen niet aan bod in de GDC (paper of presentatie). Documentatie is te vinden onder `/docs/Extra/`
- Lack of Rate Limiting
- Misconfigured CORS - Cross-Origin Resource Sharing
- Insufficient Logging & Monitoring (malicious activities go unnoticed)

### Nog uit kiezen
- Injection Flaws
- IDOR - Insecure Direct Object Reference (Manipuleren input values)
- Excessive Data Exposure
- Trusting (Manipulated) client-side data

## Gebruikte Software
- [PostreSQL](https://www.postgresql.org/) - SQL Database
- [FastAPI](https://fastapi.tiangolo.com/) - Python API Framework
- [PyTest](https://docs.pytest.org/en/stable/) - Python Code Testing
- [PyLint](https://pypi.org/project/pylint/) - Python Code Checking
- [Postman](https://www.postman.com/) - API Testing & Collaboration Software
- [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload) - Pen Testing Software for HTTP Applications