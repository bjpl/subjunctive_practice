#!/usr/bin/env python3
"""
Progress Tracking and Reporting System
Real-time monitoring and metrics for swarm task execution
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class MetricType(Enum):
    TASK_COMPLETION = "task_completion"
    AGENT_UTILIZATION = "agent_utilization"
    THROUGHPUT = "throughput"
    LATENCY = "latency"
    ERROR_RATE = "error_rate"
    RESOURCE_USAGE = "resource_usage"

@dataclass
class ProgressMetric:
    timestamp: datetime
    metric_type: MetricType
    value: float
    metadata: Dict[str, Any]

class ProgressTracker:
    """
    Real-time progress tracking and performance monitoring for task orchestration.
    Provides insights into execution efficiency and bottleneck identification.
    """
    
    def __init__(self, swarm_id: str = "swarm-1756696734588-1rik89o3r"):
        self.swarm_id = swarm_id
        self.metrics: List[ProgressMetric] = []
        self.task_timelines: Dict[str, Dict] = {}
        self.agent_performance: Dict[str, Dict] = {}
        self.system_metrics: Dict[str, Any] = {
            "start_time": datetime.now().isoformat(),
            "total_tasks_processed": 0,
            "successful_completions": 0,
            "failed_tasks": 0,
            "average_completion_time": 0,
            "peak_concurrency": 0,
            "current_throughput": 0
        }
    
    def track_task_start(self, task_id: str, agent_type: str, estimated_duration: int = None):
        """Track task start event."""
        timestamp = datetime.now()
        
        self.task_timelines[task_id] = {
            "start_time": timestamp,
            "agent_type": agent_type,
            "estimated_duration": estimated_duration,
            "status": "in_progress",
            "checkpoints": []
        }
        
        # Update agent performance tracking
        if agent_type not in self.agent_performance:
            self.agent_performance[agent_type] = {
                "tasks_started": 0,
                "tasks_completed": 0,
                "total_duration": 0,
                "average_duration": 0,
                "success_rate": 0,
                "current_load": 0
            }
        
        self.agent_performance[agent_type]["tasks_started"] += 1
        self.agent_performance[agent_type]["current_load"] += 1
        
        # Record metric
        self._record_metric(
            MetricType.TASK_COMPLETION,
            1.0,
            {"event": "task_started", "task_id": task_id, "agent": agent_type}
        )
        
        self._update_system_metrics()
    
    def track_task_checkpoint(self, task_id: str, checkpoint_name: str, progress_percentage: float):
        """Track intermediate progress checkpoints."""
        if task_id not in self.task_timelines:
            return
        
        timestamp = datetime.now()
        checkpoint = {
            "name": checkpoint_name,
            "timestamp": timestamp,
            "progress": progress_percentage
        }
        
        self.task_timelines[task_id]["checkpoints"].append(checkpoint)
        
        # Record throughput metric
        self._record_metric(
            MetricType.THROUGHPUT,
            progress_percentage,
            {"event": "checkpoint", "task_id": task_id, "checkpoint": checkpoint_name}
        )
    
    def track_task_completion(self, task_id: str, success: bool = True, results: Dict[str, Any] = None):
        """Track task completion event."""
        if task_id not in self.task_timelines:
            return
        
        timestamp = datetime.now()
        timeline = self.task_timelines[task_id]
        
        # Calculate duration
        duration = (timestamp - timeline["start_time"]).total_seconds() / 60  # minutes
        
        timeline.update({
            "end_time": timestamp,
            "duration": duration,
            "status": "completed" if success else "failed",
            "results": results or {}
        })
        
        # Update agent performance
        agent_type = timeline["agent_type"]
        agent_perf = self.agent_performance[agent_type]
        
        if success:
            agent_perf["tasks_completed"] += 1
            agent_perf["total_duration"] += duration
            agent_perf["average_duration"] = agent_perf["total_duration"] / agent_perf["tasks_completed"]
            self.system_metrics["successful_completions"] += 1
        else:
            self.system_metrics["failed_tasks"] += 1
        
        agent_perf["current_load"] -= 1
        agent_perf["success_rate"] = agent_perf["tasks_completed"] / agent_perf["tasks_started"]
        
        # Record completion metric
        self._record_metric(
            MetricType.TASK_COMPLETION,
            1.0 if success else 0.0,
            {"event": "task_completed", "task_id": task_id, "duration": duration, "success": success}
        )
        
        # Record latency metric
        estimated_duration = timeline.get("estimated_duration", 0)
        if estimated_duration > 0:
            latency_ratio = duration / estimated_duration
            self._record_metric(
                MetricType.LATENCY,
                latency_ratio,
                {"task_id": task_id, "estimated": estimated_duration, "actual": duration}
            )
        
        self.system_metrics["total_tasks_processed"] += 1
        self._update_system_metrics()
    
    def track_agent_utilization(self, agent_type: str, utilization_percentage: float):
        """Track agent resource utilization."""
        self._record_metric(
            MetricType.AGENT_UTILIZATION,
            utilization_percentage,
            {"agent_type": agent_type}
        )
    
    def track_system_resources(self, cpu_usage: float, memory_usage: float, io_usage: float = 0):
        """Track system resource usage."""
        self._record_metric(
            MetricType.RESOURCE_USAGE,
            cpu_usage,
            {"resource": "cpu", "memory": memory_usage, "io": io_usage}
        )
    
    def _record_metric(self, metric_type: MetricType, value: float, metadata: Dict[str, Any]):
        """Record a metric with timestamp."""
        metric = ProgressMetric(
            timestamp=datetime.now(),
            metric_type=metric_type,
            value=value,
            metadata=metadata
        )
        self.metrics.append(metric)
        
        # Keep only recent metrics (last 1000 entries)
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]
    
    def _update_system_metrics(self):
        """Update aggregated system metrics."""
        current_time = datetime.now()
        start_time = datetime.fromisoformat(self.system_metrics["start_time"])
        elapsed = (current_time - start_time).total_seconds() / 60  # minutes
        
        if elapsed > 0:
            self.system_metrics["current_throughput"] = self.system_metrics["total_tasks_processed"] / elapsed
        
        # Calculate average completion time
        completed_tasks = [tl for tl in self.task_timelines.values() if tl.get("duration")]
        if completed_tasks:
            avg_duration = sum(tl["duration"] for tl in completed_tasks) / len(completed_tasks)
            self.system_metrics["average_completion_time"] = avg_duration
        
        # Track peak concurrency
        current_active = sum(1 for tl in self.task_timelines.values() if tl["status"] == "in_progress")
        self.system_metrics["peak_concurrency"] = max(
            self.system_metrics["peak_concurrency"], 
            current_active
        )
    
    def get_real_time_status(self) -> Dict[str, Any]:
        """Get real-time execution status."""
        active_tasks = [tid for tid, tl in self.task_timelines.items() if tl["status"] == "in_progress"]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "swarm_id": self.swarm_id,
            "active_tasks": len(active_tasks),
            "active_task_ids": active_tasks,
            "completed_tasks": len([tl for tl in self.task_timelines.values() if tl["status"] == "completed"]),
            "failed_tasks": len([tl for tl in self.task_timelines.values() if tl["status"] == "failed"]),
            "agent_loads": {
                agent: perf["current_load"] 
                for agent, perf in self.agent_performance.items()
            },
            "system_metrics": self.system_metrics,
            "recent_throughput": self._calculate_recent_throughput(),
            "bottlenecks": self._identify_bottlenecks()
        }
    
    def get_performance_report(self, time_window_minutes: int = 60) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
        recent_metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]
        
        # Task completion analysis
        completion_metrics = [m for m in recent_metrics if m.metric_type == MetricType.TASK_COMPLETION]
        successful_completions = len([m for m in completion_metrics if m.value > 0 and m.metadata.get("event") == "task_completed"])
        failed_completions = len([m for m in completion_metrics if m.value == 0 and m.metadata.get("event") == "task_completed"])
        
        # Agent performance analysis
        agent_stats = {}
        for agent, perf in self.agent_performance.items():
            agent_stats[agent] = {
                "tasks_completed": perf["tasks_completed"],
                "success_rate": perf["success_rate"],
                "average_duration": perf["average_duration"],
                "current_load": perf["current_load"],
                "utilization": self._calculate_agent_utilization(agent, cutoff_time)
            }
        
        # Throughput analysis
        throughput_metrics = [m for m in recent_metrics if m.metric_type == MetricType.THROUGHPUT]
        avg_throughput = sum(m.value for m in throughput_metrics) / len(throughput_metrics) if throughput_metrics else 0
        
        # Latency analysis
        latency_metrics = [m for m in recent_metrics if m.metric_type == MetricType.LATENCY]
        avg_latency_ratio = sum(m.value for m in latency_metrics) / len(latency_metrics) if latency_metrics else 1.0
        
        return {
            "report_period": f"{time_window_minutes} minutes",
            "generated_at": datetime.now().isoformat(),
            "swarm_id": self.swarm_id,
            "task_completion": {
                "successful": successful_completions,
                "failed": failed_completions,
                "success_rate": successful_completions / max(1, successful_completions + failed_completions)
            },
            "agent_performance": agent_stats,
            "throughput": {
                "average": avg_throughput,
                "current": self.system_metrics["current_throughput"],
                "peak_concurrency": self.system_metrics["peak_concurrency"]
            },
            "latency": {
                "average_ratio": avg_latency_ratio,
                "accuracy": "on_time" if avg_latency_ratio <= 1.1 else "delayed"
            },
            "bottlenecks": self._identify_bottlenecks(),
            "recommendations": self._generate_recommendations(),
            "system_health": self._assess_system_health()
        }
    
    def _calculate_recent_throughput(self, window_minutes: int = 15) -> float:
        """Calculate throughput in the recent time window."""
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        recent_completions = [
            m for m in self.metrics 
            if (m.metric_type == MetricType.TASK_COMPLETION and 
                m.timestamp >= cutoff_time and 
                m.metadata.get("event") == "task_completed")
        ]
        return len(recent_completions) / window_minutes
    
    def _identify_bottlenecks(self) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks."""
        bottlenecks = []
        
        # Agent overload detection
        for agent, perf in self.agent_performance.items():
            if perf["current_load"] > 2:  # High load threshold
                bottlenecks.append({
                    "type": "agent_overload",
                    "agent": agent,
                    "current_load": perf["current_load"],
                    "severity": "high" if perf["current_load"] > 3 else "medium"
                })
        
        # Slow task detection
        for task_id, timeline in self.task_timelines.items():
            if timeline["status"] == "in_progress":
                runtime = (datetime.now() - timeline["start_time"]).total_seconds() / 60
                estimated = timeline.get("estimated_duration", 30)
                
                if runtime > estimated * 1.5:  # 50% overtime
                    bottlenecks.append({
                        "type": "slow_task",
                        "task_id": task_id,
                        "runtime": runtime,
                        "estimated": estimated,
                        "severity": "high" if runtime > estimated * 2 else "medium"
                    })
        
        # Low throughput detection
        recent_throughput = self._calculate_recent_throughput()
        if recent_throughput < 0.5:  # Less than 0.5 tasks per minute
            bottlenecks.append({
                "type": "low_throughput",
                "current_throughput": recent_throughput,
                "severity": "medium"
            })
        
        return bottlenecks
    
    def _calculate_agent_utilization(self, agent_type: str, since: datetime) -> float:
        """Calculate agent utilization percentage."""
        agent_metrics = [
            m for m in self.metrics 
            if (m.metric_type == MetricType.AGENT_UTILIZATION and 
                m.metadata.get("agent_type") == agent_type and 
                m.timestamp >= since)
        ]
        
        if not agent_metrics:
            return 0.0
        
        return sum(m.value for m in agent_metrics) / len(agent_metrics)
    
    def _generate_recommendations(self) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []
        bottlenecks = self._identify_bottlenecks()
        
        # Agent-based recommendations
        for bottleneck in bottlenecks:
            if bottleneck["type"] == "agent_overload":
                recommendations.append(
                    f"Consider spawning additional {bottleneck['agent']} agents to distribute load"
                )
            elif bottleneck["type"] == "slow_task":
                recommendations.append(
                    f"Review task {bottleneck['task_id']} for potential optimization or decomposition"
                )
            elif bottleneck["type"] == "low_throughput":
                recommendations.append(
                    "Consider increasing parallel execution or optimizing task dependencies"
                )
        
        # System-level recommendations
        if self.system_metrics["failed_tasks"] > 0:
            failure_rate = self.system_metrics["failed_tasks"] / self.system_metrics["total_tasks_processed"]
            if failure_rate > 0.1:  # More than 10% failure rate
                recommendations.append("High failure rate detected. Review error handling and task requirements")
        
        # Performance recommendations
        avg_completion_time = self.system_metrics["average_completion_time"]
        if avg_completion_time > 60:  # More than 1 hour average
            recommendations.append("Long average completion time. Consider task decomposition or resource scaling")
        
        return recommendations
    
    def _assess_system_health(self) -> Dict[str, Any]:
        """Assess overall system health."""
        total_tasks = self.system_metrics["total_tasks_processed"]
        if total_tasks == 0:
            return {"status": "initializing", "score": 100}
        
        # Calculate health score (0-100)
        score = 100
        
        # Success rate impact
        success_rate = self.system_metrics["successful_completions"] / total_tasks
        if success_rate < 0.8:
            score -= (0.8 - success_rate) * 100
        
        # Throughput impact
        current_throughput = self.system_metrics["current_throughput"]
        if current_throughput < 0.5:
            score -= (0.5 - current_throughput) * 20
        
        # Bottleneck impact
        bottlenecks = self._identify_bottlenecks()
        high_severity_bottlenecks = len([b for b in bottlenecks if b.get("severity") == "high"])
        medium_severity_bottlenecks = len([b for b in bottlenecks if b.get("severity") == "medium"])
        
        score -= high_severity_bottlenecks * 15
        score -= medium_severity_bottlenecks * 5
        
        score = max(0, min(100, score))
        
        # Determine status
        if score >= 90:
            status = "excellent"
        elif score >= 75:
            status = "good"
        elif score >= 60:
            status = "fair"
        elif score >= 40:
            status = "poor"
        else:
            status = "critical"
        
        return {
            "status": status,
            "score": score,
            "factors": {
                "success_rate": success_rate,
                "throughput": current_throughput,
                "bottlenecks": len(bottlenecks)
            }
        }
    
    def export_metrics(self, filename: str = None) -> str:
        """Export metrics to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f".claude-flow/orchestration/metrics/progress_report_{timestamp}.json"
        
        report_data = {
            "swarm_id": self.swarm_id,
            "export_time": datetime.now().isoformat(),
            "system_metrics": self.system_metrics,
            "task_timelines": {
                tid: {
                    **timeline,
                    "start_time": timeline["start_time"].isoformat() if timeline.get("start_time") else None,
                    "end_time": timeline["end_time"].isoformat() if timeline.get("end_time") else None,
                    "checkpoints": [
                        {
                            **cp,
                            "timestamp": cp["timestamp"].isoformat() if cp.get("timestamp") else None
                        } for cp in timeline.get("checkpoints", [])
                    ]
                } for tid, timeline in self.task_timelines.items()
            },
            "agent_performance": self.agent_performance,
            "recent_metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "type": m.metric_type.value,
                    "value": m.value,
                    "metadata": m.metadata
                } for m in self.metrics[-100:]  # Last 100 metrics
            ],
            "performance_report": self.get_performance_report()
        }
        
        try:
            import os
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2)
            return filename
        except Exception as e:
            print(f"Error exporting metrics: {e}")
            return ""

# Example usage
if __name__ == "__main__":
    import sys
    
    tracker = ProgressTracker()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            status = tracker.get_real_time_status()
            print(json.dumps(status, indent=2))
        
        elif command == "report":
            window = 60
            if len(sys.argv) > 2:
                try:
                    window = int(sys.argv[2])
                except:
                    pass
            
            report = tracker.get_performance_report(window)
            print(json.dumps(report, indent=2))
        
        elif command == "export":
            filename = None
            if len(sys.argv) > 2:
                filename = sys.argv[2]
            
            exported_file = tracker.export_metrics(filename)
            print(f"Metrics exported to: {exported_file}")
        
        else:
            print("Usage: python progress-tracker.py <command> [args]")
            print("Commands:")
            print("  status - Show real-time status")
            print("  report [window_minutes] - Generate performance report")
            print("  export [filename] - Export metrics to file")
    
    else:
        print("Progress Tracker initialized for swarm coordination.")
        print("Ready to monitor task execution and performance metrics.")