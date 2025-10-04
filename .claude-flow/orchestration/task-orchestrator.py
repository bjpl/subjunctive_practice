#!/usr/bin/env python3
"""
Task Orchestrator for Swarm Coordination
Swarm ID: swarm-1756696734588-1rik89o3r

This module provides task decomposition, dependency management, and parallel execution
coordination for the Claude-Flow swarm environment.
"""

import json
import time
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ExecutionStrategy(Enum):
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    ADAPTIVE = "adaptive"
    BALANCED = "balanced"

@dataclass
class Task:
    id: str
    type: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    dependencies: List[str]
    assigned_agent: Optional[str]
    estimated_duration: Optional[int]  # in minutes
    actual_duration: Optional[int]
    requirements: List[str]
    deliverables: List[str]
    memory_keys: List[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    parent_task: Optional[str]
    subtasks: List[str]
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'dependencies': self.dependencies,
            'assigned_agent': self.assigned_agent,
            'estimated_duration': self.estimated_duration,
            'actual_duration': self.actual_duration,
            'requirements': self.requirements,
            'deliverables': self.deliverables,
            'memory_keys': self.memory_keys,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'parent_task': self.parent_task,
            'subtasks': self.subtasks
        }

class TaskOrchestrator:
    """
    Central coordination system for task decomposition and execution management.
    Manages the complete lifecycle of complex objectives through intelligent task breakdown.
    """
    
    def __init__(self, swarm_id: str = "swarm-1756696734588-1rik89o3r"):
        self.swarm_id = swarm_id
        self.tasks: Dict[str, Task] = {}
        self.agent_capabilities: Dict[str, Dict] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.execution_queue: List[str] = []
        self.active_tasks: Set[str] = set()
        self.completed_tasks: Set[str] = set()
        self.failed_tasks: Set[str] = set()
        
        # Load configuration
        self._load_configurations()
    
    def _load_configurations(self):
        """Load agent capabilities and coordination settings."""
        try:
            with open('.claude-flow/orchestration/agents/agent-capabilities.json', 'r') as f:
                capabilities = json.load(f)
                self.agent_capabilities = capabilities.get('agentTypes', {})
        except FileNotFoundError:
            # Fallback capabilities
            self.agent_capabilities = {
                "coder": {"capabilities": ["implementation", "refactoring"], "loadCapacity": 3},
                "tester": {"capabilities": ["testing", "validation"], "loadCapacity": 4},
                "reviewer": {"capabilities": ["review", "quality-assurance"], "loadCapacity": 2}
            }
    
    def decompose_objective(self, objective: str, context: Dict[str, Any] = None) -> List[Task]:
        """
        Intelligent task decomposition based on objective complexity and context.
        
        Args:
            objective: High-level objective to decompose
            context: Additional context for intelligent decomposition
            
        Returns:
            List of decomposed tasks with dependencies
        """
        context = context or {}
        
        # Analyze objective complexity
        complexity_score = self._analyze_complexity(objective, context)
        decomposition_strategy = self._select_decomposition_strategy(complexity_score)
        
        # Generate tasks based on strategy
        tasks = []
        
        if "feature development" in objective.lower():
            tasks = self._decompose_feature_development(objective, context)
        elif "bug fix" in objective.lower():
            tasks = self._decompose_bug_fix(objective, context)
        elif "refactor" in objective.lower():
            tasks = self._decompose_refactoring(objective, context)
        elif "testing" in objective.lower():
            tasks = self._decompose_testing(objective, context)
        else:
            tasks = self._decompose_generic_development(objective, context)
        
        # Register tasks and build dependency graph
        for task in tasks:
            self.register_task(task)
        
        return tasks
    
    def _analyze_complexity(self, objective: str, context: Dict[str, Any]) -> int:
        """Analyze objective complexity (1-10 scale)."""
        complexity = 1
        
        # Text analysis
        if len(objective.split()) > 10:
            complexity += 2
        if any(word in objective.lower() for word in ['integrate', 'migrate', 'refactor', 'architecture']):
            complexity += 3
        if any(word in objective.lower() for word in ['system', 'platform', 'framework']):
            complexity += 2
            
        # Context analysis
        if context.get('file_count', 0) > 10:
            complexity += 2
        if context.get('has_dependencies', False):
            complexity += 1
            
        return min(complexity, 10)
    
    def _select_decomposition_strategy(self, complexity: int) -> str:
        """Select appropriate decomposition strategy based on complexity."""
        if complexity <= 3:
            return "simple"
        elif complexity <= 6:
            return "moderate"
        else:
            return "complex"
    
    def _decompose_feature_development(self, objective: str, context: Dict[str, Any]) -> List[Task]:
        """Decompose feature development objectives."""
        base_id = f"feat_{int(time.time())}"
        
        tasks = [
            Task(
                id=f"{base_id}_analysis",
                type="analysis",
                description=f"Analyze requirements for: {objective}",
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                dependencies=[],
                assigned_agent=None,
                estimated_duration=30,
                actual_duration=None,
                requirements=["Requirements documentation", "User stories"],
                deliverables=["Requirements analysis", "Implementation plan"],
                memory_keys=[f"swarm/tasks/{base_id}_analysis/requirements"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_design",
                type="design",
                description=f"Design architecture for: {objective}",
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_analysis"],
                assigned_agent=None,
                estimated_duration=45,
                actual_duration=None,
                requirements=["Requirements analysis", "System constraints"],
                deliverables=["Architecture design", "API specifications"],
                memory_keys=[f"swarm/tasks/{base_id}_design/architecture"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_implement",
                type="implementation",
                description=f"Implement core functionality for: {objective}",
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_design"],
                assigned_agent=None,
                estimated_duration=90,
                actual_duration=None,
                requirements=["Architecture design", "Development environment"],
                deliverables=["Working implementation", "Unit tests"],
                memory_keys=[f"swarm/tasks/{base_id}_implement/code"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_test",
                type="testing",
                description=f"Comprehensive testing for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_implement"],
                assigned_agent=None,
                estimated_duration=60,
                actual_duration=None,
                requirements=["Implementation", "Test frameworks"],
                deliverables=["Test suite", "Test reports"],
                memory_keys=[f"swarm/tasks/{base_id}_test/results"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_integrate",
                type="integration",
                description=f"Integration and deployment for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_test"],
                assigned_agent=None,
                estimated_duration=30,
                actual_duration=None,
                requirements=["Tested implementation", "Deployment environment"],
                deliverables=["Integrated feature", "Documentation"],
                memory_keys=[f"swarm/tasks/{base_id}_integrate/deployment"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            )
        ]
        
        return tasks
    
    def _decompose_bug_fix(self, objective: str, context: Dict[str, Any]) -> List[Task]:
        """Decompose bug fix objectives."""
        base_id = f"bug_{int(time.time())}"
        
        return [
            Task(
                id=f"{base_id}_reproduce",
                type="analysis",
                description=f"Reproduce and analyze bug: {objective}",
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                dependencies=[],
                assigned_agent=None,
                estimated_duration=20,
                actual_duration=None,
                requirements=["Bug report", "Test environment"],
                deliverables=["Reproduction steps", "Root cause analysis"],
                memory_keys=[f"swarm/tasks/{base_id}_reproduce/analysis"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_fix",
                type="implementation",
                description=f"Implement fix for: {objective}",
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_reproduce"],
                assigned_agent=None,
                estimated_duration=40,
                actual_duration=None,
                requirements=["Root cause analysis", "Code access"],
                deliverables=["Bug fix", "Regression tests"],
                memory_keys=[f"swarm/tasks/{base_id}_fix/implementation"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_verify",
                type="testing",
                description=f"Verify fix for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_fix"],
                assigned_agent=None,
                estimated_duration=20,
                actual_duration=None,
                requirements=["Bug fix", "Test cases"],
                deliverables=["Verification report", "Updated tests"],
                memory_keys=[f"swarm/tasks/{base_id}_verify/results"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            )
        ]
    
    def _decompose_refactoring(self, objective: str, context: Dict[str, Any]) -> List[Task]:
        """Decompose refactoring objectives."""
        base_id = f"refactor_{int(time.time())}"
        
        return [
            Task(
                id=f"{base_id}_analyze",
                type="analysis",
                description=f"Analyze code structure for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[],
                assigned_agent=None,
                estimated_duration=30,
                actual_duration=None,
                requirements=["Codebase access", "Quality metrics"],
                deliverables=["Code analysis", "Refactoring plan"],
                memory_keys=[f"swarm/tasks/{base_id}_analyze/metrics"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_refactor",
                type="implementation",
                description=f"Execute refactoring for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_analyze"],
                assigned_agent=None,
                estimated_duration=60,
                actual_duration=None,
                requirements=["Refactoring plan", "Test coverage"],
                deliverables=["Refactored code", "Updated tests"],
                memory_keys=[f"swarm/tasks/{base_id}_refactor/changes"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_validate",
                type="testing",
                description=f"Validate refactoring for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_refactor"],
                assigned_agent=None,
                estimated_duration=30,
                actual_duration=None,
                requirements=["Refactored code", "Test suite"],
                deliverables=["Validation report", "Performance comparison"],
                memory_keys=[f"swarm/tasks/{base_id}_validate/metrics"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            )
        ]
    
    def _decompose_testing(self, objective: str, context: Dict[str, Any]) -> List[Task]:
        """Decompose testing objectives."""
        base_id = f"test_{int(time.time())}"
        
        return [
            Task(
                id=f"{base_id}_plan",
                type="planning",
                description=f"Plan testing strategy for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[],
                assigned_agent=None,
                estimated_duration=20,
                actual_duration=None,
                requirements=["Requirements", "Code structure"],
                deliverables=["Test plan", "Test cases"],
                memory_keys=[f"swarm/tasks/{base_id}_plan/strategy"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_implement",
                type="testing",
                description=f"Implement tests for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_plan"],
                assigned_agent=None,
                estimated_duration=60,
                actual_duration=None,
                requirements=["Test plan", "Test frameworks"],
                deliverables=["Test implementation", "Test data"],
                memory_keys=[f"swarm/tasks/{base_id}_implement/tests"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_execute",
                type="testing",
                description=f"Execute test suite for: {objective}",
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_implement"],
                assigned_agent=None,
                estimated_duration=30,
                actual_duration=None,
                requirements=["Test implementation", "Test environment"],
                deliverables=["Test results", "Coverage report"],
                memory_keys=[f"swarm/tasks/{base_id}_execute/results"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            )
        ]
    
    def _decompose_generic_development(self, objective: str, context: Dict[str, Any]) -> List[Task]:
        """Decompose generic development objectives."""
        base_id = f"dev_{int(time.time())}"
        
        return [
            Task(
                id=f"{base_id}_research",
                type="research",
                description=f"Research approach for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[],
                assigned_agent=None,
                estimated_duration=20,
                actual_duration=None,
                requirements=["Objective clarification"],
                deliverables=["Research findings", "Approach recommendation"],
                memory_keys=[f"swarm/tasks/{base_id}_research/findings"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_implement",
                type="implementation",
                description=f"Implement solution for: {objective}",
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_research"],
                assigned_agent=None,
                estimated_duration=60,
                actual_duration=None,
                requirements=["Research findings", "Development environment"],
                deliverables=["Working solution", "Documentation"],
                memory_keys=[f"swarm/tasks/{base_id}_implement/solution"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            ),
            Task(
                id=f"{base_id}_validate",
                type="validation",
                description=f"Validate solution for: {objective}",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                dependencies=[f"{base_id}_implement"],
                assigned_agent=None,
                estimated_duration=20,
                actual_duration=None,
                requirements=["Working solution"],
                deliverables=["Validation results", "Quality assessment"],
                memory_keys=[f"swarm/tasks/{base_id}_validate/results"],
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                parent_task=None,
                subtasks=[]
            )
        ]
    
    def register_task(self, task: Task):
        """Register a task in the orchestration system."""
        self.tasks[task.id] = task
        self.dependency_graph[task.id] = set(task.dependencies)
        self._update_memory_status()
    
    def get_ready_tasks(self) -> List[Task]:
        """Get tasks that are ready for execution (no pending dependencies)."""
        ready_tasks = []
        
        for task_id, task in self.tasks.items():
            if (task.status == TaskStatus.PENDING and
                all(dep_id in self.completed_tasks for dep_id in task.dependencies)):
                ready_tasks.append(task)
        
        # Sort by priority
        priority_order = {TaskPriority.CRITICAL: 0, TaskPriority.HIGH: 1, 
                         TaskPriority.MEDIUM: 2, TaskPriority.LOW: 3}
        ready_tasks.sort(key=lambda t: priority_order.get(t.priority, 4))
        
        return ready_tasks
    
    def assign_task(self, task_id: str, agent_type: str) -> bool:
        """Assign a task to an agent type based on capabilities."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        # Check if agent type can handle this task
        agent_caps = self.agent_capabilities.get(agent_type, {}).get('capabilities', [])
        task_requirements = [task.type, 'general']  # Tasks can be handled by specialized or general agents
        
        if any(req in agent_caps for req in task_requirements):
            task.assigned_agent = agent_type
            task.status = TaskStatus.IN_PROGRESS
            task.started_at = datetime.now()
            self.active_tasks.add(task_id)
            self._update_memory_status()
            return True
        
        return False
    
    def complete_task(self, task_id: str, results: Dict[str, Any] = None):
        """Mark a task as completed and update dependencies."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        
        if task.started_at:
            duration = (task.completed_at - task.started_at).total_seconds() / 60
            task.actual_duration = int(duration)
        
        self.active_tasks.discard(task_id)
        self.completed_tasks.add(task_id)
        
        # Store results in memory
        if results:
            self._store_task_results(task_id, results)
        
        self._update_memory_status()
        return True
    
    def fail_task(self, task_id: str, reason: str = ""):
        """Mark a task as failed."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.FAILED
        
        self.active_tasks.discard(task_id)
        self.failed_tasks.add(task_id)
        
        self._update_memory_status()
        return True
    
    def get_execution_plan(self, strategy: ExecutionStrategy = ExecutionStrategy.ADAPTIVE) -> List[List[str]]:
        """Generate execution plan based on strategy."""
        if strategy == ExecutionStrategy.SEQUENTIAL:
            return self._generate_sequential_plan()
        elif strategy == ExecutionStrategy.PARALLEL:
            return self._generate_parallel_plan()
        elif strategy == ExecutionStrategy.BALANCED:
            return self._generate_balanced_plan()
        else:  # ADAPTIVE
            return self._generate_adaptive_plan()
    
    def _generate_sequential_plan(self) -> List[List[str]]:
        """Generate sequential execution plan respecting dependencies."""
        plan = []
        remaining_tasks = set(self.tasks.keys()) - self.completed_tasks - self.failed_tasks
        
        while remaining_tasks:
            ready = []
            for task_id in remaining_tasks:
                task = self.tasks[task_id]
                if all(dep in self.completed_tasks for dep in task.dependencies):
                    ready.append(task_id)
            
            if not ready:
                break  # Circular dependency or blocked tasks
            
            # Take highest priority task
            ready_tasks = [self.tasks[tid] for tid in ready]
            priority_order = {TaskPriority.CRITICAL: 0, TaskPriority.HIGH: 1, 
                             TaskPriority.MEDIUM: 2, TaskPriority.LOW: 3}
            ready_tasks.sort(key=lambda t: priority_order.get(t.priority, 4))
            
            next_task = ready_tasks[0].id
            plan.append([next_task])
            remaining_tasks.remove(next_task)
            self.completed_tasks.add(next_task)  # Simulate completion for planning
        
        # Restore original state
        self.completed_tasks -= set(task_id for batch in plan for task_id in batch)
        
        return plan
    
    def _generate_parallel_plan(self) -> List[List[str]]:
        """Generate maximally parallel execution plan."""
        plan = []
        remaining_tasks = set(self.tasks.keys()) - self.completed_tasks - self.failed_tasks
        completed_in_plan = set(self.completed_tasks)
        
        while remaining_tasks:
            ready_batch = []
            for task_id in remaining_tasks:
                task = self.tasks[task_id]
                if all(dep in completed_in_plan for dep in task.dependencies):
                    ready_batch.append(task_id)
            
            if not ready_batch:
                break  # Circular dependency or blocked tasks
            
            plan.append(ready_batch)
            remaining_tasks -= set(ready_batch)
            completed_in_plan.update(ready_batch)
        
        return plan
    
    def _generate_balanced_plan(self) -> List[List[str]]:
        """Generate balanced execution plan considering resource constraints."""
        # Similar to parallel but respect agent capacity limits
        plan = []
        remaining_tasks = set(self.tasks.keys()) - self.completed_tasks - self.failed_tasks
        completed_in_plan = set(self.completed_tasks)
        
        while remaining_tasks:
            ready_tasks = []
            for task_id in remaining_tasks:
                task = self.tasks[task_id]
                if all(dep in completed_in_plan for dep in task.dependencies):
                    ready_tasks.append(task)
            
            if not ready_tasks:
                break
            
            # Group by agent type and respect capacity
            agent_loads = {}
            batch = []
            
            for task in ready_tasks:
                best_agent = self._find_best_agent(task)
                if best_agent:
                    current_load = agent_loads.get(best_agent, 0)
                    capacity = self.agent_capabilities.get(best_agent, {}).get('loadCapacity', 1)
                    
                    if current_load < capacity:
                        batch.append(task.id)
                        agent_loads[best_agent] = current_load + 1
            
            if not batch:
                # Take at least one task to avoid infinite loop
                batch = [ready_tasks[0].id]
            
            plan.append(batch)
            remaining_tasks -= set(batch)
            completed_in_plan.update(batch)
        
        return plan
    
    def _generate_adaptive_plan(self) -> List[List[str]]:
        """Generate adaptive execution plan based on complexity and resources."""
        # Start with parallel approach and adjust based on constraints
        parallel_plan = self._generate_parallel_plan()
        
        # Adjust large batches to respect resource constraints
        adaptive_plan = []
        
        for batch in parallel_plan:
            if len(batch) <= 4:  # Small batches are fine
                adaptive_plan.append(batch)
            else:
                # Split large batches into smaller ones
                chunk_size = 3
                for i in range(0, len(batch), chunk_size):
                    adaptive_plan.append(batch[i:i + chunk_size])
        
        return adaptive_plan
    
    def _find_best_agent(self, task: Task) -> Optional[str]:
        """Find the best agent type for a task based on capabilities."""
        best_agent = None
        best_score = -1
        
        for agent_type, config in self.agent_capabilities.items():
            capabilities = config.get('capabilities', [])
            score = 0
            
            # Direct capability match
            if task.type in capabilities:
                score += 10
            
            # General capability match
            if 'general' in capabilities or len(capabilities) == 0:
                score += 1
            
            # Specialization bonus
            specializations = config.get('specializations', [])
            for spec in specializations:
                if spec.lower() in task.description.lower():
                    score += 5
            
            if score > best_score:
                best_score = score
                best_agent = agent_type
        
        return best_agent
    
    def _update_memory_status(self):
        """Update memory coordination status."""
        status = {
            "swarm": {
                "tasks": {
                    "status": {
                        "activeTasks": {tid: self.tasks[tid].to_dict() for tid in self.active_tasks},
                        "completedTasks": {tid: self.tasks[tid].to_dict() for tid in self.completed_tasks},
                        "failedTasks": {tid: self.tasks[tid].to_dict() for tid in self.failed_tasks},
                        "queuedTasks": {tid: task.to_dict() for tid, task in self.tasks.items() 
                                       if task.status == TaskStatus.PENDING},
                        "taskHistory": list(self.completed_tasks | self.failed_tasks)
                    }
                }
            },
            "lastUpdate": datetime.now().isoformat()
        }
        
        try:
            with open('.claude-flow/orchestration/memory/coordination-memory.json', 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not update memory status: {e}")
    
    def _store_task_results(self, task_id: str, results: Dict[str, Any]):
        """Store task results in memory."""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        for memory_key in task.memory_keys:
            # In a full implementation, this would store to the actual memory system
            # For now, we simulate by storing in our coordination memory
            pass
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report."""
        total_tasks = len(self.tasks)
        
        return {
            "swarm_id": self.swarm_id,
            "total_tasks": total_tasks,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "pending_tasks": total_tasks - len(self.active_tasks) - len(self.completed_tasks) - len(self.failed_tasks),
            "ready_tasks": len(self.get_ready_tasks()),
            "task_breakdown": {
                status.value: len([t for t in self.tasks.values() if t.status == status])
                for status in TaskStatus
            },
            "agent_assignments": {
                agent: len([t for t in self.tasks.values() if t.assigned_agent == agent])
                for agent in self.agent_capabilities.keys()
            },
            "estimated_remaining_time": sum(
                task.estimated_duration or 0 
                for task in self.tasks.values() 
                if task.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]
            ),
            "last_update": datetime.now().isoformat()
        }

# Example usage and CLI interface
if __name__ == "__main__":
    import sys
    
    orchestrator = TaskOrchestrator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            report = orchestrator.get_status_report()
            print(json.dumps(report, indent=2))
        
        elif command == "decompose" and len(sys.argv) > 2:
            objective = sys.argv[2]
            context = {}
            if len(sys.argv) > 3:
                try:
                    context = json.loads(sys.argv[3])
                except:
                    pass
            
            tasks = orchestrator.decompose_objective(objective, context)
            print(f"Decomposed '{objective}' into {len(tasks)} tasks:")
            for task in tasks:
                print(f"  - {task.id}: {task.description}")
        
        elif command == "plan":
            strategy_map = {
                "sequential": ExecutionStrategy.SEQUENTIAL,
                "parallel": ExecutionStrategy.PARALLEL,
                "balanced": ExecutionStrategy.BALANCED,
                "adaptive": ExecutionStrategy.ADAPTIVE
            }
            strategy = ExecutionStrategy.ADAPTIVE
            if len(sys.argv) > 2 and sys.argv[2] in strategy_map:
                strategy = strategy_map[sys.argv[2]]
            
            plan = orchestrator.get_execution_plan(strategy)
            print(f"Execution plan ({strategy.value}):")
            for i, batch in enumerate(plan, 1):
                print(f"  Batch {i}: {batch}")
        
        else:
            print("Usage: python task-orchestrator.py <command> [args]")
            print("Commands:")
            print("  status - Show current status")
            print("  decompose <objective> [context_json] - Decompose objective")
            print("  plan [strategy] - Generate execution plan")
    
    else:
        print("Task Orchestrator initialized for swarm-1756696734588-1rik89o3r")
        print("Ready to coordinate task execution and manage dependencies.")