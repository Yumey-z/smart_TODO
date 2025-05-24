#!/usr/bin/env python3
"""
SmartTodo Demo Script
Demonstrates the main features and capabilities of the project
"""
from datetime import datetime, timedelta
from task import Task, Priority, TaskStatus, UrgentTask, RecurringTask
from manager import TaskManager
from utils import parse_date, create_progress_bar


def demo_basic_features():
    """Demonstrate basic features"""
    print("🎯 SmartTodo Feature Demo")
    print("=" * 50)
    
    # Create task manager (use current directory instead of data/ subfolder)
    manager = TaskManager("demo_tasks.json")
    
    print("\n1. 📝 Creating different types of tasks")
    print("-" * 30)
    
    # Create normal task
    task1 = Task("Complete Python Assignment", "Implement todo manager", Priority.HIGH, 
                 parse_date("tomorrow"), "Study")
    
    # Create urgent task
    task2 = UrgentTask("Fix System Bug", "Fix critical login module error")
    
    # Create recurring task
    task3 = RecurringTask("Daily Exercise", "Stay healthy", Priority.MEDIUM,
                         parse_date("+1days"), "Health", 1)
    
    # Add tasks
    manager.add_task(task1)
    manager.add_task(task2)
    manager.add_task(task3)
    
    print(f"\n✅ Successfully added {len(manager)} tasks")
    
    print("\n2. 📋 View task list")
    print("-" * 30)
    for i, task in enumerate(manager.tasks, 1):
        print(f"{i}. {task}")
        if task.description:
            print(f"   💬 {task.description}")
    
    print("\n3. 🔍 Search functionality demo")
    print("-" * 30)
    python_tasks = manager.search_tasks("Python")
    print(f"Search results for 'Python': {len(python_tasks)} tasks")
    for task in python_tasks:
        print(f"  - {task.title}")
    
    print("\n4. 📊 Task statistics")
    print("-" * 30)
    stats = manager.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Completion progress
    total = stats['Total Tasks']
    completed = stats['Completed']
    if total > 0:
        progress_bar = create_progress_bar(completed, total)
        completion_rate = (completed / total) * 100
        print(f"\n📈 Completion Progress: {progress_bar} ({completion_rate:.1f}%)")
    
    print("\n5. ✅ Complete task demo")
    print("-" * 30)
    # Complete first task
    manager.complete_task(task1.id)
    print(f"Task '{task1.title}' completed")
    
    print("\n6. 🔄 Recurring task demo")
    print("-" * 30)
    print(f"Recurring task before completion: {task3}")
    task3.mark_completed()
    print(f"Recurring task after completion: {task3}")
    print("Note: Recurring task automatically resets to pending status and updates due date")
    
    print("\n7. 🏷️ Category management")
    print("-" * 30)
    categories = manager.get_categories()
    print(f"Task categories: {', '.join(categories)}")
    for category in categories:
        tasks_in_category = manager.get_tasks_by_category(category)
        print(f"  {category}: {len(tasks_in_category)} tasks")
    
    print("\n8. ⚡ Priority sorting")
    print("-" * 30)
    sorted_tasks = manager.sort_tasks_by_priority()
    print("Tasks sorted by priority:")
    for i, task in enumerate(sorted_tasks, 1):
        priority_name = task.priority.name
        print(f"  {i}. [{priority_name}] {task.title}")
    
    print("\n9. 💾 Data persistence")
    print("-" * 30)
    manager.save_tasks()
    print("✅ Task data saved to file")
    
    # Backup demo
    manager.backup_tasks()
    
    print("\n🎉 Demo complete!")
    print("SmartTodo demonstrates the following Python programming concepts:")
    print("  • Object-Oriented Programming (classes and inheritance)")
    print("  • Enums (Priority, TaskStatus)")
    print("  • Property decorators (@property)")
    print("  • Magic methods (__str__, __len__, __contains__)")
    print("  • Decorators (@log_action)")
    print("  • Type hints")
    print("  • Exception handling (try/except)")
    print("  • File I/O (JSON serialization)")
    print("  • List comprehensions")
    print("  • Lambda functions")


def demo_advanced_features():
    """Demonstrate advanced features"""
    print("\n🚀 Advanced Features Demo")
    print("=" * 50)
    
    manager = TaskManager("demo_advanced.json")
    
    # Create test data
    tasks = [
        Task("Learn Python", "Complete online course", Priority.HIGH, 
             datetime.now() + timedelta(days=2), "Study"),
        Task("Write Project Report", "Complete final project report", Priority.MEDIUM,
             datetime.now() - timedelta(days=1), "Study"),  # Overdue task
        UrgentTask("Handle Customer Complaint", "Urgent customer feedback handling"),
        RecurringTask("Read Tech Articles", "Daily tech learning", Priority.LOW,
                     datetime.now() + timedelta(hours=2), "Study", 1),
        Task("Workout", "Go to gym", Priority.MEDIUM,
             datetime.now().replace(hour=18, minute=0), "Health")
    ]
    
    for task in tasks:
        manager.add_task(task)
    
    print(f"\n📊 Created {len(tasks)} test tasks")
    
    # Overdue task check
    overdue_tasks = manager.get_overdue_tasks()
    print(f"\n⚠️ Overdue tasks: {len(overdue_tasks)}")
    for task in overdue_tasks:
        print(f"  - {task.title} (overdue: {task.due_date.strftime('%Y-%m-%d %H:%M')})")
    
    # Today's tasks
    today_tasks = manager.get_today_tasks()
    print(f"\n📅 Today's tasks: {len(today_tasks)}")
    for task in today_tasks:
        print(f"  - {task.title}")
    
    # Upcoming tasks
    upcoming_tasks = manager.get_upcoming_tasks(days=3)
    print(f"\n⏰ Tasks due within 3 days: {len(upcoming_tasks)}")
    for task in upcoming_tasks:
        due_str = task.due_date.strftime('%Y-%m-%d %H:%M')
        print(f"  - {task.title} (due: {due_str})")
    
    # Sort by due date
    sorted_by_date = manager.sort_tasks_by_due_date()
    print(f"\n📆 Sorted by due date:")
    for task in sorted_by_date:
        if task.due_date:
            due_str = task.due_date.strftime('%Y-%m-%d %H:%M')
            print(f"  - {task.title} (due: {due_str})")
        else:
            print(f"  - {task.title} (no due date)")
    
    print("\n🧹 Cleaning up demo data...")
    import os
    for filename in ["demo_tasks.json", "demo_advanced.json"]:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"  Deleted {filename}")


if __name__ == "__main__":
    try:
        demo_basic_features()
        demo_advanced_features()
        print("\n✨ All demos completed!")
    except Exception as e:
        print(f"❌ Error occurred during demo: {e}")
        import traceback
        traceback.print_exc() 