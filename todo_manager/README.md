# 🗂️ SmartTodo - Intelligent Task Manager

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A feature-rich, easy-to-use Python command-line task management tool that helps you efficiently manage daily tasks.

## ✨ Features

### 🎯 Core Functionality
- **Task Management**: Add, delete, complete, search tasks
- **Task Categories**: Support custom categories and category-based viewing
- **Priority Management**: Three-level priority (High, Medium, Low)
- **Due Dates**: Support multiple date formats and smart reminders
- **Overdue Detection**: Automatically identify and highlight overdue tasks

### 🚀 Advanced Features
- **Multiple Task Types**:
  - Normal Tasks
  - Urgent Tasks (automatically high priority)
  - Recurring Tasks (support custom repeat intervals)
- **Smart Sorting**: Sort by priority, due date
- **Data Persistence**: JSON format local storage
- **Statistical Analysis**: Completion rate, category statistics, etc.
- **Data Backup**: Support manual backup and recovery

### 💡 Technical Highlights
- **Object-Oriented Design**: Clear class hierarchy
- **Type Hints**: Complete Python type annotations
- **Exception Handling**: Robust error handling mechanism
- **Unit Testing**: Complete test coverage
- **Code Standards**: Follow PEP8 standards

## 📋 Project Structure

```
todo_manager/
├── main.py              # Main program entry
├── task.py              # Task class definitions
├── manager.py           # Task manager
├── utils.py             # Utility functions
├── test_todo.py         # Test suite
├── demo.py              # Demo script
├── data/                # Data storage directory
│   └── tasks.json       # Task data file
└── README.md            # Project documentation
```

## 🚀 Quick Start

### Requirements
- Python 3.8+
- No additional dependencies (uses standard library only)

### Installation and Running

1. **Download Project**
```bash
# Download project files to local directory
cd your_project_directory
```

2. **Run Program**
```bash
python main.py
```

3. **Run Tests**
```bash
python test_todo.py
```

4. **Run Demo**
```bash
python demo.py
```

## 📖 User Guide

### Basic Operations

#### Adding Tasks
Support three task types:
- **Normal Tasks**: Basic todo items
- **Urgent Tasks**: Automatically set to high priority
- **Recurring Tasks**: Auto-generate next task after completion

#### Date Format Support
- Standard formats: `2024-05-25`, `2024-05-25 14:30`
- Relative dates: `today`, `tomorrow`, `day after tomorrow`
- Relative time: `+3days`, `+1week`

#### Priority Setting
- **High**: Urgent important tasks
- **Medium**: General tasks (default)
- **Low**: Non-urgent tasks

### Advanced Features

#### Task Search
Support fuzzy search of titles, descriptions, categories

#### Task Filtering
- Filter by status (pending, completed)
- Filter by category
- View overdue tasks
- View today's tasks

#### Data Management
- Auto-save
- Manual backup
- Clear completed tasks
- Export task reports

## 🎨 Interface Preview

```
╔══════════════════════════════════════════════════════════════╗
║                   🗂️  SmartTodo Manager                      ║
║                   Make your task management smarter          ║
╚══════════════════════════════════════════════════════════════╝

============================================================
📋 Main Menu
============================================================
📝 Pending tasks: 3

Please select:
1. 📝 Add New Task
2. 📋 View Task List
3. ✅ Complete Task
4. 🗑️ Delete Task
5. 🔍 Search Tasks
6. 📊 Task Statistics
7. ⚙️ Management Functions
8. 🚪 Exit Program
```

## 🔧 Technical Implementation

### Core Class Design

#### Task Base Class
```python
class Task:
    """Task base class with basic properties and methods"""
    - Task ID, title, description
    - Priority, category, status
    - Creation time, due time
    - Serialization/deserialization methods
```

#### UrgentTask Subclass
```python
class UrgentTask(Task):
    """Urgent task, automatically high priority"""
    - Inherits all Task functionality
    - Auto-sets high priority
    - Higher priority score
```

#### RecurringTask Subclass
```python
class RecurringTask(Task):
    """Recurring task, supports cyclic repetition"""
    - Custom repeat interval
    - Auto-reset after completion
```

### Design Patterns Applied

- **Inheritance and Polymorphism**: Task class hierarchy
- **Decorator Pattern**: Log recording decorator
- **Strategy Pattern**: Multiple sorting strategies
- **Singleton Pattern**: TaskManager data management

### Python Concepts Used

- **Enums**: Priority and TaskStatus
- **Property Decorators**: Read-only properties and computed properties
- **Magic Methods**: `__str__`, `__len__`, `__contains__`, etc.
- **Type Hints**: Complete type annotations
- **Exception Handling**: Robust error handling
- **Context Management**: File operations
- **List Comprehensions**: Data filtering and processing

## 🧪 Test Coverage

Project includes complete unit tests and integration tests:

- **Task Class Tests**: Task creation, completion, serialization
- **TaskManager Tests**: CRUD operations, search, statistics
- **Utility Function Tests**: Date parsing, formatting, etc.
- **Integration Tests**: Complete workflow verification

Run tests:
```bash
python test_todo.py
```

## 📊 Project Statistics

- **Lines of Code**: ~1000 lines
- **Number of Classes**: 8 main classes
- **Number of Functions**: 50+ functions
- **Test Cases**: 30+ tests
- **Python Concepts**: Covers 20+ advanced concepts

## 🎯 Learning Value

This project is suitable for the following learning objectives:

### 🏗️ Software Engineering
- Project structure design
- Modular development
- Code organization and architecture

### 🐍 Python Advanced
- Object-oriented programming
- Inheritance and polymorphism
- Decorators and magic methods
- Type hints and documentation

### 🔧 Practical Skills
- File I/O operations
- JSON data processing
- Exception handling
- Unit testing

### 💡 Design Thinking
- User experience design
- Error handling strategies
- Data structure selection
- Algorithm optimization

## 🚀 Extension Suggestions

Project can be further extended:

1. **GUI Interface**: Using tkinter or PyQt
2. **Web Interface**: Using Flask or Django
3. **Database Support**: SQLite or PostgreSQL
4. **Sync Functionality**: Cloud synchronization
5. **Reminder Features**: System notifications
6. **Team Collaboration**: Multi-user support

## 📄 License

MIT License - See LICENSE file for details

## 👥 Contributing

Issues and Pull Requests are welcome!

## 📞 Contact

For questions or suggestions, please contact the project maintainer.

---

**🎓 COMP9001 Final Project**  
*Demonstrating Python programming skills and software development best practices* 