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
import java.util.stream.Collectors;
import java.util.stream.Stream;


@Slf4j
@Controller
@RequiredArgsConstructor
public class DocController {
    private final MongoTemplate mongoTemplate;

    @GetMapping("/docs/hot")
    public String showHotDocs(Model model, @RequestParam("word") String word, @PageableDefault(page=0, size=5) Pageable pageable) {
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

        // 각 핫토픽의 기사 개수
        long totalDocs = mongoTemplate.count(Query.query(Criteria.where("doc").in(docNames)), Doc.class, TodayUtil.todayDoc());
//        System.out.println(totalDocs);

        // pageable 객체 생성
        pageable = PageRequest.of(pageable.getPageNumber(), pageable.getPageSize());

        // paging 처리된 상태로 doc 가져옴
       List<Doc> docList = mongoTemplate.find(Query.query(Criteria.where("doc").in(docNames)).with(pageable), Doc.class, TodayUtil.todayDoc());

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

        for(String col : docCols) {
            log.info("colName {}", col);
           docs.addAll(mongoTemplate.find
                   (Query.query(Criteria.where("keyword").is(word)), Doc.class, col)
           );
        }

        List<String> docNames = docs.stream().map(doc -> {
            String docName = doc.getDoc();
            return docName;
        }).collect(Collectors.toList());
        log.info("docs {}", docNames);
        System.out.println("total document's num : " + docs.size());
        return "keyword-list"; // 그냥 임의로 만들어 놓은 것.
    }
}