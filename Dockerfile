FROM python:3.7

COPY ["*.py", "requirements.txt", "./"]
RUN apt-get -y   --no-install-recommends install curl && \
	rm -rf /var/lib/apt/lists/* 

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install gdown && gdown --no-check-certificate \
	--folder  https://drive.google.com/drive/u/1/folders/15d_hqZKPR2Z8OIe4oIzFQpWc3xWeyl_j
RUN pip install transformers
RUN pip install torch  && rm -rf /root/.cache/pip

CMD ["python3","lmr_model.py"]



