// Author: Jeremy Audet
package edu.vtc.cis3720.jxa03200;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

final class Parallel {

    /** Do nothing. Prevent this class from being subclassed. */
    private Parallel() { }

    public static void main(final String[] args) {
        System.out.println(FileStreamer
            .getFiles(new File("fixtures"))
            .unordered()
            .parallel()
            .flatMap((File file) -> {
                try {
                    return FileStreamer.getWords(file);
                } catch (FileNotFoundException exc) {
                    throw new RuntimeException(exc);
                } catch (IOException exc) {
                    throw new RuntimeException(exc);
                }
            })
            .count());
    }
}
