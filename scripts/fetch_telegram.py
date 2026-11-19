#!/usr/bin/env python3
"""Fetch recent Telegram channel/supergroup posts into data/telegram-feed.json.

Read-only by construction: this script only calls iter_dialogs / iter_messages.
It shares one session with the read-only Telegram MCP server via
~/.config/telegram-mcp/config.json (mode 0600), written by --login.

Usage:
  python3 scripts/fetch_telegram.py --login        # one-time interactive auth
  python3 scripts/fetch_telegram.py [--hours 48] [--max-per-chat 100]

Requires telethon in whatever Python environment you use, e.g.:
  python3 -m venv .venv && .venv/bin/pip install telethon
  .venv/bin/python scripts/fetch_telegram.py
"""
from __future__ import annotations

import argparse
import asyncio
import getpass
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(
    os.environ.get("TG_CONFIG_PATH")
    or Path.home() / ".config" / "telegram-mcp" / "config.json"
)
FEED_PATH = REPO_ROOT / "data" / "telegram-feed.json"
LINK_RE = re.compile(r"(?:https?|tg)://[^\s)>\]}\"']+")

try:
    from telethon import TelegramClient
    from telethon.sessions import StringSession
except ModuleNotFoundError:
    sys.exit(
        "telethon is not importable. Install it in your Python environment:\n"
        "  python3 -m pip install telethon"
    )


def button_urls(reply_markup) -> list[str]:
    """Extract URLs from inline keyboard buttons.

    Handles both Telethon's decoded InlineKeyboardButton (.url) and raw TL
    KeyboardInlineButton (.type.url). JobStash-style posts carry the apply
    link ONLY here, not in the message text.
    """
    urls: list[str] = []
    rows = getattr(reply_markup, "rows", None) or getattr(reply_markup, "inline_keyboard", []) or []
    for row in rows:
        for btn in getattr(row, "buttons", []):
            url = getattr(btn, "url", None) or getattr(getattr(btn, "type", None), "url", None)
            if url:
                urls.append(url)
    return urls


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def load_dotenv() -> None:
    """Minimal .env loader: KEY=VALUE lines, # comments, optional quotes. Does not override real env."""
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_config() -> tuple[int, str, str]:
    if not CONFIG_PATH.exists():
        sys.exit(f"No config at {CONFIG_PATH}. Run:\n  python3 scripts/fetch_telegram.py --login")
    cfg = json.loads(CONFIG_PATH.read_text())
    return int(cfg["api_id"]), cfg["api_hash"], cfg["session_string"]


async def do_login() -> None:
    load_dotenv()
    env_id = os.environ.get("TG_API_ID", "").strip()
    env_hash = os.environ.get("TG_API_HASH", "").strip()
    api_id = env_id or input("api_id (from my.telegram.org/apps): ").strip()
    api_hash = env_hash or getpass.getpass("api_hash (hidden): ").strip()
    if not api_id or not api_hash:
        sys.exit("api_id and api_hash are required. Get them at https://my.telegram.org/apps")

    client = TelegramClient(StringSession(), int(api_id), api_hash, receive_updates=False)
    await client.start(
        phone=lambda: input("Phone (international, e.g. +234...): ").strip(),
        password=lambda: getpass.getpass("2FA password (blank if none): ").strip() or None,
        code_callback=lambda: input("Code Telegram just sent you: ").strip(),
    )
    session = client.session.save()
    await client.disconnect()

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(
            {
                "api_id": int(api_id),
                "api_hash": api_hash,
                "session_string": session,
                "max_messages_per_call": 500,
            },
            indent=2,
        )
    )
    os.chmod(CONFIG_PATH, 0o600)
    print(f"Saved {CONFIG_PATH} (mode 0600).")
    print("The read-only Telegram MCP and this script can now read your channels.")


async def do_fetch(hours: float, max_per_chat: int) -> None:
    api_id, api_hash, session = load_config()
    since = datetime.now(timezone.utc) - timedelta(hours=hours)

    client = TelegramClient(StringSession(session), api_id, api_hash, receive_updates=False)
    await client.connect()
    if not await client.is_user_authorized():
        sys.exit("Session is not authorized. Re-run: python3 scripts/fetch_telegram.py --login")

    messages: list[dict] = []
    channels: list[dict] = []
    skipped_dialogs = 0

    async for dialog in client.iter_dialogs():
        if not dialog.is_channel:  # broadcast channels + megagroups only; skip DMs/basic groups/bots
            skipped_dialogs += 1
            continue
        ent = dialog.entity
        title = getattr(ent, "title", "?") or f"channel {ent.id}"
        username = getattr(ent, "username", None)
        kept = 0
        async for msg in client.iter_messages(ent, limit=max_per_chat):
            if msg.date and msg.date.astimezone(timezone.utc) < since:
                break
            text = (msg.message or "").strip()
            if not text:
                continue  # media-only posts carry no JD text
            messages.append(
                {
                    "channel": title,
                    "channelId": ent.id,
                    "username": username,
                    "messageId": msg.id,
                    "date": msg.date.astimezone(timezone.utc).isoformat() if msg.date else None,
                    "text": text,
                    "links": dedupe(LINK_RE.findall(text) + button_urls(msg.reply_markup)),
                    "url": f"https://t.me/{username}/{msg.id}" if username else None,
                    "views": getattr(msg, "views", None),
                }
            )
            kept += 1
        if kept:
            channels.append({"title": title, "username": username, "messagesKept": kept})

    await client.disconnect()

    FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "windowHours": hours,
        "since": since.isoformat(),
        "channelsScanned": len(channels),
        "dialogsSkipped": skipped_dialogs,
        "messages": messages,
        "channels": channels,
    }
    FEED_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

    print(f"Scanned {len(channels)} channels/supergroups with posts since {since.date()} "
          f"({skipped_dialogs} non-channel dialogs skipped).")
    print(f"Kept {len(messages)} text posts -> {FEED_PATH}")
    for c in sorted(channels, key=lambda c: -c["messagesKept"]):
        print(f"  {c['messagesKept']:4d}  {c['title']}")


def main() -> None:
    load_dotenv()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--login", action="store_true", help="one-time interactive auth; writes ~/.config/telegram-mcp/config.json")
    p.add_argument("--hours", type=float, default=48, help="lookback window in hours (default: 48)")
    p.add_argument("--max-per-chat", type=int, default=100, help="max messages to pull per channel (default: 100)")
    args = p.parse_args()

    if args.login:
        asyncio.run(do_login())
    else:
        asyncio.run(do_fetch(args.hours, args.max_per_chat))


if __name__ == "__main__":
    main()
