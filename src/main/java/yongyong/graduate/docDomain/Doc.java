package yongyong.graduate.docDomain;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.Dictionary;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class Doc {
    @Id
    @Field("_id")
    private String _id;

    // "2023-02-01/0"
    private String doc;
    private String title;
    private String main;
    private String press;
    private String image;
    private String summary;
    // keyword는 dictionary 타입
    private Map<String, String> keyword;
    private String date;
    private String link;
}
