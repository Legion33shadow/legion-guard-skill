#!/usr/bin/env python3
"""Opens ONE MCP session (streamable HTTP), wraps it with legion-guard, reads tools/list at the start, then re-reads it
--relist times every --interval seconds in the SAME session, without calling any tool. Prints the guard report as JSON.
Usage: watch_session.py URL [SERVER_ID] [--mode warn|block] [--relist N] [--interval S] [--no-legion] [--pins FILE]
Network: the MCP server URL; plus tlog.legion-api.com only if SERVER_ID is given and --no-legion is absent.
Exit: 0 no change detected, 1 change detected, 2 connection error, 3 nothing could be verified (UNVERIFIED)."""
import argparse, asyncio, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import legion_guard as G


async def run(a):
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client
    sources = [G.FirstUseSource(a.pins)] + ([G.LegionSource()] if a.server_id and not a.no_legion else [])
    async with streamable_http_client(a.url) as (r, w, *_):
        async with ClientSession(r, w) as s:
            await s.initialize()
            gs = G.wrap(s, a.server_id, sources=sources, mode=a.mode)
            await gs.list_tools()
            for _ in range(a.relist):
                await asyncio.sleep(a.interval)
                await gs.list_tools()
            return gs.report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("server_id", nargs="?")
    ap.add_argument("--mode", choices=["warn", "block"], default="warn")
    ap.add_argument("--relist", type=int, default=0); ap.add_argument("--interval", type=float, default=30.0)
    ap.add_argument("--no-legion", action="store_true"); ap.add_argument("--pins", default=None)
    a = ap.parse_args()
    try:
        rep = asyncio.run(run(a))
    except Exception as e:
        print(json.dumps({"verdict": None, "error": "MCP connection failed: %s" % type(e).__name__})); return 2
    print(json.dumps(rep, indent=1, ensure_ascii=False, default=str))
    v = (rep or {}).get("verdict")
    return 1 if v == "CHANGE_DETECTED" else 3 if v in ("UNVERIFIED", "GUARD_ERROR") else 0


if __name__ == "__main__":
    sys.exit(main())
