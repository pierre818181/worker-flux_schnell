FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu22.04

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /

# Install Python dependencies (Worker Template)
COPY builder/requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt && \
    pip install huggingface_hub[hf_transfer] && \
    rm /requirements.txt
ENV HF_HUB_ENABLE_HF_TRANSFER="1"
# Fetch the model
COPY builder/model_fetcher.py /model_fetcher.py
RUN python /model_fetcher.py
RUN rm /model_fetcher.py

# Add src files (Worker Template)
ADD src .

CMD [ "python", "-u", "/rp_handler.py" ]
