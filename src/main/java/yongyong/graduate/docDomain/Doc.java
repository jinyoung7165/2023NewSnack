package yongyong.graduate.docDomain;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Field;
import yongyong.graduate.common.annotation.TodayDoc;

import java.util.List;

@Data
@TodayDoc
@AllArgsConstructor
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
    private List<String> keyword;
    private String date;
    private String link;
}
