# 🎵 TaylorSwift_Database: Relational Discography Analysis & Web App

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web_Framework-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)

## 🎯 Project Overview
This project demonstrates end-to-end database management and full-stack development skills. I designed a normalized **Relational Database** to map Taylor Swift's entire discography, connecting Songs, Albums, Lyrics, and Staff (Producers, Writers, Artists), and built a **Flask Web Application** to query, visualize, and analyze the data interactively.

The goal was to move beyond simple spreadsheets and create a structured SQL system capable of handling complex Many-to-Many relationships and advanced analytical queries.

---

## 📈 Executive Functionality Summary
The application serves as a central hub for discography analysis, moving raw data into actionable insights.

| Feature | Description | Tech Stack |
| :--- | :--- | :--- |
| **Relational Modeling** | Normalized schema (3NF) handling complex production credits. | SQL, Junction Tables |
| **Advanced Search** | Multi-faceted search for Lyrics (text parsing) and People (Role-based). | SQL `LIKE`, Dynamic Routing |
| **Data Analytics** | A Q&A engine answering complex questions (e.g., "Highest avg view per album"). | Aggregations, Subqueries |

**Key Takeaway:** The project proves the ability to integrate a backend SQL engine with a frontend interface, allowing non-technical users to perform complex database queries through a UI.

---

## 🔬 Technical Deep Dive

### 1. Database Architecture (SQLite)
I implemented a highly normalized schema to ensure data integrity and efficiency.
* **Entity Resolution:** Created a central `Pessoas` (People) table to handle individuals who hold multiple roles (e.g., Taylor Swift can be an Artist, Writer, and Producer).
* **Many-to-Many Relationships:** utilized junction tables (`Produtores`, `Escritores`, `Descricoes`) to link Songs to multiple Creators and Tags.
* **SQL Mastery:** The application relies on raw SQL execution rather than an ORM, demonstrating proficiency in:
    * `LEFT JOIN` vs `INNER JOIN` for data completeness.
    * `GROUP BY` and `HAVING` clauses for aggregated reporting.
    * Nested `SELECT` statements for statistical analysis.

### 2. Full-Stack Implementation (Python & Flask)
* **Backend:** A Flask server running inside a Jupyter environment creates dynamic endpoints.
* **Frontend:** Bootstrap 5 is injected via `render_template_string` to create a responsive, mobile-friendly interface.
* **Security:** Implemented parameterized queries (e.g., `WHERE song_title LIKE ?`) to prevent SQL Injection attacks during search operations.

---

## 📊 Visual Insights & Query Logic

| Analytics Component | Logic & Implementation |
| :--- | :--- |
| **Role-Based Search** | <img src="static/taytay.jpg" width="100" align="right"> **The Challenge:** Finding every song Ed Sheeran worked on, regardless of whether he was a writer or a singer.<br>**The Solution:** A `UNION`-style logic that queries three distinct junction tables simultaneously and aggregates the results into a tabbed interface. |
| **Statistical Q&A** | **The Challenge:** "Which album has the highest average views per song?"<br>**The Solution:** A nested subquery that first calculates the average views per album, and then filters that list against the global maximum average. |

---

## 🛠️ Installation & Usage

### 1. Prerequisites
Ensure you have Python installed. The project runs within a Jupyter Notebook for interactive demonstration.

### 2. Clone & Setup
```bash
git clone [https://github.com/pedrooamaroo/taylorswift_database.git](https://github.com/pedrooamaroo/taylorswift_database.git)
cd taylorswift_database
pip install -r requirements.txt
