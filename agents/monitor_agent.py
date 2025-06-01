#!/usr/bin/env python3
"""
Monitoring Agent for Open To Close API

This agent monitors the health and performance of the main agent
and the API itself, providing metrics and alerts.
"""

import asyncio
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import OpenToCloseAPIError


class MonitorAgent:
    """Monitoring agent for Open To Close API and main agent."""
    
    def __init__(self) -> None:
        """Initialize the monitoring agent."""
        self.api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
        if not self.api_key:
            raise ValueError("OPEN_TO_CLOSE_API_KEY environment variable is required")
        
        self.client = OpenToCloseAPI(api_key=self.api_key)
        self.check_interval = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
        self.metrics_enabled = os.getenv("ENABLE_METRICS", "false").lower() == "true"
        
        # Setup logging
        self._setup_logging()
        
        # Monitoring state
        self.running = False
        self.response_times: List[float] = []
        self.error_count = 0
        self.success_count = 0
        self.metrics: Dict[str, Any] = {
            "api_health": {"status": "unknown", "last_check": None},
            "uptime_start": datetime.now()
        }
        
        self.logger.info("Monitor Agent initialized")
    
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
                logging.FileHandler(f"/app/logs/monitor_{datetime.now().strftime('%Y%m%d')}.log")
            ]
        )
        
        self.logger = logging.getLogger("MonitorAgent")
    
    async def check_api_health(self) -> Dict[str, Any]:
        """Check the health of the Open To Close API."""
        start_time = time.time()
        health_status = {
            "status": "healthy",
            "response_time": 0,
            "timestamp": datetime.now().isoformat(),
            "details": {}
        }
        
        try:
            # Test basic API connectivity
            properties = self.client.properties.list_properties()
            response_time = time.time() - start_time
            
            health_status.update({
                "response_time": round(response_time * 1000, 2),  # Convert to ms
                "details": {
                    "properties_count": len(properties),
                    "endpoint_tested": "list_properties"
                }
            })
            
            # Test additional endpoints
            try:
                contacts = self.client.contacts.list_contacts()
                health_status["details"]["contacts_count"] = len(contacts)
            except Exception as e:
                health_status["details"]["contacts_error"] = str(e)
            
            try:
                agents = self.client.agents.list_agents()
                health_status["details"]["agents_count"] = len(agents)
            except Exception as e:
                health_status["details"]["agents_error"] = str(e)
            
            self.success_count += 1
            self.response_times.append(response_time)
            
            # Keep only last 100 response times for metrics
            if len(self.response_times) > 100:
                self.response_times = self.response_times[-100:]
            
        except OpenToCloseAPIError as e:
            health_status.update({
                "status": "unhealthy",
                "error": f"API Error: {str(e)}",
                "error_type": "api_error"
            })
            self.error_count += 1
            self.logger.error(f"API health check failed: {e}")
            
        except Exception as e:
            health_status.update({
                "status": "unhealthy", 
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error"
            })
            self.error_count += 1
            self.logger.error(f"Unexpected error during health check: {e}")
        
        self.metrics["api_health"] = health_status
        return health_status
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Calculate and return performance metrics."""
        if not self.response_times:
            return {"error": "No response time data available"}
        
        return {
            "avg_response_time_ms": round(sum(self.response_times) / len(self.response_times) * 1000, 2),
            "min_response_time_ms": round(min(self.response_times) * 1000, 2),
            "max_response_time_ms": round(max(self.response_times) * 1000, 2),
            "total_requests": self.success_count + self.error_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": round(self.success_count / (self.success_count + self.error_count) * 100, 2) if (self.success_count + self.error_count) > 0 else 0,
            "uptime_hours": round((datetime.now() - self.metrics["uptime_start"]).total_seconds() / 3600, 2)
        }
    
    def check_log_files(self) -> Dict[str, Any]:
        """Check log files for recent errors or issues."""
        log_status = {
            "main_agent_log": {"exists": False, "last_modified": None, "recent_errors": 0},
            "monitor_log": {"exists": False, "last_modified": None}
        }
        
        try:
            # Check main agent log
            today = datetime.now().strftime('%Y%m%d')
            main_log_path = f"/app/logs/agent_{today}.log"
            
            if os.path.exists(main_log_path):
                stat = os.stat(main_log_path)
                log_status["main_agent_log"]["exists"] = True
                log_status["main_agent_log"]["last_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
                
                # Count recent errors (last 100 lines)
                try:
                    with open(main_log_path, 'r') as f:
                        lines = f.readlines()
                        recent_lines = lines[-100:] if len(lines) > 100 else lines
                        error_count = sum(1 for line in recent_lines if " ERROR " in line)
                        log_status["main_agent_log"]["recent_errors"] = error_count
                except Exception as e:
                    log_status["main_agent_log"]["read_error"] = str(e)
            
            # Check monitor log
            monitor_log_path = f"/app/logs/monitor_{today}.log"
            if os.path.exists(monitor_log_path):
                stat = os.stat(monitor_log_path)
                log_status["monitor_log"]["exists"] = True
                log_status["monitor_log"]["last_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
                
        except Exception as e:
            log_status["error"] = f"Error checking log files: {str(e)}"
        
        return log_status
    
    async def generate_status_report(self) -> Dict[str, Any]:
        """Generate a comprehensive status report."""
        health_check = await self.check_api_health()
        performance_metrics = self.get_performance_metrics()
        log_status = self.check_log_files()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "monitor_agent": {
                "status": "running",
                "uptime_seconds": (datetime.now() - self.metrics["uptime_start"]).total_seconds()
            },
            "api_health": health_check,
            "performance_metrics": performance_metrics,
            "log_status": log_status
        }
        
        return report
    
    def save_metrics(self, report: Dict[str, Any]) -> None:
        """Save metrics to file if enabled."""
        if not self.metrics_enabled:
            return
        
        try:
            metrics_file = f"/app/logs/metrics_{datetime.now().strftime('%Y%m%d')}.json"
            
            # Load existing metrics or create new list
            metrics_list = []
            if os.path.exists(metrics_file):
                try:
                    with open(metrics_file, 'r') as f:
                        metrics_list = json.load(f)
                except json.JSONDecodeError:
                    metrics_list = []
            
            # Append new report
            metrics_list.append(report)
            
            # Keep only last 1000 entries to prevent file from growing too large
            if len(metrics_list) > 1000:
                metrics_list = metrics_list[-1000:]
            
            # Save updated metrics
            with open(metrics_file, 'w') as f:
                json.dump(metrics_list, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving metrics: {e}")
    
    async def run_monitoring_cycle(self) -> None:
        """Run one monitoring cycle."""
        try:
            self.logger.debug("Starting monitoring cycle...")
            
            # Generate status report
            report = await self.generate_status_report()
            
            # Log key metrics
            api_status = report["api_health"]["status"]
            response_time = report["api_health"]["response_time"]
            
            if api_status == "healthy":
                self.logger.info(f"API Health: {api_status} (Response: {response_time}ms)")
            else:
                self.logger.warning(f"API Health: {api_status} - {report['api_health'].get('error', 'Unknown error')}")
            
            # Log performance summary
            perf = report["performance_metrics"]
            if "avg_response_time_ms" in perf:
                self.logger.info(f"Performance: Avg {perf['avg_response_time_ms']}ms, Success Rate: {perf['success_rate']}%")
            
            # Save metrics if enabled
            self.save_metrics(report)
            
            # Check for alerts
            await self.check_alerts(report)
            
        except Exception as e:
            self.logger.error(f"Error during monitoring cycle: {e}")
    
    async def check_alerts(self, report: Dict[str, Any]) -> None:
        """Check for alert conditions and log warnings."""
        try:
            # Alert on API unhealthy
            if report["api_health"]["status"] != "healthy":
                self.logger.warning("ALERT: API is unhealthy!")
            
            # Alert on high response times
            if "avg_response_time_ms" in report["performance_metrics"]:
                avg_response = report["performance_metrics"]["avg_response_time_ms"]
                if avg_response > 5000:  # 5 seconds
                    self.logger.warning(f"ALERT: High average response time: {avg_response}ms")
            
            # Alert on low success rate
            if "success_rate" in report["performance_metrics"]:
                success_rate = report["performance_metrics"]["success_rate"]
                if success_rate < 95 and report["performance_metrics"]["total_requests"] > 10:
                    self.logger.warning(f"ALERT: Low success rate: {success_rate}%")
            
            # Alert on recent errors in main agent log
            if "main_agent_log" in report["log_status"]:
                recent_errors = report["log_status"]["main_agent_log"].get("recent_errors", 0)
                if recent_errors > 5:
                    self.logger.warning(f"ALERT: {recent_errors} recent errors in main agent log")
            
        except Exception as e:
            self.logger.error(f"Error checking alerts: {e}")
    
    async def run(self) -> None:
        """Main monitoring loop."""
        self.logger.info("Starting Open To Close Monitor Agent...")
        self.running = True
        
        while self.running:
            try:
                await self.run_monitoring_cycle()
                
                # Wait for next cycle
                self.logger.debug(f"Waiting {self.check_interval} seconds until next check...")
                await asyncio.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.logger.info("Received keyboard interrupt, shutting down...")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Brief pause before retry
        
        self.logger.info("Monitor Agent stopped")


async def main() -> None:
    """Main entry point for the monitor agent."""
    try:
        monitor = MonitorAgent()
        await monitor.run()
    except KeyboardInterrupt:
        print("\nMonitor agent stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 