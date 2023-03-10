package yongyong.graduate.common.util;

import org.springframework.stereotype.Component;
import yongyong.graduate.common.annotation.Today;

@Today
@Component
public class TodayUtil {
    public static String getToday() {
        return TodayUtil.class.getAnnotation(Today.class).value();
    }
}