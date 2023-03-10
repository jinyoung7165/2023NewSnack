package yongyong.graduate.common.util;

import org.springframework.stereotype.Component;
import yongyong.graduate.common.annotation.Today;
import yongyong.graduate.common.annotation.TodayDoc;
import yongyong.graduate.common.annotation.TodayHot;
import yongyong.graduate.docDomain.Doc;
import yongyong.graduate.hotDomain.Hot;

@Today
@Component
public class TodayUtil { //update된 날짜 조회
    public static String getToday() {
        return TodayUtil.class.getAnnotation(Today.class).value();
    }
    public static String todayHot() { return Hot.class.getAnnotation(TodayHot.class).value(); } //_hot
    public static String todayDoc() { return Doc.class.getAnnotation(TodayDoc.class).value(); } //_doc
}