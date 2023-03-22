package yongyong.graduate.domain;

import lombok.*;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Field;
import yongyong.graduate.common.annotation.TodayHot;

import java.util.List;

@Data
@TodayHot
@AllArgsConstructor
public class Hot {
    @Id
    @Field("_id")
    private ObjectId _id;

    @Field("word")
    private String word;

    @Field("weight")
    private double weight;

    @Field("doc")
    private List<DBRef> doc;
}