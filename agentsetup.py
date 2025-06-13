#!/usr/bin/env python3
"""Minimal Agno Team – TeamLead, BackendDev, FrontendDev + Kanban"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.python import PythonTools
from agno.tools.file import FileTools

# Requirements path (no complex config needed)
REQ_FILE = Path("requirements.md")

# One shared Kanban board
board = {"tickets_todo": [], "tickets_done": []}

# Shared tool to list board

def list_board(team: Team) -> str:
    todo = "\n".join(f"- {t}" for t in board["tickets_todo"]) or "- (empty)"
    done = "\n".join(f"- {d}" for d in board["tickets_done"]) or "- (empty)"
    return f"## Kanban\n\n### TODO\n{todo}\n\n### DONE\n{done}"

# Ticket helpers

def add_ticket(agent: Agent, text: str) -> str:
    board["tickets_todo"].append(text)
    return f"Added ticket: {text}"

def done_ticket(agent: Agent, text: str) -> str:
    if text in board["tickets_todo"]:
        board["tickets_todo"].remove(text)
        board["tickets_done"].append(text)
        return f"Done: {text}"
    return "Ticket not found"

tools_lead = [add_ticket, done_ticket, list_board, FileTools(), PythonTools()]

# Agents
TeamLead = Agent(
    name="TeamLead",
    model=OpenAIChat(id="o3-2025-04-16"),
    tools=tools_lead,
    description="Lead & manage Kanban",
    instructions=dedent("""
        Read requirements.md, create tickets with add_ticket, assign them, mark done.
        Declare 'PROJECT COMPLETE' when all tickets done and devs wrote '[COMPLETED]'.
    """),
)

BackendDev = Agent(
    name="BackendDev",
    model=OpenAIChat(id="o3-2025-04-16"),
    tools=[PythonTools()],
    description="Build FastAPI backend",
    instructions="Work on backend tickets. Save real code no Stub or Skeleton Files. Append '[COMPLETED]' when done.",
)

FrontendDev = Agent(
    name="FrontendDev",
    model=OpenAIChat(id="o3-2025-04-16"),
    tools=[PythonTools()],
    description="Build React frontend",
    instructions="Work on frontend tickets. Save real code no Stub or Skeleton File. Append '[COMPLETED]' when done.",
)

team = Team(
    name="WebTeam",
    mode="coordinate",
    model=OpenAIChat(id="o3-2025-04-16"),
    members=[TeamLead, BackendDev, FrontendDev],
    tools=[list_board],
    debug_mode=True,
)
team.team_session_state = board
for m in team.members:
    m.team_session_state = board

# Simple loop
for _ in range(10):
    if "OPENAI_API_KEY" not in os.environ:
        sys.exit("OPENAI_API_KEY missing")
    resp = team.run(f"Requirements:\n\n{REQ_FILE.read_text()}" if REQ_FILE.exists() else "No requirements yet")
    if "PROJECT COMPLETE" in str(resp):
        break
    time.sleep(1)
print("Final board:", board)
