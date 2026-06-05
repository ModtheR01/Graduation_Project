# TO_DO_List API Documentation

## Overview
كل endpoints الخاصة بتطبيق `TO_DO_List` موجودة تحت مسار الجذر:

- `/todo/`

كل هذه الواجهات تتطلب مستخدم مصادق عليه بواسطة JWT، لذلك يجب إرسال هيدر:

- `Authorization: Bearer <access_token>`

---

## Endpoints

### 1. Get all lists
- Method: `GET`
- URL: `/todo/lists/`
- Auth: مطلوب

#### Response
- `200 OK`
  - {
    "data": [
      {
        "list_name": "<name>",
        "user": <user_id>,
        "task": null,
        "finished": false
      },
      ...
    ]
  }
- إذا لا توجد قوائم:
  - {
    "error": "there is no available lists for this user "
  }

---

### 2. Get items in a list
- Method: `GET`
- URL: `/todo/lists/<list_name>/`
- Auth: مطلوب

#### URL Params
- `list_name`: اسم القائمة.

#### Response
- `200 OK`
  - مصفوفة بالعناصر في القائمة:
    - [
      {
        "list_name": "<name>",
        "item_name": "<item>",
        "finished": false
      },
      ...
    ]
- إذا لم توجد القائمة:
  - {
    "error": "list not found"
  }

---

### 3. Create a new list
- Method: `POST`
- URL: `/todo/lists/create/`
- Auth: مطلوب

#### Request JSON
- {
  "list_name": "<name>"
}

#### Response
- `200 OK`
  - {
    "status": "created",
    "list_name": "<name>"
  }
- أخطاء محتملة:
  - `400 Bad Request` إذا لم يتم إرسال `list_name`:
    - { "error": "list_name is required" }
  - `400 Bad Request` إذا كانت القائمة موجودة مسبقاً:
    - { "error": "list already exists" }

---

### 4. Delete a list
- Method: `DELETE`
- URL: `/todo/lists/delete/`
- Auth: مطلوب

#### Request JSON
- {
  "list_name": "<name>"
}

#### Response
- `200 OK`
  - {
    "status": "deleted",
    "list_name": "<name>"
  }
- أخطاء محتملة:
  - `400 Bad Request` إذا لم يتم إرسال `list_name`:
    - { "error": "list_name is required" }
  - `404 Not Found` إذا لم توجد القائمة:
    - { "error": "list not found" }

---

### 5. Add a todo item
- Method: `POST`
- URL: `/todo/todo/add/`
- Auth: مطلوب

#### Request JSON
- {
  "todo_list_name": "<list_name>",
  "item_name": "<item_name>"
}

#### Response
- `200 OK`
  - {
    "status": "created",
    "item": "<item_name>"
  }
- أخطاء محتملة:
  - `404 Not Found` إذا لم توجد القائمة:
    - { "error": "list not found" }
  - `400 Bad Request` إذا كان العنصر موجوداً مسبقاً في نفس القائمة:
    - { "error": "todo already exists" }

---

### 6. Delete a todo item
- Method: `DELETE`
- URL: `/todo/todo/delete/`
- Auth: مطلوب

#### Request JSON
- {
  "todo_list_name": "<list_name>",
  "item_name": "<item_name>"
}

#### Response
- `200 OK`
  - {
    "status": "deleted",
    "item": "<item_name>"
  }
- أخطاء محتملة:
  - `404 Not Found` إذا لم توجد القائمة:
    - { "error": "list not found" }
  - `404 Not Found` إذا لم توجد المهمة داخل القائمة:
    - { "error": "no such todo" }

---

### 7. Mark a todo item finished
- Method: `PATCH`
- URL: `/todo/todo/update/`
- Auth: مطلوب

#### Request JSON
- {
  "todo_list_name": "<list_name>",
  "item_name": "<item_name>"
}

#### Response
- `200 OK`
  - {
    "status": "updated",
    "item": "<item_name>",
    "finished": true
  }
- أخطاء محتملة:
  - `404 Not Found` إذا لم توجد القائمة:
    - { "error": "list not found" }
  - `404 Not Found` إذا لم توجد المهمة:
    - { "error": "no such todo" }

---

## Notes
- يجب أن يكون المستخدم مسجّل دخول ومرسَل عبر JWT.
- جميع الطلبات تستخدم JSON.
- إذا تم استخدام رابط دون الشرط (`/todo/lists/create` بدون `/` في النهاية)`، قد يحدث إعادة توجيه داخلي أو خطأ 405.

## Example cURL
```bash
curl -X POST \
  https://romee.up.railway.app/todo/lists/create/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"list_name": "الواجب"}'
```

```bash
curl -X POST \
  https://romee.up.railway.app/todo/todo/add/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"todo_list_name": "الواجب", "item_name": "حل المسألة"}'
```
