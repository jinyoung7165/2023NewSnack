package yongyong.graduate.hotDomain;

import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface HotRepository extends MongoRepository<Hot, ObjectId> {
    List<Hot> findAll();

    List<Hot> findAllBy_id(String word);

}