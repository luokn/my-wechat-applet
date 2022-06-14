FROM python:3.9

COPY . /opt/my-wechat-applet

WORKDIR /opt/my-wechat-applet

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8086","--workers", "4"]
