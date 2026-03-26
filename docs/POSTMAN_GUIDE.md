# OrderFlow — Postman Collection Guide

> **🇧🇷 Versão em Português logo abaixo · 🇺🇸 English version first**

---

## 🇺🇸 English

### Requirements

| Tool | Version |
|------|---------|
| [Postman](https://www.postman.com/downloads/) | Any recent version |
| OrderFlow API running locally | `http://localhost:8000` |

---

### 1. Import the collection
---

### 2. Set the base URL

The collection uses a variable called `base_url`.  
Its default value is already set to `http://localhost:8000` — no extra configuration needed.

> To change it: open the collection → **Variables** tab → edit `base_url`.

---

### 3. Authenticate

All protected endpoints use a **Bearer token** that is stored automatically.

**Steps:**
1. Open folder **Auth → Login**.
2. Fill in `username` and `password` in the request body.
3. Send the request (`Ctrl+Enter`).
4. The test script runs automatically and saves `access_token` and `refresh_token` as collection variables.

> Every subsequent request in the collection will use `{{access_token}}` in the `Authorization: Bearer` header automatically — you don't need to copy/paste anything.

**Refresh the token:**  
Use **Auth → Refresh Token** when the access token expires. The new token is saved automatically.

---

### 4. Collection structure

```
📁 Health
│   └─ Health Check                    GET    /health

📁 Auth
│   ├─ Login                           POST   /api/v1/auth/
│   ├─ Refresh Token                   POST   /api/v1/auth/refresh
│   └─ Login Owner                     POST   /api/v1/auth/  (same endpoint — OWNER credentials from .env)

📁 Users
│   ├─ Create User                     POST   /api/v1/users/
│   ├─ List Users                      GET    /api/v1/users/
│   ├─ Get Me                          GET    /api/v1/users/me
│   ├─ Get My Addresses                GET    /api/v1/users/me/address
│   ├─ Get User by ID                  GET    /api/v1/users/:user_id
│   ├─ Add Address (me)                POST   /api/v1/users/me/addresses
│   ├─ Update Me                       PUT    /api/v1/users/me
│   ├─ Update My Address               PUT    /api/v1/users/me/addresses/:address_id
│   ├─ Update User by ID               PUT    /api/v1/users/:user_id
│   ├─ Set Default Address             PATCH  /api/v1/users/me/addresses/:address_id/default
│   ├─ Update User Role                PATCH  /api/v1/users/:user_id/role
│   └─ Delete User                     DELETE /api/v1/users/:user_id

📁 Accounts                            (created automatically with POST /users/)
│   ├─ Create Account                  POST   /api/v1/accounts/              🔒 admin/owner only
│   ├─ Get Account by ID               GET    /api/v1/accounts/:account_id
│   ├─ Update Account Username         PUT    /api/v1/accounts/:account_id
│   ├─ Change Password                 PATCH  /api/v1/accounts/:account_id/password
│   ├─ Suspend Account                 PATCH  /api/v1/accounts/:account_id/suspended
│   ├─ Activate Account                PATCH  /api/v1/accounts/:account_id/activate
│   └─ Deactivate Account              PATCH  /api/v1/accounts/:account_id/inactive

📁 Addresses
│   ├─ Create Address                  POST   /api/v1/addresses/
│   ├─ List Addresses                  GET    /api/v1/addresses/
│   ├─ Get Address by ID               GET    /api/v1/addresses/:address_id
│   ├─ Get Addresses by User ID        GET    /api/v1/addresses/user/:user_id
│   ├─ Update Address                  PUT    /api/v1/addresses/:address_id
│   └─ Delete Address                  DELETE /api/v1/addresses/:address_id

📁 Categories
│   ├─ Create Category                 POST   /api/v1/categories/
│   ├─ List Categories                 GET    /api/v1/categories/
│   ├─ Get Category by ID              GET    /api/v1/categories/:category_id
│   ├─ Update Category                 PUT    /api/v1/categories/:category_id
│   └─ Delete Category                 DELETE /api/v1/categories/:category_id

📁 Products
│   ├─ Create Product                  POST   /api/v1/products/
│   ├─ List Products                   GET    /api/v1/products/
│   ├─ Get Product by ID               GET    /api/v1/products/:product_id
│   ├─ Get Products by Category        GET    /api/v1/products/category/:category_id
│   ├─ Count Products by Category      GET    /api/v1/products/count/category/:category_id
│   ├─ Update Product                  PUT    /api/v1/products/:product_id
│   └─ Delete Product                  DELETE /api/v1/products/:product_id

📁 Orders
│   ├─ Create Order                    POST   /api/v1/orders/
│   ├─ List My Orders                  GET    /api/v1/orders/
│   ├─ Get Order by ID                 GET    /api/v1/orders/:order_id
│   ├─ Cancel Order                    POST   /api/v1/orders/:order_id/cancel
│   ├─ Update Order                    PUT    /api/v1/orders/:order_id
│   └─ Delete Order                    DELETE /api/v1/orders/:order_id

📁 Order Items
│   ├─ Create Order Item               POST   /api/v1/order-items/
│   ├─ List Order Items                GET    /api/v1/order-items/
│   ├─ Get Order Item by ID            GET    /api/v1/order-items/:order_item_id
│   ├─ Update Order Item               PUT    /api/v1/order-items/:order_item_id
│   └─ Delete Order Item               DELETE /api/v1/order-items/:order_item_id

📁 Reviews
│   ├─ Create Review                   POST   /api/v1/reviews/
│   ├─ List Reviews                    GET    /api/v1/reviews/
│   ├─ Get Review by ID                GET    /api/v1/reviews/:review_id
│   └─ Delete Review                   DELETE /api/v1/reviews/:review_id

📁 Admin                               🔒 admin/owner only
│   ├─ Update Order Status             PATCH  /api/v1/admin/orders/:order_id/status
│   ├─ List All Orders                 GET    /api/v1/admin/orders
│   └─ Dashboard                       GET    /api/v1/admin/dashboard

📁 Owner                               🔒 owner only
│   ├─ Promote to Admin                PATCH  /api/v1/users/:user_id/role
│   └─ Remove Admin Role               PATCH  /api/v1/users/:user_id/role
```

---

### 5. Roles and permissions

```
OWNER  ──▶  can do everything + manage roles
ADMIN  ──▶  can access /admin/* endpoints
USER   ──▶  standard access to own data
```

The system **OWNER** is created automatically on first startup via environment variables (`OWNER_EMAIL`, `OWNER_USERNAME`, `OWNER_PASSWORD`).  
Assigning the `owner` role through the API is intentionally blocked — it returns **403**.

---

### 6. Collection variables

| Variable | Description | Auto-populated |
|----------|-------------|:--------------:|
| `base_url` | API base URL | ❌ (default: `http://localhost:8000`) |
| `access_token` | JWT access token | ✅ after Login |
| `refresh_token` | JWT refresh token | ✅ after Login |
| `user_id` | Last created/used user ID | ✅ after Create User |
| `account_id` | Last created/used account ID | ✅ after Create Account |
| `address_id` | Last created/used address ID | ✅ after Add Address |
| `category_id` | Last created/used category ID | ✅ after Create Category |
| `product_id` | Last created/used product ID | ✅ after Create Product |
| `order_id` | Last created/used order ID | ✅ after Create Order |
| `order_item_id` | Last created/used order item ID | ✅ after Create Order Item |
| `review_id` | Last created/used review ID | ✅ after Create Review |

---

### 7. Quick start flow

> **Note:** `POST /users/` automatically creates the linked account in the same operation — you do **not** need to call `POST /accounts/` separately.

```
1. POST /api/v1/users/              → create user (account is created automatically)
2. POST /api/v1/auth/               → login (token saved automatically)
3. POST /api/v1/users/me/addresses  → add a delivery address
4. POST /api/v1/orders/             → place an order
5. POST /api/v1/order-items/        → add items to the order
```

---

---

## 🇧🇷 Português

### Requisitos

| Ferramenta | Versão |
|------------|--------|
| [Postman](https://www.postman.com/downloads/) | Qualquer versão recente |
| API OrderFlow rodando localmente | `http://localhost:8000` |

---

### 1. Importar a collection
---

### 2. Configurar a URL base

A collection usa uma variável chamada `base_url`.  
O valor padrão já está definido como `http://localhost:8000` — nenhuma configuração extra necessária.

> Para alterar: abra a collection → aba **Variables** → edite `base_url`.

---

### 3. Autenticar

Todos os endpoints protegidos usam um **Bearer token** que é salvo automaticamente.

**Passo a passo:**
1. Abra a pasta **Auth → Login**.
2. Preencha `username` e `password` no corpo da requisição.
3. Envie a requisição (`Ctrl+Enter`).
4. O script de teste executa automaticamente e salva `access_token` e `refresh_token` como variáveis da collection.

> Todas as requisições seguintes usarão `{{access_token}}` no header `Authorization: Bearer` automaticamente — não é necessário copiar/colar nada.

**Renovar o token:**  
Use **Auth → Refresh Token** quando o access token expirar. O novo token é salvo automaticamente.

---

### 4. Estrutura da collection

```
📁 Health
│   └─ Health Check                    GET    /health

📁 Auth
│   ├─ Login                           POST   /api/v1/auth/
│   ├─ Refresh Token                   POST   /api/v1/auth/refresh
│   └─ Login Owner                     POST   /api/v1/auth/  (mesmo endpoint — credenciais do OWNER via .env)

📁 Users
│   ├─ Create User                     POST   /api/v1/users/
│   ├─ List Users                      GET    /api/v1/users/
│   ├─ Get Me                          GET    /api/v1/users/me
│   ├─ Get My Addresses                GET    /api/v1/users/me/address
│   ├─ Get User by ID                  GET    /api/v1/users/:user_id
│   ├─ Add Address (me)                POST   /api/v1/users/me/addresses
│   ├─ Update Me                       PUT    /api/v1/users/me
│   ├─ Update My Address               PUT    /api/v1/users/me/addresses/:address_id
│   ├─ Update User by ID               PUT    /api/v1/users/:user_id
│   ├─ Set Default Address             PATCH  /api/v1/users/me/addresses/:address_id/default
│   ├─ Update User Role                PATCH  /api/v1/users/:user_id/role
│   └─ Delete User                     DELETE /api/v1/users/:user_id

📁 Accounts                            (criada automaticamente ao criar um usuário)
│   ├─ Create Account                  POST   /api/v1/accounts/              🔒 somente admin/owner
│   ├─ Get Account by ID               GET    /api/v1/accounts/:account_id
│   ├─ Update Account Username         PUT    /api/v1/accounts/:account_id
│   ├─ Change Password                 PATCH  /api/v1/accounts/:account_id/password
│   ├─ Suspend Account                 PATCH  /api/v1/accounts/:account_id/suspended
│   ├─ Activate Account                PATCH  /api/v1/accounts/:account_id/activate
│   └─ Deactivate Account              PATCH  /api/v1/accounts/:account_id/inactive

📁 Addresses
│   ├─ Create Address                  POST   /api/v1/addresses/
│   ├─ List Addresses                  GET    /api/v1/addresses/
│   ├─ Get Address by ID               GET    /api/v1/addresses/:address_id
│   ├─ Get Addresses by User ID        GET    /api/v1/addresses/user/:user_id
│   ├─ Update Address                  PUT    /api/v1/addresses/:address_id
│   └─ Delete Address                  DELETE /api/v1/addresses/:address_id

📁 Categories
│   ├─ Create Category                 POST   /api/v1/categories/
│   ├─ List Categories                 GET    /api/v1/categories/
│   ├─ Get Category by ID              GET    /api/v1/categories/:category_id
│   ├─ Update Category                 PUT    /api/v1/categories/:category_id
│   └─ Delete Category                 DELETE /api/v1/categories/:category_id

📁 Products
│   ├─ Create Product                  POST   /api/v1/products/
│   ├─ List Products                   GET    /api/v1/products/
│   ├─ Get Product by ID               GET    /api/v1/products/:product_id
│   ├─ Get Products by Category        GET    /api/v1/products/category/:category_id
│   ├─ Count Products by Category      GET    /api/v1/products/count/category/:category_id
│   ├─ Update Product                  PUT    /api/v1/products/:product_id
│   └─ Delete Product                  DELETE /api/v1/products/:product_id

📁 Orders
│   ├─ Create Order                    POST   /api/v1/orders/
│   ├─ List My Orders                  GET    /api/v1/orders/
│   ├─ Get Order by ID                 GET    /api/v1/orders/:order_id
│   ├─ Cancel Order                    POST   /api/v1/orders/:order_id/cancel
│   ├─ Update Order                    PUT    /api/v1/orders/:order_id
│   └─ Delete Order                    DELETE /api/v1/orders/:order_id

📁 Order Items
│   ├─ Create Order Item               POST   /api/v1/order-items/
│   ├─ List Order Items                GET    /api/v1/order-items/
│   ├─ Get Order Item by ID            GET    /api/v1/order-items/:order_item_id
│   ├─ Update Order Item               PUT    /api/v1/order-items/:order_item_id
│   └─ Delete Order Item               DELETE /api/v1/order-items/:order_item_id

📁 Reviews
│   ├─ Create Review                   POST   /api/v1/reviews/
│   ├─ List Reviews                    GET    /api/v1/reviews/
│   ├─ Get Review by ID                GET    /api/v1/reviews/:review_id
│   └─ Delete Review                   DELETE /api/v1/reviews/:review_id

📁 Admin                               🔒 somente admin/owner
│   ├─ Update Order Status             PATCH  /api/v1/admin/orders/:order_id/status
│   ├─ List All Orders                 GET    /api/v1/admin/orders
│   └─ Dashboard                       GET    /api/v1/admin/dashboard

📁 Owner                               🔒 somente owner
│   ├─ Promote to Admin                PATCH  /api/v1/users/:user_id/role
│   └─ Remove Admin Role               PATCH  /api/v1/users/:user_id/role
```

---

### 5. Roles e permissões

```
OWNER  ──▶  acesso total + gerenciar roles de outros usuários
ADMIN  ──▶  acesso aos endpoints /admin/*
USER   ──▶  acesso padrão aos próprios dados
```

O **OWNER** do sistema é criado automaticamente na primeira inicialização via variáveis de ambiente (`OWNER_EMAIL`, `OWNER_USERNAME`, `OWNER_PASSWORD`).  
Atribuir a role `owner` via API é bloqueado intencionalmente — retorna **403**.

---

### 6. Variáveis da collection

| Variável | Descrição | Auto-preenchida |
|----------|-----------|:---------------:|
| `base_url` | URL base da API | ❌ (padrão: `http://localhost:8000`) |
| `access_token` | JWT de acesso | ✅ após Login |
| `refresh_token` | JWT de renovação | ✅ após Login |
| `user_id` | ID do último usuário criado/usado | ✅ após Create User |
| `account_id` | ID da última conta criada/usada | ✅ após Create Account |
| `address_id` | ID do último endereço criado/usado | ✅ após Add Address |
| `category_id` | ID da última categoria criada/usada | ✅ após Create Category |
| `product_id` | ID do último produto criado/usado | ✅ após Create Product |
| `order_id` | ID do último pedido criado/usado | ✅ após Create Order |
| `order_item_id` | ID do último item de pedido criado/usado | ✅ após Create Order Item |
| `review_id` | ID da última avaliação criada/usada | ✅ após Create Review |

---

### 7. Fluxo rápido de uso

> **Atenção:** `POST /users/` já cria automaticamente a conta vinculada na mesma operação — **não é necessário** chamar `POST /accounts/` separadamente.

```
1. POST /api/v1/users/              → criar usuário (conta criada automaticamente)
2. POST /api/v1/auth/               → fazer login (token salvo automaticamente)
3. POST /api/v1/users/me/addresses  → adicionar endereço de entrega
4. POST /api/v1/orders/             → criar um pedido
5. POST /api/v1/order-items/        → adicionar itens ao pedido
```
