#!/usr/bin/env python3
"""
SmartTodo Test Module
Contains various test cases to verify program functionality
"""
import unittest
import os
import tempfile
from datetime import datetime, timedelta
from task import Task, Priority, TaskStatus, UrgentTask, RecurringTask
from manager import TaskManager
from utils import parse_date, parse_priority, format_duration


class TestTask(unittest.TestCase):
    """Task class tests"""
    
    def setUp(self):
        """Setup before tests"""
        self.task = Task("Test Task", "This is a test task", Priority.HIGH)
    
    def test_task_creation(self):
        """Test task creation"""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "This is a test task")
        self.assertEqual(self.task.priority, Priority.HIGH)
        self.assertEqual(self.task.status, TaskStatus.PENDING)
        self.assertIsNotNone(self.task.id)
        self.assertIsNotNone(self.task.created_at)
    
    def test_task_completion(self):
        """Test task completion"""
        self.task.mark_completed()
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(self.task.completed_at)
    
    def test_task_overdue(self):
        """Test overdue check"""
        # Set overdue time
        past_date = datetime.now() - timedelta(days=1)
        self.task.due_date = past_date
        self.assertTrue(self.task.is_overdue)
        
        # Should not be overdue after completion
        self.task.mark_completed()
        self.assertFalse(self.task.is_overdue)
    
    def test_task_priority_score(self):
        """Test priority score"""
        normal_task = Task("Normal Task", priority=Priority.MEDIUM)
        high_task = Task("High Priority Task", priority=Priority.HIGH)
        
        self.assertGreater(high_task.priority_score, normal_task.priority_score)
    
    def test_task_serialization(self):
        """Test task serialization"""
        task_dict = self.task.to_dict()
        restored_task = Task.from_dict(task_dict)
        
        self.assertEqual(self.task.title, restored_task.title)
        self.assertEqual(self.task.description, restored_task.description)
        self.assertEqual(self.task.priority, restored_task.priority)
        self.assertEqual(self.task.id, restored_task.id)


class TestUrgentTask(unittest.TestCase):
    """UrgentTask class tests"""
    
    def test_urgent_task_creation(self):
        """Test urgent task creation"""
        urgent_task = UrgentTask("Urgent Task")
        self.assertEqual(urgent_task.priority, Priority.HIGH)
        self.assertEqual(urgent_task.category, "Urgent")
        self.assertGreater(urgent_task.priority_score, 30)  # Should have extra priority bonus


class TestRecurringTask(unittest.TestCase):
    """RecurringTask class tests"""
    
    def test_recurring_task_creation(self):
        """Test recurring task creation"""
        due_date = datetime.now() + timedelta(days=1)
        recurring_task = RecurringTask("Recurring Task", due_date=due_date, repeat_days=7)
        
        self.assertTrue(recurring_task.is_recurring)
        self.assertEqual(recurring_task.repeat_days, 7)
    
    def test_recurring_task_completion(self):
        """Test recurring task completion"""
        due_date = datetime.now() + timedelta(days=1)
        recurring_task = RecurringTask("Recurring Task", due_date=due_date, repeat_days=7)
        original_due_date = recurring_task.due_date
        
        recurring_task.mark_completed()
        
        # Recurring task should reset to pending after completion and update due date
        self.assertEqual(recurring_task.status, TaskStatus.PENDING)
        self.assertIsNone(recurring_task.completed_at)
        self.assertGreater(recurring_task.due_date, original_due_date)


