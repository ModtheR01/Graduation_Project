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

## � Password Reset

The password reset flow involves two steps: requesting a reset link via email, and then resetting the password using the link.

### Step 1: Request Password Reset

**Endpoint:** `https://romee.up.railway.app/Users/forgot-password/`

**Method:** `POST`

**Description:** Send a password reset link to the user's email address.

**Authentication:** ❌ Not required

**Request Body:**

```json
{
  "email": "user@example.com"
}
```

**Field Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| email | string | ✅ | Registered email address |

**Example Request (cURL):**

```bash
curl -X POST http://localhost:8000/Users/forgot-password/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com"
  }'
```

**Example Request (JavaScript/Fetch):**

```javascript
const response = await fetch('http://localhost:8000/Users/forgot-password/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john@example.com'
  })
});

const data = await response.json();
console.log(data.message); // Always returns success message for security
```

**Success Response (200 OK):**

```json
{
  "message": "If this email exists, a reset link was sent."
}
```

**Notes:**
- The response is always the same for security reasons (to prevent email enumeration)
- If the email exists, a reset link is sent to the user's email
- The reset link format: `https://romee-lake.vercel.app/reset-password/{uid}/{token}/`
- **Frontend Implementation:** Create a page at `/reset-password/{uid}/{token}` that extracts `uid` and `token` from the URL parameters and allows the user to enter a new password

### Step 2: Reset Password

**Endpoint:** `https://romee.up.railway.app/Users/reset-password/`

**Method:** `POST`

**Description:** Reset the user's password using the uid and token from the reset link.

**Authentication:** ❌ Not required

**Request Body:**

```json
{
  "uid": "encoded_user_id",
  "token": "reset_token",
  "new_password": "NewSecurePassword123"
}
```

**Field Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| uid | string | ✅ | Encoded user ID from the reset link URL |
| token | string | ✅ | Reset token from the reset link URL |
| new_password | string | ✅ | New password (minimum 6 characters) |

**Example Request (cURL):**

```bash
curl -X POST http://localhost:8000/Users/reset-password/ \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "MQ",
    "token": "abc123def456",
    "new_password": "NewPassword123"
  }'
```

**Example Request (JavaScript/Fetch):**

```javascript
// Extract uid and token from URL (e.g., /reset-password/MQ/abc123def456)
const urlParams = window.location.pathname.split('/');
const uid = urlParams[2]; // MQ
const token = urlParams[3]; // abc123def456

const response = await fetch('http://localhost:8000/Users/reset-password/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    uid: uid,
    token: token,
    new_password: 'NewSecurePassword123'
  })
});

const data = await response.json();
if (response.ok) {
  console.log('Password reset successful');
  // Redirect to login page
} else {
  console.error('Error:', data.error);
}
```

**Success Response (200 OK):**

```json
{
  "message": "Password reset successful"
}
```

**Error Responses:**

❌ **Invalid link (400 Bad Request):**
```json
{
  "error": "Invalid link"
}
```

❌ **Invalid or expired token (400 Bad Request):**
```json
{
  "error": "Invalid or expired token"
}
```

❌ **Password too weak (400 Bad Request):**
```json
{
  "error": "Password too weak"
}
```

### Frontend Implementation Guide

1. **Forgot Password Page:**
   - Form with email input
   - Submit to `/Users/forgot-password/`
   - Show success message (don't indicate if email exists or not)

2. **Reset Password Page:**
   - URL: `/reset-password/{uid}/{token}`
   - Extract `uid` and `token` from URL
   - Form with new password input
   - Submit to `/Users/reset-password/` with uid, token, and new_password
   - On success, redirect to login page
   - Handle errors (invalid link, expired token, weak password)

3. **Security Notes:**
   - Reset links expire after a certain time
   - Links can only be used once
   - Always validate password strength on frontend before submission

---

## �📚 All Endpoints

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

### �️ Delete User Account

**Endpoint:** `https://romee.up.railway.app/Users/delete_user/`

**Method:** `DELETE`

**Description:** Permanently delete the authenticated user's account.

**Authentication:** ✅ Required (JWT Token)

**Headers:**

```http
Authorization: Bearer <your_access_token>
```

**Request Body:** None

**Example Request (cURL):**

```bash
curl -X DELETE http://localhost:8000/Users/delete_user/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Example Request (JavaScript/Fetch):**

```javascript
const response = await fetch('http://localhost:8000/Users/delete_user/', {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});

const data = await response.json();
console.log(data);
```

**Success Response (200 OK):**

```json
{
  "message": "User account deleted successfully"
}
```

**Error Responses:**

❌ **Missing authentication (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 🗑️ Delete Chat

**Endpoint:** `https://romee.up.railway.app/chat/delete_chat/<chat_id>/`

**Method:** `DELETE`

**Description:** Delete a specific chat for the authenticated user.

**Authentication:** ✅ Required (JWT Token)

**Headers:**

```http
Authorization: Bearer <your_access_token>
```

**Request Body:** None

**Example Request (cURL):**

```bash
curl -X DELETE http://localhost:8000/chat/delete_chat/550e8400-e29b-41d4-a716-446655440000/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Example Request (JavaScript/Fetch):**

```javascript
const response = await fetch(`http://localhost:8000/chat/delete_chat/${chatId}/`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});

const data = await response.json();
console.log(data);
```

**Success Response (200 OK):**

```json
{
  "message": "Chat deleted successfully"
}
```

**Error Responses:**

❌ **Chat not found (404 Not Found):**
```json
{
  "error": "Chat not found"
}
```

❌ **Missing authentication (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### �💬 Send Chat Message

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

## 🛫 Flight Booking and Payment Flow

This section explains the complete flow for flight booking and payment processing. The system integrates with Stripe for secure payment handling.

### 📋 Overview

The booking flow involves:
1. **Chat Interaction**: User communicates with AI assistant via chat
2. **Flight Search**: AI searches for available flights
3. **Booking Initiation**: User selects a flight, AI creates booking with payment intent
4. **Payment Processing**: Frontend handles Stripe payment using client secret
5. **Confirmation**: Webhook confirms payment and creates ticket
6. **Ticket Retrieval**: User gets the final ticket

### 🔄 Step-by-Step Flow

#### Step 1: Send Chat Message (Flight Search)
Use the existing `/chat/chat/` endpoint to start the conversation.

**Example: Search for flights**
```javascript
const response = await fetch('http://localhost:8000/chat/chat/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  },
  body: JSON.stringify({
    message: 'Find flights from Cairo to Dubai on 2026-05-10'
  })
});

