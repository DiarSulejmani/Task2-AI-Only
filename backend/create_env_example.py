import os

# Create .env.example file with default DATABASE_URL
example_path = os.path.join(os.path.dirname(__file__), ".env.example")
if not os.path.exists(example_path):
    with open(example_path, "w") as f:
        f.write("DATABASE_URL=sqlite:///./app.db\n")
content = open(example_path).read()