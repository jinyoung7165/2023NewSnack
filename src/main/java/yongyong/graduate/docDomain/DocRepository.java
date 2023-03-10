package yongyong.graduate.docDomain;

import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface DocRepository extends MongoRepository<Doc, ObjectId> {
    List<Doc> findAllByDoc(String docName);
}