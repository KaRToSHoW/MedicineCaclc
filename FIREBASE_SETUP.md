# Firebase Setup Instructions

## ⚠️ IMPORTANT: Do NOT install PostgreSQL

This project uses **Firebase Firestore** only. PostgreSQL is not required.

## Required: Firebase Service Account

Before running the project, you **MUST** have the Firebase service account JSON file.

**Required file location:**
```
medcalc-71fb2-firebase-adminsdk-fbsvc-14a7ed45c0.json
```
(Place in project root directory)

**How to get the service account file:**

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: **medcalc-71fb2**
3. Click Settings (gear icon) → Project Settings
4. Navigate to **Service Accounts** tab
5. Click **"Generate new private key"**
6. Save the JSON file as: `medcalc-71fb2-firebase-adminsdk-fbsvc-14a7ed45c0.json`
7. Place it in the project root

**Without this file, the backend will fail to start!**

## Installation

```bash
# Install frontend dependencies
npm install

# Install backend dependencies
cd api
python3 -m pip install -r requirements.txt
cd ..
```

## Running the Project

```bash
# Terminal 1: Start backend (port 8000)
npm run start-backend

# Terminal 2: Start frontend (port 3000)
npm run start
```

## Environment Configuration

Copy `.env.example` to `.env` if it doesn't exist:
```bash
cp .env.example .env
```

---

**Need help?** Contact the project owner to get the Firebase service account JSON file.
