#!/usr/bin/env python3
"""
Simple Issue Tracker for Options Trading Project
Usage: python track_issues.py [add|list|done|show] [args]
"""

import json
import os
from datetime import datetime
import sys

ISSUES_FILE = "project_issues.json"

def load_issues():
    """Load issues from JSON file"""
    if os.path.exists(ISSUES_FILE):
        with open(ISSUES_FILE, 'r') as f:
            return json.load(f)
    return {"issues": [], "next_id": 1}

def save_issues(data):
    """Save issues to JSON file"""
    with open(ISSUES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_issue(title, issue_type="todo", priority="medium"):
    """Add a new issue"""
    data = load_issues()
    
    issue = {
        "id": data["next_id"],
        "title": title,
        "type": issue_type,  # todo, bug, idea, test
        "priority": priority,  # high, medium, low
        "status": "open",
        "created": datetime.now().isoformat(),
        "completed": None
    }
    
    data["issues"].append(issue)
    data["next_id"] += 1
    save_issues(data)
    
    print(f"✅ Added #{issue['id']}: {title}")

def list_issues(status="open", issue_type=None):
    """List issues by status and type"""
    data = load_issues()
    issues = [i for i in data["issues"] if i["status"] == status]
    
    if issue_type:
        issues = [i for i in issues if i["type"] == issue_type]
    
    if not issues:
        print(f"No {status} issues found")
        return
    
    # Group by type and priority
    types = {"bug": "🐛 Bugs", "todo": "📝 TODOs", "idea": "💡 Ideas", "test": "🧪 Tests"}
    priorities = {"high": "🔥", "medium": "⚡", "low": "📌"}
    
    for issue_type_key, type_name in types.items():
        type_issues = [i for i in issues if i["type"] == issue_type_key]
        if type_issues:
            print(f"\n{type_name}")
            print("-" * 40)
            for issue in sorted(type_issues, key=lambda x: x["priority"], reverse=True):
                priority_icon = priorities.get(issue["priority"], "")
                print(f"{priority_icon} #{issue['id']} - {issue['title']} ({issue['priority']})")

def mark_done(issue_id):
    """Mark an issue as completed"""
    data = load_issues()
    
    for issue in data["issues"]:
        if issue["id"] == issue_id:
            issue["status"] = "completed"
            issue["completed"] = datetime.now().isoformat()
            save_issues(data)
            print(f"✅ Completed #{issue_id}: {issue['title']}")
            return
    
    print(f"❌ Issue #{issue_id} not found")

def show_stats():
    """Show project statistics"""
    data = load_issues()
    
    total = len(data["issues"])
    completed = len([i for i in data["issues"] if i["status"] == "completed"])
    open_issues = total - completed
    
    bugs = len([i for i in data["issues"] if i["type"] == "bug" and i["status"] == "open"])
    todos = len([i for i in data["issues"] if i["type"] == "todo" and i["status"] == "open"])
    ideas = len([i for i in data["issues"] if i["type"] == "idea"])
    
    print(f"\n📊 Project Statistics")
    print(f"=" * 30)
    print(f"Total Issues: {total}")
    print(f"Completed: {completed}")
    print(f"Open: {open_issues}")
    print(f"")
    print(f"🐛 Open Bugs: {bugs}")
    print(f"📝 Open TODOs: {todos}")
    print(f"💡 Ideas: {ideas}")
    
    if total > 0:
        completion = (completed / total) * 100
        print(f"")
        print(f"Progress: {completion:.1f}% complete")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python track_issues.py add 'Issue title' [type] [priority]")
        print("  python track_issues.py list [status] [type]")
        print("  python track_issues.py done <issue_id>")
        print("  python track_issues.py stats")
        print("")
        print("Types: todo, bug, idea, test")
        print("Priorities: high, medium, low")
        return
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) >= 3:
        title = sys.argv[2]
        issue_type = sys.argv[3] if len(sys.argv) > 3 else "todo"
        priority = sys.argv[4] if len(sys.argv) > 4 else "medium"
        add_issue(title, issue_type, priority)
    
    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else "open"
        issue_type = sys.argv[3] if len(sys.argv) > 3 else None
        list_issues(status, issue_type)
    
    elif command == "done" and len(sys.argv) >= 3:
        issue_id = int(sys.argv[2])
        mark_done(issue_id)
    
    elif command == "stats":
        show_stats()
    
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()