const data = await response.json();
console.log(data.response); // AI response with flight options
console.log(data.chat_id); // Save for continuation
```

#### Step 2: Book Selected Flight
Continue the chat to book a specific flight.

**Example: Book flight**
```javascript
const bookingResponse = await fetch('http://localhost:8000/chat/chat/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  },
  body: JSON.stringify({
    message: 'Book flight 1 with my details: John Doe, Male, 1990-01-01, john@example.com, +1234567890, A123456789, 2027-01-01, Egyptian',
    chat_id: data.chat_id
  })
});

const bookingData = await bookingResponse.json();
console.log(bookingData.response); // "Your booking is ready! Please complete the payment."
console.log(bookingData.payment_data); // Check if payment is required
```

**Payment Data Response:**
```json
{
  "response": "Your booking is ready! Please complete the payment.",
  "chat_id": "550e8400-e29b-41d4-a716-446655440000",
  "payment_data": {
    "required": true,
    "task_id": 123,
    "client_secret": "pi_xxx_secret_xxx"
  }
}
```

#### Step 3: Process Payment with Stripe
When `payment_data.required` is `true`, use the `client_secret` to process payment.

**Frontend Integration (Stripe.js):**
```html
<!-- Include Stripe.js -->
<script src="https://js.stripe.com/v3/"></script>
```

```javascript
// Initialize Stripe
const stripe = Stripe('your_publishable_key'); // Get from your Stripe dashboard

// When payment is required
if (bookingData.payment_data?.required) {
  const { client_secret } = bookingData.payment_data;
  
  // Confirm payment
  const result = await stripe.confirmPayment({
    clientSecret: client_secret,
    confirmParams: {
      return_url: 'https://yourapp.com/payment-success', // Optional redirect
    },
  });

  if (result.error) {
    console.error('Payment failed:', result.error.message);
  } else {
    console.log('Payment succeeded!');
    // Payment will be confirmed via webhook
  }
}
```

**Note:** Replace `'your_publishable_key'` with your actual Stripe publishable key.

#### Step 4: Payment Confirmation (Webhook)
Stripe automatically sends a webhook to confirm payment. No frontend action needed.

**Webhook Endpoint:** `POST /payment/webhook/stripe`
- This is handled server-side
- Updates booking status to "confirmed"
- Creates travel record

#### Step 5: Get Ticket
After payment confirmation, retrieve the ticket.

**Endpoint:** `GET /flights/get_ticket/?task_id=<task_id>`

**Example:**
```javascript
const ticketResponse = await fetch(`http://localhost:8000/flights/get_ticket/?task_id=${bookingData.payment_data.task_id}`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});

const ticketData = await ticketResponse.json();
console.log(ticketData.ticket);
```

**Success Response:**
```json
{
  "ticket": {
    "passenger": {
      "fname": "John",
      "lname": "Doe",
      "gender": "Male",
      "passport": "A123456789",
      "nationality": "Egyptian"
    },
    "flight": {
      "ticket_number": "ABC123456",
      "airline": "Emirates",
      "route": "Cairo → Dubai",
      "date": "2026-05-10",
      "time": "10:00 → 14:00",
      "price": "$285"
    },
    "status": "confirmed"
  }
}
```

### 🎯 Key Functions Involved

#### `send_message` (chat/views.py)
- Handles chat messages
- Detects payment requirements
- Returns payment data to frontend

#### `booking_flight` (flights/views.py)
- Creates booking task
- Generates Stripe payment intent
- Returns `[PAYMENT_REQUIRED]` to trigger payment flow

#### `create_payment_intent` (payment/utils.py)
- Creates Stripe PaymentIntent
- Converts price to cents
- Attaches metadata for tracking

#### `stripe_webhook` (payment/views.py)
- Receives payment confirmations from Stripe
- Updates task status
- Creates Traveling record for ticket

#### `get_ticket` (flights/views.py)
- Retrieves final ticket after payment
- Validates payment confirmation
- Returns passenger and flight details

### ⚠️ Important Notes

- **Authentication**: All endpoints require JWT token
- **Payment Security**: Never handle payment processing on frontend only
- **Webhook**: Must be configured in Stripe dashboard pointing to `/payment/webhook/`
- **Client Secret**: Use immediately and only once
- **Error Handling**: Check for payment failures and retry if needed
- **Status Checks**: Use `get_ticket` to verify payment before showing ticket

### 🔧 Frontend Implementation Tips

1. **Monitor Payment Data**: Always check `response.payment_data` in chat responses
2. **Stripe Integration**: Load Stripe.js and initialize with your publishable key
3. **User Feedback**: Show loading states during payment processing
4. **Error Recovery**: Handle payment failures gracefully
5. **Ticket Display**: Only show ticket after successful `get_ticket` call

### 📊 Status Flow

```
User Message → AI Search → Flight Selection → Booking Creation → Payment Intent → Stripe Payment → Webhook → Status Update → Ticket Available
```

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
# 🏨 Hotels API Documentation

Complete API guide for hotel search, booking, payment, and confirmation features.

---

## 📋 Table of Contents
1. [Quick Overview](../HOTELS_BOOKING_API.md#-quick-overview)
2. [Search Hotels](../HOTELS_BOOKING_API.md#-search-hotels)
3. [Hotel Booking](../HOTELS_BOOKING_API.md#-hotel-booking)
4. [Payment Processing](../HOTELS_BOOKING_API.md#-payment-processing)
5. [Webhook Handler](../HOTELS_BOOKING_API.md#-webhook-handler)
6. [Complete Workflow](../HOTELS_BOOKING_API.md#-complete-workflow)
7. [Error Handling](../HOTELS_BOOKING_API.md#-error-handling)

---

## 📌 Quick Overview

**Base URL:** `http://localhost:8000/` or `https://romee.up.railway.app/`

