package yongyong.graduate.hotDomain;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HotRepository extends MongoRepository<Hot, String> {
    List<Hot> findAll();

    List<Hot> findAllBy_id(String word);

//    List<Hot> findBy_idStartingWith(String date);
}