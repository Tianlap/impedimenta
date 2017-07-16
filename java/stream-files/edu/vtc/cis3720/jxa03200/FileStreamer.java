// Author: Jeremy Audet
package edu.vtc.cis3720.jxa03200;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** Tools for finding and reading files. */
public class FileStreamer {
    /**
     * Recursively find and return files.
     *
     * If {@code top} is a directory, recursively find all readable files
     * contained therein and return them. If top is a file, return either a
     * stream consisting of a single file or an empty stream, depending on
     * whether {@code top} is readable.
     *
     * {@code getFiles(new File("/"))} returns every readable file on the
     * filesystem.
     *
     * @param top A directory or file to search through.
     * @return A stream of files.
     */
    public static Stream<File> getFiles(File top) {
        if(top.isDirectory()) {
            return Stream.of(top.listFiles()).flatMap(file -> getFiles(file));
        }
        if(top.canRead()) {
            return Stream.of(top);
        }
        return Stream.empty();
    }

    /**
     * Return every word in the given file.
     *
     * Split the contents of {@code file} on whitespace, discard whitespace, and
     * return the remaining words. Beware that this method reads the entire
     * {@code file} in to memory before parsing it. It is inadvisable to call
     * this method on files close to or larger than available system memory.
     *
     * @param file A file to extract words from. Must be textual.
     * @return A stream of words.
     * @throws FileNotFoundException If the named file does not exist, is a
     * directory rather than a regular file, or for some other reason cannot be
     * opened for reading.
     * @throws IOException If an I/O error occurs.
     */
    public static Stream<String> getWords(File file)
    throws FileNotFoundException, IOException {
        String text = "";
        try(FileReader fileReader = new FileReader(file)) {
            try(BufferedReader bufferedReader = new BufferedReader(fileReader)) {
                int codePoint = bufferedReader.read();
                while(codePoint != -1) {
                    text += String.valueOf((char) codePoint);
                    codePoint = bufferedReader.read();
                }
            }
        }
        return getWords(text);
    }

    /**
     * Return every word in the given string.
     *
     * Split the string on whitespace, discard whitespace, and return the
     * remaining words.
     *
     * @param text A string to extract words from.
     * @return A stream of words.
     */
    public static Stream<String> getWords(String text) {
        return Stream.of(text.split("\\s+")).filter(s -> !s.equals(""));
    }
}
