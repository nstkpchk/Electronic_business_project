# Projekt - Sklep Internetowy

## Informacje o projekcie

Projekt sklepu internetowego opartego na platformie PrestaShop 1.7.8.x, realizowany w ramach przedmiotu Biznes elektroniczny.

## Wykorzystane oprogramowanie
- PrestaShop **1.7.8.x**
- PHP **8.3.26**
- MariaDB **12.1.2**
- Apache **2.4.65**
- phpMyAdmin **5.2.3**
- Docker (środowisko uruchomieniowe aplikacji)

## Sposób uruchomienia
1. Upewnij się, że masz zainstalowanego Dockera i Docker Compose.
2. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/nstkpchk/Electronic_business_project.git
   cd Electronic_business_project/
   ```
3.Uruchom kontenery Dockera:
   ```bash
   docker compose up -d
  ```
4.Poczekaj, aż kontenery się uruchomią.
Można też zobaczyć logi kontenera prestashop
   ```bash
   docker compose logs -f prestashop
  ```
5.Otwórz przeglądarkę i wpisz adres:
   ```bash
   https://localhost:8002
  ```


## Zespół
* Anastasia Kupchik
* Klim Kaliasniou
* Raman Kupreichyk
