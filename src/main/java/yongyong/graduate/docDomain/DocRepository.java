package yongyong.graduate.docDomain;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

@Repository
public interface DocRepository extends MongoRepository<Doc, String> {

//    List<Doc> findAll();
//    List<Doc> findAllByDoc(String doc);
    public List<Doc> findAllByDoc(String docName);
}