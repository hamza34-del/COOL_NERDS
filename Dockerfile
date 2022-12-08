FROM python:3.7

COPY un-ner.model/ /un-ner.model/
COPY ["*.py", "requirements.txt", "./"]
RUN apt-get -y   --no-install-recommends install curl && \
	rm -rf /var/lib/apt/lists/* 

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install transformers
RUN pip install torch  && rm -rf /root/.cache/pip

CMD ["python3","lmr_model.py"]



