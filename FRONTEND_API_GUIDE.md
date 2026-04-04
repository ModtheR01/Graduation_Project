# API Documentation for Frontend Developers

## 📌 Quick Start

**Base URL:** `http://localhost:8000/` or `https://romee.up.railway.app/`

**Authentication:** JWT Token (required for most endpoints)

---

## 🔐 Authentication

Most endpoints require a **JWT Access Token** in the request header:

```
Authorization: Bearer <your_access_token>
```

### Get JWT Tokens
1. Sign up or log in to get an `access_token` and `refresh_token`
2. Use the `access_token` for all protected endpoints
3. When the `access_token` expires, use the `refresh_token` to get a new one

---

## 📚 All Endpoints

### 1️⃣ Sign Up (Create New Account)

**Endpoint:** `https://romee.up.railway.app/Users/signup/`

**Method:** `POST`

**Description:** Create a new user account with email and password.

**Authentication:** ❌ Not required

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "fname": "John",
  "lname": "Doe",
  "phone_number": "01234567890",
  "country": "Egypt",
  "city": "Cairo",
  "street": "Main Street 123",
  "birth_date": "1995-05-15",
  "country_code": "+20"
}
```

**Field Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| email | string | ✅ | Must be unique, valid email format |
| password | string | ✅ | Minimum 8 characters recommended |
| fname | string | ✅ | First name |
| lname | string | ✅ | Last name |
| phone_number | string | ✅ | Must be unique |
| country | string | ✅ | Country name |
| city | string | ✅ | City name |
| street | string | ✅ | Street address |
| birth_date | date | ❌ | Format: YYYY-MM-DD |
| country_code | string | ✅ | Example: +20 |

**Example Request (cURL):**

```bash
curl -X POST http://localhost:8000/Users/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "MyPassword123",
    "fname": "John",
    "lname": "Doe",
    "phone_number": "01012345678",
    "country": "Egypt",
    "city": "Cairo",
    "birth_date": "1995-05-15"
  }'
```

**Example Request (JavaScript/Fetch):**

```javascript
const response = await fetch('http://localhost:8000/Users/signup/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'MyPassword123',
    fname: 'John',
    lname: 'Doe',
    phone_number: '01012345678',
    country: 'Egypt',
    city: 'Cairo',
    birth_date: '1995-05-15'
  })
});

const data = await response.json();
console.log(data);
```

**Success Response (201 Created):**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Signup Successfully"
}
```

**Error Responses:**

❌ **Email already exists (400 Bad Request):**
```json
{
  "email": ["user with this email already exists."]
}
```

❌ **Invalid password (400 Bad Request):**
```json
{
  "password": ["Password is too common.", "Password must be at least 8 characters."]
}
```

❌ **Invalid email format (400 Bad Request):**
```json
{
  "email": ["Enter a valid email address."]
}
```

---

### 2️⃣ Log In

**Endpoint:** `https://romee.up.railway.app/Users/login/`

**Method:** `POST`

**Description:** Log in with email and password to get JWT tokens.

**Authentication:** ❌ Not required

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Field Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| email | string | ✅ | Registered email |
| password | string | ✅ | Account password |

**Example Request (cURL):**

```bash
curl -X POST http://localhost:8000/Users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "MyPassword123"
  }'
```

**Example Request (JavaScript/Fetch):**

```javascript
const response = await fetch('http://localhost:8000/Users/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'MyPassword123'
  })
});

const data = await response.json();
// Save the access token for future requests
localStorage.setItem('accessToken', data.access);
localStorage.setItem('refreshToken', data.refresh);
```

**Success Response (200 OK):**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login Successfully"
}
```

**Token Lifetime:**
- **Access Token:** Valid for 60 minutes
- **Refresh Token:** Valid for 24 hours

**Error Responses:**

❌ **Invalid credentials (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

❌ **Missing fields (400 Bad Request):**
```json
{
  "email": ["This field is required."],
  "password": ["This field is required."]
}
```

---

### 🔄 Refresh Access Token

**Endpoint:** `https://romee.up.railway.app/token/refresh/`

**Method:** `POST`

**Description:** Get a new access token using your refresh token.

**Authentication:** ❌ Not required

**Request Body:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Example Request:**

```javascript
const response = await fetch('http://localhost:8000/token/refresh/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    refresh: localStorage.getItem('refreshToken')
  })
});

const data = await response.json();
localStorage.setItem('accessToken', data.access);
```

**Success Response (200 OK):**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 💬 Send Chat Message

**Endpoint:** `https://romee.up.railway.app/chat/chat/`

**Method:** `POST`

**Description:** Send a message to the AI assistant and get a response. Start a new chat or continue an existing one.

**Authentication:** ✅ Required (JWT Token)

**Request Body:**

```json
{
  "message": "What flights are available from Cairo to Dubai on April 10, 2026?",
  "chat_id": "optional-chat-id"
}
```

**Field Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| message | string | ✅ | Your question or request (max 5000 characters) |
| chat_id | string/UUID | ❌ | Omit to start a new chat, include to continue existing conversation |

**Example Request (cURL):**

```bash
curl -X POST http://localhost:8000/chat/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "message": "Who won the football world cup 2022?"
  }'
```

**Example Request (JavaScript/Fetch):**

```javascript
const accessToken = localStorage.getItem('accessToken');

// Start new chat
const response = await fetch('http://localhost:8000/chat/chat/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    message: 'What flights are available to Dubai?'
  })
});

const data = await response.json();
console.log(data.response);
console.log(data.chat_id);  // Save this for follow-up messages

// Continue existing chat
const followUpResponse = await fetch('http://localhost:8000/chat/chat/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    message: 'Can you book the cheapest flight?',
    chat_id: data.chat_id
  })
});
```

