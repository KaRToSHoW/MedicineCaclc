# UML-диаграмма архитектуры системы "Медицинский калькулятор"

## Архитектурная диаграмма

```
┌────────────────────────────────────────────────────────────────────┐
│                          МОБИЛЬНОЕ ПРИЛОЖЕНИЕ                       │
│                         (React Native + Expo)                       │
└────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS/REST API
                                    │ JSON
                                    ▼
┌────────────────────────────────────────────────────────────────────┐
│                         BACKEND API SERVER                          │
│                        (Python FastAPI)                             │
└────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ SQL Queries
                                    │ SQLAlchemy ORM
                                    ▼
┌────────────────────────────────────────────────────────────────────┐
│                          DATABASE                                   │
│                        (PostgreSQL)                                 │
└────────────────────────────────────────────────────────────────────┘
```

## Диаграмма компонентов и взаимодействий

```plantuml
@startuml Medical Calculator Architecture

' Actors
actor "Пользователь" as User
actor "Медицинский\nспециалист" as Doctor

' Components - Frontend
package "Frontend (React Native)" {
  [Экраны UI] as UI
  [Навигация\nExpo Router] as Router
  [Управление\nсостоянием\nZustand] as State
  [API Клиент\nservices/] as APIClient
  [Локальное\nхранилище\nSecureStore] as Storage
}

' Components - Backend
package "Backend (FastAPI)" {
  [API Endpoints\n/api/v1] as API
  [Бизнес-логика\nServices] as Logic
  [Аутентификация\nJWT Middleware] as Auth
  [Модели данных\nPydantic Schemas] as Schemas
}

' Database
database "PostgreSQL" {
  [users] as UsersTable
  [sessions] as SessionsTable
  [calculators] as CalcsTable
  [calculation_results] as ResultsTable
  [usage_statistics] as StatsTable
}

' External Services
cloud "Внешние сервисы" {
  [Медицинские\nбазы данных] as MedDB
  [Аналитика] as Analytics
  [Push\nуведомления] as Push
}

' User interactions
User --> UI : Взаимодействие
Doctor --> UI : Взаимодействие

' Frontend internal flow
UI --> Router : Навигация
UI --> State : Получение данных
State --> APIClient : API запросы
APIClient --> Storage : Токены сессии

' Frontend to Backend
APIClient --> API : HTTP/REST\n(JSON)

' Backend internal flow
API --> Auth : Проверка\nаутентификации
Auth --> Logic : Вызов\nбизнес-логики
Logic --> Schemas : Валидация\nданных

' Backend to Database
Logic --> UsersTable : User Model\n(id, email, name,\npassword_digest)
Logic --> SessionsTable : Session Model\n(id, user_id,\nsession_token)
Logic --> CalcsTable : Calculator Model\n(id, name, formula,\ninput_fields,\ninterpretation_rules)
Logic --> ResultsTable : CalculationResult Model\n(id, user_id,\ncalculator_id,\ninput_data,\nresult_value,\ninterpretation)
Logic --> StatsTable : UsageStatistic Model\n(id, calculator_id,\naction, meta_data)

' External integrations
Logic --> MedDB : Справочные\nданные
Logic --> Analytics : События\nиспользования
Logic --> Push : Уведомления

' Relationships
UsersTable "1" -- "N" SessionsTable : user_id
UsersTable "1" -- "N" ResultsTable : user_id
CalcsTable "1" -- "N" ResultsTable : calculator_id
CalcsTable "1" -- "N" StatsTable : calculator_id

@enduml
```

## Диаграмма последовательности: Выполнение расчета

