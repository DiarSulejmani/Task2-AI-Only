# DuoQuanto Local Development Mockup

## 1. Global Layout & Navigation

### Site Header (persistent on all pages):
- **Logo/Brand**: "DuoQuanto" (top-left). Clicking it routes to Dashboard (if logged in) or to Landing page (if not logged in).
- **Navigation Bar** (top-right):
  - If unauthenticated: "Home" | "About" | "Login" | "Register"
  - If teacher: "Dashboard" | "Create Questions" | "Analyze Progress" | "Account" | "Logout"
  - If student: "Dashboard" | "My Topics" | "My Progress" | "Account" | "Logout"

### Site Footer (persistent):
- Copyright, version number, Links: "Privacy & Terms" | "Help/FAQ" | "Contact"

### Authentication & Roles:
- **Two roles**: Teacher and Student.
- On login/register, users choose (or are assigned) a role:
  - Teacher can access "Teacher Dashboard," "Create Questions," and "Analyze Progress."
  - Student can access "Student Dashboard," "My Topics," "Take Quiz," and "My Progress."
- Uses session-based authentication with local storage. All protected routes must verify role.

## 2. Landing Page & Authentication

### 2.1 Landing Page (Unauthenticated Users):
- **Hero Section**: Big tagline ("Learn Math & Stats with Gamification"), subtext, and "Get Started" button → routes to Login/Register.
- **Features Preview**: 3-column row with icons/text:
  1. **Personalized Quizzes**: "Multiple question formats and instant feedback."
  2. **Teacher Toolkit**: "Generate and manage your own question banks."
  3. **Gamified Learning**: "Earn coins, ranks, and challenges."
- Footer as described above.

### 2.2 Register Page:
- **Form Fields**: Full Name (text), Email (email), Password (password + "Confirm Password"), Role (dropdown: Teacher / Student).
- **Validation**: Strong password; email format check; role required.
- **On Submit**: Create new user, store role in local database, redirect to respective Dashboard.

### 2.3 Login Page:
- **Form Fields**: Email (email), Password (password).
- **Forgot Password** link (placeholder; not in scope for core MVP).
- **On Submit**: Authenticate against local database, create session, redirect to Dashboard.

## 3. Teacher Module

All 'Teacher' routes are behind authentication + role check.

### 3.1 Teacher Dashboard:
- **Overview Cards** (top row):
  1. **Total Questions**: Count of all questions in this teacher's bank.
  2. **Pending Reviews**: Number of AI-generated questions awaiting human evaluation.
  3. **Course Coverage**: A progress bar showing percentage of topics covered in '335155 Mathematik und Statistik'.
- **Quick Actions** (middle row, large icons/buttons):
  1. **Create New Question** (→ routes to 'Create Questions' page).
  2. **Review AI-Generated** (→ routes to 'Review Questions' queue).
  3. **Analyze Progress** (→ routes to 'Analyze Progress' page).
- **Recent Activity Feed** (bottom): e.g., "2025-XX-XX: John Doe (Student ID 1234) scored 8/10 in Topic 'Standard Deviation'" etc.

### 3.2 Create Questions (Manual & Automated):

**Tabs or Toggle at Top**: "Automated", "Semi-Automated", "Manual".

#### 3.2.1 'Automated' Tab:
- **Instructional Text**: 'Use AI to generate sets of questions for a specified topic...'.
- **Form Fields**: Select Topic (dropdown), Question Type (Multiple-Choice, Open-Text, Calculation), Number of Questions (numeric input), Advanced Options (Difficulty, Hints, Local AI Model, Custom Prompt).
- **Generate Button**: Invokes local AI service to generate questions. Shows loading spinner.
- **Result List**: Each question shows preview, options, correct answer, explanation, buttons 'Approve', 'Edit', 'Reject'.
- **Bulk Actions**: 'Approve All', 'Reject All', 'Export CSV'.
- **Bottom**: 'Need more control?' link to Semi-Automated tab.

#### 3.2.2 'Semi-Automated' Tab:
- **Instructional Text**: 'Customize and guide AI: Provide a partially filled question template...'.
- **Form Fields**: Select Topic, Question Template, Number of Variations, AI Prompt Customization, Generate Button.
- **Review Workflow**: Same 'Approve/Edit/Reject' flow as Automated.

#### 3.2.3 'Manual' Tab:
- **Instructional Text**: 'Fill out the form to create a question from scratch.'
- **Form Fields**: Select Topic, Question Type, Question Text, Options/Answer fields, Explanation, Save Button.
- **Data Validation**: Ensure required fields per type are filled.
- **After saving**: question goes directly into Bank with status=approved.

### 3.3 Review Questions Queue
- **Navbar Link** from Teacher Dashboard.
- Displays all AI-generated (Automated + Semi-Automated) questions with status=pending.
- **Filter Options**: Topic, Question Type, AI Model Used, Date Generated.
- Batch actions and individual 'Approve/Edit/Reject' as before.

### 3.4 Analyze Progress (Teacher Analytics)
- **Instructional Text**: 'View anonymized statistics on student performance.'
- **Filters at Top**: Course Module, Date Range, Student Cohort.
- **Key Metrics** (Cards): Average Score, Completion Rate, Most Missed Question, Average Time Per Question.
- **Charts Section**: Bar Chart (attempts per question), Line Chart (score trend over time), Pie Chart (question type distribution).
- **Table of Student Summaries**: Columns: Student ID (anonymized), Attempts, Avg Score, Last Activity Date, 'View Details' modal with logs.
- **Export Options**: 'Download CSV', 'Download PDF'.
- **Security**: Data must be anonymized.

## 4. Student Module

All 'Student' routes are behind authentication + role check.

