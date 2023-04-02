package bmstu.lab;

import bmstu.lab.Controllers.GrammarController;
import bmstu.lab.Entities.Grammar;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.springframework.boot.test.context.SpringBootTest;
import static org.assertj.core.api.Assertions.assertThat;


@Slf4j
@SpringBootTest
@RunWith(value = Parameterized.class)
class LabApplicationTests {
    @ParameterizedTest
    @CsvSource(value = {"src/main/resources/test.json,src/main/resources/test_res.json",
                        "src/main/resources/test1.json,src/main/resources/test_res1.json"},
            delimiter = ',')
    public void wholeProcess_ok(String testFilename, String exceptFilename) {
        Grammar grammarResult = GrammarController.process(testFilename);
        Grammar grammarExcept = null;

        try {
            grammarExcept = GrammarController.readGrammarFromFile(exceptFilename);
        } catch (Exception e) {
            log.error("Error: {}", e.getMessage());
        }

        assertThat(grammarExcept.isEqual(grammarResult)).isTrue();
    }

    @ParameterizedTest
    @CsvSource(value = {"src/main/resources/test2.json,src/main/resources/test_res2.json"},
            delimiter = ',')
    public void partProcessWithoutRecursion_ok(String testFilename, String exceptFilename) {
        Grammar grammarResult = GrammarController.processWithoutLeftRecursion(testFilename);
        Grammar grammarExcept = null;

        try {
            grammarExcept = GrammarController.readGrammarFromFile(exceptFilename);
        } catch (Exception e) {
            log.error("Error: {}", e.getMessage());
        }

        assertThat(grammarExcept.isEqual(grammarResult)).isTrue();
    }
}
