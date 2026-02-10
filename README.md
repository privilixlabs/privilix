<img src="static/banner.jpg">

# Privilix

![alt text](https://img.shields.io/badge/python-3.12+-blue.svg)
![alt text](https://img.shields.io/badge/discord.py-2.6.4-7289DA.svg)
![alt text](https://img.shields.io/badge/dependency_management-Poetry-60A5FA.svg)
<br>
Handle mistakes in one tap. Ban appeals, clean logs, simple controls, and zero clutter. Privilix keeps your server running smoothly without turning moderation into a chore.

## 🛠️ Tech Stack

- **Framework**: [discord.py](https://discordpy.readthedocs.io/en/stable/)
- **Database**: [tortoise-orm](https://tortoise.github.io/) (for async ORM) with a [Neon(Postgres)](https://neon.tech) backend.
- **Database Migrations**: [aerich](https://github.com/tortoise/aerich)
- **Dependency Management**: [Poetry](https://python-poetry.org/)
- **Configuration**: [Pydantic](https://docs.pydantic.dev/) for environment variable validation.

### Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation) must be installed on your system.

### Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/privilixlabs/privilix.git
    ```

2.  **Install dependencies:**

    ```sh
    poetry install --no-root
    ```

3.  **Set up environment variables:**
    - Manually create a new file named `.env` in the root directory of the project.
    - Copy the contents from the [`.env.example`](.env.example) file and paste them into your new `.env` file.
    - Adjust the values in your `.env` file:
4.  **Start the bot:**
    ```sh
    poetry run python main.py
    ```
