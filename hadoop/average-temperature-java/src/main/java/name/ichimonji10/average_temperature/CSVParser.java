package name.ichimonji10.average_temperature;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Pattern;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

/**
 * Extract timestamps and temperatures from lines in an input CSV file.
 */
public class CSVParser
extends Mapper<LongWritable, Text, Text, FloatWritable> {

    /**
     * The regular expression used to split input lines.
     *
     * Instances of Pattern are immutable and thread-safe.
     */
    private static final Pattern SPLITTER = Pattern.compile(",");

    /**
     * The index of the temperature column in the input line.
     */
    private static final int TEMPERATURE = 10;

    /**
     * The index of the timestamp column in the input line.
     */
    private static final int TIMESTAMP = 0;

    /**
     * An index into the timestamp column in the input line.
     */
    private static final int TIMESTAMP_YEAR_START = 1;

    /**
     * An index into the timestamp column in the input line.
     */
    private static final int TIMESTAMP_YEAR_END = 5;

    /**
     * An index into the timestamp column in the input line.
     */
    private static final int TIMESTAMP_MONTH_START = 6;

    /**
     * An index into the timestamp column in the input line.
     */
    private static final int TIMESTAMP_MONTH_END = 8;

    /**
     * The values of the left-most columns in the header section.
     */
    private static final Set<String> HEADER_LEFT_COLUMN = new HashSet<String>(
        Arrays.asList(
            new String[]{
                "\"TIMESTAMP\"",
                "\"TOA5\"",
                "\"TS\"",
                "\"\""
            }
        )
    );

    /**
     * Extract timestamps and temperatures from lines in an input CSV file.
     *
     * Create a year-month to temperature mapping.
     *
     * @param offset The byte-wise offset into the input file.
     * @param row The input line.
     * @param context The object to which the mapping is written.
     */
    public final void map(
        final LongWritable offset,
        final Text row,
        final Context context)
    throws IOException, InterruptedException {
        final String[] fields = splitRow(row.toString());
        if (isHeaderRow(fields)) {
            return;
        }
        final Text yearMonth = new Text(getYearMonth(fields));
        final FloatWritable temp = new FloatWritable(getTemp(fields));
        context.write(yearMonth, temp);
    }

    /**
     * Split the line of input text.
     *
     * @param row A line of text from a CSV file.
     * @return The line, split on commas, without the commas.
     */
    private static String[] splitRow(final String row) {
        return SPLITTER.split(row);
    }

    /**
     * Tell whether this row is a header row.
     *
     * @param fields The fields in the current row.
     * @return True if this row is a header row, and false otherwise.
     */
    private static boolean isHeaderRow(final String[] fields) {
        return HEADER_LEFT_COLUMN.contains(fields[TIMESTAMP]);
    }

    /**
     * Get this row's year and month.
     *
     * @param fields The fields in the current row.
     * @return A string in the format {@code YYYYMM}.
     */
    private static String getYearMonth(final String[] fields) {
        final String timestamp = fields[TIMESTAMP];
        final String year = timestamp.substring(
            TIMESTAMP_YEAR_START,
            TIMESTAMP_YEAR_END
        );
        final String month = timestamp.substring(
            TIMESTAMP_MONTH_START,
            TIMESTAMP_MONTH_END
        );
        return year + "-" + month;
    }

    /**
     * Get this row's temperature.
     *
     * @param fields The fields in the current row.
     * @return The value of the {@code AirTF_Max} field.
     */
    private static Float getTemp(final String[] fields) {
        return new Float(fields[TEMPERATURE]);
    }
}
