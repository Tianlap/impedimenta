// Author: Jeremy Audet
package edu.vtc.cis3720.jxa03200;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

final class Serial {

    /** Do nothing. Prevent this class from being subclassed. */
    private Serial() { }

    public static void main(final String[] args) {
        System.out.println(FileStreamer
            .getFiles(new File("fixtures"))
            .unordered()
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
