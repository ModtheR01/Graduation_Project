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

# ...existing code...

### 3️⃣ Get User Information

**Endpoint:** `https://romee.up.railway.app/Users/user-info/`

**Method:** `GET`

**Description:** Retrieve the authenticated user's profile information.

**Authentication:** ✅ Required (JWT Token)

**Request Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Example Request (cURL):**

```bash
curl -X GET http://localhost:8000/Users/user-info/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

**Example Request (JavaScript/Fetch):**

```javascript
const accessToken = localStorage.getItem('accessToken');

const response = await fetch('http://localhost:8000/Users/user-info/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});

const userData = await response.json();
console.log('User Email:', userData.email);
console.log('User Name:', userData.first_name, userData.last_name);
```

**Success Response (200 OK):**

```json
{
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+201012345678",
  "country": "Egypt",
  "city": "Cairo",
  "street": "123 Main Street",
  "birth_date": "1995-05-15"
}
```

**Error Response:**

❌ **Not authenticated (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

❌ **Invalid token (401 Unauthorized):**
```json
{
  "detail": "Invalid token."
}
```

---

### 4️⃣ Update User Information

**Endpoint:** `https://romee.up.railway.app/Users/update-user-info/`

**Method:** `PATCH`

**Description:** Update the authenticated user's profile information. Only provided fields will be updated.

**Authentication:** ✅ Required (JWT Token)

**Request Body (All fields optional):**

```json
{
  "fname": "Jane",
  "lname": "Smith",
  "phone_number": "+201098765432",
  "country": "UAE",
  "city": "Dubai",
  "street": "456 Sheikh Zayed Road",
  "birth_date": "1995-05-15"
}
```

**Field Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| fname | string | ❌ | First name |
| lname | string | ❌ | Last name |
| phone_number | string | ❌ | Phone number |
| country | string | ❌ | Country name |
| city | string | ❌ | City name |
| street | string | ❌ | Street address |
| birth_date | date | ❌ | Format: YYYY-MM-DD |

**Example Request (cURL):**

```bash
curl -X PATCH http://localhost:8000/Users/update-user-info/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fname": "Jane",
    "city": "Dubai"
  }'
```

**Example Request (JavaScript/Fetch):**

```javascript
const accessToken = localStorage.getItem('accessToken');

const response = await fetch('http://localhost:8000/Users/update-user-info/', {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    fname: 'Jane',
    lname: 'Smith',
    phone_number: '+201098765432',
    city: 'Dubai'
  })
});

const data = await response.json();
console.log(data.message);  // "User information updated successfully"
```

**Success Response (200 OK):**

```json
{
  "message": "User information updated successfully"
}
```

**Error Responses:**

❌ **Not authenticated (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

❌ **Invalid data (400 Bad Request):**
```json
{
  "birth_date": ["Enter a valid date."]
}
```

---

### 5️⃣ Get All User Chats

**Endpoint:** `https://romee.up.railway.app/chat/user-chats/`

**Method:** `GET`

**Description:** Retrieve all chats for the authenticated user with their IDs and titles.

**Authentication:** ✅ Required (JWT Token)

**Request Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Example Request (cURL):**

```bash
curl -X GET http://localhost:8000/chat/user-chats/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

**Example Request (JavaScript/Fetch):**

```javascript
const accessToken = localStorage.getItem('accessToken');

const response = await fetch('http://localhost:8000/chat/user-chats/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});

const chats = await response.json();
chats.forEach(chat => {
  console.log(`Chat: ${chat.title} (ID: ${chat.id})`);
});
```

**Success Response (200 OK):**

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Flight Search - Cairo to Dubai"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "Hotel Recommendations in Dubai"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "title": "Travel Budget Planning"
  }
]
```

**Error Responses:**

❌ **No chats found (404 Not Found):**
```json
{
  "error": "No chats found"
}
```

❌ **Not authenticated (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Notes:**
- Returns an array of chat summaries
- Each chat has an ID (use this to fetch full conversation) and auto-generated title
- Title is based on the first message in the chat
- Display these as a list of recent conversations in your UI

---

### 6️⃣ Get Chat by ID (Full Conversation)

**Endpoint:** `https://romee.up.railway.app/chat/chat/<chat_id>/`

**Method:** `GET`

**Description:** Retrieve the complete conversation history for a specific chat.

**Authentication:** ✅ Required (JWT Token)

**URL Parameters:**

| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| chat_id | string (UUID) | ✅ | The unique identifier of the chat |

**Request Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Example Request (cURL):**

```bash
curl -X GET "http://localhost:8000/chat/chat/550e8400-e29b-41d4-a716-446655440000/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

**Example Request (JavaScript/Fetch):**

```javascript
const accessToken = localStorage.getItem('accessToken');
const chatId = '550e8400-e29b-41d4-a716-446655440000';

const response = await fetch(`http://localhost:8000/chat/chat/${chatId}/`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});

const messages = await response.json();
messages.forEach(msg => {
  if (msg.role === 'user') {
    console.log(`📤 You: ${msg.content}`);
  } else {
    console.log(`🤖 Assistant: ${msg.content}`);
  }
});
```

**Success Response (200 OK):**

```json
[
  {
    "role": "user",
    "content": "Find me flights from Cairo to Dubai on April 10, 2026"
  },
  {
    "role": "assistant",
    "content": "I found 15 flights from Cairo (CAI) to Dubai (DXB) on April 10th. Here are the top options:\n\n1. Emirates EK901\n   Departure: 08:30 AM\n   Arrival: 12:30 PM (same day)\n   Duration: 4 hours\n   Price: $320\n\n2. Flydubai FZ203\n   Departure: 02:15 PM\n   Arrival: 06:15 PM\n   Duration: 4 hours\n   Price: $285\n\n3. Air Arabia G9102\n   Departure: 10:50 PM\n   Arrival: 02:50 AM (next day)\n   Duration: 4 hours\n   Price: $195"
  },
  {
    "role": "user",
    "content": "Can you book the cheapest one?"
  },
  {
    "role": "assistant",
    "content": "I can help you book Air Arabia G9102 (the cheapest option at $195). However, I'll need some information:\n\n1. Full name (as it appears in your passport)\n2. Passport number\n3. Date of birth\n4. Email address\n5. Phone number\n6. Baggage preference (carry-on only or checked baggage)\n\nWould you like to proceed with this booking?"
  }
]
```

**Error Responses:**

❌ **Chat not found (404 Not Found):**
```json
{
  "error": "Chat not found"
}
```

❌ **Not authenticated (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

❌ **Access denied - chat belongs to different user (403 Forbidden):**
```json
{
  "error": "You don't have permission to access this chat."
}
```

**Notes:**
- Returns an array of message objects in chronological order
- Each message has `role` (either "user" or "assistant") and `content`
- Users can only access their own chats (backend enforces this)
- Use this endpoint to fetch full conversation when user clicks on a chat from the list

---

### 1️⃣ Get All Contacts

**Endpoint:** `http://localhost:8000/sending_emails/contact/`

**Method:** `GET`

**Description:** Retrieve all contacts.

**Authentication:** ✅ Required (JWT Token)

**Request Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Example Request (JavaScript/Fetch):**

```javascript
const accessToken = localStorage.getItem('accessToken');

const response = await fetch('http://localhost:8000/sending_emails/contact/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});

const contacts = await response.json();
console.log(contacts);
```

**Success Response (200 OK):**

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "0123456789"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "0198765432"
  }
]
```

**Error Response:**

❌ **Not authenticated (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Note:** 🔒 403 Forbidden means you're trying to access data that doesn't belong to your account.

---

### 2️⃣ Create Contact

**Endpoint:** `http://localhost:8000/sending_emails/contact/create/`

**Method:** `POST`

**Description:** Create a new contact.

**Authentication:** ✅ Required (JWT Token)

**Request Body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "0123456789"
}
```

**Field Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| name | string | ✅ | Contact's full name |
| email | string | ✅ | Valid email address |
| phone | string | ✅ | Phone number |

**Example Request (JavaScript/Fetch):**

```javascript
const accessToken = localStorage.getItem('accessToken');

