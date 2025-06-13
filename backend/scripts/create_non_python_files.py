import os

def write_text(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
write_text(os.path.join(root_dir, "backend", ".env.example"), "DATABASE_URL=sqlite:///./app.db\n")
write_text(os.path.join(root_dir, "backend", "requirements.txt"), "fastapi\nuvicorn\nSQLAlchemy\npython-dotenv\npydantic\n")

print("Non-Python files created")