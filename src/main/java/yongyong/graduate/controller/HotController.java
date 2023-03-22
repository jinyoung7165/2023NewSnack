package yongyong.graduate.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import yongyong.graduate.common.annotation.TodayHot;
import yongyong.graduate.common.util.TodayUtil;
import yongyong.graduate.domain.Hot;
import yongyong.graduate.service.HotService;

import java.util.List;
import java.util.Optional;

@Slf4j
@Controller
@RequiredArgsConstructor
public class HotController {
    private final HotService hotService;

    @GetMapping
    public String showHot(Model model) throws Exception {
        log.info("Hot annotation :{}", Hot.class.getAnnotation(TodayHot.class).value());
        List<Hot> hotWords = hotService.findAllHot();
        model.addAttribute("hotWords", hotWords);
        model.addAttribute("date", TodayUtil.todays(Optional.empty()));
        return "index";
    }
}