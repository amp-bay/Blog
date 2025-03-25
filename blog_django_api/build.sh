

set -o errexit

# Install dependencies using pipenv
pipenv install --deploy --ignore-pipfile

# Run commands within the pipenv environment
pipenv run python manage.py collectstatic --noinput
pipenv run python manage.py migrate

echo "Build script executed successfully."

