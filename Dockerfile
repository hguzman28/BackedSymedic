FROM public.ecr.aws/c6v0u1o0/template_python39_jamar:latest


COPY ./requirements.txt ./requirements.txt
run pip install --upgrade pip
RUN pip install -r ./requirements.txt
COPY . ${LAMBDA_TASK_ROOT}
CMD ["main.handler"] 
