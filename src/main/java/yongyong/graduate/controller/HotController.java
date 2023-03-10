package yongyong.graduate.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import yongyong.graduate.common.annotation.TodayHot;
import yongyong.graduate.common.util.TodayUtil;
import yongyong.graduate.hotDomain.Hot;

import java.util.List;

@Slf4j
@Controller
@RequiredArgsConstructor
public class HotController {

    private final MongoTemplate docMongoTemplate;

    @GetMapping("/hot")
    public String showHot(Model model) {
        log.info("Hot annotation :{}", Hot.class.getAnnotation(TodayHot.class).value());
        List<Hot> hotWords = this.docMongoTemplate.findAll(Hot.class, TodayUtil.todayHot());
        System.out.println(hotWords);
        System.out.println("hotWords size: " + hotWords.size());
        model.addAttribute("hotWords", hotWords);
        return "index";
    }

//    @GetMapping("/docs")
//    public String showDocs(Model model, @RequestParam("word") String word) {
//        List<Hot> hotWords = this.hotRepository.findAllBy_id(word);
//        List<String> docArray = new ArrayList<>();
//        for (int i = 0; i < hotWords.size(); i++) {
//            for (int j = 0; j < hotWords.get(i).getDoc().size(); j++) {
//                docArray.add(hotWords.get(i).getDoc().get(j));
//            }
//        }
//        List<Doc> docs = new ArrayList<>();
//
//        for (String docName : docArray) {
//            docs.addAll(this.docMongoTemplate.findAll(Doc.class, docName));
//        }
//        model.addAttribute("docs", docs);
//        return "doc-list";
//    }
}