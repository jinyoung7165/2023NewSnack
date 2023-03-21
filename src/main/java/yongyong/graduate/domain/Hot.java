package yongyong.graduate.domain;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Field;
import yongyong.graduate.common.annotation.TodayHot;

import java.util.List;

@Data
@TodayHot
@AllArgsConstructor
public class Hot {
    @Id
    @Field("_id")
    private String _id;

    @Field("word")
    private String word;

    @Field("weight")
    private double weight;

    @DBRef
    @Field("doc")
    private List<Doc> doc;
}