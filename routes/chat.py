from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from extensions import db
from models import Conversation, Message
from config import Config
from utils import check_subscription

import ollama

chat = Blueprint("chat", __name__)


# =========================
# NEW CHAT
# =========================
@chat.route("/new-chat")
@login_required
def new_chat():

    conversation = Conversation(
        title="New Chat",
        user_id=current_user.id
    )

    db.session.add(conversation)
    db.session.commit()

    return redirect(url_for("chat.chat_page", conversation_id=conversation.id))


# =========================
# CHAT PAGE (MAIN)
# =========================
@chat.route("/chat/<int:conversation_id>", methods=["GET", "POST"])
@login_required
def chat_page(conversation_id):

    # LOAD CONVERSATION
    conversation = Conversation.query.filter_by(
        id=conversation_id,
        user_id=current_user.id
    ).first_or_404()

    # 🔥 BEST PLACE (WEB PROTECTION)
    # BLOCK ACCESS BEFORE ANY AI / DB LOGIC
    if not check_subscription(current_user):
        return "❌ Your free trial has expired. Please upgrade your plan."

    if request.method == "POST":

        user_message = request.form.get("message")

        if user_message:

            # SAVE USER MESSAGE
            user_msg = Message(
                role="user",
                content=user_message,
                conversation_id=conversation.id
            )
            db.session.add(user_msg)
            db.session.commit()

            # AUTO TITLE
            if conversation.title == "New Chat":
                conversation.title = user_message[:30]
                db.session.commit()

            # MEMORY BUILD
            history = Message.query.filter_by(
                conversation_id=conversation.id
            ).order_by(Message.created_at.asc()).all()

            messages = [
                {"role": "system", "content": "You are AI Universe Assistant."}
            ]

            for msg in history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # AI RESPONSE
            response = ollama.chat(
                model=Config.OLLAMA_MODEL,
                messages=messages
            )

            ai_text = response["message"]["content"]

            # SAVE AI MESSAGE
            ai_msg = Message(
                role="assistant",
                content=ai_text,
                conversation_id=conversation.id
            )
            db.session.add(ai_msg)
            db.session.commit()

    # LOAD MESSAGES
    messages = Message.query.filter_by(
        conversation_id=conversation.id
    ).order_by(Message.created_at.asc()).all()

    # LOAD SIDEBAR CONVERSATIONS
    conversations = Conversation.query.filter_by(
        user_id=current_user.id
    ).order_by(Conversation.created_at.desc()).all()

    return render_template(
        "chat.html",
        messages=messages,
        conversation=conversation,
        conversations=conversations
    )


# =========================
# RENAME CHAT
# =========================
@chat.route("/rename-chat/<int:conversation_id>", methods=["POST"])
@login_required
def rename_chat(conversation_id):

    conversation = Conversation.query.filter_by(
        id=conversation_id,
        user_id=current_user.id
    ).first_or_404()

    new_title = request.form.get("title")

    if new_title:
        conversation.title = new_title[:50]
        db.session.commit()

    return redirect(url_for("chat.chat_page", conversation_id=conversation.id))


# =========================
# SOCKET.IO SUPPORT (SECURE)
# =========================
def register_socket_events(socketio):

    @socketio.on("send_message")
    def handle_send_message(data):

        from flask_login import current_user

        if not current_user.is_authenticated:
            return

        # 🔥 BEST PLACE (SOCKET PROTECTION)
        # BLOCK BEFORE PROCESSING MESSAGE
        if not check_subscription(current_user):
            socketio.emit("receive_message", {
                "text": "❌ Subscription expired. Please upgrade plan."
            })
            return

        message = data.get("message")
        conversation_id = data.get("conversation_id")

        if not message:
            return

        # SAVE USER MESSAGE
        user_msg = Message(
            role="user",
            content=message,
            conversation_id=conversation_id
        )
        db.session.add(user_msg)
        db.session.commit()

        # MEMORY BUILD
        history = Message.query.filter_by(
            conversation_id=conversation_id
        ).order_by(Message.created_at.asc()).all()

        messages = [
            {"role": "system", "content": "You are AI Universe Assistant."}
        ]

        for msg in history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # AI RESPONSE
        response = ollama.chat(
            model=Config.OLLAMA_MODEL,
            messages=messages
        )

        ai_text = response["message"]["content"]

        # SAVE AI MESSAGE
        ai_msg = Message(
            role="assistant",
            content=ai_text,
            conversation_id=conversation_id
        )
        db.session.add(ai_msg)
        db.session.commit()

        # SEND RESPONSE
        socketio.emit("receive_message", {
            "text": ai_text
        })