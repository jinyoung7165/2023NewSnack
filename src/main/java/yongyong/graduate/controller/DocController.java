package yongyong.graduate.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
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
import java.util.List;

@Slf4j
@Controller
@RequiredArgsConstructor
public class DocController {
    private final MongoTemplate mongoTemplate;

    @GetMapping("/docs/hot")
    public String showHotDocs(Model model, @RequestParam("word") String word) throws Exception {
        long stime = System.currentTimeMillis();

        Query hotQuery = new Query();
        hotQuery.fields().include("doc", "weight");
        hotQuery.addCriteria(Criteria.where("word").is(word)).limit(1);
        List<Hot> hots = mongoTemplate.find(hotQuery, Hot.class, TodayUtil.todayHot());
        List<DBRef> docRefs = hots.get(0).getDoc();
        List<Doc> docs = new ArrayList<>();

        docRefs.forEach((docRef) -> {
            Query docQuery = new Query();
            docQuery.fields().exclude("_id", "main");
            docQuery.addCriteria(Criteria.where("_id").is(docRef.get_id()));
            docs.add(mongoTemplate.find(docQuery, Doc.class, docRef.getRef()).get(0));
        });

        System.out.println("docQuery:"+(System.currentTimeMillis()-stime)+"ms"); //엄청난 시간
        model.addAttribute("docs", docs);
        model.addAttribute("date", TodayUtil.todays());
        System.out.println("소요시간:"+(System.currentTimeMillis()-stime)+"ms");
        return "doc-list";
    }

    @GetMapping("/docs")
    public String showKeywordDocs(Model model, @RequestParam("word") String word) throws Exception {
        long stime = System.currentTimeMillis();
        List<String> docCols = TodayUtil.todayDocs();  // 3일치 doc collection
        List<Doc> docs = new ArrayList<>();

        Query query = new Query();
        query.fields().exclude( "_id", "main");
        query.addCriteria(Criteria.where("keyword").is(word));

        for(String col : docCols) {
            docs.addAll(mongoTemplate.find(query, Doc.class, col));
        }

        System.out.println("total document's num : " + docs.size());
        model.addAttribute("docs", docs);
        model.addAttribute("date", TodayUtil.todays());
        System.out.println("소요시간:"+(System.currentTimeMillis()-stime)+"ms");
        return "keyword-list";
    }
}