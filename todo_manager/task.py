#!/usr/bin/env python3
"""
Task class definition module
Contains Task base class and its subclasses implementation
"""
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Task priority enumeration"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class Task:
    """Task base class"""
    
    def __init__(self, title: str, description: str = "", 
                 priority: Priority = Priority.MEDIUM,
                 due_date: Optional[datetime] = None,
                 category: str = "Default"):
        self._id = self._generate_id()
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
    
    @staticmethod
    def _generate_id() -> str:
        """Generate unique task ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    @property
    def id(self) -> str:
        """Get task ID (read-only)"""
        return self._id
    
    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.due_date is None or self.status == TaskStatus.COMPLETED:
            return False
        return datetime.now() > self.due_date
    
    @property
    def priority_score(self) -> int:
        """Get priority score for sorting"""
        base_score = self.priority.value * 10
        # Increase urgency if overdue
        if self.is_overdue:
            base_score += 20
        return base_score
    
    def mark_completed(self):
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def mark_in_progress(self):
        """Mark task as in progress"""
        self.status = TaskStatus.IN_PROGRESS
    
    def __str__(self) -> str:
        """String representation of task"""
        status_icon = "✓" if self.status == TaskStatus.COMPLETED else "○"
        priority_icon = "🔴" if self.priority == Priority.HIGH else "🟡" if self.priority == Priority.MEDIUM else "🟢"
        
        due_info = ""
        if self.due_date:
            due_str = self.due_date.strftime("%Y-%m-%d %H:%M")
            if self.is_overdue:
                due_info = f" [❗Overdue: {due_str}]"
            else:
                due_info = f" [Due: {due_str}]"
        
        return f"{status_icon} {priority_icon} [{self.category}] {self.title}{due_info}"
    
    def __repr__(self) -> str:
        return f"Task(id='{self.id}', title='{self.title}', priority={self.priority.name})"
    
    def to_dict(self) -> dict:
        """Convert task to dictionary format for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'category': self.category,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create Task object from dictionary"""
        due_date = None
        if data.get('due_date'):
            due_date = datetime.fromisoformat(data['due_date'])
            
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority(data.get('priority', 2)),
            due_date=due_date,
            category=data.get('category', 'Default')
        )
        
        # Set other attributes
        task._id = data['id']
        task.status = TaskStatus(data.get('status', TaskStatus.PENDING.value))
        task.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('completed_at'):
            task.completed_at = datetime.fromisoformat(data['completed_at'])
        
        return task


class UrgentTask(Task):
    """Urgent task subclass"""
    
    def __init__(self, title: str, description: str = "", 
                 due_date: Optional[datetime] = None,
                 category: str = "Urgent"):
        super().__init__(title, description, Priority.HIGH, due_date, category)
    
    @property
    def priority_score(self) -> int:
        """Urgent tasks have higher priority score"""
        return super().priority_score + 15
    
    def __str__(self) -> str:
        return f"🚨 {super().__str__()}"


class RecurringTask(Task):
    """Recurring task subclass"""
    
    def __init__(self, title: str, description: str = "",
                 priority: Priority = Priority.MEDIUM,
                 due_date: Optional[datetime] = None,
                 category: str = "Recurring",
                 repeat_days: int = 7):
        super().__init__(title, description, priority, due_date, category)
        self.repeat_days = repeat_days
        self.is_recurring = True
    
    def mark_completed(self):
        """When completing recurring task, create next repeat task"""
        super().mark_completed()
        if self.due_date:
            from datetime import timedelta
            self.due_date = self.due_date + timedelta(days=self.repeat_days)
            self.status = TaskStatus.PENDING
            self.completed_at = None
    
    def to_dict(self) -> dict:
        """Extend parent class serialization method"""
        data = super().to_dict()
        data['repeat_days'] = self.repeat_days
        data['is_recurring'] = True
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RecurringTask':
        """Create RecurringTask object from dictionary"""
        due_date = None
        if data.get('due_date'):
            due_date = datetime.fromisoformat(data['due_date'])
            
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority(data.get('priority', 2)),
            due_date=due_date,
            category=data.get('category', 'Recurring'),
            repeat_days=data.get('repeat_days', 7)
        )
        
        # Set other attributes
        task._id = data['id']
        task.status = TaskStatus(data.get('status', TaskStatus.PENDING.value))
        task.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('completed_at'):
            task.completed_at = datetime.fromisoformat(data['completed_at'])
        
        return task
    
    def __str__(self) -> str:
        return f"🔄 {super().__str__()}" 