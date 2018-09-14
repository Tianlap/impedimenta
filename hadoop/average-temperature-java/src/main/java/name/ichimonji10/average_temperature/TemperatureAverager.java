package name.ichimonji10.average_temperature;

import java.io.IOException;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * Average temperature readings by month.
 */
public class TemperatureAverager
extends Reducer<Text, FloatWritable, Text, FloatWritable> {

    /**
     * Average the measurements for a given year-month.
     *
     * @param key A string in the format "YYYYMM".
     * @param values Temperature measurements for that year-month.
     * @param context The object to which the reduced value is written.
     */
    public final void reduce(
        final Text key,
        final Iterable<FloatWritable> values,
        final Context context)
    throws IOException, InterruptedException {
        float sumMeasurements = 0;
        int numMeasurements = 0;
        for (FloatWritable measurement: values) {
            sumMeasurements += measurement.get();
            numMeasurements += 1;
        }
        final FloatWritable avg = new FloatWritable(new Float(
            sumMeasurements / numMeasurements
        ));
        context.write(key, avg);
    }
}
