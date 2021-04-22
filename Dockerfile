FROM python:3.9

RUN mkdir extra-test
WORKDIR ./extra-test

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get install -y wget unzip

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 90.0.4430.24
ENV CHROMEDRIVER_DIR .

RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" &&\
	unzip $CHROMEDRIVER_DIR/chromedriver* -d . && chmod +x $CHROMEDRIVER_DIR/chromedriver && apt-get install libxi6 libgconf-2-4 -y
RUN ls
RUN mkdir screens
COPY detector.py .
COPY logging_config.ini .
COPY main.py .
COPY tools.py .
COPY nux_checker.py .

CMD python main.py