### 4.1 Student Dashboard:
- **Greeting**: 'Welcome, [First Name]! Ready to learn?'
- **Progress Summary Cards**: Current Level & Coins, Streak, Next Badge.
- **Quick Actions**: 'Select Topic', 'Continue Last Quiz', 'View Leaderboard'.
- **Recent Activity**: e.g., 'You scored 8/10 on 'Variance Quiz'...'.

### 4.2 My Topics (Topic Selection):
- **Instructional Text**: 'Choose a topic to start a quiz or review materials.'
- **Grid of Topic Cards**: Each card shows topic name, progress bar, 'Start Quiz', 'Review Questions'.
- **Search Bar** to filter topics.

### 4.3 Quiz Screen (Question Flow):
1. **Quiz Setup Modal**: Number of Questions, Question Types, Difficulty, 'Begin Quiz' button.
2. **Quiz Interface**: Header with 'Question X of Y', Timer; Question Text; Input Section (MC, Open-Text, Calculation); Hint Button; Submit & Next Buttons; Progress & Gamification Bar.
3. **After Submission**: Feedback Box showing correctness, explanation, points earned; 'Next Question' button.
4. **Quiz Summary Screen**: Score card, XP/Coins earned, badges, time taken, 'Review All Questions' and 'Return to Dashboard' buttons.

### 4.4 My Progress (Student Analytics):
- **Instructional Text**: 'Track your learning journey.'
- **Summary Cards**: Total Quizzes Taken, Overall Accuracy, Current Level, Coins Balance.
- **Leaderboard Section**: Top 5 Students (anonymized) with Rank, Pseudonym, Total XP, Quizzes Completed.
- **Progress Over Time Chart**: X-axis dates, Y-axis score percentages.
- **Topic Breakdown Table**: Columns: Topic Name, Attempts, Avg Score, Best Score, Next Recommended Topic; Filter by Avg Score.
- **Badge Showcase**: Icons of earned badges with hover descriptions.

## 5. Security & Authentication Concept

- **Authentication**: Session-based authentication with secure cookies; session expiry ~1 hour.
- **Authorization**: Protected routes check session + role; e.g., `/teacher/createQuestion` only for teacher role; `/student/submitAnswer` only for student role.
- **Data Anonymization** (Teacher Analytics): Student names replaced with IDs or pseudonyms; teachers only see aggregated data.
- **Secure Storage**: Local SQLite database with bcrypt for passwords, HTTPS for local development.

## 6. Local Development Infrastructure

### Frontend:
- **Framework**: React/Angular/Vue.js served locally via development server (e.g., `npm run dev`)
- **Port**: Default localhost:3000 or localhost:4200

### Backend API:
- **Framework**: FastAPI/Flask/Express.js running locally
- **Port**: Default localhost:8000 or localhost:3001
- **Hot Reload**: Development server with auto-restart on file changes

### Database:
- **Primary DB**: Local SQLite database file with tables: `users`, `questions`, `quiz_attempts`, `student_answers`, `badges`, `topic_progress`
- **Location**: `./data/duoquanto.db` or similar local path
- **Management**: SQLite browser or built-in admin interface

### Local AI Integration:
- **Option 1**: Local LLM using Ollama or similar (llama2, mistral, etc.)
- **Option 2**: OpenAI API with local API key configuration
- **Option 3**: HuggingFace transformers running locally
- **Vector Store**: Local file-based storage or ChromaDB for RAG functionality

### Development Environment:
- **Package Management**: npm/yarn for frontend, pip/poetry for Python backend
- **Environment Variables**: `.env` file for local configuration (API keys, database path, etc.)
- **Development Scripts**: `package.json` or `Makefile` with commands for starting services

### Local File Structure:
```
duoquanto/
├── frontend/           # React/Angular app
├── backend/           # FastAPI/Flask API
├── data/             # SQLite database
├── docs/             # Documentation
├── scripts/          # Setup and utility scripts
├── .env              # Environment variables
├── docker-compose.yml # Optional: containerized development
└── README.md         # Setup instructions
```

## 7. Development Setup & Deployment

### Initial Setup:
1. Clone repository
2. Install dependencies (`npm install`, `pip install -r requirements.txt`)
3. Initialize local database (`python scripts/init_db.py`)
4. Configure environment variables in `.env`
5. Start backend server (`python main.py` or `npm run dev:backend`)
6. Start frontend server (`npm run dev`)
7. Access application at `http://localhost:3000`

### Optional Docker Setup:
- **docker-compose.yml**: Defines services for frontend, backend, and database
- **Single command startup**: `docker-compose up -d`
- **Volume mounting**: Local code changes reflected in containers

## 8. Agent Usage for Local Development

### Developer Agent:
- Reads this mockup → generates local development templates (FastAPI route stubs, React components)
- Sets up local development environment configuration

### UI/UX Designer Agent:
- Uses UI descriptions → produces component mockups or direct HTML/CSS scaffolding
- Creates responsive designs for local development preview

### Tester Agent:
- Writes pytest/jest tests for local API routes and UI functions
- Sets up local testing database and test data fixtures

### Database Architect Agent:
- Creates SQLite schema and migration scripts
- Designs local database structure with proper indexing

### Documenter Agent:
- Writes local setup README.md and development documentation
- Creates API reference docs for local development

### Manager Agent:
- Coordinates local development workflow
- Ensures all components work together in local environment
- Manages development task dependencies

## 9. Summary

This local development mockup defines every page, form, component, and data flow DuoQuanto must support for local development and testing.

**Key Changes for Local Development:**
- SQLite database instead of cloud databases
- Session-based authentication instead of JWT
- Local AI integration options
- Development server setup
- Local file storage
- Simplified deployment (no cloud infrastructure)

Agents can parse these requirements and generate a fully functional local development environment that can be easily set up and run on any developer's machine.