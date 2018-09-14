package name.ichimonji10.average_temperature;

import java.io.IOException;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

/** Tests for {@link CSVParser}. */
class CSVParserTest {

    /** Test {@link CSVParser#map} with header data. */
    @Test
    void testMapWithHeader() throws IOException, InterruptedException {
        final LongWritable offset = new LongWritable(0);
        final Text row = new Text(new String(
            "\"TOA5\",\"CR1000\",\"CR1000\",\"10113\",\"CR1000.Std.13\",\"CPU:combined_cr1000_17Dec2008.CR1\",\"8735\",\"Table1\""
        ));
        final Mapper.Context context = Mockito.mock(Mapper.Context.class);
        new CSVParser().map(offset, row, context);
        // The goal is to verify that write() isn't called. This assertion is
        // overly aggressive, and can fail valid code. Something like
        // MockingDetails.getInvocations would probably be better.
        Mockito.verifyZeroInteractions(context);
    }

    /** Test {@link CSVParser#map} with measurement data. */
    @Test
    void testMapWithMeasurements() throws IOException, InterruptedException {
        final LongWritable offset = new LongWritable(0);
        final Text row = new Text(new String(
            "\"2013-01-02 00:00:00\",424706,3.651,0,0.984,2.099,1.092,187.4,23.91,23.42,23.69,97.8,97.3,0,1002,1001,1002,0.341,0,0.119,1.365,1.365,1.365,0.205,0,0.107,2.154,1.641,1.853,-5.749,267.4,-1.024,-1.365,-1.246,-1.539,-2.052,-1.746,\"INF\",4,\"NAN\",0.546,0,0.226,3.52,3.007,3.218,-2.563,-3.417,-2.992,290.5,289.8,290.1,292.3,291.5,291.9,23.32,22.85,23.09,23.91,18.2,23.59"
        ));
        final Mapper.Context context = Mockito.mock(Mapper.Context.class);
        new CSVParser().map(offset, row, context);
        Mockito.verify(context).write(
            new Text(new String("2013-01")),
            new FloatWritable(new Float(23.69))
        );
    }
}
