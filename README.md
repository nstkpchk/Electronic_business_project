# ecommerce-store-project

## About the Project
An online store based on the PrestaShop platform, developed for the "Electronic Business" (Biznes elektroniczny) course. The project is implemented in two stages: local setup with data scraping, and automated cluster deployment.

## Tech Stack
- **PrestaShop** 1.7.8.x
- **MariaDB** 12.1.2
- **PHP** 8.3 / **Apache** 2.4
- **Docker & Docker Compose**
- **GitHub Actions** (CI/CD Pipeline)
- **Python & Selenium** (Scraping & Automated Testing)

---

## Stage 1: Local Development
This stage covers the base store setup, scraped data integration, and local testing. 

1. Clone the repository:
   ```bash
   git clone https://github.com/nstkpchk/ecommerce-store-project.git
   cd ecommerce-store-project/
   ```
2. Run the local environment (includes local MariaDB and phpMyAdmin):
   ```bash
   docker compose -f config/docker-compose.local.yml up -d
   ```
3. Check the logs to ensure the container is ready:
   ```bash
   docker compose logs -f prestashop
   ```
4. Access the store in your browser: **`https://localhost:8002`**

---

## Stage 2: Cluster Deployment & Automation
This stage introduces production-ready features tailored for the student cluster.

* **CI/CD Pipeline:** Any push to the `main` branch triggers a GitHub Actions workflow that automatically builds the Docker image and pushes it to Docker Hub.
* **Auto-Initialization:** The image contains a custom `init_db.sh` script that automatically waits for the cluster database, imports the SQL dump, and enforces performance caching settings.
* **Google Analytics:** Integrated tracking for custom events (e.g., promotional banner clicks and cart actions).

**To deploy on the cluster:**
Use the primary `docker-compose.yml` file located in the `config/` directory (which includes resource limits and connects to the cluster's external database):
```bash
docker compose up -d
```

---

## Team
* **Anastasia Kupchik**
* **Klim Kaliasniou**
* **Raman Kupreichyk**
