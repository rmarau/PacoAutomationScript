#docker build -t rmarau/pacoautomationscript:latest .
#docker push rmarau/pacoautomationscript:latest

FROM selenium/standalone-firefox:4.2.2-20220622

LABEL maintainer="Ricardo Marau"

USER root

RUN apt-get -qqy update && apt-get -qqy --no-install-recommends install \
	python3-openpyxl \
	python3-selenium \
	&& apt-get -qqy clean

USER seluser

COPY . /home/seluser/.


CMD cd /home/seluser/ ; sh launchpad.sh paco-sync.sh