**Authentication:** JWT Token (required for most endpoints)

**Payment Provider:** Stripe

**External APIs Used:**
- Booking.com API via RapidAPI (for hotel search)
- Stripe API (for payment processing)

---

## 🔍 Search Hotels

### `search_hotels()` - LangChain Tool

**Location:** `backend/Hotels/views.py`

**Method Type:** LangChain Tool (Called by AI Agent)

**Description:** 
Searches for available hotels in a given city/country within a specified date range. This function fetches data from the external Booking.com API and formats it for frontend consumption.

**Parameters:**

```python
search_hotels(
    country: str,        # City or country name (e.g., "Cairo", "Paris")
    arr_date: str,       # Check-in date in YYYY-MM-DD format (e.g., "2026-05-01")
    dep_date: str,       # Check-out date in YYYY-MM-DD format (e.g., "2026-05-05")
    num_of_adults: int,  # Number of adults (e.g., 2)
    num_of_rooms: int    # Number of rooms (e.g., 1)
)
```

**Return Value - Success:**

The function returns a JSON string wrapped in `[FINAL_ANSWER]` tag:

```json
{
  "[FINAL_ANSWER]{\"hotels\": [
    {
      \"id\": 1,
      \"real_id\": 12345,
      \"name\": \"LA Cairo Plaza Hotel\",
      \"rating\": 10.0,
      \"price\": 73.72,
      \"num of rooms\": 1,
      \"currency\": \"USD\",
      \"images\": [
        \"https://cf.bstatic.com/image1.jpg\",
        \"https://cf.bstatic.com/image2.jpg\"
      ],
      \"stars\": 5,
      \"booking_info\": {
        \"checkin_from\": \"10:00\",
        \"checkin_until\": \"12:00\",
        \"checkout_from\": \"11:00\",
        \"checkout_until\": \"13:00\"
      }
    },
    {
      \"id\": 2,
      \"real_id\": 12346,
      \"name\": \"Nile View Hotel\",
      \"rating\": 8.5,
      \"price\": 55.00,
      \"num of rooms\": 1,
      \"currency\": \"USD\",
      \"images\": [...],
      \"stars\": 4,
      \"booking_info\": {...}
    }
  ]}"
}
```

**User-Facing Display:**

```
Here are the available hotels in Cairo from 24/04/2026 to 05/05/2026:
| # | Hotel Name | Rating | Price | Stars | Check-in | Check-out | Images |
|---|------------|--------|-------|-------|----------|-----------|--------|
| 1 | LA Cairo Plaza Hotel | 10.0 | 73.72 USD | ⭐⭐⭐⭐⭐ | 10:00 → 12:00 | 11:00 → 13:00 | [Img1](https://cf.bstatic.com/image1.jpg), [Img2](https://cf.bstatic.com/image2.jpg) |
| 2 | Nile View Hotel | 8.5 | 55.00 USD | ⭐⭐⭐⭐ | 14:00 → 23:00 | 06:00 → 12:00 | [Img1](https://cf.bstatic.com/image3.jpg), [Img2](https://cf.bstatic.com/image4.jpg) |
Would you like to book any of these hotels? Just let me know which one!
```

**Return Value - Failure:**

```python
"no hotels found"                    # When no hotels match the search criteria
"message: {error_details}"           # When an error occurs during search
```

**Example Usage:**

```python
# Example 1: Search hotels in Cairo
search_hotels(
    country="Cairo",
    arr_date="2026-05-01",
    dep_date="2026-05-05",
    num_of_adults=2,
    num_of_rooms=1
)

# Example 2: Search hotels in Paris
search_hotels(
    country="Paris",
    arr_date="2026-06-10",
    dep_date="2026-06-15",
    num_of_adults=1,
    num_of_rooms=1
)
```

**Important Notes:**

| Point | Details |
|-------|---------|
| ✅ Max Results | Only returns top 5 hotels |
| ✅ Images | Always provides exactly 2 image URLs (same image repeated if only 1 available) |
| ✅ State Storage | Results stored in `state_store["last_offers"]` for booking reference |
| ⚠️ Date Format | Must be exactly `YYYY-MM-DD` format |
| ⚠️ Destination Validation | City name must be recognized by Booking.com API |

---

## 🎫 Hotel Booking

### `booking_hotel()` - LangChain Tool

**Location:** `backend/Hotels/views.py`

**Method Type:** LangChain Tool (Called by AI Agent)

**Description:**
Initiates a hotel booking by creating a task record and setting up payment via Stripe. Once successfully created, the booking enters "pending" status and awaits payment confirmation.

**Parameters:**

```python
booking_hotel(
    offer_id: int,           # Hotel offer ID from search results (1, 2, 3, ...)
    Fname: str,              # First name (e.g., "Ahmed")
    Lname: str,              # Last name (e.g., "Mohamed")
    gender: str,             # Gender (e.g., "Male" or "Female")
    BD: str,                 # Birth date in YYYY-MM-DD format (e.g., "1990-01-15")
    national_id_num: int,    # National ID number
    email: str,              # Email address
    phone_number: str,       # Phone number with country code
    nationality: str         # Nationality (e.g., "Egyptian")
)
```

**Process Flow:**

1. **Validate Offer ID:**
   - Checks if offer exists in `state_store["last_offers"]`
   - Returns error if not found

