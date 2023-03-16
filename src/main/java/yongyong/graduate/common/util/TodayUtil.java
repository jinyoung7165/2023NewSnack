package yongyong.graduate.common.util;

import org.springframework.stereotype.Component;
import yongyong.graduate.common.annotation.Today;
import yongyong.graduate.common.annotation.TodayDoc;
import yongyong.graduate.common.annotation.TodayHot;
import yongyong.graduate.domain.Doc;
import yongyong.graduate.domain.Hot;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

@Today
@Component
public class TodayUtil { //update된 날짜 조회
    public static String getToday() {
        return TodayUtil.class.getAnnotation(Today.class).value();
    }
    public static String todayHot() { return Hot.class.getAnnotation(TodayHot.class).value(); } //_hot
    public static String todayDoc() { return Doc.class.getAnnotation(TodayDoc.class).value(); } //_doc

    public static List<String> todayDocs() throws Exception {
        String today = TodayUtil.class.getAnnotation(Today.class).value();
        List<String> docCol = new ArrayList<>();
        docCol.add(todayDoc());
        for(int i=0; i<2; i++) {
            today = subtractDate(today);
            docCol.add(today + "_doc");
        }
        return docCol;
    } //_doc

    private static String subtractDate(String strDate) throws Exception {
        SimpleDateFormat dtFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date dt = dtFormat.parse(strDate);

        Calendar cal = Calendar.getInstance();
        cal.setTime(dt);

        cal.add(Calendar.DATE,  -1); //하루 전
        return dtFormat.format(cal.getTime());
    }

}