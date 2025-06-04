FROM python:3.10-alpine
WORKDIR /ram-12-factor-app
COPY requirements.txt /ram-12-factor-app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /ram-12-factor-app
EXPOSE 5000
CMD ["python", "app.py"]
# This Dockerfile sets up a Python environment with the necessary dependencies for the 12-factor app.
# It uses an Alpine-based Python image for a lightweight container.
# The application listens on port 5000, which is exposed for external access.