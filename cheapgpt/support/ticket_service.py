# Registro de tickets de soporte (reclamos) con persistencia en memoria.

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

MIN_MESSAGE_LENGTH = 10

@dataclass(frozen=True)class ComplaintData:    name: stremail: strmessage: strchannel: stris_premium: boolprevious_tickets: intlanguage: strcreated_at: datetime
@dataclass(frozen=True)
class Ticket:
    id: str
    name: str
    email: str
    message: str
    channel: str
    is_premium: bool
    previous_tickets: int
    language: str
    created_at: datetime
    priority: str
    auto_reply: str


class TicketService:
    def __init__(self, clock: Callable[[], datetime]) -> None:
        self._clock = clock
        self._tickets: list[Ticket] = []
        self._counter = 0

    def tickets_for(self, email: str) -> list[Ticket]:
        return [ticket for ticket in self._tickets if ticket.email == email]

    def submit_complaint(
        self,
        name: str,
        email: str,
        message: str,
        channel: str = "web",
        is_premium: bool = False,
        language: str = "es",
    ) -> Ticket:
        previous_tickets = len(self.tickets_for(email))
        created_at = self._clock()
       return self._register_ticket(
            ComplaintData(name, email, message, channel, is_premium, previous_tickets, language, created_at)
        )
 
    def _register_ticket(self, data: ComplaintData) -> Ticket:
        name, email, message = data.name, data.email, data.message
        channel, is_premium, language = data.channel, data.is_premium, data.language
        previous_tickets, created_at = data.previous_tickets, data.created_at
tiene menú contextual

        self._validate(name, email, message)
        priority = self._compute_priority(message, is_premium, previous_tickets)
        self._counter += 1
        ticket_id = f"CHEAP-{self._counter:04d}"
        auto_reply = self._auto_reply(language, priority)

        ticket = Ticket(
            id=ticket_id,
            name=name,
            email=email,
            message=message,
            channel=channel,
            is_premium=is_premium,
            previous_tickets=previous_tickets,
            language=language,
            created_at=created_at,
            priority=priority,
            auto_reply=auto_reply,
        )
        self._tickets.append(ticket)
        return ticket
    def _validate(self, name, email, message):
        if not name.strip():
            raise ValueError("El nombre no puede estar vacio")
        if "@" not in email:
            raise ValueError("El email no es valido")
        if len(message.strip()) < MIN_MESSAGE_LENGTH:
            raise ValueError("El mensaje es demasiado corto")

    def _compute_priority(self, message, is_premium, previous_tickets):
        if is_premium or "urgente" in message.lower():
            return "alta"
        if previous_tickets > 3:
            return "media"
        return "baja"

    def _auto_reply(self, language, priority):
        if language == "en":
            replies = {
                "alta": "We got your complaint and it's on fire (priority-wise, we hope not literally).",
                "media": "We got your complaint. You're a frequent flyer, we'll get to it soon-ish.",
                "baja": "We got your complaint. It'll sit in the queue with the other cheap problems.",
            }
        else:
            replies = {
                "alta": "Recibimos tu reclamo y esta que arde (de prioridad, esperamos que no literal).",
                "media": "Recibimos tu reclamo. Ya eres cliente frecuente del drama, lo veremos pronto.",
                "baja": "Recibimos tu reclamo. Hara fila con los demas problemas baratos.",
            }
        return replies[priority]
