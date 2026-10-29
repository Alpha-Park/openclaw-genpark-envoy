# -*- coding: utf-8 -*-
from client import OpenClawGenParkEnvoy

def main():
    envoy = OpenClawGenParkEnvoy()
    print("=== OpenClaw GenPark Agent Envoy Protocol ===")

    # Sender creates secure envelope
    pack = envoy.package_envelope(
        sender_agent_id="research_agent_v1",
        receiver_agent_id="execution_agent_v1",
        intent="TRADE_EXECUTION_REQUEST",
        payload={"pair": "ETH/USDC", "amount": 10.5, "max_slippage": 0.005}
    )
    print("Envelope Packaged:")
    print(f"  Nonce: {pack['envelope']['nonce']}")
    print(f"  Signature: {pack['signature'][:24]}...")

    # Receiver validates envelope
    unpack = envoy.verify_and_unpack(pack["envelope"], pack["signature"])
    print()
    print(f"Unpack Result: verified={unpack['verified']}, sender={unpack.get('sender')}")

if __name__ == "__main__":
    main()
