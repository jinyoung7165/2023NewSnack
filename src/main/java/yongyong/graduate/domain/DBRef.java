package yongyong.graduate.domain;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.bson.types.ObjectId;

@Data
@AllArgsConstructor
public class DBRef {

    private String ref;
    private ObjectId _id;
}
