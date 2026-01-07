# Firebase Firestore Setup

## Конфигурация Firebase

Приложение использует Firebase Firestore для хранения результатов расчётов калькуляторов с привязкой к пользователю.

### Текущая конфигурация

Файл: `services/firebase.ts`

```typescript
const firebaseConfig = {
  apiKey: "AIzaSyAGUW3la2giOJn_sG2Nz4HRAfqP1QuY0KA",
  authDomain: "medcalc-71fb2.firebaseapp.com",
  projectId: "medcalc-71fb2",
  storageBucket: "medcalc-71fb2.firebasestorage.app",
  messagingSenderId: "889371502520",
  appId: "1:889371502520:web:9d5d0e6e3f04d17054914d",
  measurementId: "G-L5RJ3MXR9D"
};
```

## Настройка Firestore

### 1. Создание коллекции

В Firebase Console создайте коллекцию `calculation_results` со следующей структурой документа:

```javascript
{
  userId: string,              // UID пользователя из Firebase Auth
  calculatorId: string,        // ID калькулятора
  inputData: object,           // Входные данные расчёта
  resultValue: number,         // Результат расчёта
  interpretation: string,      // Клиническая интерпретация
  performedAt: timestamp,      // Дата и время расчёта
  createdAt: timestamp,        // Дата создания записи
  updatedAt: timestamp         // Дата обновления записи
}
```

### 2. Настройка индекса (ОБЯЗАТЕЛЬНО!)

Для корректной работы запросов необходимо создать составной индекс:

1. Откройте Firebase Console
2. Перейдите в **Firestore Database** → **Indexes**
3. Нажмите **Create Index**
4. Настройте индекс:
   - **Collection ID**: `calculation_results`
   - **Fields to index**:
     - Field: `userId`, Mode: `Ascending`
     - Field: `performedAt`, Mode: `Descending`
   - **Query scopes**: `Collection`

**Или добавьте в `firestore.indexes.json`:**

```json
{
  "indexes": [
    {
      "collectionGroup": "calculation_results",
      "queryScope": "COLLECTION",
      "fields": [
        {
          "fieldPath": "userId",
          "order": "ASCENDING"
        },
        {
          "fieldPath": "performedAt",
          "order": "DESCENDING"
        }
      ]
    }
  ]
}
```

### 3. Правила безопасности Firestore

Установите следующие правила безопасности в Firebase Console → Firestore Database → Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Calculation results доступны только владельцу
    match /calculation_results/{resultId} {
      allow read, write: if request.auth != null && 
                           request.auth.uid == resource.data.userId;
      allow create: if request.auth != null && 
                      request.auth.uid == request.resource.data.userId;
    }
  }
}
```

### 4. Включение Firebase Authentication

1. Откройте Firebase Console → **Authentication**
2. Включите метод **Email/Password**
3. Настройте домены для авторизации (добавьте `localhost`, ваш домен)

## Архитектура работы с данными

### Сервис (services/calculation_results.ts)

Сервис работает **только с Firebase Firestore**:
- ❌ Локальное хранилище удалено
- ✅ Все данные сохраняются в Firestore
- ✅ Требуется аутентификация для всех операций
- ✅ Автоматическая проверка владельца данных

**Методы:**
- `getAll()` - Получить все результаты текущего пользователя
- `getById(id)` - Получить конкретный результат
- `create(data)` - Создать новый результат

### Store (stores/calculationResultsStore.ts)

Zustand store с обработкой ошибок аутентификации:
- Показывает сообщение "Войдите в систему" при отсутствии аутентификации
- Авт��матически обновляет список после создания результата

### UI экраны

**app/history.tsx** - История расчётов:
- Показывает prompt для входа неаутентифицированным пользователям
- Загружает результаты из Firestore для аутентифицированных

**app/calculator/[id].tsx** - Экран калькулятора:
- Сохраняет результаты в Firestore при расчёте
- Требует аутентификацию для сохранения

## Использование в коде

```typescript
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';
import { useAuth } from '@/hooks/useAuth';

// В компоненте
const { isAuthenticated } = useAuth();
const { items, loading, error, fetchAll, addItem } = useCalculationResultsStore();

// Загрузка результатов (только для аутентифицированных)
useEffect(() => {
  if (isAuthenticated) {
    fetchAll();
  }
}, [isAuthenticated]);

// Сохранение результата
const result = await addItem({
  calculatorId: calculator.id,
  inputData: inputs,
  resultValue: calculatedValue,
  interpretation: interpretation
});
```

## Миграция с локального хранилища

**Важно:** Локальное хранилище полностью удалено. Старые данные не мигрируются автоматически.

Если нужно сохранить старые данные:
1. Экспортируйте их из localStorage/SecureStore перед обновлением
2. Вручную загрузите через API после входа пользователя

## Устранение неполадок

### Ошибка: "Missing or insufficient permissions"
- Проверьте правила безопасности Firestore
- Убедитесь, что пользователь аутентифицирован
- Проверьте, что `userId` в документе совпадает с `auth.uid`

### Ошибка: "The query requires an index"
- Создайте составной индекс (см. раздел 2)
- Firestore предложит автоматическую ссылку для создания индекса в ошибке

### Результаты не загружаются
- Проверьте подключение к интернету
- Откройте консоль браузера и проверьте ошибки
- Убедитесь, что Firebase конфигурация корректна
- Проверьте, что пользователь аутентифицирован

## Мониторинг и отладка

### Firebase Console
- **Firestore Database** → Просмотр документов в реальном времени
- **Authentication** → Управление пользователями
- **Usage** → Статистика запросов и хранилища

### Консоль браузера
```javascript
// Проверка текущего пользователя
firebase.auth().currentUser

// Проверка подключения Firestore
firebase.firestore().collection('calculation_results').get()
```

## Производительность

### Оптимизация запросов
- ✅ Используется индексация по `userId` + `performedAt`
- ✅ Результаты сортируются по дате (новые первыми)
- ✅ Загружаются только данные текущего пользователя

### Лимиты бесплатного тарифа Firebase
- **Чтение**: 50,000 документов/день
- **Запись**: 20,000 документов/день
- **Удаление**: 20,000 документов/день
- **Хранилище**: 1 GB

Для большинства медицинских калькуляторов этого более чем достаточно.