2. **Create Booking Data Structure:**
   ```python
   {
     "hotel": offer,  # Selected hotel data
     "price": "73.72",  # Booking price
     "user": {
       "fname": "Ahmed",
       "lname": "Mohamed",
       "gender": "Male",
       "birth_date": "1990-01-15",
       "email": "ahmed@example.com",
       "phone": "+201234567890",
       "nationality": "Egyptian",
       "national id number": 12345678
     },
     "status": "pending"
   }
   ```

3. **Create Task in Database:**
   - Stores booking data in `Tasks` table
   - Links to current `chat_id`
   - Sets `task_type = "hotel_booking"`

4. **Initialize Payment Intent:**
   - Calls `create_payment_intent_hotels()`
   - Retrieves `client_secret` and `payment_intent_id`
   - Stores payment references in the task

**Return Values:**

### ✅ Success:
```python
"[PAYMENT_REQUIRED]"
```

**Action Required:** Display payment confirmation message:
```
"Your booking is ready! The Payment will appear here, Please complete the payment."
```

### ❌ Failures:

| Error | Meaning | Action |
|-------|---------|--------|
| `{"error": "Invalid offer ID"}` | Offer not found in search results | Perform new search |
| `{"error": "Payment system configuration error."}` | Stripe API key issue | Contact support |
| `{"error": "Invalid payment data: {details}"}` | Incomplete/invalid booking data | Verify all fields |
| `{"error": "Cannot connect to payment provider. Try again."}` | Stripe API connection failure | Retry later |
| `{"error": "Payment error. Please try again."}` | General payment error | Retry operation |
| `{"error": "Booking data is incomplete."}` | Missing required information | Verify all user data |

**Example Request:**

```python
booking_hotel(
    offer_id=1,
    Fname="Ahmed",
    Lname="Mohamed",
    gender="Male",
    BD="1990-01-15",
    national_id_num=12345678,
    email="ahmed@example.com",
    phone_number="+201234567890",
    nationality="Egyptian"
)
```

**Frontend Implementation Example:**

```javascript
// Handle booking response
if (response.includes("[PAYMENT_REQUIRED]")) {
  // Show confirmation message
  showMessage("Your booking is ready! The Payment will appear here, Please complete the payment.");
  
  // Extract payment details from context
  const { clientSecret, paymentIntentId } = getPaymentDetails();
  
  // Navigate to payment page
  navigateToPayment(clientSecret);
}
```

**Important Constraints:**

| Constraint | Details |
|-----------|---------|
| ⚠️ Valid Offer | `offer_id` must exist in current search results |
| ⚠️ Date Format | Birth date must be `YYYY-MM-DD` |
| ⚠️ Phone Format | Must include country code (e.g., +201234567890) |
| ⚠️ Email Validation | Must be a valid email format |
| ✅ Auto-Cleanup | Failed bookings auto-delete from database |

---

## 💳 Payment Processing

### `create_payment_intent_hotels()` - Payment Utility

**Location:** `backend/payment/utils.py`

**Type:** Internal utility function (called by `booking_hotel()`)

**Description:**
Creates a Stripe Payment Intent for processing hotel booking payments. This generates a `client_secret` that the frontend uses to confirm payment through Stripe.js.

**Parameters:**

```python
create_payment_intent_hotels(
    booking: dict,     # Booking data dictionary containing price and hotel info
    task_id: int       # Database task ID for tracking
)
```

**Booking Dictionary Structure:**

```python
{
    "price": 73.72,  # Must be convertible to float
    "hotel": {
        "name": "LA Cairo Plaza Hotel"
    },
    "user": {
        "email": "ahmed@example.com"
    }
}
```

**Internal Processing:**

1. **Extract & Convert Amount:**
   ```python
   price_float = float(73.72)
   price_in_cents = int(price_float * 100)  # = 7372 cents
   ```

2. **Create Stripe Payment Intent:**
   ```python
   stripe.PaymentIntent.create(
       amount=7372,                          # Amount in cents
       currency="usd",                       # USD currency
       receipt_email="ahmed@example.com",    # Auto-send receipt
       automatic_payment_methods={
           "enabled": True,                  # Enable all payment methods
           "allow_redirects": "never"        # Prevent auto-redirect
       },
       metadata={
           "task_id": "123",
           "email": "ahmed@example.com",
           "hotel": "LA Cairo Plaza Hotel"
       },
       description="Hotel Name: LA Cairo Plaza Hotel"
   )
   ```

**Return Value:**

```python
(
    "pi_1K4y8D2eZvKYlo2CpBjzQquj_secret_abc123",  # client_secret
    "pi_1K4y8D2eZvKYlo2CpBjzQquj"                  # payment_intent_id
)
```

**Return Value Properties:**

| Property | Usage | Where to Use |
|----------|-------|-------------|
| `client_secret` | Confirms payment in frontend | Send to Stripe.js |
| `payment_intent_id` | Track payment in database | Store in Task record |

**Error Handling:**

```python
stripe.error.AuthenticationError          # Invalid API credentials
stripe.error.InvalidRequestError          # Invalid payment data
stripe.error.APIConnectionError           # Cannot reach Stripe servers
stripe.error.StripeError                  # Generic Stripe error
```

**Frontend Integration - Stripe.js:**

```javascript
// 1. Initialize Stripe
const stripe = Stripe('pk_test_YOUR_PUBLISHABLE_KEY');
const elements = stripe.elements();
const cardElement = elements.create('card');
cardElement.mount('#card-element');

// 2. Confirm Payment with client_secret
stripe.confirmCardPayment(clientSecret, {
    payment_method: {
        card: cardElement,
        billing_details: {
            name: 'Ahmed Mohamed',
            email: 'ahmed@example.com'
        }
    }
})
.then(result => {
    if (result.error) {
        // Payment failed
        console.error('Payment failed:', result.error.message);
        showError(result.error.message);
    } else {
        // Payment succeeded
        console.log('Payment successful!');
        showSuccess('Payment completed. Your booking is confirmed.');
    }
});
```

**Important Notes:**

