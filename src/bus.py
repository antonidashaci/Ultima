#!/usr/bin/env python3
"""A very lightweight in-process message bus used by ULTIMA agents.
Currently just wraps an asyncio.Queue; later can be upgraded to ZeroMQ or Redis.
All messages are dicts with at least a `type` key.
"""

import asyncio
from typing import Dict, Any

class Bus:
    def __init__(self):
        self._queue: asyncio.Queue = asyncio.Queue()

    async def publish(self, message: Dict[str, Any]):
        """Put a message onto the bus."""
        await self._queue.put(message)

    async def subscribe(self):
        """Async generator that yields messages as they arrive."""
        while True:
            msg = await self._queue.get()
            yield msg

# Global bus instance
bus = Bus() 