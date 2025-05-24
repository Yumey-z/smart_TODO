"""
Task manager module
Implements CRUD operations and various management functions for tasks
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Callable
from task import Task, Priority, TaskStatus, UrgentTask, RecurringTask


def log_action(func: Callable) -> Callable:
    """Decorator: Record operation logs"""
    def wrapper(self, *args, **kwargs):
        action_name = func.__name__
        result = func(self, *args, **kwargs)
        print(f"📝 Operation log: {action_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return result
    return wrapper


class TaskManager:
    """Task manager class"""
    
    def __init__(self, data_file: str = "data/tasks.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self._ensure_data_directory()
        self.load_tasks()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        dir_path = os.path.dirname(self.data_file)
        if dir_path:  # Only create directory if there is a directory path
            os.makedirs(dir_path, exist_ok=True)
    
    @log_action
    def add_task(self, task: Task) -> bool:
        """Add task"""
        try:
            self.tasks.append(task)
            self.save_tasks()
            print(f"✅ Task added successfully: {task.title}")
            return True
        except Exception as e:
            print(f"❌ Failed to add task: {e}")
            return False
    
    @log_action
    def remove_task(self, task_id: str) -> bool:
        """Remove task"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                removed_task = self.tasks.pop(i)
                self.save_tasks()
                print(f"🗑️ Task removed successfully: {removed_task.title}")
                return True
        print(f"❌ Task with ID {task_id} not found")
        return False
    
    @log_action
    def complete_task(self, task_id: str) -> bool:
        """Complete task"""
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            self.save_tasks()
            print(f"✅ Task completed: {task.title}")
            return True
        print(f"❌ Task with ID {task_id} not found")
        return False
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get tasks by category"""
        return [task for task in self.tasks if task.category == category]
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get tasks by status"""
        return [task for task in self.tasks if task.status == status]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Get overdue tasks"""
        return [task for task in self.tasks if task.is_overdue]
    
    def get_today_tasks(self) -> List[Task]:
        """Get today's tasks"""
        today = datetime.now().date()
        return [task for task in self.tasks 
                if task.due_date and task.due_date.date() == today]
    
    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get upcoming tasks"""
        now = datetime.now()
        future = now + timedelta(days=days)
        return [task for task in self.tasks 
                if task.due_date and now <= task.due_date <= future 
                and task.status != TaskStatus.COMPLETED]
    
    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks"""
        keyword = keyword.lower()
        return [task for task in self.tasks 
                if keyword in task.title.lower() 
                or keyword in task.description.lower()
                or keyword in task.category.lower()]
    
    def sort_tasks_by_priority(self, reverse: bool = True) -> List[Task]:
        """Sort tasks by priority"""
        return sorted(self.tasks, key=lambda x: x.priority_score, reverse=reverse)
    
    def sort_tasks_by_due_date(self, reverse: bool = False) -> List[Task]:
        """Sort tasks by due date"""
        # Place tasks without due date at the end
        with_due_date = [task for task in self.tasks if task.due_date]
        without_due_date = [task for task in self.tasks if not task.due_date]
        
        sorted_with_due = sorted(with_due_date, key=lambda x: x.due_date, reverse=reverse)
        return sorted_with_due + without_due_date
    
    def get_statistics(self) -> Dict[str, int]:
        """Get task statistics"""
        stats = {
            'Total Tasks': len(self.tasks),
            'Pending': len([t for t in self.tasks if t.status == TaskStatus.PENDING]),
            'In Progress': len([t for t in self.tasks if t.status == TaskStatus.IN_PROGRESS]),
            'Completed': len([t for t in self.tasks if t.status == TaskStatus.COMPLETED]),
            'Overdue': len(self.get_overdue_tasks()),
            'High Priority': len([t for t in self.tasks if t.priority == Priority.HIGH]),
            'Medium Priority': len([t for t in self.tasks if t.priority == Priority.MEDIUM]),
            'Low Priority': len([t for t in self.tasks if t.priority == Priority.LOW])
        }
        return stats
    
    def get_categories(self) -> List[str]:
        """Get all categories"""
        categories = set(task.category for task in self.tasks)
        return sorted(list(categories))
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            data = []
            for task in self.tasks:
                task_data = task.to_dict()
                # Add type information for proper restoration
                if isinstance(task, UrgentTask):
                    task_data['task_type'] = 'UrgentTask'
                elif isinstance(task, RecurringTask):
                    task_data['task_type'] = 'RecurringTask'
                else:
                    task_data['task_type'] = 'Task'
                data.append(task_data)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Failed to save tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from file"""
        try:
            if not os.path.exists(self.data_file):
                return
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.tasks = []
            for task_data in data:
                task_type = task_data.get('task_type', 'Task')
                
                if task_type == 'UrgentTask':
                    # For UrgentTask, create normal Task first then convert
                    task = Task.from_dict(task_data)
                    urgent_task = UrgentTask(task.title, task.description, task.due_date, task.category)
                    urgent_task._id = task.id
                    urgent_task.status = task.status
                    urgent_task.created_at = task.created_at
                    urgent_task.completed_at = task.completed_at
                    task = urgent_task
                elif task_type == 'RecurringTask':
                    task = RecurringTask.from_dict(task_data)
                else:
                    task = Task.from_dict(task_data)
                
                self.tasks.append(task)
                
            print(f"📂 Successfully loaded {len(self.tasks)} tasks")
        except Exception as e:
            print(f"❌ Failed to load tasks: {e}")
            self.tasks = []
    
    def backup_tasks(self, backup_file: Optional[str] = None):
        """Backup task data"""
        if not backup_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"tasks_backup_{timestamp}.json"
        
        try:
            import shutil
            shutil.copy2(self.data_file, backup_file)
            print(f"💾 Task data backed up to: {backup_file}")
        except Exception as e:
            print(f"❌ Backup failed: {e}")
    
    def clear_completed_tasks(self) -> int:
        """Clear completed tasks"""
        completed_tasks = [task for task in self.tasks if task.status == TaskStatus.COMPLETED]
        count = len(completed_tasks)
        
        self.tasks = [task for task in self.tasks if task.status != TaskStatus.COMPLETED]
        self.save_tasks()
        
        print(f"🧹 Cleared {count} completed tasks")
        return count
    
    def __len__(self) -> int:
        """Return total number of tasks"""
        return len(self.tasks)
    
    def __iter__(self):
        """Make TaskManager iterable"""
        return iter(self.tasks)
    
    def __contains__(self, task_id: str) -> bool:
        """Check if task with specified ID exists"""
        return any(task.id == task_id for task in self.tasks) 