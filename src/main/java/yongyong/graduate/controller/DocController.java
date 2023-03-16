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

    @GetMapping("/docs")
    public String showDocs(Model model, @RequestParam("word") String word, @PageableDefault(page=0, size=5) Pageable pageable) {
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

    @GetMapping("/keyword")
    public String getKeyword() {
        // 3일치 doc 가져와서
        String[] collectionName = {"2023-03-09_doc", "2023-03-10_doc", "2023-03-11_doc"};
        // docs 담을 리트스
        List<Doc> docs = new ArrayList<>();
        // for문 3번 돌아서 docs에 저장
        for(int i = 0; i < collectionName.length; i++) {
           docs.addAll(mongoTemplate.find
                   (Query.query(Criteria.where("doc").exists(true)), Doc.class, collectionName[i])
           );
        }
        System.out.println("total document's num : " + docs.size());
        return "keyword-list"; // 그냥 임의로 만들어 놓은 것.
    }
}