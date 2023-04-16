package yongyong.graduate.service;

import lombok.RequiredArgsConstructor;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;
import yongyong.graduate.common.util.TodayUtil;
import yongyong.graduate.domain.DBRef;
import yongyong.graduate.domain.Doc;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class DocService {

    private final MongoTemplate mongoTemplate;
    public List<Doc> findHotDocs(List<DBRef> docRefs) {
        List<Doc> docs = new ArrayList<>();
        HashMap<String, ArrayList<ObjectId>> refMap = mapDocRefs(docRefs); //collection별 id list 생성

        for (String col : refMap.keySet()) {
            Query docQuery = new Query();
            docQuery.fields().exclude("_id", "main");
            docQuery.addCriteria(Criteria.where("_id").in(refMap.get(col)));
            docs.addAll(mongoTemplate.find(docQuery, Doc.class, col));
        }

        return docs;
    }

    public List<Doc> findKeywordDocs(String word) throws Exception {
        List<Doc> docs = new ArrayList<>();
        List<String> docCols = TodayUtil.todays(Optional.of("_doc"));  // 3일치 doc collection

        Query query = new Query();
        query.fields().exclude( "_id", "main");
        query.addCriteria(Criteria.where("keyword").is(word));

        for(String col : docCols) {
            docs.addAll(mongoTemplate.find(query, Doc.class, col));
        }

        return docs;
    }

    private HashMap<String, ArrayList<ObjectId>> mapDocRefs(List<DBRef> docRefs) {
        HashMap<String, ArrayList<ObjectId>> refMap = new HashMap<>();

        docRefs.forEach((docRef) -> {
            String key = docRef.getRef();
            if (refMap.containsKey(key)) {
                refMap.get(key).add(docRef.get_id());
            }
            else {
                ArrayList<ObjectId> list = new ArrayList<>();
                list.add(docRef.get_id());
                refMap.put(key, list);
            }
        });

        return refMap;
    }

}