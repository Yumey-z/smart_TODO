#!/usr/bin/env python3
"""
Smart Todo Manager
Main program file - User interface and interaction logic
"""
import sys
from datetime import datetime
from task import Task, Priority, TaskStatus, UrgentTask, RecurringTask
from manager import TaskManager
from utils import (
    parse_date, get_user_choice, confirm_action, safe_int_input,
    parse_priority, print_table, colorize_text, create_progress_bar
)


class TodoApp:
    """Todo application main class"""
    
    def __init__(self):
        self.manager = TaskManager()
        self.running = True
    
    def show_banner(self):
        """Display application banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                   🗂️  SmartTodo Manager                      ║
║                   Make your task management smarter          ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(colorize_text(banner, 'cyan'))
    
    def show_main_menu(self):
        """Display main menu"""
        print("\n" + "=" * 60)
        print("📋 Main Menu")
        print("=" * 60)
        
        # Show quick statistics
        stats = self.manager.get_statistics()
        pending = stats['Pending']
        overdue = stats['Overdue']
        
        if overdue > 0:
            print(f"⚠️  You have {colorize_text(str(overdue), 'red')} overdue tasks!")
        if pending > 0:
            print(f"📝 Pending tasks: {pending}")
        
        print()
    
    def get_main_menu_options(self):
        """Get main menu options"""
        return [
            "📝 Add New Task",
            "📋 View Task List",
            "✅ Complete Task",
            "🗑️ Delete Task",
            "🔍 Search Tasks",
            "📊 Task Statistics",
            "⚙️ Management Functions",
            "🚪 Exit Program"
        ]
    
    def run(self):
        """Run main program"""
        self.show_banner()
        
        while self.running:
            try:
                self.show_main_menu()
                options = self.get_main_menu_options()
                choice = get_user_choice(options, "Please select a function")
                
                if choice == 0:
                    self.add_task_menu()
                elif choice == 1:
                    self.view_tasks_menu()
                elif choice == 2:
                    self.complete_task_menu()
                elif choice == 3:
                    self.delete_task_menu()
                elif choice == 4:
                    self.search_tasks_menu()
                elif choice == 5:
                    self.show_statistics()
                elif choice == 6:
                    self.management_menu()
                elif choice == 7:
                    self.exit_program()
                
            except KeyboardInterrupt:
                print("\n👋 Program interrupted by user")
                self.exit_program()
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")
    
    def add_task_menu(self):
        """Add task menu"""
        print("\n📝 Add New Task")
        print("-" * 30)
        
        # Select task type
        task_types = ["Normal Task", "Urgent Task", "Recurring Task"]
        task_type = get_user_choice(task_types, "Select task type")
        
        # Get task information
        title = input("Task title: ").strip()
        if not title:
            print("❌ Task title cannot be empty")
            return
        
        description = input("Task description (optional): ").strip()
        category = input("Task category (default: Default): ").strip() or "Default"
        
        # Parse due date
        due_date = None
        due_input = input("Due date (format: YYYY-MM-DD HH:MM or tomorrow/+3days, optional): ").strip()
        if due_input:
            due_date = parse_date(due_input)
            if due_date is None:
                print("⚠️ Invalid date format, due date will be ignored")
        
        # Create task
        if task_type == 0:  # Normal task
            priority_input = input("Priority (high/medium/low, default: medium): ").strip() or "medium"
            priority = Priority(parse_priority(priority_input))
            task = Task(title, description, priority, due_date, category)
        
        elif task_type == 1:  # Urgent task
            task = UrgentTask(title, description, due_date, category)
        
        else:  # Recurring task
            priority_input = input("Priority (high/medium/low, default: medium): ").strip() or "medium"
            priority = Priority(parse_priority(priority_input))
            repeat_days = safe_int_input("Repeat interval (days, default: 7): ", 7, 1, 365)
            task = RecurringTask(title, description, priority, due_date, category, repeat_days)
        
        # Add task
        if self.manager.add_task(task):
            print(f"✅ Task added successfully! ID: {task.id}")
        
        input("\nPress Enter to continue...")
    
    def view_tasks_menu(self):
        """View tasks menu"""
        print("\n📋 View Task List")
        print("-" * 30)
        
        view_options = [
            "All Tasks",
            "Pending Tasks",
            "Completed Tasks",
            "Overdue Tasks",
            "Today's Tasks",
            "Upcoming Tasks",
            "View by Category",
            "Sort by Priority",
            "Sort by Due Date"
        ]
        
        choice = get_user_choice(view_options, "Select view method")
        
        tasks = []
        if choice == 0:
            tasks = list(self.manager.tasks)
        elif choice == 1:
            tasks = self.manager.get_tasks_by_status(TaskStatus.PENDING)
        elif choice == 2:
            tasks = self.manager.get_tasks_by_status(TaskStatus.COMPLETED)
        elif choice == 3:
            tasks = self.manager.get_overdue_tasks()
        elif choice == 4:
            tasks = self.manager.get_today_tasks()
        elif choice == 5:
            tasks = self.manager.get_upcoming_tasks()
        elif choice == 6:
            categories = self.manager.get_categories()
            if categories:
                cat_choice = get_user_choice(categories, "Select category")
                tasks = self.manager.get_tasks_by_category(categories[cat_choice])
        elif choice == 7:
            tasks = self.manager.sort_tasks_by_priority()
        elif choice == 8:
            tasks = self.manager.sort_tasks_by_due_date()
        
        self.display_tasks(tasks)
        input("\nPress Enter to continue...")
    
    def display_tasks(self, tasks):
        """Display task list"""
        if not tasks:
            print("📝 No tasks found")
            return
        
        print(f"\nFound {len(tasks)} tasks:")
        print("-" * 80)
        
        for i, task in enumerate(tasks, 1):
            status_color = 'green' if task.status == TaskStatus.COMPLETED else 'red' if task.is_overdue else 'white'
            task_str = f"{i:2d}. {task}"
            print(colorize_text(task_str, status_color))
            
            if task.description:
                print(f"     💬 {task.description}")
            
            print(f"     🆔 ID: {task.id}")
            print()
    
    def complete_task_menu(self):
        """Complete task menu"""
        pending_tasks = self.manager.get_tasks_by_status(TaskStatus.PENDING)
        if not pending_tasks:
            print("📝 No pending tasks")
            input("Press Enter to continue...")
            return
        
        print("\n✅ Complete Task")
        print("-" * 30)
        
        self.display_tasks(pending_tasks)
        
        task_id = input("Enter task ID to complete: ").strip()
        if task_id in self.manager:
            if confirm_action("Confirm to complete this task"):
                self.manager.complete_task(task_id)
        else:
            print("❌ Task ID does not exist")
        
        input("Press Enter to continue...")
    
    def delete_task_menu(self):
        """Delete task menu"""
        if not self.manager.tasks:
            print("📝 No tasks found")
            input("Press Enter to continue...")
            return
        
        print("\n🗑️ Delete Task")
        print("-" * 30)
        
        self.display_tasks(list(self.manager.tasks))
        
        task_id = input("Enter task ID to delete: ").strip()
        if task_id in self.manager:
            task = self.manager.get_task_by_id(task_id)
            if confirm_action(f"Confirm to delete task '{task.title}'"):
                self.manager.remove_task(task_id)
        else:
            print("❌ Task ID does not exist")
        
        input("Press Enter to continue...")
    
    def search_tasks_menu(self):
        """Search tasks menu"""
        print("\n🔍 Search Tasks")
        print("-" * 30)
        
        keyword = input("Enter search keyword: ").strip()
        if not keyword:
            print("❌ Search keyword cannot be empty")
            input("Press Enter to continue...")
            return
        
        results = self.manager.search_tasks(keyword)
        print(f"\nSearch results for '{keyword}':")
        self.display_tasks(results)
        
        input("Press Enter to continue...")
    
    def show_statistics(self):
        """Display statistics"""
        print("\n📊 Task Statistics")
        print("-" * 30)
        
        stats = self.manager.get_statistics()
        
        # Basic statistics
        print("📈 Basic Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Completion rate
        total = stats['Total Tasks']
        completed = stats['Completed']
        if total > 0:
            completion_rate = (completed / total) * 100
            progress_bar = create_progress_bar(completed, total)
            print(f"\n📊 Completion Progress: {progress_bar} ({completion_rate:.1f}%)")
        
        # Category statistics
        categories = self.manager.get_categories()
        if categories:
            print("\n📂 Category Statistics:")
            for category in categories:
                count = len(self.manager.get_tasks_by_category(category))
                print(f"   {category}: {count} tasks")
        
        input("\nPress Enter to continue...")
    
    def management_menu(self):
        """Management functions menu"""
        print("\n⚙️ Management Functions")
        print("-" * 30)
        
        mgmt_options = [
            "🧹 Clear Completed Tasks",
            "💾 Backup Task Data",
            "🔄 Reload Data",
            "📤 Export Task Report",
            "🔙 Return to Main Menu"
        ]
        
        choice = get_user_choice(mgmt_options, "Select management function")
        
        if choice == 0:
            if confirm_action("Confirm to clear all completed tasks"):
                count = self.manager.clear_completed_tasks()
                print(f"✅ Cleared {count} completed tasks")
        
        elif choice == 1:
            self.manager.backup_tasks()
        
        elif choice == 2:
            self.manager.load_tasks()
            print("✅ Data reloaded successfully")
        
        elif choice == 3:
            self.export_report()
        
        elif choice == 4:
            return
        
        input("Press Enter to continue...")
    
    def export_report(self):
        """Export task report"""
        try:
            filename = f"task_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("SmartTodo Task Report\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Statistics
                stats = self.manager.get_statistics()
                f.write("Statistics:\n")
                for key, value in stats.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
                
                # Task list
                f.write("Task List:\n")
                f.write("-" * 30 + "\n")
                
                for task in self.manager.tasks:
                    f.write(f"Title: {task.title}\n")
                    f.write(f"Status: {task.status.value}\n")
                    f.write(f"Priority: {task.priority.name}\n")
                    f.write(f"Category: {task.category}\n")
                    if task.due_date:
                        f.write(f"Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M')}\n")
                    if task.description:
                        f.write(f"Description: {task.description}\n")
                    f.write(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}\n")
                    f.write("-" * 30 + "\n")
            
            print(f"📤 Report exported to: {filename}")
        
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def exit_program(self):
        """Exit program"""
        print("\n👋 Thank you for using SmartTodo!")
        print("💾 Data has been automatically saved")
        self.running = False
        sys.exit(0)


def main():
    """Main function"""
    try:
        app = TodoApp()
        app.run()
    except Exception as e:
        print(f"❌ A serious error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 