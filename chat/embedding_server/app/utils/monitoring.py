"""
Performance monitoring utilities.
"""

import time
import psutil
import threading
from typing import Dict, Any, Optional
from ..core.config import settings


class PerformanceMonitor:
    """Monitor system and application performance."""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.total_processing_time = 0.0
        self._lock = threading.Lock()
    
    def record_request(self, processing_time: float, success: bool = True):
        """Record request metrics."""
        with self._lock:
            self.request_count += 1
            self.total_processing_time += processing_time
            if not success:
                self.error_count += 1
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                },
                "network": {
                    "connections": len(psutil.net_connections())
                }
            }
        except Exception as e:
            return {"error": f"Failed to get system metrics: {str(e)}"}
    
    def get_application_metrics(self) -> Dict[str, Any]:
        """Get application performance metrics."""
        with self._lock:
            uptime = time.time() - self.start_time
            avg_processing_time = (
                self.total_processing_time / self.request_count 
                if self.request_count > 0 else 0.0
            )
            error_rate = (
                (self.error_count / self.request_count) * 100 
                if self.request_count > 0 else 0.0
            )
            
            return {
                "uptime": uptime,
                "request_count": self.request_count,
                "error_count": self.error_count,
                "error_rate": error_rate,
                "avg_processing_time": avg_processing_time,
                "total_processing_time": self.total_processing_time
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status."""
        system_metrics = self.get_system_metrics()
        app_metrics = self.get_application_metrics()
        
        # Determine health status
        health_status = "healthy"
        
        # Check system health
        if "error" in system_metrics:
            health_status = "degraded"
        elif system_metrics.get("cpu", {}).get("percent", 0) > 90:
            health_status = "warning"
        elif system_metrics.get("memory", {}).get("percent", 0) > 90:
            health_status = "warning"
        
        # Check application health
        if app_metrics.get("error_rate", 0) > 10:
            health_status = "degraded"
        
        return {
            "status": health_status,
            "timestamp": time.time(),
            "system": system_metrics,
            "application": app_metrics
        }
    
    def reset_metrics(self):
        """Reset all metrics."""
        with self._lock:
            self.start_time = time.time()
            self.request_count = 0
            self.error_count = 0
            self.total_processing_time = 0.0


# Global performance monitor instance
performance_monitor = PerformanceMonitor()
