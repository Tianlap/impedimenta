run: measurements.txt
	./average-temperatures.awk $<

measurements.txt: measurements.zip
	unzip -p $< 20130101-20160531.txt > $@

measurements.zip:
	wget -O $@ http://www.pchapin.org/VTC/cis-4250/20130101-20160531.zip

.PHONY: run
