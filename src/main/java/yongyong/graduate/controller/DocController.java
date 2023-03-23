package yongyong.graduate.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import yongyong.graduate.common.util.TodayUtil;
import yongyong.graduate.domain.DBRef;
import yongyong.graduate.domain.Doc;
import yongyong.graduate.service.DocService;
import yongyong.graduate.service.HotService;

import java.util.List;
import java.util.Optional;

@Slf4j
@Controller
@RequiredArgsConstructor
public class DocController {
    private final HotService hotService;
    private final DocService docService;

    @GetMapping("/docs/hot")
    public String showHotDocs(Model model, @RequestParam("word") String word) throws Exception {
        List<DBRef> docRefs = hotService.findWordHot(word).getDoc();
        List<Doc> docs = docService.findHotDocs(docRefs);
        String regex = "\n";

        model.addAttribute("docs", docs);
        model.addAttribute("regex", regex);
        model.addAttribute("date", TodayUtil.todays(Optional.empty()));
        return "doc-list";
    }

    @GetMapping("/docs")
    public String showKeywordDocs(Model model, @RequestParam("word") String word) throws Exception {
        List<Doc> docs = docService.findKeywordDocs(word);
        String regex = "\n";

        model.addAttribute("docs", docs);
        model.addAttribute("regex", regex);
        model.addAttribute("date", TodayUtil.todays(Optional.empty()));
        return "keyword-list";
    }
}