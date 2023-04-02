package bmstu.lab.Entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Setter;
import lombok.experimental.Accessors;


@Accessors(chain = true)
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class Symbol {
    @JsonProperty("-type")
    public String type;

    @JsonProperty("-spell")
    public String spell;

    @JsonProperty("-name")
    public String name;
}
