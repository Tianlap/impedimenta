# Author: Jeremy Audet
#
# The `lib` directory must either contain or link to:
#
# * junit.jar, from org.junit
# * hamcrest-core.jar, from org.hamcrest
CLASSPATH:="lib/*:$$CLASSPATH"

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  help"
	@echo "    to show this message"
	@echo "  compile"
	@echo "    to compile all code (not necessary except for development)"
	@echo "  docs"
	@echo "    to compile API documentation"
	@echo "  test"
	@echo "    to execute unit tests"
	@echo "  run-parallel"
	@echo "    to execute the Parallel class"
	@echo "  run-serial"
	@echo "    to execute the Serial class"

compile: edu/vtc/cis3720/jxa03200/TestFileStreamer.class \
		edu/vtc/cis3720/jxa03200/Parallel.class \
		edu/vtc/cis3720/jxa03200/Serial.class

docs:
	CLASSPATH=$(CLASSPATH) javadoc edu.vtc.cis3720.jxa03200 -d docs

test: edu/vtc/cis3720/jxa03200/TestFileStreamer.class
	CLASSPATH=$(CLASSPATH) java org.junit.runner.JUnitCore edu.vtc.cis3720.jxa03200.TestFileStreamer

run-parallel: edu/vtc/cis3720/jxa03200/Parallel.class
	CLASSPATH=$(CLASSPATH) java edu.vtc.cis3720.jxa03200.Parallel

run-serial: edu/vtc/cis3720/jxa03200/Serial.class
	CLASSPATH=$(CLASSPATH) java edu.vtc.cis3720.jxa03200.Serial

edu/vtc/cis3720/jxa03200/Parallel.class: edu/vtc/cis3720/jxa03200/FileStreamer.class

edu/vtc/cis3720/jxa03200/Serial.class: edu/vtc/cis3720/jxa03200/FileStreamer.class

edu/vtc/cis3720/jxa03200/TestFileStreamer.class: edu/vtc/cis3720/jxa03200/FileStreamer.class

%.class: %.java
	CLASSPATH=$(CLASSPATH) javac -Xlint $<

.PHONY: help compile test
