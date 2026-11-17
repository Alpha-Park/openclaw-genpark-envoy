# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkEnvoy

envoy = OpenClawGenParkEnvoy()

def run_tool(name, args):
    if name == "package_envelope":
        sender = args.get("sender_agent_id", "agent_a")
        receiver = args.get("receiver_agent_id", "agent_b")
        intent = args.get("intent", "task_delegation")
        payload = args.get("payload", {})
        return envoy.package_envelope(sender, receiver, intent, payload)
    elif name == "verify_and_unpack":
        env = args.get("envelope", {})
        sig = args.get("signature", "")
        return envoy.verify_and_unpack(env, sig)
    else:
        raise ValueError(f"Unknown tool: {name}")

from typing import Any, Dict, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("MCP requires the mcp package. Run: python -m pip install -r requirements.txt") from exc

mcp = FastMCP('openclaw-genpark-envoy')

@mcp.tool()
def package_envelope(sender_agent_id: str = "agent_a", receiver_agent_id: str = "agent_b", intent: str = "task_delegation", payload: Optional[Dict[str, Any]] = None) -> str:
    """Package a signed inter-agent envelope."""
    return json.dumps(run_tool('package_envelope', {'sender_agent_id': sender_agent_id, 'receiver_agent_id': receiver_agent_id, 'intent': intent, 'payload': payload if payload is not None else {}}))

@mcp.tool()
def verify_and_unpack(envelope: Optional[Dict[str, Any]] = None, signature: str = "") -> str:
    """Verify and unpack a signed inter-agent envelope."""
    return json.dumps(run_tool('verify_and_unpack', {'envelope': envelope if envelope is not None else {}, 'signature': signature}))

def main():
    if "--test" in sys.argv:
        print("[TEST] Running OpenClaw Envoy Self-Test...")
        pkg = envoy.package_envelope("agent_001", "agent_002", "ping", {"data": "hello"})
        res = envoy.verify_and_unpack(pkg["envelope"], pkg["signature"])
        assert res["verified"] is True
        # Replay attack test
        res_replay = envoy.verify_and_unpack(pkg["envelope"], pkg["signature"])
        assert res_replay["verified"] is False
        assert res_replay["reason"] == "REPLAY_ATTACK_DETECTED"
        print("[TEST] All tests passed successfully!")
        return

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
