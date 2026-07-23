import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="Two-Page Site API")

app.add_middleware(
CORSMiddleware,
allow_origins=["http://localhost:5173"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

supabase: Client = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SECRET_KEY"],
)

class ButtonEvent(BaseModel):
    page_slug: str
    button_label: str

@app.get("/api/pages/{slug}")
def get_page(slug: str):
    result = (
        supabase
        .table("pages")
        .select("*")
        .eq("slug", slug)
        .single()
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Page not found")

    return result.data

@app.post("/api/events/button-click")
def save_button_click(event: ButtonEvent):
    result = supabase.table("button_events").insert(
        {
            "page_slug": event.page_slug,
            "button_label": event.button_label,
        }
    ).execute()

    return {"ok": True, "event": result.data}