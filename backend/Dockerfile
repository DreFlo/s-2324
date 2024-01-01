FROM python:3.10-slim

WORKDIR /app/

COPY requirements.txt ./

RUN apt-get update && apt-get install libgomp1

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 80

ENTRYPOINT [ "uvicorn" ]
CMD [ "main:app", "--host", "0.0.0.0", "--port", "80", "--reload" ]