const response = await fetch('http://localhost:8000/sending_emails/contact/create/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    phone: '0123456789'
  })
});

const newContact = await response.json();
console.log('Contact created:', newContact);
```

**Success Response (201 Created):**

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "0123456789"
}
```

**Error Responses:**

❌ **Missing required field (400 Bad Request):**
```json
{
  "email": ["This field is required."]
}
```

❌ **Invalid email (400 Bad Request):**
```json
{
  "email": ["Enter a valid email address."]
}
```

---

### 3️⃣ Update Contact

**Endpoint:** `http://localhost:8000/sending_emails/contact/update/<id>/`

**Method:** `PUT`

**Description:** Update an existing contact by ID.

**Authentication:** ✅ Required (JWT Token)

**URL Parameters:**

| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| id | integer | ✅ | The contact ID |

**Request Body:**

```json
{
  "name": "Updated Name",
  "email": "updated@example.com",
  "phone": "0100000000"
}
```

**Example Request (JavaScript/Fetch):**

```javascript
const accessToken = localStorage.getItem('accessToken');
const contactId = 1;

const response = await fetch(`http://localhost:8000/sending_emails/contact/update/${contactId}/`, {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Updated Name',
    email: 'updated@example.com',
    phone: '0100000000'
  })
});

const updatedContact = await response.json();
console.log('Contact updated:', updatedContact);
```

**Success Response (200 OK):**

```json
{
  "id": 1,
  "name": "Updated Name",
  "email": "updated@example.com",
  "phone": "0100000000"
}
```

**Error Responses:**

❌ **Contact not found (404 Not Found):**
```json
{}
```

❌ **Invalid email (400 Bad Request):**
```json
{
  "email": ["Enter a valid email address."]
}
```

---

### 4️⃣ Delete Contact

**Endpoint:** `http://localhost:8000/sending_emails/contact/delete/<id>/`

