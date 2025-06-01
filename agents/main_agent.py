#!/usr/bin/env python3
"""
Main Background Agent for Open To Close API

This agent runs continuously and performs various background tasks
such as syncing properties, monitoring changes, and processing updates.
"""

import asyncio
import logging
import os
import signal
import sys
import time
from datetime import datetime
from typing import Optional

from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import OpenToCloseAPIError


class OpenToCloseAgent:
    """Main background agent for Open To Close API operations."""
    
    def __init__(self) -> None:
        """Initialize the agent with configuration from environment variables."""
        self.api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
        if not self.api_key:
            raise ValueError("OPEN_TO_CLOSE_API_KEY environment variable is required")
        
        self.client = OpenToCloseAPI(api_key=self.api_key)
        self.interval = int(os.getenv("AGENT_INTERVAL_SECONDS", "60"))
        self.max_retries = int(os.getenv("AGENT_MAX_RETRIES", "3"))
        self.environment = os.getenv("ENVIRONMENT", "development")
        
        # Setup logging
        self._setup_logging()
        
        # Agent state
        self.running = False
        self.last_run = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info(f"OpenToClose Agent initialized for {self.environment} environment")
        self.logger.info(f"Running every {self.interval} seconds")
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # Create logs directory if it doesn't exist
        os.makedirs("/app/logs", exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(f"/app/logs/agent_{datetime.now().strftime('%Y%m%d')}.log")
            ]
        )
        
        self.logger = logging.getLogger("OpenToCloseAgent")
    
    def _signal_handler(self, signum: int, frame: object) -> None:
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    async def health_check(self) -> bool:
        """Perform a basic health check by testing API connectivity."""
        try:
            # Simple API call to verify connectivity
            properties = self.client.properties.list_properties()
            self.logger.debug("Health check passed - API is accessible")
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    async def sync_properties(self) -> None:
        """Sync and process properties data."""
        try:
            self.logger.info("Starting property sync...")
            
            # Get all properties
            properties = self.client.properties.list_properties()
            self.logger.info(f"Found {len(properties)} properties")
            
            # Process each property
            for prop in properties:
                await self._process_property(prop)
                
            self.logger.info("Property sync completed successfully")
            
        except OpenToCloseAPIError as e:
            self.logger.error(f"API error during property sync: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error during property sync: {e}")
    
    async def _process_property(self, property_data: dict) -> None:
        """Process individual property data."""
        try:
            property_id = property_data.get("id")
            if property_id is None:
                self.logger.warning("Property has no ID, skipping")
                return
                
            address = property_data.get("address", "Unknown")
            
            self.logger.debug(f"Processing property {property_id}: {address}")
            
            # Example: Check for new notes
            notes = self.client.property_notes.list_property_notes(int(property_id))
            self.logger.debug(f"Property {property_id} has {len(notes)} notes")
            
            # Example: Check for new tasks
            tasks = self.client.property_tasks.list_property_tasks(int(property_id))
            self.logger.debug(f"Property {property_id} has {len(tasks)} tasks")
            
            # Add your custom property processing logic here
            # For example:
            # - Send notifications for overdue tasks
            # - Update external systems
            # - Generate reports
            # - Monitor price changes
            
        except Exception as e:
            self.logger.error(f"Error processing property {property_data.get('id')}: {e}")
    
    async def monitor_contacts(self) -> None:
        """Monitor contacts for updates or new entries."""
        try:
            self.logger.info("Starting contact monitoring...")
            
            # Get recent contacts
            contacts = self.client.contacts.list_contacts()
            self.logger.info(f"Found {len(contacts)} contacts")
            
            # Add your contact monitoring logic here
            # For example:
            # - Check for new leads
            # - Update contact scores
            # - Send follow-up reminders
            
            self.logger.info("Contact monitoring completed")
            
        except OpenToCloseAPIError as e:
            self.logger.error(f"API error during contact monitoring: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error during contact monitoring: {e}")
    
    async def run_cycle(self) -> None:
        """Run one complete cycle of agent tasks."""
        cycle_start = time.time()
        self.logger.info("Starting agent cycle...")
        
        try:
            # Perform health check
            if not await self.health_check():
                self.logger.warning("Health check failed, skipping this cycle")
                return
            
            # Run main tasks
            await self.sync_properties()
            await self.monitor_contacts()
            
            # Add more tasks here as needed
            # await self.process_teams()
            # await self.generate_reports()
            # await self.cleanup_old_data()
            
            cycle_duration = time.time() - cycle_start
            self.logger.info(f"Agent cycle completed in {cycle_duration:.2f} seconds")
            
        except Exception as e:
            self.logger.error(f"Error during agent cycle: {e}")
        
        self.last_run = datetime.now()
    
    async def run(self) -> None:
        """Main agent loop."""
        self.logger.info("Starting OpenToClose background agent...")
        self.running = True
        
        while self.running:
            try:
                await self.run_cycle()
                
                # Wait for next cycle
                if self.running:  # Check again in case we got a shutdown signal
                    self.logger.debug(f"Waiting {self.interval} seconds until next cycle...")
                    await asyncio.sleep(self.interval)
                    
            except KeyboardInterrupt:
                self.logger.info("Received keyboard interrupt, shutting down...")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {e}")
                if self.running:
                    await asyncio.sleep(5)  # Brief pause before retry
        
        self.logger.info("OpenToClose background agent stopped")


async def main() -> None:
    """Main entry point for the agent."""
    try:
        agent = OpenToCloseAgent()
        await agent.run()
    except KeyboardInterrupt:
        print("\nAgent stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 