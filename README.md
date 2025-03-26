# Django Projects Portfolio <!-- omit in toc -->

A modern Django application for showcasing your development projects. Built with
Django 5.1 and styled with Tailwind CSS, this application provides a clean and
responsive interface to display your portfolio of projects.

At this time it is not fully customizable, but this will be fixed very shortly.

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Using uv (Recommended)](#using-uv-recommended)
  - [Using Traditional pip/venv](#using-traditional-pipvenv)
- [Configuration](#configuration)
  - [PostgreSQL Database (Optional)](#postgresql-database-optional)
  - [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Add your Projects, Personal Details and skills](#add-your-projects-personal-details-and-skills)
  - [Adding Projects](#adding-projects)
  - [In-App Settings](#in-app-settings)
- [Caching](#caching)
- [Production Deployment](#production-deployment)
  - [Security Features](#security-features)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Development](#development)
- [License](#license)

## Features

- 🚀 Built with Django 5.1
- 💅 Modern UI with Tailwind CSS. We use `django-tailwind-cli` to make the
  integration easier. This uses the Tailwind CLI and does NOT require Node.js to
  be installed
- 🧩 Component-based templates using `django-cotton` and `django-shadcn`
- 👤 Custom Models and Admin pages to customize the settings and text
- 📝 Contact form with Google reCAPTCHA v2 integration for spam protection and
  stored in the database as well as sent by email to the site owner
- 🔒 Environment-based configuration with customization from the database
- 🛠️ Modern development tools integration (`uv`, `pre-commit`, `ruff`, `mypy`)
- 📱 Fully responsive design
- 🌓 Light/Dark mode options, with a dropdown for user preference or system
  setting.
- 💾 Optional caching using memcached for improved performance
- 🔄 Live browser reload during development
- 🔐 Enhanced security features for production deployment
- 🚀 Production-ready with gunicorn integration

## Requirements

- Python 3.10+
- Django 5.1+

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

### PostgreSQL Database (Optional)

By default, the application uses SQLite for the database. However, you can
configure it to use PostgreSQL instead by setting the following environment
variables:

- `DJANGO_USE_POSTGRES`: Set to 1 to use PostgreSQL instead of SQLite
- `DJANGO_POSTGRES_DB`: PostgreSQL database name
- `DJANGO_POSTGRES_USER`: PostgreSQL username
- `DJANGO_POSTGRES_PASSWORD`: PostgreSQL password
- `DJANGO_POSTGRES_HOST`: PostgreSQL host (default: localhost)
- `DJANGO_POSTGRES_PORT`: PostgreSQL port (default: 5432)

> [!NOTE]
>
> The PostgreSQL user and database **must already exist**, and the user needs to
> have **ownership** (or access) to that database.
>
> For SQLite, the local database file will be created when the migrations are
> run.

> [!IMPORTANT]
>
> This project uses the binary version of `psycopg` which is not compatible with
> some older systems (primarily older Macs or if using PyPy Python). If you
> encounter compatibility issues, you should remove the `psycopg[binary]`
> package and use the plain `psycopg` package instead, or compile it locally.
> For more information, see the [psycopg documentation on supported
> systems](https://www.psycopg.org/psycopg3/docs/basic/install.html#supported-systems).

### Environment Variables

The application uses environment variables for configuration. Most of them do
have a default setting that will be used if not specified.

 Key settings:

- `DJANGO_SECRET_KEY`: Your Django secret key. This MUST be set to a secure
  string.
- `DJANGO_DEBUG`: Set to 1 for development, 0 for production
- `DJANGO_SECURE_MODE`: Set to 1 to enable enhanced security features for
  production (see [Security Features](#security-features) section)
- `DJANGO_CSRF_TRUSTED_ORIGINS`: JSON array of trusted origins for CSRF
  protection, e.g. `["https://www.myserver.com"]`
- `DJANGO_ALLOWED_HOSTS`: JSON array of allowed hosts, e.g. `[".myserver.com"]`
- `DJANGO_STATIC_ROOT`: Path where static files will be collected in production
  mode
- `DJANGO_USE_CACHE`: Set to 1 to enable caching for the whole application. This
  uses `memcached` and that needs to be installed locally. Defaults to 0 (better
  for development) See the [Caching](#caching) secton below.
- `DJANGO_CACHE_TIMEOUT`: Cache expiry length, in seconds (Defaults to 600, 10
  minutes)
- `DJANGO_ADMIN_IPS_ALLOWED`: JSON array of IP addresses allowed to access the
  admin panel, e.g. `["127.0.0.1", "192.168.1.100"]`. If not set, defaults to
  `["127.0.0.1", "localhost"]`

> [!NOTE]
>
> If you do specify a value of `DJANGO_ADMIN_IPS_ALLOWED`, the defaults are
> REMOVED. Should you still want the defaults, they need to be manually added to
> the env var along with your custom addresses.

- `RECAPTCHA_SITE_KEY`: Your Google reCAPTCHA v2 site key
- `RECAPTCHA_SECRET_KEY`: Your Google reCAPTCHA v2 secret key
- `USE_LIVE_EMAIL`: Set to 1 to send actual emails, 0 or unset to output to
  console
- `EMAIL_HOST`: SMTP server host (required if USE_LIVE_EMAIL=1)
- `EMAIL_PORT`: SMTP server port (required if USE_LIVE_EMAIL=1)
- `EMAIL_HOST_USER`: SMTP username (required if USE_LIVE_EMAIL=1)
- `EMAIL_HOST_PASSWORD`: SMTP password (required if USE_LIVE_EMAIL=1)
- `EMAIL_USE_TLS`: Set to 1 to use TLS for SMTP (optional, defaults to 1)
- `DEFAULT_FROM_EMAIL`: Default sender email address (required if
  USE_LIVE_EMAIL=1)
- `CONTACT_FORM_RECIPIENT`: Email address where contact form submissions will be
  sent (required if USE_LIVE_EMAIL=1)

Create an `.env` file in the project root with the following content, or set the
environment variables directly:

```ini
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=1 # sets debug mode
DJANGO_SECURE_MODE=0 # set to 1 for production security features

# Database settings (optional - defaults to SQLite if not set)
DJANGO_USE_POSTGRES=0 # set to 1 to use PostgreSQL
DJANGO_POSTGRES_DB=mydatabase
DJANGO_POSTGRES_USER=myuser
DJANGO_POSTGRES_PASSWORD=your-postgres-password
DJANGO_POSTGRES_HOST=localhost
DJANGO_POSTGRES_PORT=5432

# Production settings (required when DJANGO_DEBUG=0)
DJANGO_CSRF_TRUSTED_ORIGINS=["https://www.myserver.com"]
DJANGO_ALLOWED_HOSTS=[".myserver.com"]
DJANGO_STATIC_ROOT="/var/www/myproject/static/"

DJANGO_USE_CACHE=0 # set to 0 for development, 1 for production when the database rarely changes
DJANGO_CACHE_TIMEOUT=3600 # defaults to 600 (10 minutes) if not set
DJANGO_ADMIN_IPS_ALLOWED=["127.0.0.1", "192.168.1.100"] # IP addresses allowed to access admin panel

RECAPTCHA_SITE_KEY=your-recaptcha-site-key
RECAPTCHA_SECRET_KEY=your-recaptcha-secret-key

# Email settings (optional - if USE_LIVE_EMAIL=0, emails will output to console only)
USE_LIVE_EMAIL=1
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-smtp-password
EMAIL_USE_TLS=1
DEFAULT_FROM_EMAIL=your-email@example.com
CONTACT_FORM_RECIPIENT=recipient@example.com
```

> [!NOTE]
>
> There is an `.example.env` file in the project root you can rename and modify
> to your own settings

To get your reCAPTCHA keys (required for the contact form functionality):

1. Visit the [Google reCAPTCHA Admin
   Console](https://www.google.com/recaptcha/admin)
2. Sign in with your Google account
3. Click the "+" button to create a new site
4. Choose "reCAPTCHA v2" and "I'm not a robot" Checkbox
5. Add your domain(s) to the list (you can use '127.0.0.1' for local testing, be
   sure to add the correct domain when you deploy)
6. Copy the "Site Key" to `RECAPTCHA_SITE_KEY` and "Secret Key" to
   `RECAPTCHA_SECRET_KEY`

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

## Add your Projects, Personal Details and skills

You can customize the portfolio with your own skills and projects through the
Django Admin interface at <http://localhost:8000/admin>

### Adding Projects

After logging in to the admin interface, you can add new projects by clicking on
the "Projects" link. Each project has the following fields:

- **Title**: The name of your project (maximum 100 characters)
- **Details**: A detailed description of your project. This field supports
  multiple paragraphs and can be left blank if needed
- **Priority**: An optional integer value that determines the display order
  (lower numbers appear first)
- **Repository URL**: The URL to your project's source code repository
  (optional)
- **Website URL**: The URL to your project's live website or demo (optional)
- **Tags**: Associate relevant tags with your project to categorize it
  (optional)

Projects are displayed on your portfolio page in the following order:

1. Projects with a `priority` value are shown first, sorted by priority (lower
   numbers appear first and duplicate priorities are sorted by their
   `created_at` date.)
2. Projects without a `priority` value are then displayed, sorted by creation
   date (oldest to newest)

You can set a project's priority in the admin interface. This allows you to
highlight your most important projects by giving them lower priority numbers.

### In-App Settings

The application provides additional configuration options through the Django
admin interface at `/admin/app/siteconfiguration/`. These settings allow you to
customize various aspects of your portfolio:

- **Site Content**
  - `owner_name`: The Owner of the site. This will be the page title and the
    text in the header of the page content (default: "The Developer")
  - `hero_title`: The main title displayed on your portfolio (default: "Full
    Stack Developer")
  - `hero_info`: Primary text content for the hero section (up to 500
    characters, no default)
  - `hero_secondary`: Secondary text content for the hero section (up to 500
    characters, no default)

- **Social Media Links**
  - `github_username`: Your GitHub username
  - `twitter_username`: Your Twitter/X username
  - `linkedin_username`: Your LinkedIn username
  - `youtube_username`: Your YouTube channel username
  - `medium_username`: Your Medium username

  Any social media usernames left blank will not be displayed on your portfolio.

- **Languages and Frameworks**

  You can manage your programming languages and frameworks through the Django
  admin interface by editing the `Site Configuration` database.

  - **Languages** : Add programming languages you work with
    - `name`: Name of the programming language (e.g., "Python", "JavaScript")

  - **Frameworks** (`/admin/app/framework/`): Add frameworks and libraries you
    work with
    - `name`: Name of the framework (e.g., "Django", "React")

  Both languages and frameworks will be displayed on your portfolio to showcase
  your technical stack. If you have none added, the whole **My SKills** section
  will not be displayed.

These settings can be modified at any time through the admin interface and
changes will be reflected immediately on your portfolio (though, see the note
below on **Caching**)

## Caching

This Django application is set up for optional caching which is disabled by
default. Generally it is not much use when you are setting up or customizing the
database since any changes will take 10 minutes to actually be visible in the
front-end. It is a bit overkill for this application but a good skill to learn.

> [!NOTE]
>
> Probably best **not** to enable this until your database is set up to your
> liking, as the default is a 10 minute cache time-out. See below how to change
> this.

I have chosen to use [memcached](https://www.memcached.org/) for this, though
you can use **Redis**, **File Caching**, **Local Memory** or any other method
that Django supports. See the [Django docs on
Caching](https://docs.djangoproject.com/en/5.1/topics/cache/) for more info.

You need to install [memcached](https://www.memcached.org/) for this to work. If
this is not installed and the cache enabled your application will crash.

See the link above for how to install for your server, under Debian/Ubuntu it is
available as a package:

```console
sudo apt install memcached
```

Finally, to enable the caching, set the below variable in your `.env` file or
environment:

```ini
DJANGO_USE_CACHE=1
```

If this variable is 0 or missing, caching will be disabled.

You can change the length of time that the database is cached by setting the
below variable:

```ini
DJANGO_CACHE_TIMEOUT=1200 # Default is 600 (10 Minutes)
```

## Production Deployment

For production deployment, it's recommended to:

1. Set `DJANGO_DEBUG=0` to disable debug mode
2. Set `DJANGO_SECURE_MODE=1` to enable security features
3. Use PostgreSQL instead of SQLite by setting `DJANGO_USE_POSTGRES=1` and
   configuring the related database settings
4. Configure the production-specific environment variables:
   - `DJANGO_CSRF_TRUSTED_ORIGINS`: Your domain(s) as a JSON array
   - `DJANGO_ALLOWED_HOSTS`: Your domain(s) as a JSON array
   - `DJANGO_STATIC_ROOT`: The path where static files will be collected

The application includes gunicorn for production deployment. A typical command
to run the application in production would be:

```console
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

For a proper production setup, you should:

1. Run gunicorn as a systemd service for automatic startup and monitoring
2. Use Nginx as a reverse proxy in front of gunicorn to handle static files,
   SSL, and more

For a detailed guide on setting up Django with Nginx and Gunicorn in production,
see: <https://realpython.com/django-nginx-gunicorn/>

You should also collect static files before deployment:

```console
python manage.py collectstatic
```

### Security Features

When `DJANGO_SECURE_MODE=1` (and `DJANGO_DEBUG=0`), the following security
features are enabled:

- HTTP Strict Transport Security (HSTS) - Initially set to 30 seconds for
  testing, with a commented option to increase to 15552000 seconds (180 days)
  once you've verified everything works correctly

> [!CAUTION]
>
> Be very careful when setting the HSTS timeout to a longer value (like 180
> days). Once set, it can be almost impossible to change later as browsers
> will remember this setting for the specified duration. However, setting a
> longer timeout is highly recommended once you've verified that HSTS is
> working correctly for your site.

- Secure cookies for CSRF and sessions
- SSL redirection
- Secure referrer policy
- Permissions policy headers that restrict potentially dangerous browser
  features
- IP-based admin access restriction - Only allows specified IP addresses to
  access the admin panel

These features follow Django security best practices and help protect your
application against common web vulnerabilities.

## Project Structure

```pre
├── app/               # Main application code
├── assets/            # Static assets
│   └── css/           # CSS files
│   └── js/            # JavaScript files
│   └── favicon.ico    # Put your favicon here or use the existing one
├── config/            # Project configuration
├── templates/         # HTML templates
│   ├── app/           # Application templates
│   └── cotton/        # Component templates
└── manage.py          # Django management script
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

This project is licensed under the MIT License - see the LICENSE file for
details.
