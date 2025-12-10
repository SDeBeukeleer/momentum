# Momentum - Hetzner VPS Deployment Guide

## Server Details
- **IP Address:** 91.99.160.39
- **App Port:** 3001 (ActionFlow uses 3000)
- **URL:** http://91.99.160.39:3001

---

## Quick Deployment (5 minutes)

### Step 1: Connect to Server

```bash
ssh root@91.99.160.39
```

### Step 2: Clone Repository

```bash
cd /opt
git clone https://github.com/SDeBeukeleer/momentum.git
cd momentum
```

### Step 3: Configure Environment

```bash
# Copy the production environment template
cp .env.production .env

# Generate secure passwords
DB_PASS=$(openssl rand -base64 16 | tr -d '/+=' | head -c 20)
AUTH_SECRET=$(openssl rand -base64 32)

# Update the .env file
sed -i "s/change_me_to_secure_password/$DB_PASS/" .env
sed -i "s/change_me_generate_with_openssl_rand/$AUTH_SECRET/" .env

# Verify the changes
cat .env
```

### Step 4: Deploy!

```bash
# Build and start all services (uses docker-compose.prod.yml)
docker compose -f docker-compose.prod.yml up -d --build

# Watch the logs (optional)
docker compose -f docker-compose.prod.yml logs -f
```

Wait 2-3 minutes for the build to complete.

### Step 5: Initialize Database

```bash
# Run Prisma migrations
docker compose -f docker-compose.prod.yml exec app npx prisma db push
```

### Step 6: Test It!

Open your browser and go to:
```
http://91.99.160.39:3001
```

You should see Momentum! 🎉

---

## Useful Commands

### View Logs
```bash
cd /opt/momentum

# All services
docker compose -f docker-compose.prod.yml logs -f

# Just the app
docker compose -f docker-compose.prod.yml logs -f app
```

### Restart Services
```bash
cd /opt/momentum
docker compose -f docker-compose.prod.yml restart
```

### Update Application
```bash
cd /opt/momentum
git pull
docker compose -f docker-compose.prod.yml up -d --build
```

### Stop Everything
```bash
cd /opt/momentum
docker compose -f docker-compose.prod.yml down
```

### Check Status
```bash
docker compose -f docker-compose.prod.yml ps
```

---

## Backup Database

```bash
docker compose -f docker-compose.prod.yml exec db pg_dump -U momentum momentum > backup_$(date +%Y%m%d).sql
```

---

## Running Apps on Server

| App | Port | URL |
|-----|------|-----|
| ActionFlow | 80/3000 | http://91.99.160.39 |
| Momentum | 3001 | http://91.99.160.39:3001 |
