package yongyong.graduate.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.*;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.web.PageableDefault;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import yongyong.graduate.common.util.TodayUtil;
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
        Query query = new Query();
        query.fields().include("doc", "weight"); //weight 왜 필요한 걸까
        query.addCriteria(Criteria.where("word").is(word));
        Hot hot = mongoTemplate.find(
                query, Hot.class, TodayUtil.todayHot()).get(0);

        List<Doc> docs = hot.getDoc();

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

        System.out.println("total document's num : " + docs.size());
        model.addAttribute("docs", docs);
        model.addAttribute("date", TodayUtil.todays());
        return "keyword-list";
    }
}