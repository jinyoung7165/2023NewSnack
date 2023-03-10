package yongyong.graduate.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import yongyong.graduate.common.annotation.Today;
import yongyong.graduate.common.annotation.TodayDoc;
import yongyong.graduate.common.annotation.TodayHot;
import yongyong.graduate.common.util.TodayUtil;
import yongyong.graduate.docDomain.Doc;
import yongyong.graduate.hotDomain.Hot;

import java.time.LocalDate;

import static yongyong.graduate.common.util.ReflectUtil.changeAnnotationValue;

@Slf4j
@RestController
public class TodayController {

    @GetMapping("/today")
    public String updateToday() {
        Today todayAnt = TodayUtil.class.getAnnotation(Today.class);
        TodayHot todayHotAnt = Hot.class.getAnnotation(TodayHot.class);
        TodayDoc todayDocAnt = Doc.class.getAnnotation(TodayDoc.class);
        changeAnnotationValue("value", LocalDate.now().toString(),
                todayAnt, todayHotAnt, todayDocAnt);
        log.info("[TodayController] updatedToday : {}", TodayUtil.getToday()); //바뀐 날짜 확인
        return TodayUtil.getToday();
    }
}
