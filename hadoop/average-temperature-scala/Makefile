# It would be nice to implement this functionality with SBT instead of make.

# If any prerequisites are newer than the target, make rebuilds the target. This
# is problematic when unpacking an archive, as an archive file will always be
# newer than its contents. We use order-only prerequisites to work around this.
# See: https://www.gnu.org/software/make/manual/make.html#Prerequisite-Types

data: data/measurements.txt data/hadoop-3.1.1

data/measurements.txt:
	scripts/install-measurements-txt.sh

data/hadoop-3.1.1:
	scripts/install-hadoop.sh
