.PHONY: all build clean shell test

IMAGE_ID = mozilla-services/mozilla-pipeline-schemas

all: build

build:
	docker build -t $(IMAGE_ID) .

clean:
	docker rmi -f $(IMAGE_ID)

shell: build
	docker run -it --rm $(IMAGE_ID) /bin/bash

test: build
	docker run -it --rm $(IMAGE_ID)
