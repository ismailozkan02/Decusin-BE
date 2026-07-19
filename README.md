# DECUSIN Portal Backend Repo

## Setup Instructions

1. Clone the repository.
2. Create and activate a Python virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Check your env file!


---

## Running the Project

### Locally

1. Make sure your `.env` file is configured and the database is reachable.
2. Start the FastAPI server:
```bash
.venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
3. API will be available at `http://127.0.0.1:8000`
4. Swagger UI: `http://127.0.0.1:8000/docs`

### Server

1. Check that the `.env` file on the server is up to date.
2. Install [WinSCP](https://winscp.net/) (sFTP) and [PuTTY](https://www.putty.org/) (SSH).  
   Open PuTTY directly from WinSCP via `Ctrl+P`.

#### First-time setup: create systemd service

3. Create the service file:
```bash
sudo nano /etc/systemd/system/portal-backend.service
```

Paste the following:
```ini
[Unit]
Description=EuroLink Portal Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/portal-backend
EnvironmentFile=/var/www/portal-backend/.env
ExecStart=/var/www/portal-backend/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

4. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable portal-backend
sudo systemctl start portal-backend
```

#### Deploying updates

5. Pull latest code and restart:
```bash
cd /var/www/portal-backend
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart portal-backend
```

6. Check status and logs:
```bash
sudo systemctl status portal-backend
sudo journalctl -u portal-backend -f
```