| Note | Details |
|------|---------|
| ⚠️ Amount | Must be in **cents** (multiply by 100) |
| ✅ Automatic Methods | Multiple payment methods enabled by default |
| ✅ No Redirect | Prevents unwanted page redirects |
| 📧 Receipt Email | Automatically sent to the provided email |
| 🔒 Metadata | Used by webhook to match payment with booking |

---

## 🔗 Webhook Handler

### `stripe_webhook()` - Payment Confirmation Handler

**Location:** `backend/payment/views.py`

**Endpoint:** Must be registered with Stripe (configured in backend)

**Method:** POST

**Description:**
Webhook endpoint that receives payment confirmation events from Stripe. When a payment succeeds, this endpoint creates the final booking record in the database.

**How It Works:**

```
1. User completes payment on frontend
   ↓
2. Stripe processes payment
   ↓
3. Stripe sends 'payment_intent.succeeded' event to webhook
   ↓
4. Webhook verifies Stripe signature
   ↓
5. Webhook retrieves task from database using metadata
   ↓
6. Webhook creates booking record in Hotels table
   ↓
7. Webhook updates task status to 'confirmed'
```

**Webhook Event Structure:**

```json
{
    "type": "payment_intent.succeeded",
    "data": {
        "object": {
            "id": "pi_1K4y8D2eZvKYlo2CpBjzQquj",
            "status": "succeeded",
            "amount": 7372,
            "currency": "usd",
            "metadata": {
                "task_id": "123",
                "email": "ahmed@example.com",
                "hotel": "LA Cairo Plaza Hotel"
            }
        }
    }
}
```

**Security Verification:**

```python
# Webhook verifies signature using Stripe_Webhook_Secret
event = stripe.Webhook.construct_event(
    payload,           # Request body from Stripe
    sig_header,        # Stripe-Signature header
    Stripe_Webhook_Secret  # Secret key (prevents fake requests)
)
```

**Processing Hotel Booking:**

When `task.task_type == "hotel_booking"`:

1. **Extract Hotel Data:**
   ```python
   hotel = task.booking_data.get("hotel", {})
   booking_data = task.booking_data
   ```

2. **Generate Unique Booking Number:**
   ```python
   booking_number = "BK-A1B2C3D4"  # Format: BK-{8 random chars}
   ```

3. **Create Hotel Record:**
   ```python
   Hotels.objects.create(
       task_id=123,
       booking_number="BK-A1B2C3D4",
       hotel_name="LA Cairo Plaza Hotel",
       number_of_persons=booking_data.get("num_of_adults"),
       number_of_rooms=booking_data.get("num_of_rooms"),
       check_in_date="2026-05-01",
       check_out_date="2026-05-05"
   )
   ```

4. **Update Task Status:**
   ```python
   task.booking_data["status"] = "confirmed"
   task.save()
   ```

**HTTP Response Codes:**

| Code | Meaning | Scenario |
|------|---------|----------|
| 200 | Success | Payment processed / Booking already exists |
| 400 | Bad Request | Invalid signature / malformed payload |
| 404 | Not Found | Task ID from metadata doesn't exist |
| 500 | Server Error | Database error creating hotel record |

**Logging & Monitoring:**

```python
# Success logging
print("✅ Payment confirmed for task: 123")

# Error logging
print("Error creating Hotel record: {error_details}")
```

**Important Security Notes:**

| Security Aspect | Details |
|-----------------|---------|
| 🔒 Signature Verification | **Always verify** webhook signature |
| 🔒 Idempotency | Handles duplicate events gracefully (returns 200) |
| 🔒 No Side Effects | Failed hotel creation returns 500 without task update |
| ✅ Auto-Retry | Stripe retries failed webhook deliveries |

---

## 🎟️ Get Hotel Booking

### `get_hotel_booking()` - Booking Confirmation Retrieval

**Location:** `backend/Hotels/views.py`

**Endpoint:** `GET /Hotels/get_hotel_booking/`

**Method Type:** HTTP GET Request

**Description:**
Retrieves the complete hotel booking confirmation details after successful payment. This endpoint verifies that the payment has been confirmed via Stripe, ensures the booking record exists, and returns all relevant booking information to the frontend for display.

**Parameters:**

```
GET /Hotels/get_hotel_booking/?task_id=<task_id>
```

| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| task_id | integer | ✅ | Task ID returned from payment processing |

**Request Headers:**
```
Authorization: Bearer <JWT_ACCESS_TOKEN>
Content-Type: application/json
```

**Process Flow:**

1. **Retrieve Task Record:**
   - Fetches the Task object from database using `task_id`
   - Returns 404 if task not found

2. **Verify Payment Status:**
   - Checks if booking status is "confirmed"
   - If not confirmed, checks Stripe payment intent status
   - Updates task status to "confirmed" if payment succeeded

3. **Validate Hotel Record:**
   - Ensures corresponding hotel booking record exists in database
   - Returns 404 if hotel record not created yet

4. **Return Booking Details:**
   - Formats and returns all booking information
   - Includes guest details, hotel info, and confirmation number

**Example Request (cURL):**

```bash
curl -X GET "http://localhost:8000/Hotels/get_hotel_booking/?task_id=123" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

**Example Request (JavaScript/Fetch):**

```javascript
const taskId = 123;  // Received from booking_hotel response
const accessToken = localStorage.getItem('accessToken');

const response = await fetch(`http://localhost:8000/Hotels/get_hotel_booking/?task_id=${taskId}`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});

const bookingData = await response.json();

