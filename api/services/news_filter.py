"""
News Filter Service for GenX FX Trading Platform
Provides functionality to pause trading during high-impact economic news events.
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import aiohttp

logger = logging.getLogger(__name__)

class NewsFilter:
    """
    A service that fetches economic calendar data and provides a flag to
    pause trading during high-impact news events.
    """

    def __init__(self, impact_threshold: str = "HIGH"):
        self.impact_threshold = impact_threshold
        self.events = []
        self.last_update = None
        self.update_interval = 3600  # Update every hour
        self.pause_window_before = 30  # Minutes before event to pause
        self.pause_window_after = 30   # Minutes after event to resume

    async def update_calendar(self):
        """
        Fetches the latest economic calendar data.
        In a real implementation, this would call a financial calendar API.
        """
        try:
            # Mock implementation of fetching calendar data
            # Real implementation could use ForexFactory, EconomicCalendar, etc.
            logger.info("Updating economic calendar...")

            # Example mock events
            now = datetime.now()
            self.events = [
                {
                    "title": "NFP (Non-Farm Payrolls)",
                    "impact": "HIGH",
                    "time": now + timedelta(minutes=45),
                    "currency": "USD"
                },
                {
                    "title": "FOMC Meeting Minutes",
                    "impact": "HIGH",
                    "time": now + timedelta(hours=2),
                    "currency": "USD"
                }
            ]

            self.last_update = now
            logger.info(f"Economic calendar updated with {len(self.events)} events.")

        except Exception as e:
            logger.error(f"Failed to update economic calendar: {e}")

    async def should_pause_trading(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Checks if trading should be paused based on upcoming or recent high-impact news.

        Returns:
            Tuple[bool, Optional[Dict[str, Any]]]: (True if trading should be paused, the event causing the pause)
        """
        if not self.last_update or (datetime.now() - self.last_update).total_seconds() > self.update_interval:
            await self.update_calendar()

        now = datetime.now()

        for event in self.events:
            if event["impact"] == self.impact_threshold:
                event_time = event["time"]

                # Check if we are within the pause window
                start_pause = event_time - timedelta(minutes=self.pause_window_before)
                end_pause = event_time + timedelta(minutes=self.pause_window_after)

                if start_pause <= now <= end_pause:
                    logger.warning(f"Trading paused due to high-impact event: {event['title']} at {event_time}")
                    return True, event

        return False, None

    async def get_upcoming_events(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Returns upcoming high-impact events within the specified time frame.
        """
        now = datetime.now()
        upcoming = [
            e for e in self.events
            if e["impact"] == self.impact_threshold and now <= e["time"] <= now + timedelta(hours=hours)
        ]
        return upcoming
