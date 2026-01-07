// Firebase initializer
import { initializeApp } from 'firebase/app';
import { getAuth, onAuthStateChanged, User as FirebaseUser } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "AIzaSyAGUW3la2giOJn_sG2Nz4HRAfqP1QuY0KA",
  authDomain: "medcalc-71fb2.firebaseapp.com",
  projectId: "medcalc-71fb2",
  storageBucket: "medcalc-71fb2.firebasestorage.app",
  messagingSenderId: "889371502520",
  appId: "1:889371502520:web:9d5d0e6e3f04d17054914d",
  measurementId: "G-L5RJ3MXR9D"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);

// Promise that resolves once Firebase Auth has initialized and fired first state
export const authReady: Promise<FirebaseUser | null> = new Promise(resolve => {
  const unsubscribe = onAuthStateChanged(auth, user => {
    unsubscribe();
    resolve(user);
  });
});

export async function getCurrentFirebaseUser(): Promise<FirebaseUser | null> {
  await authReady;
  return auth.currentUser;
}

export default app;
