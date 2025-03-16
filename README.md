# Django Projects Portfolio

A modern Django application for showcasing your development projects. Built with Django 5.1 and styled with Tailwind CSS, this application provides a clean and responsive interface to display your portfolio of projects.

At this time it is not complete, and it is not easily customizable, this will be
fixed very shortly.

## Features

- 🚀 Built with Django 5.1
- 💅 Modern UI with Tailwind CSS. We use `django-tailwind-cli` to make the
  integration easier
- 🧩 Component-based templates using `django-cotton` and `django-shadcn`
- 👤 Custom user authentication system
- 📝 Contact form with Google reCAPTCHA v2 integration for spam protection
- 🔒 Environment-based configuration
- 🛠️ Modern development tools integration (`pre-commit`, `ruff`, `mypy`)
- 📱 Fully responsive design
- 🔄 Live browser reload during development

## Requirements

- Python 3.10+
- Django 5.1+
- Node.js (for Tailwind CSS)

## Installation

### Using uv (Recommended)

1. Clone the repository:

```console
git clone https://github.com/seapagan/django-projects
cd django-projects
```

2. Install dependencies using uv:

```console
uv venv
uv sync --no-dev
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```

### Using Traditional pip/venv

1. Clone the repository:

```console
git clone https://github.com/seapagan/django-projects
cd django-projects
```

2. Create and activate a virtual environment:

```console
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:

```console
pip install -r requirements.txt
```

## Configuration

The application uses environment variables for configuration. Key settings:

- `DJANGO_SECRET_KEY`: Your Django secret key
- `DJANGO_DEBUG`: Set to 1 for development, 0 for production
- `RECAPTCHA_SITE_KEY`: Your Google reCAPTCHA v2 site key
- `RECAPTCHA_SECRET_KEY`: Your Google reCAPTCHA v2 secret key

Create an `.env` file in the project root with the following content, or set the
environment variables directly:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=1 # sets debug mode
RECAPTCHA_SITE_KEY=your-recaptcha-site-key
RECAPTCHA_SECRET_KEY=your-recaptcha-secret-key
```

To get your reCAPTCHA keys (required for the contact form functionality):

1. Visit the [Google reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin)
2. Sign in with your Google account
3. Click the "+" button to create a new site
4. Choose "reCAPTCHA v2" and "I'm not a robot" Checkbox
5. Add your domain(s) to the list (you can use '127.0.0.1' for local testing, be
   sure to add the correct domain when you deploy)
6. Copy the "Site Key" to `RECAPTCHA_SITE_KEY` and "Secret Key" to `RECAPTCHA_SECRET_KEY`

> [!NOTE]
>
> For a Production or User-Facing project, **ALWAYS set `DJANGO_DEBUG=0`**

## Usage

1. Apply database migrations:

```console
python manage.py migrate
```

2. Create a superuser:

```console
python manage.py createsuperuser
```

3. Run the development server:

```console
python manage.py tailwind runserver
```

4. Visit <http://localhost:8000/admin> to add your projects
5. View your portfolio at <http://localhost:8000>

## Adding Projects via Admin Interface

After logging in to the admin interface at <http://localhost:8000/admin>, you can add new projects by clicking on the "Projects" link. Each project has the following fields:

- **Title**: The name of your project (maximum 100 characters)
- **Details**: A detailed description of your project. This field supports multiple paragraphs and can be left blank if needed
- **Repository URL**: The URL to your project's source code repository (optional)
- **Website URL**: The URL to your project's live website or demo (optional)

Projects will be displayed on your portfolio page in the order they were added,
oldest to newest. Shortly we will add a priority order too so some projects can
be bumped to the top.

## Project Structure

```
├── app/                    # Main application code
├── assets/                 # Static assets
│   └── css/               # CSS files
├── config/                # Project configuration
├── templates/             # HTML templates
│   ├── app/              # Application templates
│   └── cotton/           # Component templates
└── manage.py             # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

This project uses several development tools to maintain code quality:

- `pre-commit` hooks for code formatting and linting
- `ruff` for Python linting
- `mypy` for type-checking
- `django-browser-reload` for live development
- `django-stubs` for improved type checking

Install development dependencies and set up pre-commit:

Using uv (Recommended):

```console
uv sync
pre-commit install
```

Using pip:

```console
pip install -r requirements-dev.txt
pre-commit install
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
