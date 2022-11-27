FROM python:3.8
WORKDIR /
COPY libs.txt .
RUN python -m pip install --upgrade pip
RUN git clone https://github.com/Skand21/SRGAN.git
RUN git clone https://github.com/jlaihong/image-super-resolution.git
RUN mv image-super-resolution/* ./
RUN pip install -r libs.txt
RUN python3 where.py
RUN python3 main.py
