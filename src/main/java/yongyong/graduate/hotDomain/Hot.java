package yongyong.graduate.hotDomain;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;

@Data
@Getter
@Setter
@Document(collection = "#{T(java.time.LocalDate).now().toString()}")
@NoArgsConstructor
@AllArgsConstructor
public class Hot {
    @Id
    @Field("_id")
    private String _id;

    @Field("weight")
    private double weight;

    @Field("doc")
    private List<String> doc;
}