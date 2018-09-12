SHELL := /bin/bash
JAR = target/mozilla-pipeline-schemas-1.0-SNAPSHOT.jar
CIRCLE_TAG ?= 1.0-SNAPSHOT
NEW_VERSION = $(CIRCLE_TAG:v%=%)

.PHONY: jar
jar: $(JAR)

.PHONY: src/main/resources
src/main/resources:
	rm -rf $@
	mkdir -p $@
	cp -r ../schemas $@/

$(JAR): src/main/resources
	mvn clean package

.PHONY: deploy
deploy: src/main/resources
	mvn versions:set -DnewVersion=$(NEW_VERSION)
	mvn clean deploy
