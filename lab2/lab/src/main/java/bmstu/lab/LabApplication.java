package bmstu.lab;

import bmstu.lab.Controllers.GrammarController;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class LabApplication {

    public static void main(String[] args) {
        GrammarController.process("src/main/resources/test1.json");
    }

}
