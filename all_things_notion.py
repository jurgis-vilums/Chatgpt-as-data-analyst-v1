import json
import requests
import pandas as pd
import os
from filter_generator import filter_for_notion
import sqlite3
import time

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
DATABASE_ID = os.environ["DATABASE_ID"]

if not NOTION_API_KEY or not DATABASE_ID:
    raise EnvironmentError("NOTION_API_KEY or DATABASE_ID environment variables are not set.")


def fetch_notes(filter):
    headers = {
        'Authorization': f"Bearer {NOTION_API_KEY}",
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    all_results = []
    has_more = True
    next_cursor = None
    start_time = time.time()

    while has_more:
        if next_cursor:
            filter["start_cursor"] = next_cursor

        if time.time() - start_time > 30:
            return "Too long to execute"

        response = requests.post(url, headers=headers, data=json.dumps(filter))
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor", None)
        else:
            print(f"Failed to fetch data: {response.status_code}")
            print(response.text)
            break

    notes = []
    for result in all_results:
        properties = result["properties"]

        # Handling the 'Episode' title
        episode_title = properties.get("Episode", {}).get("title", [])
        title = episode_title[0].get("text", {}).get("content", "") if episode_title else ""

        priority_select = properties.get("Priority", {}).get("select")
        priority = priority_select.get("name") if priority_select else "None"

        dates_gc = properties.get("Dates(GC)", {}).get("date", {})

        # Building the note dictionary, you can remove fileds if not needed
        note = {
            "ID": result["id"],
            "Episode": title, 
            "statuss": properties.get("statuss", {}).get("select", {}).get("name", ""),
            "Created": properties.get("Created", {}).get("created_time", ""),
            "Tags": ", ".join(tag.get("name", "") for tag in properties.get("Tags", {}).get("multi_select", [])),
            "Keep": properties.get("Keep", False),
            "Dates(GC)": dates_gc.get("start", {}) if dates_gc else {},
            "Priority": priority,
            "Updated": properties.get("Updated", {}).get("last_edited_time", ""),
        }
        notes.append(note)

    return notes

def filter_notes(question):
    if not question:
        return {"error": "No question provided"}
    
    #Ask a question to the ai provider, and it will return proper filter
    filter = filter_for_notion(question)
    notes = fetch_notes(filter)
    
    # Store response in SQLite
    conn = sqlite3.connect('questions_responses.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO responses (question, response_status, filter_body, notes)
        VALUES (?, ?, ?, ?)
    ''', (json.dumps(question), 200, json.dumps(filter), json.dumps(notes)))
    conn.commit()
    conn.close()

    return {
        "filter_body": filter,
        "notes": notes
    }


fetch_notes_string = '''
def fetch_notes(filter):
    headers = {
        'Authorization': f"Bearer {NOTION_API_KEY}",
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    all_results = []
    has_more = True
    next_cursor = None

    while has_more:
        if next_cursor:
            filter["start_cursor"] = next_cursor

        response = requests.post(url, headers=headers, data=json.dumps(filter))
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor", None)
        else:
            print(f"Failed to fetch data: {response.status_code}")
            print(response.text)
            break

    notes = []
    for result in all_results:
        properties = result["properties"]

        # Handling the 'Episode' title
        episode_title = properties.get("Episode", {}).get("title", [])
        title = episode_title[0].get("text", {}).get("content", "") if episode_title else ""

        priority_select = properties.get("Priority", {}).get("select")
        priority = priority_select.get("name") if priority_select else "None"

        dates_gc = properties.get("Dates(GC)", {}).get("date", {})

        # Building the note dictionary, you can remove fileds if not needed
        note = {
            "ID": result["id"],
            "Episode": title, 
            "statuss": properties.get("statuss", {}).get("select", {}).get("name", ""),
            "Created": properties.get("Created", {}).get("created_time", ""),
            "Tags": ", ".join(tag.get("name", "") for tag in properties.get("Tags", {}).get("multi_select", [])),
            "Keep": properties.get("Keep", False),
            "Dates(GC)": dates_gc.get("start", {}) if dates_gc else {},
            "Priority": priority,
            "Updated": properties.get("Updated", {}).get("last_edited_time", ""),
        }
        notes.append(note)

    return notes
'''