```plantuml
@startuml Calculation Flow

actor Пользователь
participant "UI\nЭкран" as UI
participant "Store\nZustand" as Store
participant "API\nКлиент" as Client
participant "Backend\nAPI" as API
participant "Logic\nСервис" as Logic
participant "Database\nPostgreSQL" as DB

Пользователь -> UI: Выбрать калькулятор
UI -> Store: getCalculator(id)
Store -> Client: GET /api/v1/calculators/{id}
Client -> API: HTTP Request
API -> Logic: fetch_calculator(id)
Logic -> DB: SELECT * FROM calculators WHERE id=?
DB --> Logic: Calculator data
Logic --> API: Calculator object
API --> Client: JSON Response
Client --> Store: Calculator data
Store --> UI: Отобразить форму

Пользователь -> UI: Ввести параметры\n(вес, рост, возраст)
Пользователь -> UI: Нажать "Рассчитать"
UI -> UI: Валидация полей
UI -> Store: createCalculation(data)
Store -> Client: POST /api/v1/calculation_results

note right of Client
  Payload:
  {
    calculator_id: 1,
    input_data: {
      weight: 75,
      height: 180
    }
  }
end note

Client -> API: HTTP Request\n+ JWT Token
API -> Logic: Проверка токена
Logic -> Logic: Валидация данных
Logic -> Logic: Вычисление формулы:\nresult = formula(input_data)
Logic -> Logic: Интерпретация:\ninterpretation = interpret(result)
Logic -> DB: INSERT INTO calculation_results
DB --> Logic: Saved result (id, result_value)
Logic --> API: CalculationResult object
API --> Client: JSON Response

note right of API
  Response:
  {
    id: 123,
    result_value: 23.1,
    interpretation: "Нормальный вес",
    input_data: {...}
  }
end note

Client --> Store: Result data
Store --> UI: Обновить состояние
UI --> Пользователь: Показать результат

@enduml
```

## Диаграмма классов: Модели данных

```plantuml
@startuml Data Models

class User {
  +id: Integer
  +email: String
  +name: String
  +password_digest: String
  +role: String
  +created_at: DateTime
  +updated_at: DateTime
  --
  +sessions: List<Session>
  +calculation_results: List<CalculationResult>
}

class Session {
  +id: Integer
  +user_id: Integer
  +session_token: String
  +ip_address: String
  +user_agent: String
  +created_at: DateTime
  +updated_at: DateTime
  --
  +user: User
}

class Calculator {
  +id: Integer
  +name: String
  +description: Text
  +formula: Text
  +category: String
  +input_fields: JSON
  +interpretation_rules: JSON
  +created_at: DateTime
  +updated_at: DateTime
  --
  +calculation_results: List<CalculationResult>
}

class CalculationResult {
  +id: Integer
  +user_id: Integer
  +calculator_id: Integer
  +input_data: JSON
  +result_value: Float
  +interpretation: Text
  +performed_at: DateTime
  +created_at: DateTime
  +updated_at: DateTime
  --
  +user: User
  +calculator: Calculator
}

class UsageStatistic {
  +id: Integer
  +user_id: Integer
  +calculator_id: Integer
  +action: String
  +meta_data: JSON
  +created_at: DateTime
}

User "1" -- "N" Session : has many
User "1" -- "N" CalculationResult : has many
Calculator "1" -- "N" CalculationResult : has many
User "1" -- "N" UsageStatistic : has many
Calculator "1" -- "N" UsageStatistic : has many

@enduml
```

## Диаграмма вариантов использования

```plantuml
@startuml Use Cases

left to right direction
actor "Неавторизованный\nпользователь" as Guest
actor "Авторизованный\nпользователь" as User
actor "Администратор" as Admin

rectangle "Система Медицинский калькулятор" {
  usecase "Просмотр калькуляторов" as UC1
  usecase "Поиск калькулятора" as UC2
  usecase "Фильтр по категориям" as UC3
  usecase "Выполнить расчет" as UC4
  usecase "Зарегистрироваться" as UC5
  usecase "Войти в систему" as UC6
  usecase "Выйти из системы" as UC7
  usecase "Просмотр истории" as UC8
  usecase "Сохранить результат" as UC9
  usecase "Удалить результат" as UC10
  usecase "Просмотр статистики" as UC11
  usecase "Редактировать профиль" as UC12
  usecase "Управление калькуляторами" as UC13
  usecase "Просмотр аналитики" as UC14
}

Guest --> UC1
Guest --> UC2
Guest --> UC3
Guest --> UC4
Guest --> UC5

User --> UC1
User --> UC2
User --> UC3
User --> UC4
User --> UC6
User --> UC7
User --> UC8
User --> UC9
User --> UC10
User --> UC11
User --> UC12

Admin --> UC13
Admin --> UC14

UC4 ..> UC9 : <<include>>
UC8 ..> UC6 : <<requires>>
UC9 ..> UC6 : <<requires>>

@enduml
```

