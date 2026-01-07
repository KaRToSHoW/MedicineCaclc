/*
  Seeder: uploads calculators_seed.json into Firestore using Firebase Admin SDK.
  Usage:
    1. Create a Firebase service account JSON in scripts/serviceAccountKey.json
       (Firebase Console -> Project Settings -> Service accounts -> Generate private key)
    2. Run: node scripts/seed_calculators_firestore.js
*/

const fs = require('fs');
const path = require('path');

const seedPath = path.join(__dirname, 'calculators_seed.json');
if (!fs.existsSync(seedPath)) {
  console.error('Seed file not found:', seedPath);
  process.exit(1);
}

const serviceAccountPath = path.join(__dirname, 'serviceAccountKey.json');
if (!fs.existsSync(serviceAccountPath)) {
  console.error('Service account key not found:', serviceAccountPath);
  console.error('Create a service account in Firebase Console and place JSON at scripts/serviceAccountKey.json');
  process.exit(1);
}

const admin = require('firebase-admin');
const serviceAccount = require(serviceAccountPath);

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

async function slugify(name) {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

async function run() {
  const data = JSON.parse(fs.readFileSync(seedPath, 'utf8'));

  for (const calc of data) {
    const id = await slugify(calc.name);
    const ref = db.collection('calculators').doc(id);
    // Add timestamps if missing
    const now = new Date().toISOString();
    const payload = Object.assign({ createdAt: now, updatedAt: now }, calc);
    await ref.set(payload);
    console.log('Upserted calculator:', id);
  }

  console.log('Seeding completed:', data.length, 'calculators');
  process.exit(0);
}

run().catch(err => {
  console.error('Seeding failed:', err);
  process.exit(1);
});
