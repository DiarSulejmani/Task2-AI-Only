# DuoQuanto Frontend

This project was bootstrapped with [Vite](https://vitejs.dev/) and uses **React 18 + TypeScript**.

## Available Scripts

Inside the `frontend/` folder you can run:

```bash
npm install   # or yarn
npm run dev   # Runs the app in the development mode.
npm run build # Builds the app for production.
npm run preview # Preview the production build.
```

The app will be available at http://localhost:5173 by default.

## Project Structure

- `src/contexts` – React Context providers (e.g. authentication)
- `src/components` – Reusable UI components (Layout, ProtectedRoute, etc.)
- `src/pages` – Page level components rendered by React Router
- `src/styles` – Global & module CSS (you can switch to styled-components if you prefer)

## Authentication

The `AuthContext` handles login, register and logout actions via
backend endpoints:

- `POST /auth/login`
- `POST /auth/register`

A successful response is expected to include `{ id, role, token }`.
These details are persisted in `localStorage` to keep the user signed-in
after a page refresh.
