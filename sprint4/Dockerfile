FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# данные лежат в /app/data; для сохранения между запусками монтируйте том
CMD ["python", "main.py"]
