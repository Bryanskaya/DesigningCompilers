package com.bmstu.lab;

import com.bmstu.lab.model.CParser;
import com.bmstu.lab.model.Parser;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;


class LabApplicationTests {
	private final Parser parser = new Parser();
	private final CParser cParser = new CParser();

	@Test
	void checkEval() {
		assertThat(parser.eval("C")).isTrue();
		assertThat(parser.eval("i")).isTrue();

		assertThat(parser.eval("CC")).isFalse();
		assertThat(parser.eval("abcde")).isFalse();

		assertThat(parser.eval("(i)")).isTrue();
		assertThat(parser.eval("(C-C+i)")).isTrue();
		assertThat(parser.eval("(C-C+i)*C")).isTrue();
		assertThat(parser.eval("C+C")).isTrue();
		assertThat(parser.eval("(C*C)")).isTrue();
		assertThat(parser.eval("C+(C+i)*(C*C)")).isTrue();

		assertThat(parser.eval("C+(C+i*(C*C)")).isFalse();
		assertThat(parser.eval("C+(C+i*(C*C))")).isTrue();

		assertThat(parser.eval("C<=C")).isTrue();
		assertThat(parser.eval("C>C")).isTrue();
		assertThat(parser.eval("C=(C+i*(C*C))")).isTrue();
	}

	@Test
	void checkRun() {
		assertThat(cParser.eval("C")).isFalse();
		assertThat(cParser.eval(
				"{" +
				"C" +
				"}"
		)).isFalse();

		assertThat(cParser.eval(
				"{" +
						"C=i" +
					"}"
		)).isFalse();

		assertThat(cParser.eval(
				"{" +
						"i=C" +
					"}"
		)).isTrue();

		assertThat(cParser.eval(
				"{" +
						"i=C;" +
						"i=C/i;" +
						"i=i>=i*i*(C+i)" +
					"}"
		)).isTrue();
	}

}
