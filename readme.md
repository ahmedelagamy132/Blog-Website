# Flask Blog Application

## Overview

This is a Flask-based blog application that features user profiles, post management, and various analytics. The application is designed to allow users to create, read, update, and delete posts, view user profiles, and access statistical insights about the blog's content and users.

## Features

- **User Management**: Register, log in, and manage user profiles.
- **Post Management**: Create, view, edit, and delete posts.
- **Profile Management**: Upload and display profile pictures, update user details.
- **Statistics**: View post statistics and gender distribution.
- **APIs**: Average age of users, text summarization, and keyword extraction.

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MySQL
- **APIs**: Transformers for text summarization, NLTK for keyword extraction
- **Deployment**: Docker, Docker Compose
- **Version Control**: Git

## Time Allocation

| Task               | Time Spent    |
|--------------------|---------------|
| Research           | 10 hours       |
| Development        | 40 hours       |
| Testing            | 15 hours       |
| Deployment         | 10 hours       |

- **Research**: Included evaluating technologies, libraries, and frameworks, and reviewing best practices for Flask and Docker.
- **Development**: Coding the Flask application, creating routes, templates, and integrating external libraries.
- **Testing**: Debugging issues, writing unit tests, and verifying functionality.
- **Deployment**: Setting up Docker and Docker Compose, and configuring deployment environments.

## Methodology

### Development Methodology

The development process followed an iterative approach with the following stages:

1. **Requirement Gathering**: Identified core features and functionality required for the blog application.
2. **Technology Selection**: Chose Flask as the web framework due to its flexibility and ease of use. SQLAlchemy was selected for ORM and MySQL for the database due to its robustness.
3. **Design**: Designed the application architecture, including database schema and application structure.
4. **Implementation**: Developed the application in stages, including user authentication, post management, and profile management. Integrated third-party libraries for APIs.
5. **Testing**: Conducted thorough testing to ensure functionality and fix any issues.
6. **Deployment**: Dockerized the application for consistent deployment across environments and used Docker Compose to manage multi-container setups.

### Selection Criteria for Technologies, Libraries, and Frameworks

- **Flask**: Lightweight and flexible, suitable for building web applications with minimal boilerplate.
- **SQLAlchemy**: Provides a high-level ORM for managing database interactions.
- **MySQL**: Reliable and widely used database management system.
- **Transformers**: Advanced NLP library for summarization tasks.
- **NLTK**: Useful for text processing and keyword extraction.
- **Docker**: Ensures consistent development and production environments.
- **Bootstrap**: Provides a responsive and visually appealing frontend framework.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
