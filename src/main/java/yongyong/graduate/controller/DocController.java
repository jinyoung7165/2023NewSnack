package yongyong.graduate.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import yongyong.graduate.common.util.TodayUtil;
import yongyong.graduate.domain.DBRef;
import yongyong.graduate.domain.Doc;
import yongyong.graduate.domain.Hot;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

@Slf4j
@Controller
@RequiredArgsConstructor
public class DocController {
    private final MongoTemplate mongoTemplate;

    @GetMapping("/docs/hot")
    public String showHotDocs(Model model, @RequestParam("word") String word) throws Exception {
        Query hotQuery = new Query();
        hotQuery.fields().include("doc", "weight");
        hotQuery.addCriteria(Criteria.where("word").is(word)).limit(1);
        List<Hot> hots = mongoTemplate.find(hotQuery, Hot.class, TodayUtil.todayHot());
        List<DBRef> docRefs = hots.get(0).getDoc();
        List<Doc> docs = new ArrayList<>();

        HashMap<String, ArrayList<ObjectId>> refMap = new HashMap<>(); //collection별 id list 생성
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

        for (String col : refMap.keySet()) {
            Query docQuery = new Query();
            docQuery.fields().exclude("_id", "main");
            docQuery.addCriteria(Criteria.where("_id").in(refMap.get(col)));
            docs.addAll(mongoTemplate.find(docQuery, Doc.class, col));
        }

        model.addAttribute("docs", docs);
        model.addAttribute("date", TodayUtil.todays());
        return "doc-list";
    }

    @GetMapping("/docs")
    public String showKeywordDocs(Model model, @RequestParam("word") String word) throws Exception {
        List<String> docCols = TodayUtil.todayDocs();  // 3일치 doc collection
        List<Doc> docs = new ArrayList<>();

        Query query = new Query();
        query.fields().exclude( "_id", "main");
        query.addCriteria(Criteria.where("keyword").is(word));

        for(String col : docCols) {
            docs.addAll(mongoTemplate.find(query, Doc.class, col));
        }

        model.addAttribute("docs", docs);
        model.addAttribute("date", TodayUtil.todays());
        return "keyword-list";
    }
}