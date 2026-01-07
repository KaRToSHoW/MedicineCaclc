Recommended Firestore rules

Apply these rules in Firebase Console → Firestore → Rules. They allow public read access to `calculators` and restrict `calculation_results` to authenticated users owning the document.

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Public calculators collection
    match /calculators/{docId} {
      allow read: if true;
      allow write: if false; // managed via admin seeder only
    }

    // Per-user calculation results
    match /calculation_results/{docId} {
      allow read: if request.auth != null && resource.data.userId == request.auth.uid;
      allow create: if request.auth != null && request.resource.data.userId == request.auth.uid;
      allow update, delete: if request.auth != null && resource.data.userId == request.auth.uid;
    }
  }
}
```

Notes:
- After publishing these rules, the frontend should be able to read `calculators` and allow authenticated users to create/read/update/delete their own `calculation_results`.
- If you use server-side migration/seeder with the Admin SDK, that process is unaffected by these rules.