if (response.ok) {
  console.log('Booking Confirmed:', bookingData.booking);
  // Display booking details to user
} else {
  console.error('Error:', bookingData.error);
}
```

**✅ Success Response (200 OK):**

```json
{
  "booking": {
    "booking_number": "BK-A1B2C3D4",
    "hotel_name": "LA Cairo Plaza Hotel",
    "check_in": "2026-05-01",
    "check_out": "2026-05-05",
    "rooms": 1,
    "persons": 2,
    "guest": {
      "fname": "Ahmed",
      "lname": "Mohamed",
      "email": "ahmed@example.com",
      "nationality": "Egyptian"
    },
    "status": "confirmed"
  }
}
```

**Response Field Details:**

| Field | Type | Description |
|-------|------|-------------|
| booking_number | string | Unique confirmation number (Format: BK-{8 chars}) |
| hotel_name | string | Name of the booked hotel |
| check_in | date | Check-in date (YYYY-MM-DD format) |
| check_out | date | Check-out date (YYYY-MM-DD format) |
| rooms | integer | Number of booked rooms |
| persons | integer | Number of guests |
| guest.fname | string | Guest first name |
| guest.lname | string | Guest last name |
| guest.email | string | Guest email address |
| guest.nationality | string | Guest nationality |
| status | string | Booking status (always "confirmed" for success) |

**❌ Error Responses:**

### ❌ Missing task_id Parameter (400 Bad Request)

```json
{
  "error": "task_id is required"
}
```

**Solution:** Include `task_id` as query parameter in the URL.

```javascript
// ✅ Correct
/Hotels/get_hotel_booking/?task_id=123

// ❌ Wrong
/Hotels/get_hotel_booking/
```

---

### ❌ Task Not Found (404 Not Found)

```json
{
  "error": "Task not found"
}
```

**Possible Causes:**
- Invalid `task_id` provided
- Task was deleted from database
- Task ID from different user

**Solution:**
```
✅ Verify task_id is correct
✅ Ensure booking was initiated by this user
✅ Check task_id immediately after booking
```

---

### ❌ Payment Not Initiated (400 Bad Request)

```json
{
  "error": "Payment not initiated"
}
```

**Meaning:** Task exists but no payment intent was created.

**Possible Causes:**
- Booking creation failed before payment
- Incomplete payment setup

**Solution:** Reattempt booking from beginning.

---

### ❌ Payment Not Confirmed (402 Payment Required)

```json
{
  "error": "Payment not confirmed yet"
}
```

**Meaning:** Payment has not been verified yet.

**Possible Causes:**
- Stripe webhook hasn't processed payment yet
- User hasn't completed payment
- Payment is still pending

**Solution:**
```
✅ Wait a few seconds (webhook may be processing)
✅ Retry the request
✅ Verify payment was completed in Stripe dashboard
```

---

### ❌ Hotel Record Not Ready (404 Not Found)

```json
{
  "error": "Booking not ready yet"
}
```

**Meaning:** Payment is confirmed, but hotel booking record hasn't been created yet.

**Possible Causes:**
- Webhook processing delay
- Database transaction in progress
- Webhook failed to create hotel record

**Solution:**
```
✅ Retry after 2-3 seconds
✅ Check browser console for errors
✅ Verify webhook is configured correctly
✅ Contact support if persists
```

---

### ❌ Could Not Verify Payment (500 Internal Server Error)

```json
{
  "error": "Could not verify payment"
}
```

**Meaning:** Backend failed to check payment status with Stripe.

**Possible Causes:**
- Stripe API connection failure
- Invalid Stripe API key
- Stripe account issues

**Solution:**
```
✅ Retry after 30 seconds
✅ Check if Stripe is operational
✅ Contact support
```

---

### ❌ Not Authenticated (401 Unauthorized)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Meaning:** JWT token is missing or invalid.

**Solution:**
```javascript
// ✅ Ensure token is included
const accessToken = localStorage.getItem('accessToken');
if (!accessToken) {
  // User must log in
  redirectToLogin();
}
```

---

## 🔄 Complete Booking Flow with get_hotel_booking()

### Full User Journey Including Confirmation

```
Step 1: SEARCH HOTELS
└─ User: "Find hotels in Cairo from 2026-05-01 to 2026-05-05"
└─ Response: 5 hotels displayed

Step 2: BOOK SELECTED HOTEL
└─ User: "Book hotel #1 with my details..."
└─ Backend: Creates task, generates payment intent
└─ Response: "[PAYMENT_REQUIRED]" + client_secret
└─ Store: Save task_id for later confirmation

Step 3: PROCESS PAYMENT
└─ Frontend: stripe.confirmCardPayment(clientSecret)
└─ User: Completes payment in Stripe modal
└─ Backend: Webhook creates hotel booking record
└─ Status: Task marked as "confirmed"

Step 4: RETRIEVE BOOKING CONFIRMATION (← This step)
└─ Frontend: GET /Hotels/get_hotel_booking/?task_id=123
└─ Backend: Verifies payment, returns booking details
└─ Frontend: Display confirmation with booking number
└─ User: Sees: BK-A1B2C3D4, Hotel name, Check-in/out dates
```

---

### Frontend Integration Example

```javascript
// Step 1: Extract task_id from payment response
let bookingTaskId;

async function initiateBooking() {
  const bookingResponse = await fetch('/chat/chat/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: `Book hotel #1 with details: Ahmed Mohamed, Male, 1990-01-15, ahmed@example.com, +201234567890, 12345678, Egyptian`,
      chat_id: currentChatId
    })
  });

  const bookingData = await bookingResponse.json();
  
  // Extract task_id from payment data
  if (bookingData.payment_data) {
    bookingTaskId = bookingData.payment_data.task_id;
    console.log('Task ID saved:', bookingTaskId);
    
    // Proceed to payment
    await processPayment(bookingData.payment_data.client_secret);
  }
}