**Method:** `DELETE`

**Description:** Delete a contact by ID.

**Authentication:** ✅ Required (JWT Token)

**URL Parameters:**

| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| id | integer | ✅ | The contact ID |

**Example Request (JavaScript/Fetch):**

```javascript
const accessToken = localStorage.getItem('accessToken');
const contactId = 1;

const response = await fetch(`http://localhost:8000/sending_emails/contact/delete/${contactId}/`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});

if (response.status === 204) {
  console.log('Contact deleted successfully');
}
```

**Success Response (204 No Content):**

```
(Empty response body)
```

**Error Response:**

❌ **Contact not found (404 Not Found):**
```json
{}
```

# ...existing code...

# ...existing code...

### 7️⃣ Login with Google (OAuth 2.0)

**Endpoint:** `https://romee.up.railway.app/Users/login/google/`

**Method:** `POST`

**Description:** Authenticate user with Google OAuth 2.0. Creates a new account automatically if the user doesn't exist.

**Authentication:** ❌ Not required

**Prerequisites:**
1. User must have a Google account
2. Frontend must handle Google OAuth flow and get authorization code
3. Google API credentials must be configured in backend

---

## 🔑 How Google Login Works (Flow Diagram)

```
1. User clicks "Login with Google" button
   ↓
2. Frontend redirects to Google login page
   ↓
3. Google returns authorization CODE to your frontend
   ↓
4. Frontend sends CODE to backend (this endpoint)
   ↓
5. Backend exchanges CODE for Google tokens
   ↓
6. Backend verifies user identity with Google
   ↓
7. Backend creates/updates user in database
   ↓
8. Backend returns JWT access token
   ↓
9. Frontend stores JWT and user is logged in
```

---

## 📝 Request Body

```json
{
  "code": "4/0AX4XfWg1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7"
}
```

**Field Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| code | string | ✅ | Authorization code from Google OAuth flow (valid for 10 minutes) |

---

## 🚀 Frontend Implementation Guide

### Step 1: Install Google OAuth Library

```bash
npm install @react-oauth/google
```

### Step 2: Setup Google OAuth Provider (React Example)

```javascript
import { GoogleOAuthProvider } from '@react-oauth/google';

export default function App() {
  return (
    <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
      <YourComponents />
    </GoogleOAuthProvider>
  );
}
```

### Step 3: Create Google Login Button Component

```javascript
import { useGoogleLogin } from '@react-oauth/google';

export default function GoogleLoginButton() {
  const login = useGoogleLogin({
    onSuccess: (codeResponse) => handleGoogleLogin(codeResponse.code),
    onError: (error) => console.log('Login Failed:', error),
    flow: 'auth-code'  // Important: Get authorization code, not access token
  });

  const handleGoogleLogin = async (code) => {
    try {
      const response = await fetch('http://localhost:8000/Users/login/google/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code })
      });

      const data = await response.json();

      if (response.ok) {
        // Store tokens
        localStorage.setItem('accessToken', data.access);
        localStorage.setItem('refreshToken', data.refresh);
        
        console.log(data.message);  // "Login Successfully"
        console.log('Is new user:', data.is_new_user);
        
        // Redirect to dashboard
        window.location.href = '/dashboard';
      } else {
        console.error('Login error:', data.error);
      }
    } catch (error) {
      console.error('Network error:', error);
    }
  };

  return (
    <button onClick={() => login()}>
      🔵 Login with Google
    </button>
  );
}
```

### Step 4: Using the Official Google Button (Alternative)

