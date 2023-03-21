package yongyong.graduate.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import yongyong.graduate.common.annotation.TodayHot;
import yongyong.graduate.common.util.TodayUtil;
import yongyong.graduate.domain.Hot;

import java.util.List;

@Slf4j
@Controller
@RequiredArgsConstructor
public class HotController {

    private final MongoTemplate mongoTemplate;

    @GetMapping()
    public String showHot(Model model) throws Exception {
        log.info("Hot annotation :{}", Hot.class.getAnnotation(TodayHot.class).value());
        Query query = new Query();
        query.fields().exclude("_id", "doc");
        List<Hot> hotWords = mongoTemplate.find(query, Hot.class, TodayUtil.todayHot());
        System.out.println("hotWords size: " + hotWords.size());
        model.addAttribute("hotWords", hotWords);
        model.addAttribute("date", TodayUtil.todays());
        return "index";
    }
}