**Success Response (200 OK):**

```json
{
  "response": "I found 15 flights from Cairo to Dubai on April 10th. The cheapest option is Flydubai at $285 per person, departing at 8:30 AM.",
  "chat_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Error Responses:**

❌ **Missing authentication (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

❌ **Invalid chat ID (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

❌ **Missing message field (400 Bad Request):**
```json
{
  "message": ["This field is required."]
}
```

❌ **AI confused (200 OK - Empty response):**
```json
{
  "response": "Sorry, I am a bit confused. Can you rephrase?",
  "chat_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## 🛠️ Helper Functions

### JavaScript - Store and Use Tokens

```javascript
// After login/signup, save tokens
function saveTokens(accessToken, refreshToken) {
  localStorage.setItem('accessToken', accessToken);
  localStorage.setItem('refreshToken', refreshToken);
}

// Use token in requests
function getHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  };
}

// Remove tokens on logout
function logout() {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
}
```

### JavaScript - Auto-Refresh Token

```javascript
async function makeAuthenticatedRequest(url, method, body) {
  let response = await fetch(url, {
    method: method,
    headers: getHeaders(),
    body: JSON.stringify(body)
  });

  // If token expired, refresh it
  if (response.status === 401) {
    const refreshToken = localStorage.getItem('refreshToken');
    const refreshResponse = await fetch('http://localhost:8000/token/refresh/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken })
    });

    if (refreshResponse.ok) {
      const data = await refreshResponse.json();
      localStorage.setItem('accessToken', data.access);

      // Retry the original request
      response = await fetch(url, {
        method: method,
        headers: getHeaders(),
        body: JSON.stringify(body)
      });
    }
  }

  return response;
}
```

---

## 📊 Common Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | ✅ OK | Request successful |
| 201 | ✅ Created | Resource created successfully |
| 400 | ❌ Bad Request | Invalid input or missing fields |
| 401 | ❌ Unauthorized | Missing or invalid authentication token |
| 403 | ❌ Forbidden | Access denied (resource belongs to different user) |
| 404 | ❌ Not Found | Resource not found |
| 405 | ❌ Method Not Allowed | Wrong HTTP method (e.g., GET instead of POST) |
| 500 | ❌ Server Error | Server error occurred |

---

## 🔍 Debugging Tips

### ✅ Check Token Expiration

```javascript
// Decode JWT token to see expiration
function getTokenExpiration(token) {
  const payload = token.split('.')[1];
  const decoded = JSON.parse(atob(payload));
  const exp = new Date(decoded.exp * 1000);
  console.log('Token expires at:', exp);
  return exp;
}
```

### ✅ Log Request Details

```javascript
async function debugRequest(url, method, body) {
  console.log('📤 Request:', {
    url: url,
    method: method,
    body: body,
    header: getHeaders()
  });

  const response = await fetch(url, {
    method: method,
    headers: getHeaders(),
    body: JSON.stringify(body)
  });

  const data = await response.json();
  console.log('📥 Response:', {
    status: response.status,
    data: data
  });

  return data;
}
```

---

## 🚀 Example Frontend Workflow

### 1. Sign Up
```javascript
// User fills form and clicks "Sign Up"
const signupResponse = await fetch('http://localhost:8000/Users/signup/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'newuser@example.com',
    password: 'SecurePass123',
    fname: 'Jane'
  })
});

const { access, refresh } = await signupResponse.json();
localStorage.setItem('accessToken', access);
localStorage.setItem('refreshToken', refresh);
// Redirect to home page
```

### 2. Send Chat Message
```javascript
// User types message and clicks "Send"
const chatResponse = await fetch('http://localhost:8000/chat/chat/', {
  method: 'POST',
  headers: getHeaders(),
  body: JSON.stringify({
    message: 'Find me a flight to Dubai',
    chat_id: sessionStorage.getItem('currentChatId')
  })
});

const { response, chat_id } = await chatResponse.json();
sessionStorage.setItem('currentChatId', chat_id);
// Display AI response to user
displayMessage('assistant', response);

---

## ❓ FAQ

**Q: What is JWT?**  
A: JWT (JSON Web Token) is a secure way to send information between the client and server. It contains encoded data and cannot be modified without the secret key.

**Q: My token expired, what do I do?**  
A: Use your refresh token to get a new access token from the `/token/refresh/` endpoint.

**Q: Can I use the same token on multiple devices?**  
A: Yes, but each device should request its own tokens. Sharing tokens across devices is not recommended for security.

**Q: How do I know if my token is invalid?**  
A: You'll get a 401 Unauthorized response. Try logging in again or refreshing the token.

**Q: Are account details updated after signup?**  
A: No, you'll need an update profile endpoint (not shown yet in the API). Contact your backend team if needed.

**Q: Can I delete my account?**  
A: No delete endpoint is available yet. Contact your backend team if you need this feature.

---

## 📞 Support

For questions or issues, contact your backend team or check the full API documentation at:
- Chat Module: [CHAT_API_DOCUMENTATION.md](./chat/CHAT_API_DOCUMENTATION.md)
- API Keys: [API_KEYS_DOCUMENTATION.md](./chat/API_KEYS_DOCUMENTATION.md)

---

**Last Updated:** April 4, 2026  
**Version:** 1.0  
**Status:** Production Ready ✅

