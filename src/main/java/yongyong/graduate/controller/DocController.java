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
import yongyong.graduate.domain.Doc;
import yongyong.graduate.domain.Hot;

import java.util.ArrayList;
import java.util.List;


@Slf4j
@Controller
@RequiredArgsConstructor
public class DocController {
    private final MongoTemplate mongoTemplate;

    @GetMapping("/docs")
    public String showDocs(Model model, @RequestParam("word") String word) {
        List<Hot> hotWords = mongoTemplate.find(
                Query.query(Criteria.where("word").is(word)), Hot.class, TodayUtil.todayHot());

        List<String> docNames = new ArrayList<>();
        for (Hot hot : hotWords) {
            for (String doc : hot.getDoc()) docNames.add(doc);
        }

        List<Doc> docs = new ArrayList<>();
        for (String docName : docNames) {
            docs.addAll(mongoTemplate.find(
                    Query.query(Criteria.where("doc").is(docName)), Doc.class, TodayUtil.todayDoc())
            );
        }
        model.addAttribute("docs", docs);
        return "doc-list";
    }
}
