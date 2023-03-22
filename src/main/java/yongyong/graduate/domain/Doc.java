package yongyong.graduate.domain;

import lombok.*;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Field;
import yongyong.graduate.common.annotation.TodayDoc;

import java.util.List;

@Data
@TodayDoc
@AllArgsConstructor
public class Doc {
    @Id
    @Field("_id")
    private ObjectId _id;

    private String title;
    private String press;
    private String image;
    private String summary;
    @Indexed
    private List<String> keyword;
    private String date;
    private String link;
}
