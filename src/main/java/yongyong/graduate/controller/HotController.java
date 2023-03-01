package yongyong.graduate.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import yongyong.graduate.docDomain.Doc;
import yongyong.graduate.docDomain.DocRepository;
import yongyong.graduate.docDomain.DocRepositoryImpl;
import yongyong.graduate.hotDomain.Hot;
import yongyong.graduate.hotDomain.HotRepository;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@Controller // index.html과 연동하려면 @RestController는 안 됨
public class HotController {

    @Qualifier("db2MongoTemplate")
    @Autowired
    private MongoTemplate docMongoTemplate;

    @Autowired
    private HotRepository hotRepository;

    @Autowired
    private DocRepository docRepository;

    @GetMapping("/hot")
    public String showHot(Model model) {
        List<Hot> hotWords = this.hotRepository.findAll();
        System.out.println(hotWords);
        System.out.println("hotWords size: " + hotWords.size());
        model.addAttribute("hotWords", hotWords);
        return "index";
    }

    @GetMapping("/docs")
    public String showDocs(Model model, @RequestParam("word") String word) {
        List<Hot> hotWords = this.hotRepository.findAllBy_id(word);
        List<String> docArray = new ArrayList<>();
        for (int i = 0; i < hotWords.size(); i++) {
            for (int j = 0; j < hotWords.get(i).getDoc().size(); j++) {
                docArray.add(hotWords.get(i).getDoc().get(j));
            }
        }
        List<Doc> docs = new ArrayList<>();
        for (String docName : docArray) {
            docs.addAll(this.docMongoTemplate.findAll(Doc.class, docName));
        }
        model.addAttribute("docs", docs);
        return "doc-list";
    }
}