package yongyong.graduate.docDomain;

import lombok.RequiredArgsConstructor;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
@RequiredArgsConstructor
public abstract class DocRepositoryImpl implements DocRepository{

    private final MongoOperations mongoOperations;

    @Override
    public List<Doc> findAllByDoc(String docName) {
        return mongoOperations.findAll(Doc.class, docName);
    }
}
