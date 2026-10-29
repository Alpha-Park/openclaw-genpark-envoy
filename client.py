# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Envoy - Inter-Agent Mutual Handshake & Secure Envelope Router
Standard Library only: hmac, hashlib, json, time, typing.
Cryptographic agent-to-agent envelope serialization, replay attack protection,
and capability handshake verification.
"""

import hmac
import hashlib
import json
import time
from typing import Dict, List, Any

class OpenClawGenParkEnvoy:
    def __init__(self, shared_secret: str = "openclaw-agent-envoy-key-2026"):
        self.secret = shared_secret.encode("utf-8")
        self.seen_nonces = set()

    def package_envelope(self, sender_agent_id: str, receiver_agent_id: str,
                         intent: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates an HMAC-SHA256 authenticated envelope with timestamp and unique nonce.
        """
        timestamp = time.time()
        nonce = hashlib.sha256(f"{sender_agent_id}:{timestamp}:{time.time_ns()}".encode("utf-8")).hexdigest()[:16]

        body = {
            "sender": sender_agent_id,
            "receiver": receiver_agent_id,
            "intent": intent,
            "timestamp": timestamp,
            "nonce": nonce,
            "payload": payload
        }

        canonical_bytes = json.dumps(body, sort_keys=True, separators=(',', ':')).encode("utf-8")
        signature = hmac.new(self.secret, canonical_bytes, hashlib.sha256).hexdigest()

        return {
            "envelope": body,
            "signature": signature
        }

    def verify_and_unpack(self, envelope: Dict[str, Any], signature: str,
                          max_drift_seconds: float = 300.0) -> Dict[str, Any]:
        """
        Verifies HMAC signature, checks for replay attacks, and enforces validity window.
        """
        canonical_bytes = json.dumps(envelope, sort_keys=True, separators=(',', ':')).encode("utf-8")
        expected_sig = hmac.new(self.secret, canonical_bytes, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            return {"verified": False, "reason": "INVALID_SIGNATURE", "payload": {}}

        nonce = envelope.get("nonce")
        if nonce in self.seen_nonces:
            return {"verified": False, "reason": "REPLAY_ATTACK_DETECTED", "payload": {}}
        self.seen_nonces.add(nonce)

        # Check timestamp drift
        t = float(envelope.get("timestamp", 0))
        if abs(time.time() - t) > max_drift_seconds:
            return {"verified": False, "reason": "TIMESTAMP_EXPIRED", "payload": {}}

        return {
            "verified": True,
            "sender": envelope["sender"],
            "intent": envelope["intent"],
            "payload": envelope["payload"]
        }