```javascript
import { GoogleLogin } from '@react-oauth/google';

export default function LoginPage() {
  const handleSuccess = async (credentialResponse) => {
    const code = credentialResponse.credential;  // This is the authorization code
    
    const response = await fetch('http://localhost:8000/Users/login/google/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ code })
    });

    const data = await response.json();
    
    if (response.ok) {
      localStorage.setItem('accessToken', data.access);
      localStorage.setItem('refreshToken', data.refresh);
      window.location.href = '/dashboard';
    }
  };

  return (
    <GoogleLogin
      onSuccess={handleSuccess}
      onError={() => console.log('Login Failed')}
    />
  );
}
```

---

## ✅ Success Response (200 OK)

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6ImpvaG5AZ21haWwuY29tIn0...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ...",
  "message": "Login Successfully",
  "is_new_user": true
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| access | string | JWT access token (valid for 60 minutes) - Use this for API requests |
| refresh | string | JWT refresh token (valid for 24 hours) - Use to get new access token |
| message | string | Confirmation message |
| is_new_user | boolean | `true` if new account was created, `false` if existing user |

---

## ❌ Error Responses

### ❌ Missing Authorization Code (400 Bad Request)

```json
{
  "error": "Code is required"
}
```

**Solution:** Ensure Google OAuth flow completed and code was received.

---

### ❌ Failed Token Exchange (400 Bad Request)

```json
{
  "error": "Failed to obtain token"
}
```

**Possible Causes:**
- Authorization code expired (only valid for 10 minutes)
- Invalid redirect URI configured in Google Console
- Google Client ID or Secret is incorrect

**Solution:** 
- Get a fresh authorization code by clicking login again
- Verify Google Console OAuth settings match backend configuration

---

### ❌ ID Token Not Found (400 Bad Request)

```json
{
  "error": "ID token not found"
}
```

**Solution:** Ensure authorization code is valid and from Google.

---

### ❌ Invalid Google Token (400 Bad Request)

```json
{
  "error": "Invalid Google token"
}
```

**Possible Causes:**
- Token signature doesn't match Google's public keys
- Token expired
- Token was issued for a different Google App

**Solution:** Get a fresh authorization code from Google login.

---

### ❌ Email Not Provided by Google (400 Bad Request)

```json
{
  "error": "Email not provided by Google"
}
```

**Possible Causes:**
- User's Google account has no email
- User restricted email sharing in consent screen

**Solution:** Ask user to use a valid Google account with email.

---

### ❌ Email Not Verified (400 Bad Request)

```json
{
  "error": "Email not verified"
}
```

**Possible Causes:**
- User's Google account email is not verified by Google

**Solution:** Ask user to verify their email in Google account settings.

---

## 🔐 What Happens Behind the Scenes

1. **Frontend gets authorization code** from Google (via OAuth flow)
2. **Frontend sends code to backend** (this endpoint)
3. **Backend exchanges code for tokens** with Google
4. **Backend verifies token** - ensures it's from Google and your app
5. **Backend extracts user info** - email, name from Google
6. **Backend checks if user exists**:
   - ✅ **Exists:** Returns JWT tokens
   - ❌ **Doesn't exist:** Creates new user automatically and returns JWT tokens
7. **User is logged in** with JWT tokens

---
## ⚙️ Backend Configuration Required

**Your backend should have these Google credentials configured in `chat/api_keys.py`:**

```python
AUTH_GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
AUTH_GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
AUTH_GOOGLE_REDIRECT_URI = "http://localhost:3000/callback"
```

---

## 🔄 After Successful Login

**For New Users:**
- Account is created automatically
- User should complete their profile (First name, Last name, etc.)
- Redirect to `/profile-setup` or similar

**For Existing Users:**
- User is logged in immediately
- Redirect to `/dashboard`

**Store tokens and use them:**

```javascript
// Get the access token
const accessToken = localStorage.getItem('accessToken');

// Use it in API requests
const response = await fetch('http://localhost:8000/Users/user-info/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});
```

---

## 📌 Important Notes

✅ **Do's:**
- Always use authorization code flow (`flow: 'auth-code'`)
- Get fresh authorization code for each login attempt
- Store JWT tokens securely (httpOnly cookies preferred)
- Display user-friendly error messages

❌ **Don'ts:**
- Don't send Google access token directly to backend
- Don't store authorization code long-term
- Don't expose Client ID and Secret on frontend
- Don't use implicit flow (deprecated by Google)

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Invalid Google token" | Get fresh auth code, don't reuse expired ones |
| "Failed to obtain token" | Check Google Console redirect URI matches backend config |
| "Code is required" | Ensure OAuth flow completed successfully |
| User created but no name | Google account might have restricted name sharing |
| "Email not verified" | Ask user to verify email in Google account |

# ...existing code...