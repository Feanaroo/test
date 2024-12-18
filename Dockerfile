FROM python:3.9-slim
COPY requirements.txt /api_project/
COPY server.py /api_project/
COPY db.py /api_project/
COPY handler.py /api_project/
COPY tests_db.py /api_project/tests/
COPY tests_handler.py /api_project/tests/
WORKDIR "/api_project"
RUN pip install -r requirements.txt
RUN alembic init alembic
RUN pip install pymysql

CMD [ "python", "-u", "server.py" ]
