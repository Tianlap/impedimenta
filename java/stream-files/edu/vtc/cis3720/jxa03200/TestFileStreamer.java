// Author: Jeremy Audet
package edu.vtc.cis3720.jxa03200;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

/** Tests for {@link FileStreamer}. */
public class TestFileStreamer {
    /** Test {@link FileStreamer#getFiles(File)}. Pass in a directory name. */
    @Test
    public void getFilesDirectory() {
        Set<File> expected = new HashSet<>();
        expected.add(new File("fixtures/README.txt"));
        expected.add(new File("fixtures/empty.txt"));
        expected.add(new File("fixtures/non-empty.txt"));
        expected.add(new File("fixtures/level-two/level-two.txt"));
        expected.add(new File("fixtures/level-two/level-three.txt"));
        expected.add(new File("fixtures/level-two/level-three/level-two.txt"));
        expected.add(new File("fixtures/level-two/level-three/level-three.txt"));
        expected.add(new File("fixtures/level-two/level-three/01.txt"));
        expected.add(new File("fixtures/level-two/level-three/02.txt"));
        expected.add(new File("fixtures/level-two/level-three/03.txt"));
        Set<File> actual = FileStreamer
            .getFiles(new File("fixtures"))
            .collect(Collectors.toSet());
        assertEquals(expected, actual);
    }

    /** Test {@link FileStreamer#getFiles(File)}. Pass in a file name. */
    @Test
    public void getFilesFile() {
        Set<File> expected = new HashSet<>();
        expected.add(new File("fixtures/level-two/level-two.txt"));
        Set<File> actual = FileStreamer
            .getFiles(new File("fixtures/level-two/level-two.txt"))
            .collect(Collectors.toSet());
        assertEquals(expected, actual);
    }

    /**
     * Test {@link FileStreamer#getWords(File)}. Pass in a non-empty file.
     *
     * @throws FileNotFoundException If the named file does not exist, is a
     * directory rather than a regular file, or for some other reason cannot be
     * opened for reading.
     * @throws IOException If an I/O error occurs.
     */
    @Test
    public void getWordsFileNonEmpty() throws FileNotFoundException, IOException {
        List<String> expected = Arrays.asList("foo", "bar", "biz", "baz");
        List<String> actual = FileStreamer
            .getWords(new File("fixtures/non-empty.txt"))
            .collect(Collectors.toList());
        assertEquals(expected, actual);
    }

    /**
     * Test {@link FileStreamer#getWords(File)}. Pass in an empty file.
     *
     * @throws FileNotFoundException If the named file does not exist, is a
     * directory rather than a regular file, or for some other reason cannot be
     * opened for reading.
     * @throws IOException If an I/O error occurs.
     */
    @Test
    public void getWordsFileEmpty() throws FileNotFoundException, IOException {
        List<String> expected = new ArrayList<>();
        List<String> actual = FileStreamer
            .getWords(new File("fixtures/empty.txt"))
            .collect(Collectors.toList());
        assertEquals(expected, actual);
    }

    /** Test {@link FileStreamer#getWords(String)}. Pass in a non-empty string. */
    @Test
    public void testGetWordsStringNonEmpty() {
        List<String> expected = Arrays.asList("foo", "bar");
        List<String> actual = FileStreamer
            .getWords("   foo  \r\n\r\n  bar   ")
            .collect(Collectors.toList());
        assertEquals(expected, actual);
    }

    /** Test {@link FileStreamer#getWords(String)}. Pass in an empty string. */
    @Test
    public void testGetWordsStringEmpty() {
        List<String> expected = new ArrayList<>();
        List<String> actual = FileStreamer
            .getWords("")
            .collect(Collectors.toList());
        assertEquals(expected, actual);
    }
}
