Firebase setup (quick)

1. Create a Firebase project and enable Firestore and Email/Password Authentication.
2. Add a Web App in Firebase settings and copy the config into `services/firebase.ts`.
3. Add the admin service account JSON at `scripts/serviceAccountKey.json` to run the seeder (`scripts/seed_calculators_firestore.js`). Keep this file secret.
4. Publish Firestore rules — see `docs/FIRESTORE_RULES.md` for recommended rules.
5. Run the seeder (optional) to populate `calculators` collection:

```bash
node scripts/seed_calculators_firestore.js
```

6. On the client, sign up or sign in. Local results will be migrated to Firestore automatically after sign-in.
