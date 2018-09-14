package name.ichimonji10.average_temperature;

import java.io.IOException;
import java.util.Arrays;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

/**
 * Tests for {@link TemperatureAverager}.
 */
class TemperatureAveragerTest {

    /** Test {@link TemperatureAverager#reduce}. */
    @Test
    void testReduce() throws IOException, InterruptedException {
        final Text key = new Text(new String("foo"));
        final Iterable<FloatWritable> values = Arrays.asList(
            new FloatWritable(new Float(1.2)),
            new FloatWritable(new Float(3.4))
        );
        final Reducer.Context context = Mockito.mock(Reducer.Context.class);
        final TemperatureAverager temperatureAverager = new TemperatureAverager();
        temperatureAverager.reduce(key, values, context);
        Mockito.verify(context).write(
            new Text(new String("foo")),
            new FloatWritable((new Float(1.2) + new Float(3.4)) / 2)
        );
    }
}