class TestTaskManager(unittest.TestCase):
    """TaskManager class tests"""
    
    def setUp(self):
        """Setup before tests"""
        # Use temporary file to avoid affecting actual data
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.manager = TaskManager(self.temp_file.name)
    
    def tearDown(self):
        """Cleanup after tests"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_task(self):
        """Test add task"""
        task = Task("Test Task")
        result = self.manager.add_task(task)
        
        self.assertTrue(result)
        self.assertEqual(len(self.manager), 1)
        self.assertIn(task.id, self.manager)
    
    def test_remove_task(self):
        """Test remove task"""
        task = Task("Test Task")
        self.manager.add_task(task)
        
        result = self.manager.remove_task(task.id)
        self.assertTrue(result)
        self.assertEqual(len(self.manager), 0)
        
        # Remove non-existent task
        result = self.manager.remove_task("nonexistent")
        self.assertFalse(result)
    
    def test_complete_task(self):
        """Test complete task"""
        task = Task("Test Task")
        self.manager.add_task(task)
        
        result = self.manager.complete_task(task.id)
        self.assertTrue(result)
        self.assertEqual(task.status, TaskStatus.COMPLETED)
    
    def test_search_tasks(self):
        """Test search tasks"""
        task1 = Task("Python Learning", "Learn Python programming")
        task2 = Task("Math Homework", "Complete calculus homework")
        task3 = Task("Programming Project", "Develop Python project")
        
        self.manager.add_task(task1)
        self.manager.add_task(task2)
        self.manager.add_task(task3)
        
        # Search for tasks containing "Python"
        results = self.manager.search_tasks("Python")
        self.assertEqual(len(results), 2)
        
        # Search for tasks containing "homework"
        results = self.manager.search_tasks("homework")
        self.assertEqual(len(results), 1)
    
    def test_get_tasks_by_status(self):
        """Test get tasks by status"""
        task1 = Task("Task 1")
        task2 = Task("Task 2")
        self.manager.add_task(task1)
        self.manager.add_task(task2)
        
        # Complete one task
        self.manager.complete_task(task1.id)
        
        pending_tasks = self.manager.get_tasks_by_status(TaskStatus.PENDING)
        completed_tasks = self.manager.get_tasks_by_status(TaskStatus.COMPLETED)
        
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(len(completed_tasks), 1)
    
    def test_get_overdue_tasks(self):
        """Test get overdue tasks"""
        # Create overdue task
        past_date = datetime.now() - timedelta(days=1)
        overdue_task = Task("Overdue Task", due_date=past_date)
        normal_task = Task("Normal Task")
        
        self.manager.add_task(overdue_task)
        self.manager.add_task(normal_task)
        
        overdue_tasks = self.manager.get_overdue_tasks()
        self.assertEqual(len(overdue_tasks), 1)
        self.assertEqual(overdue_tasks[0].id, overdue_task.id)
    
    def test_task_statistics(self):
        """Test task statistics"""
        task1 = Task("Task 1", priority=Priority.HIGH)
        task2 = Task("Task 2", priority=Priority.LOW)
        self.manager.add_task(task1)
        self.manager.add_task(task2)
        
        # Complete one task
        self.manager.complete_task(task1.id)
        
        stats = self.manager.get_statistics()
        self.assertEqual(stats['Total Tasks'], 2)
        self.assertEqual(stats['Completed'], 1)
        self.assertEqual(stats['Pending'], 1)
        self.assertEqual(stats['High Priority'], 1)
        self.assertEqual(stats['Low Priority'], 1)
    
    def test_save_and_load_tasks(self):
        """Test save and load tasks"""
        # Add different types of tasks
        normal_task = Task("Normal Task")
        urgent_task = UrgentTask("Urgent Task")
        recurring_task = RecurringTask("Recurring Task", repeat_days=3)
        
        self.manager.add_task(normal_task)
        self.manager.add_task(urgent_task)
        self.manager.add_task(recurring_task)
        
        # Save and reload
        self.manager.save_tasks()
        new_manager = TaskManager(self.temp_file.name)
        
        self.assertEqual(len(new_manager), 3)
        
        # Verify task types are correctly restored
        task_types = [type(task).__name__ for task in new_manager.tasks]
        self.assertIn('Task', task_types)
        self.assertIn('UrgentTask', task_types)
        self.assertIn('RecurringTask', task_types)


class TestUtils(unittest.TestCase):
    """Utility functions tests"""
    
    def test_parse_date(self):
        """Test date parsing"""
        # Test standard format
        date1 = parse_date("2024-12-25")
        self.assertIsNotNone(date1)
        self.assertEqual(date1.year, 2024)
        self.assertEqual(date1.month, 12)
        self.assertEqual(date1.day, 25)
        
        # Test relative dates
        today = parse_date("today")
        self.assertIsNotNone(today)
        self.assertEqual(today.date(), datetime.now().date())
        
        # Test relative time
        future_date = parse_date("+3days")
        expected_date = datetime.now() + timedelta(days=3)
        self.assertIsNotNone(future_date)
        self.assertEqual(future_date.date(), expected_date.date())
        
        # Test invalid format
        invalid_date = parse_date("invalid")
        self.assertIsNone(invalid_date)
    
    def test_parse_priority(self):
        """Test priority parsing"""
        self.assertEqual(parse_priority("high"), 3)
        self.assertEqual(parse_priority("medium"), 2)
        self.assertEqual(parse_priority("low"), 1)
        self.assertEqual(parse_priority("h"), 3)
        self.assertEqual(parse_priority("3"), 3)
        self.assertEqual(parse_priority("invalid"), 2)  # Default value
    
    def test_format_duration(self):
        """Test time formatting"""
        self.assertEqual(format_duration(30), "30 seconds")
        self.assertEqual(format_duration(90), "1 minutes")
        self.assertEqual(format_duration(3600), "1 hours")
        self.assertEqual(format_duration(3690), "1 hours 1 minutes")


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        """Setup before tests"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.manager = TaskManager(self.temp_file.name)
    
    def tearDown(self):
        """Cleanup after tests"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_complete_workflow(self):
        """Test complete workflow"""
        # 1. Add various types of tasks
        tasks = [
            Task("Learn Python", "Complete Python tutorial", Priority.HIGH, category="Study"),
            UrgentTask("Fix Bug", "Fix critical bug in production"),
            RecurringTask("Daily Exercise", "Stay healthy", repeat_days=1, category="Health")
        ]
        
        for task in tasks:
            self.manager.add_task(task)
        
        self.assertEqual(len(self.manager), 3)
        
        # 2. Search tasks
        python_tasks = self.manager.search_tasks("Python")
        self.assertEqual(len(python_tasks), 1)
        
        # 3. Get tasks by category
        study_tasks = self.manager.get_tasks_by_category("Study")
        self.assertEqual(len(study_tasks), 1)
        
        # 4. Complete task
        self.manager.complete_task(tasks[0].id)
        completed_tasks = self.manager.get_tasks_by_status(TaskStatus.COMPLETED)
        self.assertEqual(len(completed_tasks), 1)
        
        # 5. Get statistics
        stats = self.manager.get_statistics()
        self.assertEqual(stats['Total Tasks'], 3)
        self.assertEqual(stats['Completed'], 1)
        self.assertEqual(stats['Pending'], 2)
        
        # 6. Data persistence
        self.manager.save_tasks()
        
        # 7. Reload and verify
        new_manager = TaskManager(self.temp_file.name)
        self.assertEqual(len(new_manager), 3)
        
        # Verify completion status is maintained
        reloaded_completed = new_manager.get_tasks_by_status(TaskStatus.COMPLETED)
        self.assertEqual(len(reloaded_completed), 1)


def run_tests():
    """Run all tests"""
    print("🧪 Starting SmartTodo test suite...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestTask,
        TestUrgentTask,
        TestRecurringTask,
        TestTaskManager,
        TestUtils,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Output results
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
    
    print(f"📊 Test statistics: Ran {result.testsRun} tests")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests() 