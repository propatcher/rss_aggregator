# 📰 FeedFlow – Personal RSS Aggregator

A clean and functional RSS feed aggregator built with FastAPI. This pet project demonstrates modern backend development with async tasks, real-time analytics, and a domain-driven architecture.

---

## ✨ Features

- **Add RSS Feeds**: Subscribe to any RSS/Atom feed and get a unified news stream  
- **Auto Sync**: Feeds are automatically parsed every hour in the background  
- **Smart Tagging**: Articles are auto-tagged from feed categories or keywords  
- **Search & Filter**: Find articles by keyword or filter by tag  
- **Read Tracking**: Mark articles as read and focus on what’s new  
- **User Accounts**: Securely manage your own feeds and articles  
- **RESTful API**: Full control via a clean, documented API  
- **Built-in Analytics**: See unread counts, tag stats, and feed activity  
- **Auto Docs**: Interactive API documentation (Swagger UI) powered by FastAPI  

---

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI  
- **Database**: PostgreSQL
- **Task Queue**: Celery  
- **Message Broker & Cache**: Redis  
- **ORM**: SQLAlchemy 2.0 (modern declarative style)  
- **Parsing**: `feedparser`  
- **Auth**: JWT (CustomAuth)  
- **Architecture**: Feature-based (each entity in its own module)  
- **Containerization**: Docker & Docker Compose 

---

## 🚀 How It Works (Simplified)

1. You **add an RSS feed**
2. The FastAPI app **validates and stores it** in the database  
3. Every hour, a **Celery worker** (via Redis) fetches new articles from all your feeds  
4. New articles are **saved with auto-generated tags** and marked as unread  
5. You **browse your unified feed** via the API:  
   - Search by keyword  
   - Filter by tag  
   - Mark as read  
6. Real-time **analytics** (unread count, top tags) are always available  

All of this happens **without email, without bloat** — just clean data and automation.
