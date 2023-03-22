package yongyong.graduate.common.util;

import org.springframework.stereotype.Component;
import yongyong.graduate.common.annotation.Today;
import yongyong.graduate.common.annotation.TodayHot;
import yongyong.graduate.domain.Hot;

import java.text.SimpleDateFormat;
import java.util.*;

@Today
@Component
public class TodayUtil { //update된 날짜 조회
    public static String getToday() {
        return TodayUtil.class.getAnnotation(Today.class).value();
    }
    public static String todayHot() { return Hot.class.getAnnotation(TodayHot.class).value(); } //_hot

    private static String subtractDate(String strDate) throws Exception {
        SimpleDateFormat dtFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date dt = dtFormat.parse(strDate);

        Calendar cal = Calendar.getInstance();
        cal.setTime(dt);

        cal.add(Calendar.DATE,  -1); //하루 전
        return dtFormat.format(cal.getTime());
    }

//    public static List<String> todays() throws Exception {
//        String today = getToday();
//        List<String> todays = new ArrayList<>();
//        todays.add(today);
//        for(int i=0; i<2; i++) {
//            today = subtractDate(today);
//            todays.add(today);
//        }
//        return todays;
//    }

    public static List<String> todays(Optional<String> doc) throws Exception {
        String tail = "";
        if (doc.isPresent()) { //_doc
            tail = doc.get();
        }
        String today = getToday() + tail;
        List<String> todays = new ArrayList<>();
        todays.add(today);
        for(int i=0; i<2; i++) {
            today = subtractDate(today);
            todays.add(today + tail);
        }
        return todays;
    }

}