// Step 2: After payment succeeds, retrieve booking
async function retrieveBookingConfirmation() {
  try {
    const response = await fetch(`/Hotels/get_hotel_booking/?task_id=${bookingTaskId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.status === 402) {
      // Payment not confirmed yet, retry after delay
      console.log('Payment confirmation pending, retrying...');
      setTimeout(retrieveBookingConfirmation, 2000);
      return;
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error);
    }

    const bookingData = await response.json();
    displayBookingConfirmation(bookingData.booking);
    
  } catch (error) {
    console.error('Failed to retrieve booking:', error);
    showErrorMessage(error.message);
  }
}

// Step 3: Display confirmation to user
function displayBookingConfirmation(booking) {
  const confirmationHTML = `
    <div class="booking-confirmation">
      <h2>✅ Booking Confirmed!</h2>
      <p><strong>Booking Number:</strong> ${booking.booking_number}</p>
      <p><strong>Hotel:</strong> ${booking.hotel_name}</p>
      <p><strong>Check-in:</strong> ${booking.check_in}</p>
      <p><strong>Check-out:</strong> ${booking.check_out}</p>
      <p><strong>Rooms:</strong> ${booking.rooms}</p>
      <p><strong>Guests:</strong> ${booking.persons}</p>
      <p><strong>Guest Name:</strong> ${booking.guest.fname} ${booking.guest.lname}</p>
      <p><strong>Email:</strong> ${booking.guest.email}</p>
      <p><strong>Status:</strong> ${booking.status}</p>
    </div>
  `;
  
  document.getElementById('booking-confirmation-container').innerHTML = confirmationHTML;
}
```

---

### Timing Considerations

| Step | Typical Duration | Notes |
|------|-----------------|-------|
| Payment processing | 1-2 seconds | Stripe processes immediately |
| Webhook delivery | 1-5 seconds | AWS queue may add delay |
| Hotel record creation | <1 second | Instant database insert |
| **Total delay** | **2-6 seconds** | Recommend 1-second polling/retry |

**Frontend Recommendation:**
```javascript
// Poll for confirmation (user-friendly approach)
async function pollForConfirmation(maxAttempts = 10) {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      const response = await fetch(`/Hotels/get_hotel_booking/?task_id=${bookingTaskId}`, {...});
      
      if (response.ok) {
        return await response.json();
      }
      
      if (response.status !== 402) {
        throw new Error(await response.json());
      }
      
      // Status 402: Not ready yet, wait and retry
      await new Promise(resolve => setTimeout(resolve, 1000));
      
    } catch (error) {
      console.error('Attempt', attempt + 1, 'failed:', error);
    }
  }
  
  throw new Error('Booking confirmation timeout. Please refresh to check status.');
}
```

---

## 🔄 Complete Workflow

### Full User Journey

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BOOKING FLOW                         │
└─────────────────────────────────────────────────────────────┘

Step 1: SEARCH PHASE
├─ User specifies: Country, Check-in, Check-out, Guests, Rooms
├─ Frontend triggers: search_hotels()
├─ Backend fetches: Hotel list from Booking.com API
├─ Response: 5 hotels with details (stored in state_store)
└─ Display: Hotel table with options

Step 2: SELECTION PHASE
├─ User selects: Hotel #1
├─ User provides: Personal information (name, email, phone, etc.)
├─ Frontend validates: All required fields
└─ Ready: For booking

Step 3: BOOKING PHASE
├─ Frontend calls: booking_hotel(offer_id=1, user_data...)
├─ Backend creates: Task record (status: pending)
├─ Backend calls: create_payment_intent_hotels()
├─ Response: [PAYMENT_REQUIRED] + client_secret
└─ Display: Payment form

Step 4: PAYMENT PHASE
├─ User enters: Card details
├─ Frontend calls: Stripe.confirmCardPayment(clientSecret)
├─ Stripe processes: Payment
├─ Stripe sends: payment_intent.succeeded to webhook
└─ Display: Processing message

Step 5: CONFIRMATION PHASE
├─ Webhook receives: Payment confirmation
├─ Webhook verifies: Stripe signature
├─ Webhook creates: Hotel booking record
├─ Webhook updates: Task status to 'confirmed'
├─ Webhook returns: HTTP 200 OK
└─ Display: Confirmation page with booking number
```

### Example Request/Response Sequence

#### Request 1: Search Hotels
```javascript
// Frontend
const response = await callAI({
  message: "Search hotels in Cairo from 2026-05-01 to 2026-05-05 for 2 adults in 1 room"
});

// Backend processes: search_hotels("Cairo", "2026-05-01", "2026-05-05", 2, 1)
// Response includes hotel table with 5 options
```

#### Request 2: Book Hotel
```javascript
// Frontend
const response = await callAI({
  message: "Book hotel #1. My name is Ahmed Mohamed, email: ahmed@example.com, phone: +201234567890"
});

// Backend processes: booking_hotel(1, "Ahmed", "Mohamed", ..., "egyptian")
// Response: "[PAYMENT_REQUIRED]"
// Also returns: clientSecret, paymentIntentId
```

#### Request 3: Confirm Payment (Stripe)
```javascript
// Frontend
const result = await stripe.confirmCardPayment(clientSecret, {
  payment_method: {
    card: cardElement,
    billing_details: { name: 'Ahmed Mohamed' }
  }
});

// Stripe processes payment → sends webhook
// Backend: stripe_webhook() creates hotel booking record
// Response: HTTP 200 OK + Task status updated to 'confirmed'
```

---

## ⚠️ Error Handling

### Common Issues & Solutions

#### 1. "no hotels found"

**Possible Causes:**
```
❌ City name not recognized by Booking.com API
❌ Date format incorrect (not YYYY-MM-DD)
❌ Invalid API key or connection issue
```

**Solutions:**
```python
# ✅ Correct format
search_hotels(country="Cairo", arr_date="2026-05-01", dep_date="2026-05-05", num_of_adults=2, num_of_rooms=1)

# ✅ Try alternative city names
"Cairo" / "Giza"  # For Egypt
"Paris" / "Île-de-France"  # For France

# ✅ Verify date format
arr_date="2026-05-01"  # ✅ Correct: YYYY-MM-DD
arr_date="01-05-2026"  # ❌ Wrong format
arr_date="2026/05/01"  # ❌ Wrong separator
```

#### 2. "Invalid offer ID"

**Causes:**
```
❌ Offer ID doesn't match search results
❌ Previous search expired
❌ User performed new search after selection
```

**Solution:**
```python
# Always use IDs from current search
# If user searches again, IDs reset (1, 2, 3, ...)
booking_hotel(offer_id=1, ...)  # ✅ From current search results
```

#### 3. Payment System Configuration Error

**Causes:**
```
❌ Stripe API key invalid/missing
❌ Backend environment variables not set
❌ Stripe account not properly configured
```

**Solution:**
```python
# Check environment variables
STRIPE_SECRET_KEY = "sk_test_..."  # ✅ Should be present
STRIPE_WEBHOOK_SECRET = "whsec_..."  # ✅ Should be present

# Verify Stripe account
- Test mode is enabled
- API keys are valid
- Webhook endpoint registered
```

#### 4. "Payment error. Please try again."

**Causes:**
```
❌ Network connectivity issue
❌ Stripe servers temporarily down
❌ Card declined
```

**Solution:**
```
✅ Retry after 30 seconds
✅ Check card validity
✅ Verify sufficient funds
✅ Contact Stripe support if persistent
```

#### 5. Webhook Not Triggering

**Causes:**
```
❌ Webhook URL not registered in Stripe dashboard
❌ Webhook endpoint returning non-200 status
❌ Signature verification failing
```

**Solution:**
```
✅ Register webhook in Stripe Dashboard:
   - Event: payment_intent.succeeded
   - URL: https://yourdomain.com/payment/stripe-webhook/

✅ Ensure endpoint returns 200 OK

✅ Verify STRIPE_WEBHOOK_SECRET is correct
```

### Error Response Examples

```javascript
// Frontend error handling
try {
  const response = await bookHotel(bookingData);
  
  if (response.includes("[PAYMENT_REQUIRED]")) {
    navigateToPayment();
  } else if (response.error) {
    showError(response.error);  // Display error message
  }
} catch (error) {
  console.error('Booking failed:', error);
  showError('An unexpected error occurred. Please try again.');
}
```

---

## 📊 Data Models

### Hotel Object Structure

```javascript
{
  "id": 1,                          // Sequential ID (1, 2, 3, ...)
  "real_id": 12345,                 // Booking.com real ID
  "name": "LA Cairo Plaza Hotel",   // Hotel name
  "rating": 10.0,                   // Review rating (0-10)
  "price": 73.72,                   // Total price for all rooms (USD)
  "num of rooms": 1,                // Number of rooms
  "currency": "USD",                // Currency code
  "images": [                       // Hotel images
    "https://cf.bstatic.com/image1.jpg",
    "https://cf.bstatic.com/image2.jpg"
  ],
  "stars": 5,                       // Star rating (1-5)
  "booking_info": {                 // Check-in/Check-out details
    "checkin_from": "10:00",
    "checkin_until": "12:00",
    "checkout_from": "11:00",
    "checkout_until": "13:00"
  }
}
```

### Task Object Structure

```python
{
    "id": 123,
    "chat_id": "abc-123",
    "task_type": "hotel_booking",
    "created_at": "2026-04-25 14:30:00",
    "booking_data": {
        "hotel": {...},
        "price": 73.72,
        "user": {
            "fname": "Ahmed",
            "lname": "Mohamed",
            "gender": "Male",
            "birth_date": "1990-01-15",
            "email": "ahmed@example.com",
            "phone": "+201234567890",
            "nationality": "Egyptian",
            "national id number": 12345678
        },
        "status": "pending/confirmed",
        "payment_intent_id": "pi_...",
        "client_secret": "pi_..._secret_..."
    }
}
```

### Booking Confirmation Record

```python
{
    "id": 1,
    "task_id": 123,
    "booking_number": "BK-A1B2C3D4",
    "hotel_name": "LA Cairo Plaza Hotel",
    "number_of_persons": 2,
    "number_of_rooms": 1,
    "check_in_date": "2026-05-01",
    "check_out_date": "2026-05-05",
    "created_at": "2026-04-25 14:35:00"
}
```

---

## 🔒 Security Considerations

### For Frontend Developers

**DO:**
```javascript
✅ Use HTTPS for all requests
✅ Store client_secret in sessionStorage (temporary)
✅ Never log sensitive payment data
✅ Validate user input before sending
✅ Use official Stripe.js library
✅ Implement CSP headers
```

**DON'T:**
```javascript
❌ Store card numbers (frontend)
❌ Store client_secret in localStorage
❌ Log payment details
❌ Send raw card data to backend
❌ Hardcode API keys
❌ Use unofficial payment libraries
```

### For Backend Developers

**DO:**
```python
✅ Store API keys in environment variables
✅ Verify webhook signatures
✅ Log payment events
✅ Implement rate limiting
✅ Use try-catch for all Stripe calls
✅ Validate all input data
```

**DON'T:**
```python
❌ Hardcode API keys in code
❌ Skip signature verification
❌ Process payments without verification
❌ Store card numbers
❌ Log sensitive data to files
❌ Trust client-provided data
```

---

## 📚 Related Resources

- [Stripe Documentation](https://stripe.com/docs)
- [Stripe.js Reference](https://stripe.com/docs/js)
- [Booking.com API](https://rapidapi.com/booking-com15/api/booking-com15)
- [Django Documentation](https://docs.djangoproject.com/)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)

---

## 🔄 API Endpoints Summary

| Function | Type | Status Code | Response |
|----------|------|-------------|----------|
| `search_hotels()` | LangChain Tool | N/A | JSON array of hotels |
| `booking_hotel()` | LangChain Tool | N/A | `[PAYMENT_REQUIRED]` or error |
| `create_payment_intent_hotels()` | Utility | N/A | `(client_secret, intent_id)` |
| `stripe_webhook()` | Webhook | 200/400/404/500 | HTTP status |

---

**Last Updated:** April 25, 2026  
**Version:** 1.0  
**Status:** ✅ Complete

For questions or updates, contact the backend development team.
