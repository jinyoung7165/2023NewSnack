package yongyong.graduate.docDomain;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public abstract class DocRepositoryImpl implements DocRepository{
    @Autowired
    private MongoOperations mongoOperations;

    @Override
    public List<Doc> findAllByDoc(String docName) {
        return mongoOperations.findAll(Doc.class, docName);
    }
}
