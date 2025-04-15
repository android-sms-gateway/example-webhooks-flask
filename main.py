import hashlib
import hmac
from datetime import datetime

import httpx
from flask import Flask, current_app, jsonify, request
from pydantic import BaseModel, Field, ValidationError


class SMSReceivedData(BaseModel):
    message: str
    received_at: datetime = Field(alias="receivedAt")
    message_id: str = Field(alias="messageId")
    phone_number: str = Field(alias="phoneNumber")
    sim_number: int = Field(alias="simNumber")


class WebhookPayload(BaseModel):
    device_id: str = Field(..., alias="deviceId")
    event: str = Field(..., pattern="^(sms:received)$")
    id: str
    webhook_id: str = Field(..., alias="webhookId")
    payload: SMSReceivedData


def create_app():
    app = Flask(__name__)
    app.config["SMS_GATE_API_URL"] = "https://api.sms-gate.app/3rdparty/v1"
    app.config.from_prefixed_env()

    @app.route("/webhook/sms-received", methods=["POST"])
    def handle_sms_webhook():
        body = request.get_data()

        if current_app.config.get("WEBHOOK_SECRET"):
            signature = request.headers.get("X-Signature")
            timestamp = request.headers.get("X-Timestamp")
            if not signature or not timestamp:
                return jsonify({"detail": "Missing signature headers"}), 401

            expected_signature = hmac.new(
                current_app.config.get("WEBHOOK_SECRET").encode(),
                body + timestamp.encode(),
                hashlib.sha256,
            ).hexdigest()

            if not hmac.compare_digest(signature, expected_signature):
                return jsonify({"detail": "Invalid signature"}), 401

        try:
            payload = WebhookPayload.model_validate_json(body)
        except ValidationError as e:
            return jsonify({"detail": "Invalid payload format"}), 400

        if payload.webhook_id != current_app.config["WEBHOOK_ID"]:
            return jsonify({"detail": "Invalid webhook ID"}), 400

        print("Received SMS:")
        print(f"SIM: {payload.payload.sim_number}")
        print(f"From: {payload.payload.phone_number}")
        print(f"Message: {payload.payload.message}")
        print(f"Received at: {payload.payload.received_at}")

        return jsonify({"status": "ok"})

    return app


def register_webhook() -> None | str:
    if not all(
        [
            current_app.config.get("SMS_GATE_API_USERNAME"),
            current_app.config.get("SMS_GATE_API_PASSWORD"),
            current_app.config.get("WEBHOOK_URL"),
        ]
    ):
        return

    with httpx.Client() as client:
        response = client.post(
            f"{current_app.config["SMS_GATE_API_URL"]}/webhooks",
            auth=(
                current_app.config["SMS_GATE_API_USERNAME"],
                current_app.config["SMS_GATE_API_PASSWORD"],
            ),
            json={"url": current_app.config["WEBHOOK_URL"], "event": "sms:received"},
        )
        response.raise_for_status()
        webhook_id = response.json()["id"]
        current_app.config["WEBHOOK_ID"] = webhook_id

        print(f"Registered webhook ID: {webhook_id}")

        return webhook_id


def unregister_webhook(webhook_id: str | None):
    if not all(
        [
            current_app.config.get("SMS_GATE_API_USERNAME"),
            current_app.config.get("SMS_GATE_API_PASSWORD"),
            current_app.config.get("WEBHOOK_ID"),
        ]
    ):
        return

    with httpx.Client() as client:
        response = client.delete(
            f"{current_app.config['SMS_GATE_API_URL']}/webhooks/{current_app.config["WEBHOOK_ID"]}",
            auth=(
                current_app.config["SMS_GATE_API_USERNAME"],
                current_app.config["SMS_GATE_API_PASSWORD"],
            ),
        )
        response.raise_for_status()
        print(f"Unregistered webhook ID: {current_app.config["WEBHOOK_ID"]}")


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        webhook_id = register_webhook()

    try:
        ssl_context = (
            (app.config["SSL_CERT_PATH"], app.config["SSL_KEY_PATH"])
            if app.config.get("SSL_CERT_PATH") and app.config.get("SSL_KEY_PATH")
            else None
        )
        app.run(
            host="0.0.0.0", port=8443 if ssl_context else 8080, ssl_context=ssl_context
        )
    finally:
        with app.app_context():
            unregister_webhook(webhook_id)
