#!/usr/bin/env python3
"""
Swarm Coordination Validation System
Validates proper swarm setup, task assignment, and completion protocols
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class CoordinationValidator:
    """
    Validates the proper functioning of swarm coordination system.
    Ensures task orchestration, dependency management, and memory coordination.
    """
    
    def __init__(self, swarm_id: str = "swarm-1756696734588-1rik89o3r"):
        self.swarm_id = swarm_id
        # Use absolute path or current directory if we're already in orchestration
        if os.path.basename(os.getcwd()) == "orchestration":
            self.orchestration_path = "."
        else:
            self.orchestration_path = ".claude-flow/orchestration"
        self.validation_results = []
    
    def validate_full_system(self) -> Dict[str, Any]:
        """Run comprehensive system validation."""
        results = {
            "swarm_id": self.swarm_id,
            "validation_time": datetime.now().isoformat(),
            "components": {},
            "overall_status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # Validate each component
        results["components"]["file_structure"] = self._validate_file_structure()
        results["components"]["configuration"] = self._validate_configuration()
        results["components"]["orchestrator"] = self._validate_orchestrator()
        results["components"]["progress_tracker"] = self._validate_progress_tracker()
        results["components"]["memory_system"] = self._validate_memory_system()
        results["components"]["agent_capabilities"] = self._validate_agent_capabilities()
        results["components"]["dependency_tracking"] = self._validate_dependency_tracking()
        
        # Assess overall status
        component_scores = [comp.get("score", 0) for comp in results["components"].values()]
        overall_score = sum(component_scores) / len(component_scores) if component_scores else 0
        
        if overall_score >= 90:
            results["overall_status"] = "excellent"
        elif overall_score >= 75:
            results["overall_status"] = "good"
        elif overall_score >= 60:
            results["overall_status"] = "fair"
        else:
            results["overall_status"] = "needs_attention"
        
        # Collect issues and recommendations
        for component, data in results["components"].items():
            results["issues"].extend(data.get("issues", []))
            results["recommendations"].extend(data.get("recommendations", []))
        
        return results
    
    def _validate_file_structure(self) -> Dict[str, Any]:
        """Validate orchestration file structure."""
        required_files = [
            "task-orchestrator.py",
            "progress-tracker.py",
            "coordination-validation.py",
            "swarm/coordination-status.json",
            "agents/agent-capabilities.json",
            "tasks/task-template.json",
            "tasks/dependency-tracker.json",
            "memory/coordination-memory.json"
        ]
        
        missing_files = []
        existing_files = []
        
        for file_path in required_files:
            full_path = os.path.join(self.orchestration_path, file_path)
            if os.path.exists(full_path):
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        score = (len(existing_files) / len(required_files)) * 100
        
        result = {
            "score": score,
            "status": "pass" if score == 100 else "fail",
            "existing_files": existing_files,
            "missing_files": missing_files,
            "issues": [],
            "recommendations": []
        }
        
        if missing_files:
            result["issues"].append(f"Missing critical files: {missing_files}")
            result["recommendations"].append("Ensure all orchestration files are properly initialized")
        
        return result
    
    def _validate_configuration(self) -> Dict[str, Any]:
        """Validate configuration files."""
        result = {
            "score": 0,
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        score = 0
        checks = 0
        
        # Validate coordination status
        coord_status_path = os.path.join(self.orchestration_path, "swarm/coordination-status.json")
        if os.path.exists(coord_status_path):
            try:
                with open(coord_status_path, 'r') as f:
                    coord_data = json.load(f)
                
                checks += 1
                if coord_data.get("swarmId") == self.swarm_id:
                    score += 25
                else:
                    result["issues"].append("Swarm ID mismatch in coordination status")
                
                if coord_data.get("orchestrator", {}).get("status") == "active":
                    score += 25
                else:
                    result["issues"].append("Orchestrator not marked as active")
                
            except Exception as e:
                result["issues"].append(f"Failed to load coordination status: {e}")
        else:
            result["issues"].append("Coordination status file missing")
        
        # Validate agent capabilities
        agent_caps_path = os.path.join(self.orchestration_path, "agents/agent-capabilities.json")
        if os.path.exists(agent_caps_path):
            try:
                with open(agent_caps_path, 'r') as f:
                    agent_data = json.load(f)
                
                checks += 1
                agent_types = agent_data.get("agentTypes", {})
                if len(agent_types) >= 3:  # At least 3 agent types
                    score += 25
                else:
                    result["issues"].append("Insufficient agent type definitions")
                
                # Check if all agents have required fields
                required_fields = ["capabilities", "loadCapacity"]
                all_valid = True
                for agent_type, config in agent_types.items():
                    if not all(field in config for field in required_fields):
                        all_valid = False
                        break
                
                if all_valid:
                    score += 25
                else:
                    result["issues"].append("Agent configurations missing required fields")
                
            except Exception as e:
                result["issues"].append(f"Failed to load agent capabilities: {e}")
        else:
            result["issues"].append("Agent capabilities file missing")
        
        result["score"] = score
        result["status"] = "pass" if score >= 75 else "fail"
        
        if result["score"] < 100:
            result["recommendations"].append("Review and complete configuration files")
        
        return result
    
    def _validate_orchestrator(self) -> Dict[str, Any]:
        """Validate task orchestrator functionality."""
        result = {
            "score": 0,
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        orchestrator_path = os.path.join(self.orchestration_path, "task-orchestrator.py")
        
        if not os.path.exists(orchestrator_path):
            result["issues"].append("Task orchestrator file missing")
            result["status"] = "fail"
            return result
        
        try:
            # Test orchestrator import
            import sys
            sys.path.insert(0, self.orchestration_path)
            
            # Basic functionality test
            score = 0
            
            # Check if file is executable
            with open(orchestrator_path, 'r') as f:
                content = f.read()
                
            # Look for key classes and methods
            required_components = [
                "class TaskOrchestrator",
                "def decompose_objective",
                "def get_ready_tasks",
                "def assign_task",
                "def complete_task",
                "def get_execution_plan"
            ]
            
            for component in required_components:
                if component in content:
                    score += 100 / len(required_components)
                else:
                    result["issues"].append(f"Missing component: {component}")
            
            result["score"] = score
            result["status"] = "pass" if score >= 80 else "fail"
            
            if score < 100:
                result["recommendations"].append("Complete orchestrator implementation")
            
        except Exception as e:
            result["issues"].append(f"Orchestrator validation failed: {e}")
            result["status"] = "fail"
        
        return result
    
    def _validate_progress_tracker(self) -> Dict[str, Any]:
        """Validate progress tracking functionality."""
        result = {
            "score": 0,
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        tracker_path = os.path.join(self.orchestration_path, "progress-tracker.py")
        
        if not os.path.exists(tracker_path):
            result["issues"].append("Progress tracker file missing")
            result["status"] = "fail"
            return result
        
        try:
            with open(tracker_path, 'r') as f:
                content = f.read()
            
            required_components = [
                "class ProgressTracker",
                "def track_task_start",
                "def track_task_completion",
                "def get_real_time_status",
                "def get_performance_report",
                "def _identify_bottlenecks"
            ]
            
            score = 0
            for component in required_components:
                if component in content:
                    score += 100 / len(required_components)
                else:
                    result["issues"].append(f"Missing component: {component}")
            
            result["score"] = score
            result["status"] = "pass" if score >= 80 else "fail"
            
            if score < 100:
                result["recommendations"].append("Complete progress tracker implementation")
            
        except Exception as e:
            result["issues"].append(f"Progress tracker validation failed: {e}")
            result["status"] = "fail"
        
        return result
    
    def _validate_memory_system(self) -> Dict[str, Any]:
        """Validate memory coordination system."""
        result = {
            "score": 0,
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        memory_path = os.path.join(self.orchestration_path, "memory/coordination-memory.json")
        
        if not os.path.exists(memory_path):
            result["issues"].append("Memory coordination file missing")
            result["status"] = "fail"
            return result
        
        try:
            with open(memory_path, 'r') as f:
                memory_data = json.load(f)
            
            score = 0
            
            # Check required memory structure
            required_sections = ["swarm", "memoryKeys", "lastUpdate"]
            for section in required_sections:
                if section in memory_data:
                    score += 100 / len(required_sections)
                else:
                    result["issues"].append(f"Missing memory section: {section}")
            
            # Check swarm subsections
            if "swarm" in memory_data:
                swarm_data = memory_data["swarm"]
                required_swarm_sections = ["tasks", "agents", "coordination"]
                
                swarm_score = 0
                for section in required_swarm_sections:
                    if section in swarm_data:
                        swarm_score += 1
                
                if swarm_score == len(required_swarm_sections):
                    # Bonus for complete swarm structure
                    score = min(100, score + 20)
            
            result["score"] = score
            result["status"] = "pass" if score >= 70 else "fail"
            
            if score < 100:
                result["recommendations"].append("Complete memory coordination structure")
            
        except Exception as e:
            result["issues"].append(f"Memory system validation failed: {e}")
            result["status"] = "fail"
        
        return result
    
    def _validate_agent_capabilities(self) -> Dict[str, Any]:
        """Validate agent capability definitions."""
        result = {
            "score": 0,
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        caps_path = os.path.join(self.orchestration_path, "agents/agent-capabilities.json")
        
        if not os.path.exists(caps_path):
            result["issues"].append("Agent capabilities file missing")
            result["status"] = "fail"
            return result
        
        try:
            with open(caps_path, 'r') as f:
                caps_data = json.load(f)
            
            score = 0
            
            agent_types = caps_data.get("agentTypes", {})
            
            # Check minimum agent types
            essential_agents = ["coder", "reviewer", "tester"]
            existing_essential = [agent for agent in essential_agents if agent in agent_types]
            score += (len(existing_essential) / len(essential_agents)) * 50
            
            # Check agent configuration completeness
            if agent_types:
                complete_configs = 0
                total_agents = len(agent_types)
                
                for agent_type, config in agent_types.items():
                    if all(key in config for key in ["capabilities", "loadCapacity"]):
                        if isinstance(config["capabilities"], list) and len(config["capabilities"]) > 0:
                            if isinstance(config["loadCapacity"], int) and config["loadCapacity"] > 0:
                                complete_configs += 1
                
                config_score = (complete_configs / total_agents) * 50 if total_agents > 0 else 0
                score += config_score
            
            # Check load balancing configuration
            if "loadBalancing" in caps_data:
                lb_config = caps_data["loadBalancing"]
                if all(key in lb_config for key in ["algorithm", "preferredUtilization"]):
                    score = min(100, score + 10)
            
            result["score"] = score
            result["status"] = "pass" if score >= 80 else "fail"
            
            if len(existing_essential) < len(essential_agents):
                result["issues"].append(f"Missing essential agent types: {set(essential_agents) - set(existing_essential)}")
            
            if score < 100:
                result["recommendations"].append("Complete agent capability definitions")
            
        except Exception as e:
            result["issues"].append(f"Agent capabilities validation failed: {e}")
            result["status"] = "fail"
        
        return result
    
    def _validate_dependency_tracking(self) -> Dict[str, Any]:
        """Validate dependency tracking system."""
        result = {
            "score": 0,
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        deps_path = os.path.join(self.orchestration_path, "tasks/dependency-tracker.json")
        
        if not os.path.exists(deps_path):
            result["issues"].append("Dependency tracker file missing")
            result["status"] = "fail"
            return result
        
        try:
            with open(deps_path, 'r') as f:
                deps_data = json.load(f)
            
            score = 0
            
            # Check required sections
            required_sections = ["dependencyGraph", "dependencyRules", "parallelizationRules"]
            for section in required_sections:
                if section in deps_data:
                    score += 100 / len(required_sections)
                else:
                    result["issues"].append(f"Missing dependency section: {section}")
            
            # Check dependency rules
            if "dependencyRules" in deps_data:
                rules = deps_data["dependencyRules"]
                essential_rules = ["testing", "review", "integration"]
                existing_rules = [rule for rule in essential_rules if rule in rules]
                
                if len(existing_rules) == len(essential_rules):
                    score = min(100, score + 20)
                elif len(existing_rules) > 0:
                    score = min(100, score + 10)
            
            result["score"] = score
            result["status"] = "pass" if score >= 75 else "fail"
            
            if score < 100:
                result["recommendations"].append("Complete dependency tracking configuration")
            
        except Exception as e:
            result["issues"].append(f"Dependency tracking validation failed: {e}")
            result["status"] = "fail"
        
        return result
    
    def generate_validation_report(self) -> str:
        """Generate comprehensive validation report."""
        validation_results = self.validate_full_system()
        
        report_lines = [
            f"# Swarm Coordination Validation Report",
            f"**Swarm ID**: {self.swarm_id}",
            f"**Validation Time**: {validation_results['validation_time']}",
            f"**Overall Status**: {validation_results['overall_status'].upper()}",
            "",
            "## Component Status",
            ""
        ]
        
        for component, data in validation_results["components"].items():
            status_icon = "✅" if data["status"] == "pass" else "❌"
            report_lines.extend([
                f"### {component.replace('_', ' ').title()} {status_icon}",
                f"- **Score**: {data['score']:.1f}/100",
                f"- **Status**: {data['status']}",
                ""
            ])
            
            if data.get("issues"):
                report_lines.append("**Issues**:")
                for issue in data["issues"]:
                    report_lines.append(f"- {issue}")
                report_lines.append("")
            
            if data.get("recommendations"):
                report_lines.append("**Recommendations**:")
                for rec in data["recommendations"]:
                    report_lines.append(f"- {rec}")
                report_lines.append("")
        
        if validation_results["issues"]:
            report_lines.extend([
                "## Critical Issues",
                ""
            ])
            for issue in validation_results["issues"]:
                report_lines.append(f"- {issue}")
            report_lines.append("")
        
        if validation_results["recommendations"]:
            report_lines.extend([
                "## Recommendations",
                ""
            ])
            for rec in validation_results["recommendations"]:
                report_lines.append(f"- {rec}")
        
        return "\n".join(report_lines)

# CLI interface
if __name__ == "__main__":
    import sys
    
    validator = CoordinationValidator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "validate":
            results = validator.validate_full_system()
            print(json.dumps(results, indent=2))
        
        elif command == "report":
            report = validator.generate_validation_report()
            print(report)
            
            # Optionally save to file
            if len(sys.argv) > 2 and sys.argv[2] == "--save":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f".claude-flow/orchestration/validation_report_{timestamp}.md"
                try:
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, 'w') as f:
                        f.write(report)
                    print(f"\nReport saved to: {filename}")
                except Exception as e:
                    print(f"\nError saving report: {e}")
        
        else:
            print("Usage: python coordination-validation.py <command> [options]")
            print("Commands:")
            print("  validate - Run validation and output JSON results")
            print("  report [--save] - Generate human-readable report")
    
    else:
        print("Swarm Coordination Validation System")
        print("Run with 'validate' or 'report' command for detailed results")