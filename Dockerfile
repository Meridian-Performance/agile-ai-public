FROM agile-ai-base:latest
################################

ENV PATH /usr/local/bin:$PATH
ENV PROJECT_HOME /usr/src
ENV DISPLAY=:99

COPY agile_ai $PROJECT_HOME/agile_ai
COPY agile_ai_tests $PROJECT_HOME/agile_ai_tests
COPY Pipfile $PROJECT_HOME/Pipfile
COPY Pipfile.lock $PROJECT_HOME/Pipfile.lock
COPY .venv $PROJECT_HOME/.venv
COPY scripts $PROJECT_HOME/scripts
COPY README.md $PROJECT_HOME/README.md
COPY .git $PROJECT_HOME/.git
RUN chmod -R +x $PROJECT_HOME/agile_ai
WORKDIR $PROJECT_HOME
RUN pipenv run setup
CMD ["/bin/bash"]
