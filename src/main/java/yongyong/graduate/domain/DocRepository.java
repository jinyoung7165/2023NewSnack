package yongyong.graduate.domain;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DocRepository extends MongoRepository<Doc, String> {
}
