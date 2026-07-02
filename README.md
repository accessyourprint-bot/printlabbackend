# Alt Print Backend — Production Setup Guide

## Tech Stack
- **Backend**: Python 3.12+ / FastAPI
- **Database**: PostgreSQL 16
- **Cache + Broker**: Redis 7
- **Background Jobs**: Celery + Celery Beat
- **Storage**: AWS S3 or Cloudflare R2 (AES-256-GCM encrypted)
- **Auth**: JWT (access + refresh tokens) + RBAC
- **Real-time**: WebSocket
- **Deployment**: Docker + Docker Compose

---

## Quick Start

### 1. Clone and configure

```bash
git clone <your-repo>
cd altprint

# Copy and fill in environment variables
cp .env.example .env
nano .env   # Edit all required values
```

### 2. Generate secure keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate AES_ENCRYPTION_KEY (32 chars minimum)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Start the full stack

```bash
docker compose up -d
```

### 4. Verify

```bash
# Check all containers are healthy
docker compose ps

# Test health endpoint
curl http://localhost:8000/health

# View API docs (only available in DEBUG=true mode)
open http://localhost:8000/docs
```

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | App secret key (min 32 chars) |
| `JWT_SECRET_KEY` | ✅ | JWT signing key (min 32 chars) |
| `AES_ENCRYPTION_KEY` | ✅ | File encryption key |
| `DATABASE_URL` | ✅ | PostgreSQL async URL |
| `REDIS_URL` | ✅ | Redis connection URL |
| `SUPER_ADMIN_EMAIL` | ✅ | Super admin email |
| `SUPER_ADMIN_PASSWORD` | ✅ | Super admin password |
| `AWS_ACCESS_KEY_ID` | ✅* | AWS S3 key (*or R2) |
| `AWS_SECRET_ACCESS_KEY` | ✅* | AWS S3 secret |
| `RAZORPAY_KEY_ID` | ⚠️ | Payment gateway key |
| `GOOGLE_MAPS_API_KEY` | ⚠️ | For delivery distance |

---

## API Endpoints Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login (email+password or phone+OTP) |
| POST | `/api/v1/auth/otp/send` | Send OTP to phone |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/logout` | Revoke refresh token |
| GET | `/api/v1/auth/me` | Get current user |

### System (Super Admin)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/system/config` | Get system config |
| PUT | `/api/v1/system/config` | Update config |
| PUT | `/api/v1/system/maintenance?enabled=true` | Toggle maintenance |
| PUT | `/api/v1/system/emergency?locked=true` | Emergency lock |

### Feature Flags
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/features` | List global flags |
| GET | `/api/v1/features?shop_id=shop-001` | List shop flags |
| POST | `/api/v1/features/toggle` | Toggle a flag |
| POST | `/api/v1/features/enable` | Enable a flag |
| POST | `/api/v1/features/disable` | Disable a flag |

### Shops (Super Admin)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/shops` | Create shop |
| GET | `/api/v1/shops` | List all shops |
| GET | `/api/v1/shops/{id}` | Get shop |
| PUT | `/api/v1/shops/{id}` | Update shop |
| PATCH | `/api/v1/shops/{id}/enable` | Enable shop |
| PATCH | `/api/v1/shops/{id}/disable` | Disable shop |
| DELETE | `/api/v1/shops/{id}` | Delete shop |

### Files
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/files/upload` | Upload single file |
| POST | `/api/v1/files/upload/multiple` | Upload multiple files |
| GET | `/api/v1/files/my` | List my files |
| DELETE | `/api/v1/files/{id}` | Delete file |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/orders/calculate-price` | Get price estimate |
| POST | `/api/v1/orders` | Place order |
| GET | `/api/v1/orders` | List orders |
| GET | `/api/v1/orders/{id}` | Get order |
| PATCH | `/api/v1/orders/{id}/status` | Update status |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/payments/create` | Create payment |
| POST | `/api/v1/payments/verify` | Verify Razorpay payment |
| POST | `/api/v1/payments/webhook` | Razorpay webhook |

### Audit
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/audit` | Get audit logs (Super Admin) |

### WebSocket
| Endpoint | Description |
|----------|-------------|
| `ws://host/ws?token=JWT` | Real-time updates |

---

## WebSocket Events

Connect: `ws://localhost:8000/ws?token=YOUR_ACCESS_TOKEN`

### Events you receive:
```json
// System config change
{"type": "SYSTEM_CONFIG_UPDATE", "payload": {"app_enabled": true, "maintenance_mode": false, ...}, "timestamp": "..."}

// Feature flag toggle
{"type": "FEATURE_FLAG_UPDATE", "payload": {"feature_name": "delivery", "enabled": false, "scope": "shop", "shop_id": "shop-001"}, "timestamp": "..."}

// Order status update
{"type": "ORDER_STATUS_UPDATE", "payload": {"order_id": "...", "status": "ready"}, "timestamp": "..."}
```

### Keep-alive:
```
Send: "ping"
Receive: "pong"
```

---

## Security Features

- **AES-256-GCM** encryption for all stored files
- **Random filenames** — original names never stored in S3/R2
- **JWT** access tokens (30 min) + refresh tokens (30 days)
- **Token rotation** on refresh
- **RBAC**: `super_admin`, `shop_admin`, `user`
- **Rate limiting**: 60 req/min global, 5 req/min for login
- **Brute force protection**: account lockout after 5 failed logins
- **Auto-delete**: files purged after 7 days (irreversible)
- **Secure headers**: HSTS, X-Frame-Options, CSP, etc.
- **SQL injection protection**: SQLAlchemy ORM with parameterized queries
- **Input validation**: Pydantic v2 on all endpoints

---

## File Auto-Delete

Files are automatically deleted after `FILE_RETENTION_DAYS` (default: 7 days).

- Celery Beat runs deletion every 6 hours
- Storage key is overwritten with "DELETED"
- Encrypted bytes are purged from S3/R2
- This is **irreversible** by design

---

## Database Tables

| Table | Description |
|-------|-------------|
| `users` | All users (super_admin, shop_admin, user) |
| `shops` | Registered print shops |
| `system_config` | Platform-wide toggles (1 row) |
| `feature_flags` | Global + shop-level feature toggles |
| `audit_log` | Immutable action history |
| `orders` | Customer orders |
| `order_files` | Files attached to orders (encrypted) |
| `payments` | Payment records |
| `refresh_tokens` | JWT refresh token store |
| `websocket_sessions` | Active WS connections |

---

## Monitoring

- **Celery Flower**: http://localhost:5555 (task monitoring)
- **Health Check**: http://localhost:8000/health
- **API Docs** (debug only): http://localhost:8000/docs

---

## Production Checklist

- [ ] Change all default passwords in `.env`
- [ ] Set `DEBUG=false`
- [ ] Configure real AWS S3 or Cloudflare R2 credentials
- [ ] Add Razorpay live credentials
- [ ] Set up SSL/TLS (nginx reverse proxy recommended)
- [ ] Configure `ALLOWED_ORIGINS` to your domain(s)
- [ ] Set up log aggregation (e.g., CloudWatch, Datadog)
- [ ] Configure automated DB backups
- [ ] Set up alerting for emergency lock events
