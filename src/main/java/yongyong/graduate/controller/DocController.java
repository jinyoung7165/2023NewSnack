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
    public String showHotDocs(Model model, @RequestParam("word") String word, @PageableDefault(page=0, size=5) Pageable pageable) {
        Query query = new Query();
        query.fields().include("doc", "weight"); //weight 왜 필요한 걸까
        query.addCriteria(Criteria.where("word").is(word));
        Hot hot = mongoTemplate.find(
                query, Hot.class, TodayUtil.todayHot()).get(0);

        List<Doc> docs = hot.getDoc();

        // 각 핫토픽의 기사 개수
        long totalDocs = docs.size();
        // 전체 페이지 개수
        int totalPages = (int) Math.ceil((double) totalDocs / pageable.getPageSize());

        int nowPage = pageable.getPageNumber() + 1; // 처음이 0 이므로

        // 시작 페이지 -> 현재 페이징 된 페이지 기준 앞으로 4개
        int startPage = Math.max(nowPage - 4, 1);

        // 끝 페이지 -> 현재 페이징 된 페이지 기준 뒤로 9개
        int endPage = Math.min(nowPage + 9, totalPages);

        model.addAttribute("docs", docs);
        model.addAttribute("nowPage", nowPage);
        model.addAttribute("startPage", startPage);
        model.addAttribute("endPage", endPage);
        model.addAttribute("currentPage", pageable.getPageNumber());
        model.addAttribute("pageSize", pageable.getPageSize());
        model.addAttribute("totalPages", totalPages);
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
        return "keyword-list";
    }
}