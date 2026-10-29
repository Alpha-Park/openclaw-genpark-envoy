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

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            res = run_tool(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"jsonrpc": "2.0", "id": req.get("id"), "result": res}))
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