## Диаграмма состояний: Жизненный цикл расчета

```plantuml
@startuml Calculation State Machine

[*] --> Создан : Пользователь нажал "Рассчитать"

Создан --> Валидация : Проверка входных данных

Валидация --> Ошибка : Некорректные данные
Валидация --> ВПроцессе : Данные корректны

ВПроцессе --> Вычисление : Применить формулу
Вычисление --> Интерпретация : Результат получен
Интерпретация --> Сохранение : Интерпретация завершена

Сохранение --> Завершен : Сохранено в БД
Сохранение --> Ошибка : Ошибка БД

Завершен --> [*]
Ошибка --> [*] : Показать ошибку

note right of Вычисление
  formula_evaluator.evaluate(
    formula, input_data
  )
end note

note right of Интерпретация
  interpreter.interpret(
    rules, result_value
  )
end note

@enduml
```

## Диаграмма развертывания

```plantuml
@startuml Deployment Diagram

node "iOS/Android\nУстройство" {
  [Expo Go/\nNative App]
}

node "Web\nБраузер" {
  [React App\n(Web)]
}

node "Backend\nServer" {
  [FastAPI\nApplication]
  [Uvicorn\nASGI Server]
}

node "Database\nServer" {
  database "PostgreSQL\n15.0"
}

cloud "CDN" {
  [Static Assets]
}

cloud "External\nServices" {
  [Analytics]
  [Push Service]
}

[Expo Go/\nNative App] -- [FastAPI\nApplication] : HTTPS/REST
[React App\n(Web)] -- [FastAPI\nApplication] : HTTPS/REST
[FastAPI\nApplication] -- "PostgreSQL\n15.0" : SQL/asyncpg
[FastAPI\nApplication] -- [Analytics] : Events
[FastAPI\nApplication] -- [Push Service] : Notifications
[React App\n(Web)] -- [Static Assets] : Load assets

@enduml
```

## Активные сущности системы

### 1. Пользователи
- **Неавторизованные пользователи**: могут просматривать калькуляторы и выполнять расчеты
- **Авторизованные пользователи**: полный доступ + история + статистика
- **Администраторы**: управление контентом и аналитика

### 2. Мобильное приложение (Frontend)
- Expo/React Native приложение
- Работает на iOS, Android, Web
- Управляет UI и локальным состоянием

### 3. API Сервер (Backend)
- Python FastAPI
- Обрабатывает REST API запросы
- Выполняет бизнес-логику

### 4. База данных
- PostgreSQL
- Хранит пользователей, калькуляторы, результаты
- Обеспечивает персистентность данных

### 5. Внешние сервисы
- Медицинские справочники (планируется)
- Аналитика (планируется)
- Push-уведомления (планируется)

## Модели данных для обмена

### UserModel
```typescript
{
  id: number
  email: string
  name?: string
  role: string
  created_at: datetime
}
```

### CalculatorModel
```typescript
{
  id: number
  name: string
  description?: string
  formula: string
  category: string
  input_fields: InputField[]
  interpretation_rules?: InterpretationRule[]
}
```

### CalculationResultModel
```typescript
{
  id: number
  user_id: number
  calculator_id: number
  input_data: Record<string, any>
  result_value: number
  interpretation?: string
  performed_at: datetime
}
```

### SessionModel
```typescript
{
  session_token: string
  user: UserModel
}
```

## Механизмы взаимодействия

1. **Аутентификация**: JWT токены в HTTP заголовках
2. **Авторизация**: Проверка токена middleware
3. **API запросы**: REST JSON через HTTPS
4. **Валидация**: Pydantic схемы на backend, форм-валидация на frontend
5. **Хранение**: SecureStore для токенов, PostgreSQL для данных
6. **Кэширование**: Zustand store на frontend
7. **Вычисления**: Mathjs для безопасной оценки формул

---

**Примечание:** Для рендеринга PlantUML диаграмм используйте:
- Online: http://www.plantuml.com/plantuml
- Local: VS Code PlantUML extension
- CLI: plantuml tool

Файлы .puml можно создать отдельно из блоков кода выше.
