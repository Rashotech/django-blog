## Installation
1. Clone the repository:
```
git clone https://github.com/Rashotech/django-blog.git
```
2. Navigate to the project directory:
```
cd `django-blog`
```
3. Create and activate a new virtual environment:
```
python -m venv env
source env/bin/activate
```
4. Install the project dependencies:
```
pip install -r requirements.txt
```
5. Run the Tailwind CSS configuration command:
```python
python manage.py tailwind init
```
6. Create the database tables:
```python
python manage.py migrate
```
7. Run the development server:
```python
python manage.py runserver
```
8. Run test:
```python
python manage.py test
```

## Technologies used
1. HTML
2. CSS
3. JavaScript
4. Python

### Primary Modules used
1. Django==5.0.7
2. django-tailwind==3.8.0
3. Jinja2==3.1.4

## Pages
- `Home`: The landing page of the website, which displays latest blog posts with pagination and links to individual post pages and links to other pages.
- `Search Blog Post`: A page that shows search result of blog posts.
- `Author Blog Post`: A page that shows list of blog posts published by an author.
- `Category Blog Post`: A page that shows list of blog posts that belongs to a category.
- `Blog Post`: A page that displays the content of a single blog post, including the title, author, date, content, and comments.
- `New Post`: A page that accessible to logged in authors where they can publish new blog post.
- `Edit Post`: A page where authors can edit their blog posts.
- `Profile`: A page that displays a user's blog posts and allowing editing of profile information.
- `Register`: A page that where user can register
- `Login`: A page that where user can login