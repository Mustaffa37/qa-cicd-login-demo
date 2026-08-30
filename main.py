import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load variables from .env file
load_dotenv()

MOCK_EMAIL = os.getenv("MOCK_EMAIL")
MOCK_PASSWORD = os.getenv("MOCK_PASSWORD")

app = FastAPI(title="Modern SQA Demo App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/login")
def login(data: LoginRequest):
    if data.email == MOCK_EMAIL and data.password == MOCK_PASSWORD:
        return {
            "status": "success",
            "message": "Authentication successful",
            "token": f"bearer-{uuid.uuid4()}"  # Generates unique session token
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SQA Automation Demo App</title>
        <script src="https://cdn.tailwindcss.com"></script>

    </head>

    <body class="bg-slate-900 text-slate-100 flex items-center justify-center min-h-screen">

        <!-- LOGIN CARD -->
        <div id="login-card" class="w-full max-w-md p-8 rounded-2xl bg-slate-800/80 backdrop-blur-md border border-slate-700 shadow-2xl">
            <div class="mb-6 text-center">
                <h2 class="text-3xl font-bold tracking-tight text-indigo-400">Welcome Back</h2>
                <p class="text-sm text-slate-400 mt-1">Please enter your credentials to log in.</p>

            </div>

            <div id="error-toast" class="hidden mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/50 text-red-400 text-sm text-center"></div>

            <form id="login-form" onsubmit="handleLogin(event)" class="space-y-5">
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">Email Address</label>
                    <input type="email" id="email" required placeholder="admin@qa.com" 
                           class="w-full px-4 py-3 rounded-xl bg-slate-900/60 border border-slate-700 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-slate-100">

                </div>
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">Password</label>
                    <input type="password" id="password" required placeholder="••••••••" 
                           class="w-full px-4 py-3 rounded-xl bg-slate-900/60 border border-slate-700 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-slate-100">

                </div>
                <button type="submit" id="login-btn" 
                        class="w-full py-3 px-4 rounded-xl font-semibold bg-indigo-600 hover:bg-indigo-500 active:scale-[0.98] transition shadow-lg shadow-indigo-600/30">
                    Sign In
                </button>

            </form>

        </div>

        <!-- WELCOME DASHBOARD -->
        <div id="welcome-card" class="hidden w-full max-w-md p-8 rounded-2xl bg-slate-800/80 backdrop-blur-md border border-slate-700 shadow-2xl text-center">
            <div class="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-4 border border-emerald-500/30">
                ✓
            </div>
            <h2 id="welcome-title" class="text-2xl font-bold text-slate-100 mb-2">Welcome Back, Admin!</h2>
            <p class="text-sm text-slate-400 mb-6">You have successfully authenticated into the SQA Test Application.</p>

            <button onclick="logout()" id="logout-btn" 
                    class="py-2.5 px-6 rounded-xl font-medium bg-slate-700 hover:bg-slate-600 transition text-slate-200">
                Log Out
            </button>

        </div>

        <script>
            async function handleLogin(e) {
                e.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                const toast = document.getElementById('error-toast');
                
                toast.classList.add('hidden');

                try {
                    const response = await fetch('/api/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });
                    
                    const data = await response.json();

                    if (response.ok) {
                        document.getElementById('login-card').classList.add('hidden');
                        document.getElementById('welcome-card').classList.remove('hidden');
                    } else {
                        toast.innerText = data.detail || 'Login failed';
                        toast.classList.remove('hidden');
                    }
                } catch (err) {
                    toast.innerText = 'Network error occurred';
                    toast.classList.remove('hidden');
                }
            }

            function logout() {
                document.getElementById('welcome-card').classList.add('hidden');
                document.getElementById('login-card').classList.remove('hidden');
                document.getElementById('email').value = '';
                document.getElementById('password').value = '';
            }
        </script>

    </body>

    </html>

    """