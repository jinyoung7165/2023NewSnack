package yongyong.graduate.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
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
import yongyong.graduate.service.DocService;

import java.util.ArrayList;
import java.util.List;


@Slf4j
@Controller
@RequiredArgsConstructor
public class DocController {
    private final MongoTemplate mongoTemplate;
    private final DocService docService;
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

        Page<Doc> docList = docService.docList(pageable);

        //페이지블럭 처리
        //1을 더해주는 이유는 pageable은 0부터라 1을 처리하려면 1을 더해서 시작해주어야 한다.
        int nowPage = docList.getPageable().getPageNumber() + 1;
        //-1값이 들어가는 것을 막기 위해서 max값으로 두 개의 값을 넣고 더 큰 값을 넣어주게 된다.
        int startPage =  Math.max(nowPage - 4, 1);
        int endPage = Math.min(nowPage+9, docList.getTotalPages());
        model.addAttribute("docs", docs);
//        model.addAttribute("pages", docList);
//        model.addAttribute("maxPage", 5);
        model.addAttribute("nowPage",nowPage);
        model.addAttribute("startPage", startPage);
        model.addAttribute("endPage", endPage);
        model.addAttribute("currentPage", pageable.getPageNumber()); // 현재 페이지
        model.addAttribute("pageSize", pageable.getPageSize()); // 페이지 사이즈
        return "doc-list";
    }
}