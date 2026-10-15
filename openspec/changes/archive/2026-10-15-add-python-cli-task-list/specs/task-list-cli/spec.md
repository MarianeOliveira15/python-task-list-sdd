# Spec Delta

## Purpose

Esta capability permite gerenciar tarefas pessoais por uma interface de linha de comando em Python, mantendo a lista local disponível entre diferentes execuções.

## ADDED Requirements

### Requirement: Add a task
The CLI SHALL create and persist a new task with a unique identifier and an incomplete status when given a non-empty description.

#### Scenario: Adding a task
- **WHEN** the user adds a task with a non-empty description
- **THEN** the CLI creates an incomplete task, assigns it a unique identifier, persists it, and reports that identifier

#### Scenario: Adding an empty task
- **WHEN** the user adds a description containing only whitespace
- **THEN** the CLI reports an input error and does not create a task

### Requirement: List tasks
The CLI SHALL display each stored task's identifier, description, and completion status.

#### Scenario: Listing existing tasks
- **WHEN** the user lists tasks and tasks exist
- **THEN** the CLI displays every task with its identifier, description, and whether it is incomplete or complete

#### Scenario: Listing an empty list
- **WHEN** the user lists tasks and no tasks exist
- **THEN** the CLI reports that there are no tasks

### Requirement: Portuguese user-facing messages
The CLI SHALL present its user-facing messages in Portuguese, including success and error messages and command help.

#### Scenario: Displaying command feedback
- **WHEN** the CLI displays help, success feedback, or an error
- **THEN** the CLI-generated message is in Portuguese

### Requirement: Complete a task
The CLI SHALL mark a task complete when the user supplies an identifier or a prefix that matches exactly one task.

#### Scenario: Completing a task by identifier prefix
- **WHEN** the user completes a task using its full identifier or a prefix that matches exactly one task
- **THEN** the task is marked complete, the change is persisted, and the CLI confirms completion

#### Scenario: Completing a task with an unknown prefix
- **WHEN** the user attempts to complete a task using a prefix that matches no task
- **THEN** the CLI reports in Portuguese that no task matches and leaves the stored tasks unchanged

#### Scenario: Completing a task with an ambiguous prefix
- **WHEN** the user attempts to complete a task using a prefix that matches more than one task
- **THEN** the CLI reports in Portuguese that the prefix is ambiguous and leaves the stored tasks unchanged

### Requirement: Persist tasks locally
The CLI SHALL retain task descriptions, identifiers, and completion statuses in local JSON storage across separate invocations.

#### Scenario: Reloading persisted tasks
- **WHEN** the CLI starts after tasks have been saved by a previous invocation
- **THEN** those tasks are available with their previously saved descriptions and completion statuses
